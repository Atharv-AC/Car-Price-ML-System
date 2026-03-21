from car_price_prediction.pipeline.train_model import (
    model_linear,
    model_ridge,
    model_lasso,
    model_rf,
    preprocessor,
    X_train,
    X_test,
    y_train,
    y_test
)

from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np


def evaluate_linear():

    model = model_linear(preprocessor, X_train, y_train)

    pred = model.predict(X_test)

    rsq = model.score(X_train, y_train)
    rsq2 = model.score(X_test, y_test)

    mse = mean_squared_error(y_test, pred)

    print("-" * 35)
    print("For linear regression Model ....")
    print(f"Training score: {rsq * 100:.2f}%")
    print(f"Testing score: {rsq2 * 100:.2f}%")
    print("Test Mean Squared error:", mse)
    print("-" * 35 , "\n")


def evaluate_ridge():

    best_model, grid = model_ridge(preprocessor, X_train, y_train)

    pred = best_model.predict(X_test)

    mse = mean_squared_error(y_test, pred)

    print("-" * 35)
    print("For Ridge Model ....")
    print("Best alpha:", grid.best_params_)
    print("Best CV score:", grid.best_score_)
    print("Test R2:", best_model.score(X_test, y_test))
    print("Test Mean Squared error:", mse)
    print("-" * 35 , "\n")


def evaluate_lasso():

    best_model, grid = model_lasso(preprocessor, X_train, y_train)

    pred = best_model.predict(X_test)

    mse = mean_squared_error(y_test, pred)

    print("-" * 35)
    print("For Lasso Model ....")
    print("Best alpha:", grid.best_params_)
    print("Best CV score:", grid.best_score_)
    print("Test R2:", best_model.score(X_test, y_test))
    print("Test Mean Squared error:", mse)
    print("-" * 35 , "\n")


def evaluate_rf():

    best_model, grid = model_rf(preprocessor, X_train, y_train)

    pred = best_model.predict(X_test)

    best_cv = grid.best_score_

    rsq = best_model.score(X_train, y_train)
    rsq2 = best_model.score(X_test, y_test)

    mse = mean_squared_error(y_test, pred)
    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mse)

    print("-" * 35)
    print("For Random Forest Model ....")
    print("Best Hyperparameters:", grid.best_params_)
    print("Best CV score:", best_cv)
    print(f"Training score: {rsq * 100:.2f}%")
    print(f"Testing score: {rsq2 * 100:.2f}%")
    print("Test Mean Squared error:", mse)
    print("Test Root Mean Squared error:", rmse)
    print("Test Mean Absolute error:", mae)
    print("-" * 35, "\n")


if __name__ == "__main__":

    evaluate_linear()
    evaluate_ridge()
    evaluate_lasso()
    evaluate_rf()