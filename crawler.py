import requests
import json
from selenium import webdriver

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
    'Cookie': '',
    'Connection': 'keep-alive',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Host': 'p.3.cn',
    'Referer': 'https://book.jd.com/booktop/0-0-0.html?category=1713-0-0-0-10001-1'
}

# 京东
def get_price_JD(item_id):
    url_jd = 'https://p.3.cn/prices/mgets?&pin=null&skuIds=J_' + item_id
    resp_jd = requests.get(url_jd, headers = headers)
    price_json_jd = json.loads(resp_jd.text)
    price_jd = float(price_json_jd[0]['p'])
    return price_jd


# 联想
def get_price_LX(item_id):
    url_lx = 'https://papi.lenovo.com.cn/batch/get?params=' \
             '[{%22uri%22:%22/batch/openapi/goods/detail/mget/B00001%22,' \
             '%22param%22:{%22code%22:' + item_id + ',%22ss%22:721}}]'

    resp_lx = requests.get(url_lx)
    price_json_lx = json.loads(resp_lx.text)
    price_lx = float(price_json_lx['data'][0]['result'][item_id]['detail']['basePrice'])
    return price_lx


# 苏宁
def get_price_SN(group_id, item_id):
    url_sn = 'https://icps.suning.com/icps-web/getVarnishAllPriceNoCache/0000000' + item_id + \
             '_010_0100100_' + group_id + '_1_getClusterPrice.jsonp?callback=getClusterPrice'
    resp_sn = requests.get(url_sn)
    len_resp = len(resp_sn.text)
    price_json_sn = json.loads(resp_sn.text[17:len_resp - 3])
    price_sn = float(price_json_sn['price'])
    return price_sn


# 淘宝
def get_price_TB(group_id, item_id):
    # chrome_drive = r"D:\Anaconda3\chromedriver.exe"
    # browser = webdriver.Chrome(executable_path=chrome_drive)
    # 配置浏览器
    browser = webdriver.Firefox()
    browser.get('https://detail.tmall.com/item.htm?id=' + group_id + '&skuId=' + item_id)
    browser.implicitly_wait(20)
    browser.find_element_by_xpath('//*[@id="sufei-dialog-close"]').click()
    browser.implicitly_wait(20)
    divs = browser.find_elements_by_xpath('/html/body/div[5]/div/div[2]/div/div[1]/div[1]/div/div[2]/dl[1]/dd/span')
    price_tb = divs[0].text
    browser.close()
    return price_tb
