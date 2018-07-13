#-*- coding: utf-8 -*
import urllib
import time
import os
from urllib2 import urlopen
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

class DataCrawler:
    def __init__(self):
        self.Fin = False # 종목 추출 완료 확인.

    def Crawling_from_naver(self,stockCode,start_date='', end_date=''):
        print("")
        stockCode= str(stockCode).zfill(6) #종목 코드 변환 // 5930 to 005930
        print(stockCode)
        start_date,end_date = set_date(start_date,end_date)

        dayPriceUrl = 'http://finance.naver.com/item/sise_day.nhn?code=' + stockCode
        dayPriceHtml = urlopen(dayPriceUrl)
        dayPriceSource = BeautifulSoup(dayPriceHtml.read(), "html.parser")
        dayPricePageNavigation = dayPriceSource.find_all("table", align="center")
        dayPriceMaxPageSection = dayPricePageNavigation[0].find_all("td", class_="pgRR")
        if dayPriceMaxPageSection == []:
            dayPriceMaxPageSection = dayPricePageNavigation[0].find_all("td", class_="on")
        try: 
            dayPriceMaxPageNum = int(dayPriceMaxPageSection[0].a.get('href')[-3:])
        #"""
        except ValueError:
            MaxPage = dayPriceMaxPageSection[0].a.get('href')[-3:]
        
            if MaxPage[0] == "=":
                dayPriceMaxPageNum = int(dayPriceMaxPageSection[0].a.get('href')[-2:])
            elif MaxPage[1] == "=":
                dayPriceMaxPageNum = int(dayPriceMaxPageSection[0].a.get('href')[-1:])
            else:
                print("ERROR")
        #"""
        stock = []
        for page in range(1, dayPriceMaxPageNum + 1):
            url = 'http://finance.naver.com/item/sise_day.nhn?code=' + stockCode + '&page=' + str(page)
            html = urlopen(url)
            source = BeautifulSoup(html.read(), "html.parser")
            srlists = source.find_all("tr")
            isCheckNone = None

            # day: 날짜
            # closingPrice: 종가
            # variation: 전일대비
            # openingPrice: 시가
            # highestPrice: 고가
            # lowestPrice: 저가
            # volume: 거래량
            if self.Fin == True:
                break
            for i in range(1, len(srlists) - 1): 
                if (srlists[i].span != isCheckNone):
                    day = srlists[i].find_all("td", align="center")[0].text
                    this_day = date_format(day)
                    if this_day <= end_date and this_day >= start_date:
                        closingPrice = srlists[i].find_all("td", class_="num")[0].text
                        #openingPrice = srlists[i].find_all("td", class_="num")[2].text #시가
                        #highestPrice = srlists[i].find_all("td", class_="num")[3].text #고가
                        #lowestPrice = srlists[i].find_all("td", class_="num")[4].text #저가
                        #volume = srlists[i].find_all("td", class_="num")[5].text #거래량

                        """
                        print("날짜: " + day, end=" ")
                        print("종가: " + closingPrice, end="\n")
                        print("시가: " + openingPrice, end=" ")
                        print("고가: " + highestPrice, end=" ")
                        print("저가: " + lowestPrice, end=" ")
                        print("거래량: " + volume)
                        #"""
                        stock.append([stockCode,day,closingPrice])
                    elif this_day<start_date: #크롤링 완료
                        self.Fin=True
                        break
                    else: #시작점 맞춤
                        pass
        return closingPrice


def getPrice(stockCode):
    Crawling = DataCrawler()
    price =Crawling.Crawling_from_naver(stockCode)
    return price


if __name__ == "__main__":
    getPrice(5930)