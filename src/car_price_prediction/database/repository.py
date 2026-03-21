from car_price_prediction.database.models import Prediction


# * Save prediction to database
def save_prediction(session, features, price, version):

    record = Prediction(
        features=features,
        predicted_price=price,
        model_version=version
    )

    session.add(record)
    session.commit()
    session.refresh(record)

    return record