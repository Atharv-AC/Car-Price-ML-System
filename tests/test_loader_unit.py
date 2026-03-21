# monkeypatch temporarily replaces:                                       
    # loader.joblib.load  --->  fake_load 

# This function checks for correct model
def test_load_model(monkeypatch):
    from car_price_prediction import loader

    def fake_load(path):
        assert "latest.joblib" in path
        return "fake_model"

    monkeypatch.setattr(loader.joblib, "load", fake_load)

    result = loader.load_model()

    # ✅ Ensure the correct model is returned
    assert result == "fake_model"



# This function checks for file not found or model not found
def test_load_model_failure(monkeypatch):
    from car_price_prediction import loader
    import pytest

    def fake_load(path):
        raise FileNotFoundError("missing")

    monkeypatch.setattr(loader.joblib, "load", fake_load)

    with pytest.raises(FileNotFoundError):
        loader.load_model()
    



def test_save_model(monkeypatch):
    from car_price_prediction import loader 

    called = {}


    def fake_dump(model, path):
        called["model"] = model
        called["path"] = path

    monkeypatch.setattr(loader.joblib, "dump", fake_dump)
    loader.save_model("dummy_model", "test.joblib")

    assert called["model"] == "dummy_model"
    assert "test.joblib" in called["path"]