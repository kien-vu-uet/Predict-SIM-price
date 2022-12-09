import argparse
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import pickle5 as pickle
from sklearn.svm import SVR

DIVIDE_PRICE_BY = 100000

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type = str, default = 'preprocess_train.csv')
    parser.add_argument("--output", type = str, default = 'models/')
    parser.add_argument("--n-jobs", type = int, default = 20)
    parser.add_argument("--n-segment", type = int, default = 1)
    args = parser.parse_args()

    df = pd.read_csv(args.input, index_col=0)
    X_train = df.drop(['sim_number', 'price_vnd'], axis=1).values
    y_train = df['price_vnd'].astype(int).values / DIVIDE_PRICE_BY

    models = [
        ('linear_regression', LinearRegression(n_jobs=args.n_jobs)),
        ('dicisiontree_regressor', DecisionTreeRegressor(max_depth=30, random_state=42)),
        ('randomforest_regressor', RandomForestRegressor(n_estimators=200, max_depth=30, random_state=42, n_jobs=args.n_jobs)),
        # ('svm_regressor', SVR(max_iter=10000, kernel='sigmoid')),
        ('xgboost_regressor', XGBRegressor(max_depth=20, learning_rate=0.3, random_state=42, n_jobs=args.n_jobs)),
        ('lightgbm_regressor', LGBMRegressor(n_estimators=200, max_depth=20, learning_rate=0.3, random_state=42, n_jobs=args.n_jobs)),
        ('catboost_regressor', CatBoostRegressor(iterations=2000, learning_rate=0.3, max_depth=10, random_state=42))
    ]

    results = []

    for model_name, model in models:
        model.fit(X_train, y_train)
        rmse = np.sqrt(mean_squared_error(y_train, np.abs(model.predict(X_train)))) * DIVIDE_PRICE_BY
        results.append((model_name, rmse))
        pickle.dump(model, open(f"{args.output}{model_name}_{args.n_segment}.sav", 'wb'))

    best_model, best_result = results[0]
    for model_name, result in results:
        print('RMSE of', model_name, ':', result)
        if result < best_result:
            best_model = model_name
            best_result = result

    print('Best model is', best_model, 'with rmse =', best_result)
    print('Done!')
    

    