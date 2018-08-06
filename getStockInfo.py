from urllib.request import urlopen
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
import datetime
from selenium import webdriver
import pandas as pd
import sys
import pymysql
import FinanceDataReader as fdr 
from apscheduler.schedulers.blocking import BlockingScheduler

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
            print("NULL")
    df.to_excel("./DATA/Sector.xlsx",index=False)

def crawling_from_naver():
    dt = datetime.datetime.now()
    dt = dt.strftime("%Y-%m-%d")
    lst= []
    tmp = []
    driver = webdriver.Chrome(executable_path='./chromedriver')# 크롬웹드라이버 실행코드
    driver.implicitly_wait(10)
    driver.get('https://finance.naver.com/sise/sise_market_sum.nhn?sosok=0&page=1')
    driver.find_element_by_xpath("""//*[@id="option1"]""").click()
    driver.find_element_by_xpath("""//*[@id="option24"]""").click()
    driver.find_element_by_xpath("""//*[@id="contentarea_left"]/div[2]/form/div/div/div/a[1]/img""").click()
    for sosok in range(2): 
        url = 'https://finance.naver.com/sise/sise_market_sum.nhn?sosok=%s&page=1'%sosok
        html = urlopen(url)
        source = BeautifulSoup(html.read(), "html.parser")
        dayPricePageNavigation = source.find_all("table", align="center")
        dayPriceMaxPageSection = dayPricePageNavigation[0].find_all("td", class_="pgRR")
        dayPriceMaxPageNum = int(dayPriceMaxPageSection[0].a.get('href')[-2:])
        
        for k in range(1,dayPriceMaxPageNum+1):                           
        #for k in range(1,3):                           
            driver.get('https://finance.naver.com/sise/sise_market_sum.nhn?sosok=%s&page=%s'%(sosok,k))#주소불러와서 크롤링 시작
            time.sleep(2) 
            for i in range(2,79):
                if i == 7 or i == 8 or i == 9 or i == 15 or i == 16 or i == 17 or i == 23 or i == 24 or i == 25 or i == 31 or i == 32 or i == 33 or i == 39 or i == 40 or i == 41 or i == 47 or i == 48 or i == 49 or i == 55 or i == 56 or i == 57 or i == 63 or i == 64 or i == 65 or i==71 or i==72 or i==73:
                    pass                     
                else:
                    if sosok == 0:
                        num = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[1]"""%i).text
                        name = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[2]/a"""%i).text                                   
                        cur  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[3]"""%i).text.replace(',','')
                        diff = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[4]/span"""%i).text.replace(',','')
                        fluck= driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[5]/span"""%i).text
                        face  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[6]"""%i).text.replace(',','')
                        stocks_listed  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[7]"""%i).text.replace(',','')
                        market_cap  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[8]"""%i).text.replace(',','')
                        foriegn  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[9]"""%i).text.replace(',','')
                        per  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[10]"""%i).text.replace(',','').replace('N/A','')
                        roe  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[11]"""%i).text.replace(',','').replace('N/A','')
                        pbr  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[12]"""%i).text.replace(',','').replace('N/A','')
                        tmp = [dt, name,cur,diff,fluck,face,stocks_listed,market_cap,foriegn,per,roe,pbr]
                        lst.append(tmp)
                        if num == '1480':
                            break
                    else: 
                        num = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[1]"""%i).text
                        name = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[2]/a"""%i).text                                   
                        cur  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[3]"""%i).text.replace(',','')
                        diff = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[4]/span"""%i).text.replace(',','')
                        fluck= driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[5]/span"""%i).text
                        face  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[6]"""%i).text.replace(',','')
                        stocks_listed  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[7]"""%i).text.replace(',','')
                        market_cap  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[8]"""%i).text.replace(',','')
                        foriegn  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[9]"""%i).text.replace(',','')
                        per  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[10]"""%i).text.replace(',','').replace('N/A','')
                        roe  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[11]"""%i).text.replace(',','').replace('N/A','')
                        pbr  = driver.find_element_by_xpath("""//*[@id="contentarea"]/div[3]/table[1]/tbody/tr[%s]/td[12]"""%i).text.replace(',','').replace('N/A','')
                        tmp = [dt, name,cur,diff,fluck,face,stocks_listed,market_cap,foriegn,per,roe,pbr]
                        lst.append(tmp)
                        if num == '1276':
                            break
            

    driver.quit()               

    df = pd.DataFrame(lst,columns=["날짜","종목명","현재가","전일비","등락률","액면가","상장주식수","시가총액","외국인비율","PER","ROE","PBR"])
    df.to_excel("./DATA/crawling_data.xlsx")


