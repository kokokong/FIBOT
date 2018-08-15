#-*- coding: utf-8 -*
from flask import jsonify
from flask import Flask
from flask import request
from flask import make_response
from GetPrice import *
from Explain import *
from tosql import *
import sys

app = Flask(__name__) 
app.secret_key = 'secret'

def gVal(value):
    value = value.strip("\u200b")
    return value

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
        }
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
    if 'sessionAttributes' not in dataReceive['session']:
        dataReceive['session']['sessionAttributes'] = {}
    sessAttribute = dataReceive['session']['sessionAttributes']
    print(sessAttribute)
    try:
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
                    Values = gVal(slots["menu"]["value"])
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

            elif intentName == u"펀드타입":
                KEYS = list(slots.keys())
                for key in KEYS:
                    keys.append(gVal(slots[key]["name"]))
                    values.append(gVal(slots[key]["value"]))

                return Multi(sessAttribute, intentName,keys,values,"수익률 조회 기간은 어떻게 되나요?")

            elif intentName ==u"기간설정":
                if sessAttribute != {}:
                    if "FundType" not in sessAttribute:
                        sessAttribute = {"intent":"펀드추천"}
                        return repeat(sessAttribute,"조회를 원하시는 펀드 유형을 먼저 골라주세요.")
                    else:
                        ans = "문의하신 " + sessAttribute["FundType"]+" "+intent['slots']['terms']['value']+"의 추천 상품은 "
                        funds= GetFunds(sessAttribute["FundType"], intent["slots"]["terms"]["value"])
                        for s in funds:
                            ans += s
                            ans += " "
                        ans += " 입니다."
                        return EndMsg(ans)
                else:
                    if "FundType" not in intent["slots"]:
                        return repeat(sessAttribute,"조회를 원하시는 펀드 유형을 먼저 골라주세요")
                    ans = "문의하신 " + intent["slots"]["FundType"]["value"]+" "+intent['slots']['terms']['value']+"의 추천 상품은 "
                    funds = GetFunds(intent["slots"]["FundType"]["value"], intent["slots"]["terms"]["value"])
                    for s in funds:
                        ans += s
                        ans += " "
                    ans += " 입니다."
                    return EndMsg(ans)

            elif intentName ==u"용어설명":
                if "Dictionary" not in slots:
                    return repeat(sessAttribute,"알고 싶은 용어를 말해 주세요")
                DICT = gVal(slots["Dictionary"]["value"])
                #DICT = DICT.strip("\u200b")
                ans = "질문한 " +DICT+"은 "
                ans +=  explain(DICT)
                return Message(ans)

            elif intentName == u"미래추천":
                return Multi(sessAttribute,intentName,"","", "국내펀드, 해외펀드, 대체투자 상품중에 어떤 상품을 추천해 드릴까요?")

            elif intentName == u"자산군":
                assetgroup = slots["AssetGroup"]["value"]
                ans = "문의하신 "+ assetgroup +"의 미래에셋 추천 펀드는 "
                refunds =recomFunds(assetgroup)
                for refund in refunds:
                    ans += refund + " "
                ans += "입니다."
                url = "https://www.miraeassetdaewoo.com/hks/hks4000/n02.do"
                return Message(ans)

            elif intentName ==u"주식추천":
                if slots == None or "Dic" not in slots:
                    return repeat(sessAttribute,"추천 받고 싶은 기준을 설정해 주세요.")
                
                KEYS = list(slots.keys())
                for key in KEYS:
                    keys.append(gVal(slots[key]["name"]))
                    values.append(gVal(slots[key]["value"]))

                #target = slots["Dic"]["value"]
                #number = slots["number"]["value"]
                if "Dic" not in slots:
                    if "Dic" in sessAttribute:
                        target = sessAttribute["Dic"]
                    else:
                        return Multi(sessAttribute, intentName,keys,values,"어떤 기준으로 추천받기 원하시나요?")
                else:
                    target = gVal(slots["Dic"]["value"])

                if "number" not in slots:
                    if "number" in sessAttribute:
                        number = sessAttribute["number"]
                    else:
                        return Multi(sessAttribute, intentName,keys,values,"제한 값은 어느정도를 원하나요?")
                else:
                    number = gVal(slots["number"]["value"])

                if "condition" not in slots:
                    if "condition" in sessAttribute:
                        condition = sessAttribute["condition"]
                    else:
                        return Multi(sessAttribute, intentName,keys,values,"이상으로 원하시나요 이하로 원하시나요?")
                else:
                    condition = gVal(slots["condition"]["value"])
                if "Industry" not in slots:
                    industry = ""
                else:
                    industry = gVal(slots["Industry"]["value"])
                ans = "문의하신 %s, %s이 %s %s인 종목은 "%(industry,target,number,condition)
                lst = StockRecommend(target,condition,number,industry)
                print(lst)
                for stock in lst:
                    print(stock[0])
                    ans += stock[0]
                    ans += " 1년 수익률 "
                    ans += str(stock[1])
                    ans += ", "
                ans += "입니다."
                print(ans)
                return Message(ans)

            elif intentName == u"주가확인":
                if 'stockname' not in slots:
                    return repeat(sessAttribute,"조회하고 싶은 종목을 말해주세요.")
                Code = gVal(slots['stockname']['value'])
                Code = Code.zfill(6)
                price = getPrice(Code)
                msg = "조회한 종목의 현재 가격은 "+str(price)+"원 입니다.\n 다른 종목의 가격들도 확인해 보세요."
                uID = dataReceive["context"]["System"]["user"]["userId"]
                addUserData_to_Sql(uID,Code)
                return Message(msg)
            else:
                return repeat(sessAttribute)
    except:
        return repeat(sessAttribute)



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=443)
