#-*- coding: utf-8 -*
from flask import jsonify
from flask import Flask
from flask import request
from flask import make_response
from GetPrice import getPrice
from crawler import *
from Explain import *
import sys

app = Flask(__name__) 
app.secret_key = 'secret'



def repeat(sessAttribute,ans="잘 모르겠어요"):
    return jsonify({ 
        "version" : "0.1.0",
        "sessionAttributes":sessAttribute,
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
        "reprompt" : {
            "outputSpeech" : {
                "type" : "SimpleSpeech",
            "values" : {
                "type" : "PlainText",
                "lang" : "ko",
                "value" : "말씀이 없으시면, 주문을 취소할까요?"
                }
            }
        },
        "shouldEndSession": False
        }
    })

def Multi(sessAttribute, intent,keys=[],values=[],ans="잘 모르겠어요"):
    sessAttribute["intent"] = intent
    print(sessAttribute)
    print(keys)
    print(values)
    for i in range(len(keys)):
        sessAttribute[keys[i]] = values[i]
    
    return jsonify({ 
        "version" : "0.1.0",
        "sessionAttributes":sessAttribute,
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
        "reprompt" : {
            "outputSpeech" : {
                "type" : "SimpleSpeech",
            "values" : {
                "type" : "PlainText",
                "lang" : "ko",
                "value" : "말씀이 없으시면, 주문을 취소할까요?"
                }
            }
        },
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

def EndMsg(ans,url=None):
    return jsonify({
    "version": "0.1.0",
    "sessionAttributes": {},
    "response": {
        "outputSpeech": {
            "type": "SimpleSpeech",
            "values": 
            {
                "type": "PlainText",
                "lang": "ko",
                "value": ans 
            }
        },
        "card": {
            "type": "ImageText",
            "imageUrl": {
                "type": "url",
                "value": "https://img.miraeassetdaewoo.com/new2016/layout/img_logo.gif"
            },
            "mainText": {
                "type": "string",
                "value": "리오넬 메시"
            },
            "referenceText": {
                "type": "string",
                "value": "검색결과"
            },
            "referenceUrl": {
                "type": "url",
                "value": url
            },
            "subTextList": [
                {
                "type": "string",
                "value": "FC 바르셀로나"
                }
            ],
            "thumbImageType": {
                "type": "string",
                "value": "인물"
            },
            "thumbImageUrl": {
                "type": "url",
                "value": "https://img.miraeassetdaewoo.com/new2016/layout/img_logo.gif"
            }
        },
        "directives": [],
        "shouldEndSession": True
        }
    })

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/',methods=["POST"])
def ECHO():
    dataReceive = request.get_json()
    print(dataReceive)
    req = dataReceive['request']
    #try:
    if 'sessionAttributes' not in dataReceive['session']:
        dataReceive['session']['sessionAttributes'] = {}
    sessAttribute = dataReceive['session']['sessionAttributes']
    print(sessAttribute)
    if req['type'] == u'LaunchRequest':
        return Message("안녕하세요 모이라입니다.무엇을 도와드릴까요?")
        #return Message("안녕하세요 미래에셋 대우입니다. 무엇을 도와드릴까요?")

    else:
        intent = req['intent']
        intentName = intent['name']
        slots = intent["slots"]
        print(intentName)
        keys = []; values = []
        if intentName == u"기능설명":
            if "menu" in slots:
                Values = slots["menu"]["value"]
                print(Values)
            else:
                Values = ""
            if Values == u"펀드추천":
                msg = "펀드 추천기능은 6개월 혹은 1년 수익률이 좋은 펀드들을 추천하고 있습니다. 추천 받을 수 있는 펀드의 종류는 주식형, 채권형, 혼합형, M.M.F, E.T.F, 기타형 펀드가 있습니다. 사용 하시려면 '펀드 추천해줘?'처럼 물어보세요"
                return Multi(sessAttribute,intentName,"","", msg)
            elif Values == u"용어사전":
                msg = "용어 사전은 모르는 금융용어를 알려주는 기능이에요. 모르는 용어가 있다면 '시가총액이 뭐야?'처럼 물어보세요"
                return Multi(sessAttribute,intentName,"","", msg)
            elif Values == u"미래에셋추천펀드":
                msg = "미래에셋 추천펀드는 매달 미래에셋이 추천하는 펀드를 자산군별로 확인할 수 있는 기능이에요. '미래에셋 추천펀드 알려줘'처럼 사용해 보세요"
                return Multi(sessAttribute,intentName,"","", msg)
            elif Values == u"주식추천":
                msg = "주식 추천 기능은 원하는 기준에 맞는 종목들을 5개 뽑아주는 기능이에요. 사용하시려면 'PBR이 12보다 높은 주식 검색해줘'처럼 물어보세요"
                return Multi(sessAttribute,intentName,"","", msg)
            elif Values == u"주가확인":
                msg = "주가확인은 원하시는 종목의 현재 가격을 알 수 있는 기능이에요. '삼성전자 가격 알려줘' 말해서 사용할 수 있어요."
                return Multi(sessAttribute,intentName,"","", msg)
            else :
                msg = "저희가 제공하는 기능은 주가확인, 주식추천, 펀드추천, 미래에셋 추천펀드 조회, 금융 용어사전이 있어요. 각 기능의 사용방법을 알고 싶다면 '펀드추천 기능 설명해줘'라고 물어보세요"
                return Multi(sessAttribute,intentName,"","", msg)
        
        elif intentName == u"펀드추천":
            return Multi(sessAttribute,intentName,"","", "어떤 종류의 펀드를 추천해 드릴까요?")
        elif intentName ==u"용어설명":
            DICT = slots["Dictionary"]["value"]
            ans = "질문한 " +DICT+"은 "
            ans +=  explain(DICT)
            return Message(ans)
        elif intentName == u"자산군":
            assetgroup = slots["AssetGroup"]["value"]
            ans = "문의하신 "+ assetgroup +"의 미래에센 추천 펀드는 "
            refunds =recomFunds(assetgroup)
            for refund in refunds:
                ans += refund + " "
            ans += "입니다"
            url = "https://www.miraeassetdaewoo.com/hks/hks4000/n02.do"
            return EndMsg(ans,url)

        elif intentName == u"펀드타입":
            print(slots)
            KEYS = list(slots.keys())
            for key in KEYS:
                keys.append(slots[key]["name"])
                values.append(slots[key]["value"])

            return Multi(sessAttribute, intentName,keys,values,"수익률 조회 기간은 어떻게 되나요?")

        elif intentName ==u"기간설정":
            if sessAttribute != {}:
                if "FundType" not in sessAttribute:
                    return repeat(sessAttribute)
                else:
                    ans = "문의하신 " + sessAttribute["FundType"]+" "+intent['slots']['terms']['value']+"의 추천 상품은 "
                    funds, url = GetFunds(sessAttribute["FundType"], intent["slots"]["terms"]["value"])
                    for s in funds:
                        ans += s
                        ans += " "
                    ans += " 입니다."
                    return EndMsg(ans,url)
            else:
                ans = "문의하신 " + intent["slots"]["FundType"]["value"]+" "+intent['slots']['terms']['value']+"의 추천 상품은 "
                funds, url = GetFunds(intent["slots"]["FundType"]["value"], intent["slots"]["terms"]["value"])
                for s in funds:
                    ans += s
                    ans += " "
                ans += " 입니다."
                return EndMsg(ans,url)

        elif intentName == u"주가확인":
            Code = intent['slots']['stockname']['value']
            Code = Code.zfill(6)
            price = getPrice(Code)
            msg = "조회한 종목의 현재 가격은 "+str(price)+"원 입니다.\n 다른 종목의 가격들도 확인하시겠습니까?"
            
            return Message(msg)
        else:
            return repeat(sessAttribute)
    #except:
    #    return Nonsuccess(sessAttribute)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=443)
