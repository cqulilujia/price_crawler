import json
import re
import pymysql
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pymysql.converters import escape_string


conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       passwd='mysql',
                       charset='utf8'
                       )
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


def get_request(url):
    resp = requests.get(url, headers=headers)
    return resp


def ini_database():
    conn.connect()
    cursor = conn.cursor()
    cursor.execute("create database if not exists `douban`;")
    cursor.execute("use douban;")

    sql = 'create table if not exists `user`(' \
          'id varchar(50) not null primary key, ' \
          'name varchar(100) not null);'
    cursor.execute(sql)
    sql = 'create table if not exists `work`(' \
          'id varchar(50) not null primary key, ' \
          'name varchar(100), ' \
          'type varchar(50));'
    cursor.execute(sql)
    sql = 'create table if not exists `comment`(' \
          'id varchar(50) not null primary key, ' \
          'u_id varchar(50), ' \
          'w_id varchar(50), ' \
          'title varchar(100), ' \
          'content longtext,' \
          'foreign key(u_id) references user(id) on update cascade on delete cascade,' \
          'foreign key(w_id) references work(id) on update cascade on delete cascade);'
    cursor.execute(sql)

    conn.commit()
    cursor.close()
    conn.close()


def write_file(text):
    file = open('temp.txt', 'w', encoding='utf-8')
    file.write(text)
    file.close()


def get_comment_text(comment_url):
    resp = get_request(comment_url)
    soup = BeautifulSoup(resp.text, features='html.parser')
    text = soup.find('div', class_='main-bd')('div')[0]('div')[0].text
    return text.strip()


def update_database(sql):
    conn.connect()
    cursor = conn.cursor()
    try:
        conn.begin()
        cursor.execute("use douban;")
        cursor.execute(sql)
        conn.commit()
        # print("插入成功")
    except Exception as e:
        print(e)
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def crawl_comments(user_id):
    user_url = 'https://www.douban.com/people/{}/reviews'.format(user_id)
    resp = get_request(user_url)
    soup = BeautifulSoup(resp.text, features='html.parser')

    # name
    title = soup.find('title').text.strip()
    user_name = re.findall(r'(.+?)的评论', title)[0]

    sql = u'insert into user values(\"{}\", \"{}\");'.format(user_id, user_name)
    update_database(sql)

    comments = soup.find_all('div', class_='main review-item')

    print('正在抓取{}({})的评论，共有{}条评论'.format(user_name, user_id, len(comments)))

    for comment in comments:
        comment_id = comment.attrs['id']

        work_url = comment.find('a', class_='subject-img').attrs['href']
        if 'location' in work_url:  # 豆瓣同城
            (work_type, work_id) = re.findall('https://www.douban.com/location/(.+?)/(.+?)/', work_url)[0]
        else:
            (work_type, work_id) = re.findall('https://(.+?).douban.com/subject/(.+?)/', work_url)[0]
        work_name = comment.find('img').attrs['alt']

        comment_url = comment.find('h2')('a')[0]['href']
        comment_title = comment.find('h2')('a')[0].text
        comment_content = get_comment_text(comment_url)
        comment_content = escape_string(comment_content)

        sql = u'insert into work values(\"{}\", \"{}\", \"{}\");'.format(work_id, work_name, work_type)
        update_database(sql)

        sql = u'insert into comment values(' \
              u'\"{}\", \"{}\", \"{}\",\"{}\",\"{}\");'.format(comment_id, user_id, work_id, comment_title,
                                                               comment_content)
        update_database(sql)

    if len(comments)>0:
        print('{}({})的评论保存完毕'.format(user_name, user_id))


if __name__ == '__main__':
    ini_database()
    user_list = ['gdhdun', '63940068', '140644813', '126474710', 'nonizh', '128748027']
    for user_id in user_list:
        crawl_comments(user_id)
