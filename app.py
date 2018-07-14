#-*- coding: utf-8 -*
from flask import jsonify
from flask import Flask
from flask import request
from flask import make_response
from GetPrice import getPrice
from crawler import recom
import sys

app = Flask(__name__) 
app.secret_key = 'secret'


def Nonsuccess(ans):
    return jsonify({ 
        "response": {
            "outputSpeech": {
            "type": "SimpleSpeech",
            "values": {
                "type": "PlainText",
                "lang": "ko",
                "value": ans
            }
            },
            "card": {},
            "directives": [],
            "shouldEndSession": False
        }
    })
   

def Message(ans):
    return jsonify({
        "version": "0.1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "SpeechList",
                "values": [
                {
                    "type": "PlainText",
                    "lang": "ko",
                    "value": ans 
                }
                ]
            },
            "card": {},
            "directives": [],
            "shouldEndSession": False
            }
    })


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/test',methods=["GET"])
def test():
    return jsonify({
        "version": "0.1.0",
        "sessionAttributes": {},
        "response": {
            "outputSpeech": {
                "type": "SpeechList",
                "values": [
                {
                    "type": "PlainText",
                    "lang": "ko",
                    "value": "안녕하세요 미래에셋 대우입니다."
                }
                ]
            },
            "card": {},
            "directives": [],
            "shouldEndSession": False
            }
    })
@app.route('/',methods=["POST"])
def ECHO():
    dataReceive = request.get_json()
    print(dataReceive)
    intent = dataReceive['request']['intent']
    intentName = intent['name']
    print(intentName)
    if intentName == u"펀드추천":
        return Message(recom())
    elif intentName == u"추천이유":
        return Message("다양한 해외주식형 펀드 및 ETF에 재간접으로 투자가능하며 시장환경에 따라 적극적 배분을 통해 장기적인 수익 추구하는 상품입니다.")
    elif intentName == u"피자주문":
        print(len(intent["slots"]))
        if intent["slots"]["PizzaAmount"] == None:
            return Nonsuccess("몇판 주문하실 겁니까?")
        else:
            msg ="주문이 완료되었습니다."
            return Message(msg)
    elif intentName == u"주가확인":
        Code = intent['slots']['stockname']['value']
        Code = Code.zfill(6)
        price = getPrice(Code)
        msg = "조회한 종목의 현재 가격은 "+str(price)+"원 입니다.\n 다른 종목의 가격들도 확인하시겠습니까?"
        
        return Message(msg)
    else:
        return Message("잘 모르겠어요.")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=443)
