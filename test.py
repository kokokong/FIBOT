from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import datetime
import math
import numpy as np
import sys
import pymysql
'''
dt = datetime.datetime.now()
dt = dt.strftime("%Y-%m-%d")


lst= []
tmp = []
for sosok in range(1,2):
    url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok='+str(sosok)+'&page=1'
    html = urlopen(url)
    source = BeautifulSoup(html.read(), "html.parser")
    dayPricePageNavigation = source.find_all("table", align="center")
    dayPriceMaxPageSection = dayPricePageNavigation[0].find_all("td", class_="pgRR")
    dayPriceMaxPageNum = int(dayPriceMaxPageSection[0].a.get('href')[-2:])

    for page in range(1,dayPriceMaxPageNum):
        url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok='+str(sosok)+'&page='+str(page)
        html = urlopen(url)
        source = BeautifulSoup(html.read(), "html.parser")
        body = source.body
        table = source.find_all("table",class_="type_2")
        #print(table[0].find_all("a",class_="tltle"))
        tds = source.find_all("td",class_="number")
        col_count = 0
        #"""
        print(source.find_all("a",class_="tltle")[0].text)
        for i in range(0,len(tds)):
            if i%10==0:
                name = source.find_all("a",class_="tltle")[col_count].text
                name = re.sub(";","",name)
                tmp.append(dt)
                tmp.append(name)
            Source = source.find_all("td",class_="number")[i].text
            Source = re.sub("[/n,/t,\n,\t]","",Source)
            tmp.append(Source)
            if (i+1)%10 == 0 and i != 0:
                col_count+=1
                lst.append(tmp)
                tmp = []
    

df = pd.DataFrame(lst,columns=["날짜","종목명","현재가","전일비","등락률","액면가","상장주식수","시가총액","외국인비율","거래량","PER","ROE","PBR"])
print(df.head())
print(df.tail())
df.to_excel("주가정보.xlsx",index=False)
'''

df2 = pd.read_excel("./DATA/Sector.xlsx")
df = pd.read_excel("./DATA/crawling_data.xlsx")

df =df.merge(df2,on="종목명",how='left')
#df_a.merge(df_b, on='mukey', how='left')
df["PER"] = df["PER"].fillna(sys.maxsize)
df["PBR"] = df["PBR"].fillna(sys.maxsize)
df["ROE"] = df["ROE"].fillna(-sys.maxsize)
df["Returns"] = df["Returns"].fillna(-sys.maxsize)
#print(df2["ROE"])
print(df.tail())
print(df.head())
conn = pymysql.Connect(host='pythondb.ceekfdzgubcw.ap-northeast-2.rds.amazonaws.com',
                       port = 3306,
                       user = 'root',
                       passwd = 'wldnjs0216',
                       database = 'ppp',
                       charset = 'utf8',
                       autocommit=True)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS `stockInfo`")
cursor.execute("CREATE TABLE IF NOT EXISTS `stockInfo`(`date` VARCHAR(50) NULL ,`name` VARCHAR(50) NULL ,`price` FLOAT(20) NULL ,`diff` FLOAT(20) NULL  ,`diff_per` VARCHAR(20) NULL  ,`face` FLOAT(20) NULL  ,`stocks_listed` FLOAT(20) NULL  ,`market_cap` FLOAT(20) NULL ,`foriegn` FLOAT(20) NULL  ,`per` FLOAT(20) NULL ,`roe` FLOAT(20) NULL ,`pbr` FLOAT(20) NULL, `Symbol` VARCHAR(10) NULL, `sector` VARCHAR(10) NULL, `returns` FLOAT(20) NULL,PRIMARY KEY(`name`))")
for i in  range(len(df.index)):
    cursor.execute("INSERT INTO `stockInfo` VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],df.iloc[i,4],df.iloc[i,5],df.iloc[i,6],df.iloc[i,7],df.iloc[i,8],df.iloc[i,9],df.iloc[i,10],df.iloc[i,11],df.iloc[i,12],df.iloc[i,13],df.iloc[i,14]))