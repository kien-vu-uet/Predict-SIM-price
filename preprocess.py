import argparse
import pandas as pd
from sklearn.decomposition import PCA
import json

# def reduce_dim(df, col, idx):
#     pca = PCA(n_components = 1)
#     pca.fit(df[col])
#     pca_red = pca.transform(df[col])
#     pca_df = pd.DataFrame(data = pca_red, columns = ['pca_f' + str(idx)])
#     df = pd.concat([pca_df, df], ignore_index = False, sort = False, axis = 1)
#     df.drop(col, axis = 1, inplace=True)
#     return df

def reduce_dim(df, col, idx):
    pca = PCA(n_components = 1)
    pca.fit(df[col])
    pca_red = pca.transform(df[col])
    df[f"pca_f{str(idx)}"] = pca_red
    df = df.drop(col, axis = 1)
    return df

def main(df, rm_cols, pca, output):
    rm_cols = [col for col in rm_cols if col in df.columns]
    if rm_cols is not []:
        df = df.drop(rm_cols, axis=1)

    for i in range(len(pca)):
        pca_cols = pca[i]
        if len(pca_cols) < 2: continue
        df = reduce_dim(df.copy(), pca_cols, i)

    df.to_csv(output)
    
    

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type = str, default = 'features_train.csv')
    parser.add_argument("--output", type = str, default = 'preprocess_train.csv')
    parser.add_argument("--cfg", type = str, default = 'cfg/preprocess_cfg.json')
    args = parser.parse_args()

    cfg = json.load(open(args.cfg, 'r'))

    df = pd.read_csv(args.input, index_col=0)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(['Unnamed: 0'], axis=1)

    rm_cols = cfg['rm_cols']
    df = df.drop(rm_cols, axis=1)           
    pca = cfg['pca']      
    main(df, rm_cols, pca, args.output)
    print("Done!")

