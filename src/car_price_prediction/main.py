# from car_price_prediction.loader import load_csv, save_model, load_model
# # from preprocess import build_preprocessor
# # from train import model_ridge, model_lasso, model_rf, model_linear
# # from evaluate import evaluate, learning_curve, decision_tree, random_forest_tree
# # from predict import predict_price
# # from train import train_ridge_model

# def main(): 
#     model_loaded = False
#     data_load = False

#     df = X_train = X_test = y_train = y_test = model = pred = scaler = feature = preprocessor = target = None

#     while True:
#         # print("1. Load Dataset")
#         # print("2. Preprocess + Split Data")
#         # print("3. Train Linear Regression")
#         # print("4. Train Ridge Regression")
#         # print("5. Train Lasso Regression")
#         # print("6. Train Random Forest Regression")
#         # print("7. Evaluate Model")
#         # print("8. Save Best Model")
#         print("9. Load Saved Model")
#         print("10. Predict House Price")
#         print("11. Exit")

#         try:
#             choice = int(input("Enter your choice: "))
#         except ValueError:
#             print("Invalid choice. Please select 1-9.\n")
#             continue


        
#         # if choice == 6:
            
#         #     base_path = os.path.dirname(__file__)
#         #     model_path = os.path.join(base_path, "..", "models", "Titanic_model.pkl")

#         #     try:
#         #         # data = joblib.load(model_path)
#         #         model = data["model"]
#         #         scaler = data["scaler"]
#         #         feature_names = data.get("feature_names", None)
#         #         model_loaded = True
#         #         print("-" * 35)
#         #         print("Model loaded successfully")
#         #         print("-" * 35, "\n")
#         #         continue

#         #     except Exception as e:
#         #         print("Error loading model:", e)
            
        

#         # if choice == 1:
#         #     df = load_csv()
#         #     data_load = True
#         #     print("-" * 35)
#         #     print("Data loaded successfully..")
#         #     print("-" * 35, "\n")

#         # elif not data_load and choice in [3]:
#         #     print("-" * 35)
#         #     print("Please load Data first......")
#         #     print("-" * 35, "\n")
#         #     continue


#         # elif choice == 2:
#         #     from sklearn.model_selection import train_test_split

#         #     if df is None:
#         #         print("-" * 35)
#         #         print("Please load data first....")
#         #         print("-" * 35, "\n")
#         #         continue

#         #     feature, target, preprocessor = build_preprocessor(df)
#         #     X_train, X_test, y_train, y_test = train_test_split(
#         #         feature, target, test_size=0.2, random_state=10
#         #     )
#         #     print("-" * 35)
#         #     print("Data preprocessed successfully....")
#         #     print("-" * 35, "\n")


       
#         # elif choice == 3:
#         #     if X_train is None:
#         #         print("-" * 35)
#         #         print("Please preprocess first....")
#         #         print("-" * 35, "\n")
#         #     else:
#         #         pred, model = model_linear(preprocessor, X_train, y_train, X_test, y_test)
                

#         # elif choice == 4:
#         #     if X_train is None:
#         #         print("-" * 35)
#         #         print("Please load and preprocess data for evaluation")
#         #         print("-" * 35, "\n")
#         #     else:
#         #         pred, model = model_ridge(preprocessor, X_train, y_train, X_test, y_test)
               
                

#         # elif choice == 5:
#         #     if X_train is None:
#         #         print("-" * 35)
#         #         print("Please load and preprocess data for evaluation")
#         #         print("-" * 35, "\n")
#         #     else:
#         #         pred, model = model_lasso(preprocessor, X_train, y_train, X_test, y_test)
               
                
        
#         # elif choice == 6:
#         #     if X_train is None:
#         #         print("-" * 35)
#         #         print("Please preprocess first")
#         #         print("-" * 35 , "\n")
#         #         continue

#         #     pred, model = model_rf(preprocessor, X_train, y_train, X_test, y_test)

            

#         # elif choice == 7:
#         #     if pred is None or y_test is None:
#         #         print("Train a model first")
#         #         continue
#         #     evaluate(y_test, pred)
#         #     learning_curve(model, X_train, y_train)
#         #     random_forest_tree(X_train, y_train, X_test, y_test, preprocessor)


#         # elif choice == 8:
#         #     save_model(model)
#         #     print("-" * 35)
#         #     print("Model saved successfully....")
#         #     print("-" * 35, "\n")

#         def predict_price(model):
#             import pandas as pd
#             import numpy as np

#             mileage = float(input("Enter the mileage of the car: "))
#             engine = float(input("Enter the engine of the car: "))
#             max_power = float(input("Enter the max power of the car: "))
#             torque = float(input("Enter the torque of the car: "))
#             km_driven_per_year = float(input("Enter the km driven per year of the car: "))
#             car_age = float(input("Enter the age of the car: "))
#             fuel = input("Enter the fuel type of the car: ")
#             transmission = input("Enter the transmission type of the car: ")
#             owner = input("Enter the number of owners of the car: ")

#             user_df = pd.DataFrame([{
#                 "mileage": mileage,
#                 "engine": engine,
#                 "max_power": max_power,
#                 "torque": torque,
#                 "km_driven_per_year": km_driven_per_year,
#                 "car_age": car_age,

#                 "fuel": fuel,
#                 "transmission": transmission,
#                 "owner": owner

#             }])

#             pred = model.predict(user_df)[0]
#             actual_price = np.exp(pred)
#             print("-" * 35)
#             print(f"Predicted selling price: {actual_price:.2f}")
#             print("-" * 35, "\n")

        
#         model = load_model()
        
#         if choice == 9:
#             load_model()
#             print("-" * 35)
#             print("Model loaded successfully....")
#             print("-" * 35, "\n")

#         elif choice == 10:
#             if model is None:
#                 print("-" * 35)
#                 print("Please train a model first")
#                 print("-" * 35, "\n")
#                 continue
              
#             predict_price(model)



       
        
#         elif choice == 11:
#             break





# if __name__ == '__main__':
#     main()

