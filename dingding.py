import json
import requests


class DingTalk_Base:
    def __init__(self):
        self.__headers = {'Content-Type': 'application/json;charset=utf-8'}
        self.url = ''

    def send_msg(self, text):
        json_text = {
            "msgtype": "text",
            "text": {
                "content": text
            },
            "at": {
                "atMobiles": [
                    ""
                ],
                "isAtAll": False
            }
        }
        return requests.post(self.url, json.dumps(json_text), headers=self.__headers).content


class DingTalk_Disaster(DingTalk_Base):
    def __init__(self):
        super().__init__()
        # 填写机器人的url
        self.url = 'https://oapi.dingtalk.com/robot/send?access_token=' \
                   '1edbe67dbf9b443e9baf36e35ab6496dc1b625da5b1ee35d80c3f1efc3db2c69'