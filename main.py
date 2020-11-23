#!/usr/bin/python3.6

import time
import json
from random import random
from time import sleep
import requests
from selenium import webdriver

PRICE = 6099  # 设置提醒的最低价格
FREQUENCY = 10  # 多少分钟查询一次


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


def get_price():
    price_dict = {}
    # 京东
    item_id_jd = '100004841883'
    url_jd = 'https://p.3.cn/prices/mgets?skuIds=J_' + item_id_jd
    resp_jd = requests.get(url_jd)
    price_json_jd = json.loads(resp_jd.text)
    price_jd = float(price_json_jd[0]['p'])
    price_dict['京东1'] = price_jd

    # 联想
    item_id_lx = '1005900'
    item_id_lx = '1005867'
    url_lx = 'https://papi.lenovo.com.cn/batch/get?params=' \
             '[{%22uri%22:%22/batch/openapi/goods/detail/mget/B00001%22,' \
             '%22param%22:{%22code%22:' + item_id_lx + ',%22ss%22:721}}]'

    url_lx = 'https://papi.lenovo.com.cn/batch/get?params=[{%22uri%22:%22/batch/openapi/goods/detail/mget/B00001%22,%22param%22:{%22code%22:1010322,%22ss%22:721}}]'
    resp_lx = requests.get(url_lx)
    price_json_lx = json.loads(resp_lx.text)
    price_lx = float(price_json_lx['data'][0]['result'][item_id_lx]['detail']['basePrice'])
    price_dict['联想1'] = price_lx

    # 苏宁
    item_group_sn = ['0070146323', '0070794264']
    item_id_sn = ['00646461986', '11508683103']
    result_sn = ''
    for i in range(len(item_group_sn)):
        url_sn = 'https://icps.suning.com/icps-web/getVarnishAllPriceNoCache/0000000' + item_id_sn[i] + \
                 '_010_0100100_' + item_group_sn[i] + '_1_getClusterPrice.jsonp?callback=getClusterPrice'
        resp_sn = requests.get(url_sn)
        len_resp = len(resp_sn.text)
        price_json_sn = json.loads(resp_sn.text[17:len_resp - 3])
        # print(price_json_sn)
        # print(price_json_sn['price'])
        price_sn = float(price_json_sn['price'])
        price_dict['苏宁' + str(i + 1)] = price_sn

    # 第三个商品
    url_sn = 'https://pas.suning.com/nspcsale_0_000000011579176669_000000011579176669_' \
             '0071022348_10_010_0100100_157122_1000000_9017_10106_Z001___R1502002_1.28_1___' \
             '000051303___.html?callback=pcData&_=1574947148686'
    resp_sn = requests.get(url_sn)
    len_resp = len(resp_sn.text)
    price_json_sn = json.loads(resp_sn.text[7:len_resp - 2])
    price_sn = float(price_json_sn['data']['price']['saleInfo'][0]['netPrice'])
    price_dict['苏宁3'] = price_sn

    # 淘宝
    chrome_drive = r"D:\Anaconda3\chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chrome_drive)
    browser.get('https://detail.tmall.com/item.htm?id=629951165955&ns=1&abbucket=4&skuId=4498388169331')
    browser.implicitly_wait(20)
    browser.find_element_by_xpath('//*[@id="sufei-dialog-close"]').click()
    browser.implicitly_wait(20)
    divs = browser.find_elements_by_xpath('/html/body/div[5]/div/div[2]/div/div[1]/div[1]/div/div[2]/dl[1]/dd/span')
    price_tb = divs[0].text
    browser.close()
    price_dict['淘宝'] = price_tb

    return price_dict


def main():
    ding = DingTalk_Disaster()
    hour = time.strftime('%H', time.localtime(time.time()))
    if hour == '00':
        ding.send_msg('晚安，Lucas')
    cnt = 0
    while cnt < 60 // FREQUENCY:  # 一小时内要查询的次数
        result = get_price()
        print(result)
        ding_msg = ''
        min_price = 10000
        for good, price in result.items():
            ding_msg = ding_msg + good + '：' + ('%0.2f' % price) + '\n'
            # if good != '苏宁3':
            min_price = min(min_price, price)
        if min_price <= PRICE:
            ding.send_msg(ding_msg[:len(ding_msg) - 1])  # 删去最后一个换行符

        interval = FREQUENCY * (random() % 7 + 57)  # 平均FREQUENCY分钟一次
        # interval = (random() % 7 + 57)  # 平均60s一次
        sleep(interval)
        cnt = cnt + 1


if __name__ == '__main__':
    main()