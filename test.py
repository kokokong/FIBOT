dic = {
    "version": "0.1.0",
    "session": {
        "sessionId": "57e23688-b1fd-4f6e-9594-fac8ce51a2e8",
        "user": {
            "userId": "fgCr2Dg_RRGVr8GTXPWY9g",
            "accessToken": "cbab1d69-d414-4aa4-9c65-24a84b78a206"
        },
        "new": True
    },
    "context": {
        "System": {
            "user": {
                "userId": "fgCr2Dg_RRGVr8GTXPWY9g",
                "accessToken": "cbab1d69-d414-4aa4-9c65-24a84b78a206"
            },
            "device": {
                "deviceId": "8d4aa457-d082-4911-b6de-dd452a2f875d",
                "display": {
                    "size": "l100",
                    "orientation": "landscape",
                    "dpi": 96,
                    "contentLayer": {
                        "width": 640,
                        "height": 360
                    }
                }
            }
        }
    },
    "request": {
        "type": "IntentRequest",
        "intent": {
            "name": "주식추천",
            "slots": {
                "number": {
                    "name": "number",
                    "value": "20"
                },
                "condition": {
                    "name": "condition",
                    "value": "이하"
                },
                "Dic": {
                    "name": "Dic",
                    "value": "피이알"
                }
            }
        }
    }
}

print(dic["context"]["System"]["user"]["userId"])