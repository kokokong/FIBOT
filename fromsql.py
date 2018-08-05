"""
import pyodbc 
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
server = 'tcp:myserver.database.windows.net' 
database = 'mydb' 
username = 'myusername' 
password = 'mypassword' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
"""

import urllib
import time
import pandas as pd
import os
from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime as dt

url = 'https://finance.naver.com/fund/fundTypeEarningRate.nhn'
html = urlopen(url)
source = BeautifulSoup(html.read(), "html.parser")
body = source.body
table = source.find_all("table","tbl_fund")
Price =table[0].find_all("td","num")[0].text
print(Price)