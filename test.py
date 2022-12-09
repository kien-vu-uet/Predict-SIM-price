import argparse
import pandas as pd
import numpy as np
from catboost import CatBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, StackingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
import pickle5 as pickle
from sklearn.svm import SVR
import json
from train import DIVIDE_PRICE_BY

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type = str, default = 'preprocess_test.csv')
    parser.add_argument("--model", type = str, default = 'models/xgboost_regressor.sav')
    parser.add_argument("--output", type = str, default = 'test_results/test_result_without_segment.csv')
    parser.add_argument("--big-case", type = str, default = "big_case.json")
    args = parser.parse_args()

    big_case = json.load(open(args.big_case, 'r'))
    df = pd.read_csv(args.input, index_col=0)
    X_test = df.drop(['sim_number'], axis=1).values

    model = pickle.load(open(args.model, 'rb'))
    y_pred = model.predict(X_test)

    df['price_vnd'] = np.abs(y_pred * DIVIDE_PRICE_BY)

    for i in range(df['sim_number'].shape[0]):
        if df['sim_number'][i] in [int(k) for k in big_case.keys()]:
            df['price_vnd'][i] = big_case.get(f"0{df['sim_number'][i]}")

    df[['sim_number', 'price_vnd']].to_csv(args.output, index=False)
    print('Done!')

