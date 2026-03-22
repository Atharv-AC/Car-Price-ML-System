from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from car_price_prediction.pipeline.features import build_preprocessor, load_csv
import numpy as np
import pandas as pd

df = load_csv()
from sklearn.model_selection import train_test_split

features, target, preprocessor = build_preprocessor(df)
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)


def build_pipeline(preprocessor, model_type="linear"):
    if model_type == "linear":
        model = LinearRegression()

    elif model_type == "ridge":
        model = Ridge(alpha=1.0)
    
    elif model_type == "lasso":
        model = Lasso(alpha=1.0)
    
    elif model_type == "rf":
        model = RandomForestRegressor(random_state=42)

    else:
        raise ValueError("Invalid model type")

    pipeline = Pipeline(
        steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ])

    return pipeline



def model_ridge(preprocessor, X_train, y_train):

        pipeline = build_pipeline(preprocessor, model_type="ridge")
        model = pipeline

        param_grid = {"model__alpha": [0.001, 0.01, 0.1, 1, 10, 100, 1000]}
        grid_search = GridSearchCV(
        estimator=model,
        param_grid = param_grid,
        cv=5,
        scoring= "r2",
        n_jobs=-1
        )

        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_

        return best_model, grid_search


# # model_ridge(preprocessor, X_train, y_train, X_test, y_test)

def model_lasso(preprocessor, X_train, y_train):

        pipeline = build_pipeline(preprocessor, model_type="lasso")
        model = pipeline

        param_grid = {"model__alpha": [0.001, 0.01, 0.1, 1, 10, 100, 1000]}
        grid_search = GridSearchCV(
        estimator=model,
        param_grid = param_grid,
        cv=5,
        scoring= "r2",
        n_jobs=-1
        )

        grid_search.fit(X_train, y_train)

        best_model = grid_search.best_estimator_

        return best_model, grid_search


# # model_lasso(preprocessor, X_train, y_train, X_test, y_test)


def model_rf(preprocessor, X_train, y_train, X_test, y_test):

        pipeline = build_pipeline(preprocessor, model_type="rf")
        model = pipeline

        # param_grid = {
        # 'model__n_estimators': [100, 200, 300],
        # 'model__max_depth': [None, 10, 20],
        # 'model__min_samples_split': [2, 5],
        # 'model__min_samples_leaf': [1, 2]
        # }

        param_grid = {
            'model__n_estimators': [200, 300, 400, 500],
            'model__max_depth': [10, 20, 30, None],
            'model__min_samples_split': [2, 5, 10],
            'model__min_samples_leaf': [1, 2, 4],
            'model__max_features': ['sqrt', 'log2', None]
        }

        grid = RandomizedSearchCV(
        estimator=model,
        param_distributions=param_grid,
        cv=5,
        scoring= "r2",
        n_jobs=-1,
        n_iter=20,
        random_state=42
        )

        grid.fit(X_train, y_train)

        best_model = grid.best_estimator_

        # from sklearn.inspection import permutation_importance

        # # feature importance
        # result = permutation_importance(
        #     best_model, X_test, y_test, n_repeats=10, random_state=42
        # )

        # importance = pd.DataFrame({
        #     "feature": X_test.columns,
        #     "importance": result.importances_mean
        # }).sort_values(by="importance", ascending=False)

        # print(importance.head(10))

        return best_model, grid, grid.best_params_, grid.best_score_, grid.score(X_train, y_train), grid.score(X_test, y_test)

        
        # ? Before Hyperparameter Tuning
        # -----------------------------------
        # For Random Forest Model ....
        # Training score: 98.25%
        # Testing score: 90.34%
        # Test Mean Squared error: 0.043160905774091846
        # ----------------------------------- 

        # ? After Hyperparameter Tuning and GridSearch
        # -----------------------------------
        # For Random Forest Model ....
        # Best Hyperparameters: {'model__max_depth': 20, 'model__min_samples_leaf': 2, 'model__min_samples_split': 2, 'model__n_estimators': 300}
        # Training score: 96.53%
        # Testing score: 90.39%
        # Test Mean Squared error: 0.04293900495110988
        # ----------------------------------- 

        # ? After RandomizedSearchCV
        # -----------------------------------
        # For Random Forest Model ....
        # Best Hyperparameters: {'model__n_estimators': 400, 'model__min_samples_split': 5, 'model__min_samples_leaf': 1, 'model__max_features': 'sqrt', 'model__max_depth': 20}
        # Training score: 96.29%
        # Testing score: 90.98%
        # Test Mean Squared error: 0.04029572457399936
        # ----------------------------------- 


        # ? Final Model
        # -----------------------------------
        # For Random Forest Model ....
        # Best Hyperparameters: {'model__n_estimators': 200, 'model__min_samples_split': 5, 'model__min_samples_leaf': 1, 'model__max_features': 'log2', 'model__max_depth': 20}
        # Best CV score: 0.898935371953335
        # Training score: 96.30%
        # Testing score: 90.98%
        # Test Mean Squared error: 0.040273077450295035
        # Test Root Mean Squared error: 0.20068153240967398
        # Test Mean Absolute error: 0.14100274625976136
        # ----------------------------------- 

                    #   feature  importance
        # 7             car_age    0.613105
        # 5           max_power    0.109581
        # 6              torque    0.095946
        # 3             mileage    0.036146
        # 4              engine    0.031487
        # 2               owner    0.022220
        # 0                fuel    0.014741
        # 8  km_driven_per_year    0.011628
        # 1        transmission    0.003838


model_rf(preprocessor, X_train, y_train, X_test, y_test)


def model_linear(preprocessor, X_train, y_train):

        pipeline = build_pipeline(preprocessor, model_type="linear")

        pipeline.fit(X_train, y_train)

        return pipeline

