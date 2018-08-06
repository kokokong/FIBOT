#-*- coding: utf-8 -*
import urllib
import time
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime as dt
import pymysql
import pyodbc
import pandas as pd
import time

def date_format(d): #날짜 포매팅 함수
    d = str(d).replace('-', '.')
    
    yyyy = int(d.split('.')[0]) 
    mm = int(d.split('.')[1])
    dd = int(d.split('.')[2])

    this_date= dt.date(yyyy, mm, dd)
    return this_date

def set_date(start_date='',end_date=''): 
    if start_date:   # start_date가 있으면
        start_date = date_format(start_date)   # date 포맷으로 변환
    else:    # 없으면
        start_date = dt.date.today()   # 오늘 날짜를 지정
    if end_date:   
        end_date = date_format(end_date)   
    else:   
        end_date = dt.date.today() 
    return start_date,end_date



def Crawling_from_naver(stockCode,start_date='', end_date=''):
    print("")
    stockCode= str(stockCode).zfill(6) #종목 코드 변환 // 5930 to 005930
    print(stockCode)
    start_date,end_date = set_date(start_date,end_date)

    url = 'http://finance.naver.com/item/sise_day.nhn?code=' + stockCode + '&page=1' 
    html = urlopen(url)
    source = BeautifulSoup(html.read(), "html.parser")
    srlists = source.find_all("tr")
    isCheckNone = None

    # closingPrice: 종가
    for i in range(1, len(srlists) - 1): 
        if (srlists[i].span != isCheckNone):
            closingPrice = srlists[i].find_all("td", class_="num")[0].text
            break
        else: #시작점 맞춤
            pass
    return closingPrice


def getPrice(stockCode):
    price =Crawling_from_naver(stockCode)
    return price

# industry = sector 
# 테이블 구성 : date, name, price, diff, diff_per, face, stocks_listed, market_cap, foriegn, per, roe, pbr, symbol, sector, returns
#              날짜  종목명 현재가                 액면가   상장주식수     시가총액    외인비율                종목코드  자산군   수익률  
def StockRecommend(Feature,Condition,number,industry='*'):
    conn = pymysql.Connect(host='pythondb.ceekfdzgubcw.ap-northeast-2.rds.amazonaws.com',
                        port = 3306,
                        user = 'root',
                        passwd = 'wldnjs0216',
                        database = 'ppp',
                        charset = 'utf8',
                        autocommit=True)
    cursor = conn.cursor()
    lst = []
    fe_DIC = {"피이알":"per","시가총액":"market_cap","외인비율":"foriegn","피비알":"pbr","알오이":"roe","시가":"price"}
    cond_DIC = {"이하":"<=","이상":">="}
    feature = fe_DIC[Feature]
    condition = cond_DIC[Condition]
    print(condition)

    if industry == '*':
        if feature == 'pbr' or feature == 'per' and condition =='<=':
            cursor.execute("SELECT `name`,`returns` FROM `ppp`.`stockInfo` WHERE `%s` %s %s and `%s` > 0 ORDER BY `returns` DESC limit 5"%(feature,condition,number,feature))
        else:
            cursor.execute("SELECT `name`,`returns`,FROM `ppp`.`stockInfo` WHERE `%s` %s %s ORDER BY `returns` DESC limit 5"%(feature,condition,number))
    
    else:
        if feature == 'pbr' or feature == 'per' and condition =='<=':
            cursor.execute("SELECT `name`,`returns` FROM `ppp`.`stockInfo` WHERE `%s` %s %s and `%s`>0 and `sector`= '%s' ORDER BY `returns` DESC limit 5"%(feature,condition,number,feature,industry))
        else:
            cursor.execute("SELECT `name`,`returns` FROM `ppp`.`stockInfo` WHERE `%s` %s %s and `sector`= '%s' ORDER BY `returns` DESC limit 5"%(feature,condition,number,industry))

    rows = cursor.fetchall()

    for row in rows:
        lst.append(row)

    cursor.close()
    conn.close()

    return lst


if __name__ == "__main__":
    print(getPrice(5930))
