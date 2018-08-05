from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
import time


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

def GetFunds(FundType,ret="1년 수익률"):
    IDX = {'주식형':2, '채권형':3, '혼합형':4, 'MMF':5, 'ETF':6, '기타':7}
    index = IDX[FundType]
    MAIN_URL =  'http://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/damoa/DISFundAnnFundUnit.xml&divisionId=MDIS0800%s000000000&serviceId=SDIS0800%s000000'%(index,index)
    driver = webdriver.Chrome(executable_path='./chromedriver.exe')
    driver.implicitly_wait(3) # 특정요소가 나타날떄까지 기다려준다. 동적으로 움직이는걸  기다려주는게 매우중요하다.
    driver.get(MAIN_URL)
    j = 6
    
    if ret == "6개월 수익률":
        j = 5
        
    driver.find_element_by_xpath("""//*[@id="grdMain_h_{0}"]""".format(j)).click()
    driver.find_element_by_xpath("""//*[@id="grdMain_h_{0}"]""".format(j)).click()
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    def myfunc():
        top5 = [1,2,3,4,5]
        for i in range(1,6):
            url = 'tbody#grdMain_body_tbody > tr:nth-of-type(%s) > td'%i
            notices = soup.select(url)
            stock = [1,2,3,4,5,6,7,8,9,10]
            for j in range(10):
                stock[j] = notices[j].text
            #print (stock)
            top5[i-1]=stock[1]
        return top5

    top5 = myfunc()
    driver.quit()
    print(top5)
    return top5,MAIN_URL # {2:주식형 3:채권형 4: 혼합형 5: MMF 6: ETF 7:기타}


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
    