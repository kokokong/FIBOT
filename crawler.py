from urllib.request import urlopen
from bs4 import BeautifulSoup


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
if __name__ == "__main__":
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