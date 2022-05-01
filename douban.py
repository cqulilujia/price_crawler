import json
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def get_selenium(user_id='29229048108885'):
    driver = webdriver.Firefox()  # 将驱动放入到python同目录
    driver.get('https://www.douban.com/people/140644813/reviews')
    # input_tag = driver.find_element_by_id('key')  # 定位输入框
    # input_tag.send_keys('口罩')  # 模拟键盘输入文字
    # input_tag.send_keys(Keys.ENTER)  # 模拟键盘回车键
    time.sleep(20)


def get_request(item_id):
    url_jd = 'https://www.douban.com/people/140644813/reviews'
    resp_jd = requests.get(url_jd, headers = headers)
    # price_json_jd = json.loads(resp_jd.text)
    # price_jd = float(price_json_jd[0]['p'])
    # return price_jd


# get_selenium()


url_jd = 'https://www.douban.com/people/140644813/reviews'
resp_jd = requests.get(url_jd, headers = headers)
# price_json_jd = json.loads(resp_jd.text)
# price_jd = float(price_json_jd[0]['p'])
# return price_jd