def to_sql():
    df = pd.read_excel("./DATA/crawling_data.xlsx")
    sector = pd.read_excel("./DATA/Sector.xlsx")

    df =df.merge(sector,on="종목명",how='left')
    df["PER"] = df["PER"].fillna(sys.maxsize)
    df["PBR"] = df["PBR"].fillna(sys.maxsize)
    df["ROE"] = df["ROE"].fillna(-sys.maxsize-1)
    df["Returns"]= df["Returns"].fillna(-sys.maxsize)
    print(df["ROE"].tail())
    print(df["ROE"])

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
        print(i)
        cursor.execute("INSERT INTO `stockInfo` VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"%(df.iloc[i,0],df.iloc[i,1],df.iloc[i,2],df.iloc[i,3],df.iloc[i,4],df.iloc[i,5],df.iloc[i,6],df.iloc[i,7],df.iloc[i,8],df.iloc[i,9],df.iloc[i,10],df.iloc[i,11],df.iloc[i,12],df.iloc[i,13],df.iloc[i,14]))

def top5_byMonth(index,month,driver):
    MAIN_URL = 'http://dis.kofia.or.kr/websquare/index.jsp?w2xPath=/wq/damoa/DISFundAnnFundUnit.xml&divisionId=MDIS0800%s000000000&serviceId=SDIS0800%s000000'%(index,index)
    
    driver.get(MAIN_URL)
    
    tmp_str = ''
    if index == 2:
        tmp_str = '주식형'
    elif index == 3:
        tmp_str = '채권형' 
    elif index == 4:
        tmp_str = '혼합형' 
    elif index == 5:
        tmp_str = 'MMF' 
    elif index == 6:
        tmp_str = 'ETF'
    else:
        tmp_str = '기타' 
    
    j = 6
    
    if month == 6:
        j = 5


    driver.find_element_by_xpath("""//*[@id="grdMain_h_{0}"]""".format(j)).click()
    driver.find_element_by_xpath("""//*[@id="grdMain_h_{0}"]""".format(j)).click()
    time.sleep(1)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    
    def myfunc(tmp_str,month):
        top5 = [1,2,3,4,5]
        for i in range(1,6):
            url = 'tbody#grdMain_body_tbody > tr:nth-of-type(%s) > td'%i
            notices = soup.select(url)
            stock = [1,2,3,4,5,6,7,8,9,10]
            for j in range(10):
                stock[j] = notices[j].text
            print (stock)
            top5[i-1]=[tmp_str,stock[1],stock[5],stock[6],month]
        return top5

    list_top5 = myfunc(tmp_str,month)
    print(list_top5)
    return(list_top5)

def DoCrawling():
    driver = webdriver.Chrome(executable_path='./chromedriver_win32/chromedriver')
    driver.implicitly_wait(3) # 특정요소가 나타날떄까지 기다려준다. 동적으로 움직이는걸 
                            # 기다려주는게 매우중요하다.
    tmp_lst=[]
    for i in range(2,8):
        a = top5_byMonth(i,6,driver)
        for j in range(5):
            tmp_lst.append(a[j])
        b =top5_byMonth(i,12,driver)
        for j in range(5):
            tmp_lst.append(b[j])
    print(tmp_lst)
    conn = pymysql.Connect(host='pythondb.ceekfdzgubcw.ap-northeast-2.rds.amazonaws.com',
                        port = 3306,
                        user = 'root',
                        passwd = 'wldnjs0216',
                        database = 'ppp',
                        charset = 'utf8',
                        autocommit=True)
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS `fund`")
    cursor.execute("CREATE TABLE IF NOT EXISTS `fund`(`FundType` VARCHAR(10) NOT NULL,`name` VARCHAR(50) NOT NULL,`6month_return` FLOAT(10) NULL ,`12month_return` FLOAT NULL,`month` INT(10) NOT NULL)") 
    for i in range(len(tmp_lst)):
        cursor.execute("INSERT INTO `fund` VALUES('%s','%s','%s','%s','%s')"%(tmp_lst[i][0],tmp_lst[i][1],tmp_lst[i][2],tmp_lst[i][3],tmp_lst[i][4]))
    cursor.close()
    conn.close()


sched = BlockingScheduler()
@sched.scheduled_job('cron', day_of_week='mon-sun', hour=21,minute=10)
def _Main():
    DoCrawling()
    cal_1yRet()
    crawling_from_naver()
    to_sql()
sched.start()

if __name__ == "__main__":
    #crawling_from_naver()
    #to_sql()
    #_Main()
    pass
    """
    cursor.execute("SELECT `name`,`pbr`,`market_cap` FROM `ppp`.`stockInfo` WHERE `sector`='제조업' and `pbr`<10 and `pbr`>0 ORDER BY `market_cap` DESC limit 5")
    rows = cursor.fetchall()
    lst=[]
    for row in rows:
        lst.append(row)
    cursor.close()
    conn.close()
    """
