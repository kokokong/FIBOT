#-*- coding: utf-8 -*
from flask import jsonify
from flask import Flask
from flask import request
from flask import make_response
from GetPrice import getPrice
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

@app.route('/test',methods=["POST"])
def test():
    return "yeb"
@app.route('/stock',methods=["POST"])
def ECHO():
    dataReceive = request.get_json()
    print(dataReceive)
    intent = dataReceive['request']['intent']
    intentName = intent['name']
    print(intentName)
    if intentName == u"Launch":
        return Message("무엇을 도와드릴까요?")
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


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=443)
