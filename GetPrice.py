#-*- coding: utf-8 -*
import urllib
import time
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime as dt

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


if __name__ == "__main__":
    print(getPrice(5930))
