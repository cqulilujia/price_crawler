#!/usr/bin/python3.6
import time
import json
from random import random
from time import sleep
import requests
from crawler import *
from dingding import *

PRICE = 6099  # 设置提醒的最低价格
FREQUENCY = 10  # 多少分钟查询一次


def get_price():
    price_dic = {'京东': {}, '联想': {}, '淘宝': {}, '苏宁': {}}
    item_jd = [['联想京东自营旗舰店', '100016071154'], ['联想育新授权专卖店', '10023342795726'],
               ['联想有点授权专卖店', '27675465562'], ['联想西南授权专卖店', '10023317585961']]
    item_sn = [['嘉合永兴电脑旗舰店', '0070146323', '12170939373'], ['世博电脑专营店', '0070131803', '12159852966'],
               ['永轩电脑专营店', '0070175628', '11724380104'], ['联想坚盾专卖店', '0070180585', '12184814775']]
    item_tb = [['联想通恒本厚专卖店', '629625904707', '4651731462643'], ['联想联保专卖店', '629616720439', '4672250167060'],
               ['联想艾克兰斯专卖店', '630338129909', '4683008051985'], ['联想天晴东方专卖店', '630104253721', '4481350972261']]
    item_lx = [['无货款', '1010533'], ['在售款', '1010875']]
    for item in item_jd:
        price_dic['京东'][item[0]] = get_price_JD(item[1])
    for item in item_sn:
        price_dic['苏宁'][item[0]] = get_price_SN(group_id=item[1], item_id=item[2])
    for item in item_lx:
        price_dic['联想'][item[0]] = get_price_LX(item[1])

    # 淘宝部分需要配置
    # for item in item_tb:
    #     price_dic['淘宝'][item[0]] = get_price_TB(group_id=item[1], item_id=item[2])

    return price_dic


def process_meessage(price_dic):
    message = ''
    for key, value in price_dic.items():        # key代表平台名字，value代表多个店铺的价格汇总
        message = message + key + '\n'
        for key_p, value_p in value.items():    # key代表店铺名字，value代表每个店铺的价格
            message = message + key_p + '：' + str(value_p) + '\n'
    return message[:-1]


def get_min_price(price_dic):
    min_price = 1000000
    for key, value in price_dic.items():        # key代表平台名字，value代表多个店铺的价格汇总
        for key_p, value_p in value.items():    # key代表店铺名字，value代表每个店铺的价格
            min_price = min(min_price, value_p)
    return min_price


def sava_data(price_dic):   # 待更新，保存数据函数
    return


def main():
    ding = DingTalk_Disaster()
    while True:
        hour = time.strftime('%H', time.localtime(time.time()))
        price = get_price()
        message = process_meessage(price)
        sava_data(price)

        # 供第一次执行时的测试
        ding.send_msg(message)

        # 每天早上八点
        if hour == '23':
            ding.send_msg('晚安，Lucas')
        if hour == '08':                        # 每天早上8点发送一次价格消息
            price = get_price()
            message = process_meessage(price)
            ding.send_msg(message)

        min_price = get_min_price(price)
        if min_price <= PRICE:              # 价格小于设定价格时发送消息
            ding.send_msg(message)

        interval = FREQUENCY * (random() % 7 + 57)  # 平均FREQUENCY分钟一次
        sleep(interval)


if __name__ == '__main__':
    ding = DingTalk_Disaster()
    main()
