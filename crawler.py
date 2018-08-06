from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pymysql

""" 개발자 도구 차단으로 개발 중단
def recom():
    url = 'https://www.miraeassetdaewoo.com/hks/hks4000/n02.do'
    html = urlopen(url)
    source = BeautifulSoup(html.read(), "html.parser")
    body = source.body
    table = source.find_all("table")
    prod = table[0].find_all("li")
    STR = "이달의 추천 상품은 "
    for i in prod:
        STR = STR + i.text + ", "
    STR += "입니다."
    return STR

def reason():
    pass

def fundPrice():
    url = 'https://finance.naver.com//fund/fundDailyQuoteList.nhn?fundCd=KR5225812712'
    html = urlopen(url)
    source = BeautifulSoup(html.read(), "html.parser")
    body = source.body
    table = source.find_all("table","tbl_fund")
    Price =table[0].find_all("td","num")[0].text
    return Price  
"""


def GetFunds(FundType,Terms="1년 수익률"):
    type_Dic = {"인덱스":"기타","인덱스형":"기타","ETF형":"ETF","이티에프형":"ETF"}
    ret_DIC = {"6개월 수익률":6, "1년 수익률":12,"12개월 수익률":12}
    Ftype = type_Dic[FundType]
    term = ret_DIC[Terms]

    conn = pymysql.Connect(host='pythondb.ceekfdzgubcw.ap-northeast-2.rds.amazonaws.com',
                        port = 3306,
                        user = 'root',
                        passwd = 'wldnjs0216',
                        database = 'ppp',
                        charset = 'utf8',
                        autocommit=True)
    cursor = conn.cursor()
    lst=[]
    cursor.execute("SELECT `name` FROM `fund` WHERE `FundType`='%s' and `month`= %s ORDER BY `%smonth_return` DESC"%(Ftype,term,term))
    rows = cursor.fetchall()
    for row in rows:
        lst.append(row[0])
    return lst



if __name__ == "__main__":
    """
    url = 'https://www.miraeassetdaewoo.com/hks/hks4000/n02.do'
    html = urlopen(url)
    source = BeautifulSoup(html.read(), "html.parser")
    body = source.body
    table = source.find_all("table")
    tt =table[1].find_all("li")
    STR = " "
    for i in tt:
        STR = STR + i.text + ", "
    STR += "입니다."
    print(STR)
    """
    print(GetFunds("주식형"))
    