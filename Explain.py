import pandas as pd
import numpy as np

def explain(DICT):
    df = pd.read_excel("./DATA/Terms.xlsx",index_col="용어")
    df =df.transpose()
    try:
        explain = df.iloc[0][DICT]
    except KeyError:
        TD = {"아로이":"ROE","단기금융상품":"MMF"}
        DICT = TD[DICT]
        explain = df.iloc[0][DICT]
    return explain


def recomFunds(assetgroup):
    df = pd.read_excel("./DATA/july_funds.xlsx")
    df2 = df[df["자산군"]==assetgroup]
    products = df2["상품명"][:]
    products = products.as_matrix()
    return products

if __name__ == "__main__":
    print(recomFunds("해외주식"))