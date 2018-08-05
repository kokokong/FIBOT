import FinanceDataReader as fdr 
import pandas as pd 
import datetime
def cal_1yRet():
    df = pd.read_excel("./DATA/Sector.xlsx")
    today = datetime.date.today()
    last_year = today.replace(year=today.year-1)

    #"""
    for i in range(len(df)):
        name = df.iloc[i,1]
        code = str(df.iloc[i,0])
        print(name)
        code = code.zfill(6)
        print(code)
        try:
            fdf = fdr.DataReader(code, last_year,today)["Close"]
            ret = (fdf.iloc[-1]-fdf.iloc[0])/fdf.iloc[0] * 100
            print(ret)
            df["Returns"][i] = ret
        except:
            pass
    df.to_excel("./DATA/Sector.xlsx",index=False)

if __name__ == "__main__":
    #cal_1yRet()
    #"""
    today = datetime.date.today()
    last_year = today.replace(year=today.year-1)
    df2 = fdr.DataReader('005930', '2018-01-01', '2018-08-03')["Close"]
    print(df2.iloc[-1])
    print(df2.iloc[0])
    ret = (df2.iloc[-1]-df2.iloc[0])/df2.iloc[0] * 100
    print(ret)

    #"""