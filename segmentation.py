import argparse
import pickle
import pandas as pd
from catboost import CatBoostClassifier
from sklearn.metrics import classification_report
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type = str, default = 'preprocess_train.csv')
    parser.add_argument("--output", type = str, default = "segmentation_train.csv")
    parser.add_argument("--is-test-set", type = bool, default = False)
    parser.add_argument("--cfg", type = str, default = 'cfg/segment_2_cfg.json')
    args = parser.parse_args()

    df = pd.read_csv(args.input, index_col=0)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(['Unnamed: 0'], axis=1)
    cfg = json.load(open(args.cfg, 'r'))
    cfg['price_threshold'].sort()
    if not args.is_test_set:
        label = []
        for price in df['price_vnd']:
            cls = 0
            for p in cfg['price_threshold']:
                if price > p:
                    cls += 1
            label.append({'phan_khuc' : cls})
        label = pd.DataFrame.from_dict(label)
        df_ = pd.concat([df, label], axis=1)

        X_train = df_.drop(['sim_number', 'price_vnd', 'phan_khuc'], axis=1).values
        y_train = df_['phan_khuc'].astype(int).values
        cbc = CatBoostClassifier(iterations=2000, learning_rate=0.3, max_depth=10, random_state=42).fit(X_train, y_train)
        print(classification_report(y_train, cbc.predict(X_train)))
        pickle.dump(cbc, open(cfg['model'], 'wb'))
        # df_ = df_[['sim_number', 'price_vnd', 'phan_khuc']]
        
    else:
        model = pickle.load(open(cfg['model'], 'rb'))
        label = model.predict(df.drop(['sim_number'], axis=1).values)
        label = label.reshape(label.shape[0],)
        print(label)
        label = pd.DataFrame.from_dict([{'phan_khuc' : cls} for cls in label])
        df_ = pd.concat([df, label], axis=1)

    df_.to_csv(args.output)
    print('Done')