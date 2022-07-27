# coding=utf-8
#中国政府采购网和易找标数据量对比脚本

from yzb_tag_extract import *
from yzb_db_connect import *
import requests
import sys
import datetime
import AguaSpider
import json
from yzb_conf import config as conf
from sshtunnel import SSHTunnelForwarder
from test_MQ import RabbitMQ
import os
from datetime import datetime, date, timedelta
import random
import time
import html
from remote_control import ControPy
import ip_proxy
from retrying import retry
from apscheduler.schedulers.blocking import BlockingScheduler


logger = Logger()
# server = SSHTunnelForwarder(ssh_address_or_host=('39.96.69.104', 22), ssh_username='root',
#                                 ssh_password='vitW0Pks2A*Cf*CH', remote_bind_address=(conf.host, 3306))
# server.start()

# d_save = MySQL(host='127.0.0.1', port=server.local_bind_port, user=conf.user, password=conf.password, db=conf.db,
#                charset=conf.charset)
d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
               charset=conf.charset)

class Campare_ccgp_yzb():

    def get_ccgp_amount(self):
        pass



@retry(stop_max_attempt_number=2)
def get_page_url(u='',date='',ip_list=None,keyWord='',start_time=None,end_time=None):

    try:
        # time.sleep(1)

        params = {
            'searchtype': '2',
            'page_index': '1',
            'bidSort': '0',
            'pinMu': '0',
            'bidType': '0',
            'kw': keyWord,
            'start_time': start_time,
            'end_time': end_time,
            'timeType': '6'
        }
        headers = {
            'Cookie': 'JSESSIONID=EgPd86-6id_etA2QDV31Kks3FrNs-4gwHMoSmEZvnEktWIakHbV3!354619916; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; td_cookie=2144571454; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1545611064,1545618402,1545618414; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1545618495',
            # 'Cookie': 'UM_distinctid=16b882cb78b7f6-04ea86bf03217f-5a40201d-1fa400-16b882cb78c990; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1569467097,1569476101,1569479884,1569479974; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1569480034; JSESSIONID=231sWvpmQV90biZXbmgczIedW5cI-y7ummVBIoxhOFix7JPNySGz!-1490526721; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1569399637,1569400221,1569476103,1569480964; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1569481021',
            'Host': 'search.ccgp.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.8 Safari/537.36'
        }
        proxies = ip_proxy.proxy_list(ip_list)
        print(proxies)
        response = requests.get(u, headers=headers, params=params, proxies=proxies, timeout=3)
        # print(response)
        text = response_html(response)
        # print(text)
        amount = amount_ex(text)
        print(amount)

        save_amount('ccgp_amount',amount,date)

    except:
        # logger.exception(sys.exc_info())
        logger.error(sys.exc_info())

# 保存数据
def save_amount(type,amount,date):

    a_dict = {}
    try:
        notnull_dict(str(amount), a_dict, type)
        notnull_dict(date, a_dict, 'date')
        try:
            id = d_save.insert('t_compare', a_dict)
            d_save.commit_insert()
            # print(id)
        except:
            if type == 'ccgp_amount':
                result = d_save.select_where('id,yzb_amount', 't_compare', 'date=' + '"' + date + '"')[0]
            else:
                result = d_save.select_where('id,ccgp_amount', 't_compare', 'date=' + '"' + date + '"')[0]
            id = result[0]
            amount_r = result[1]
            if amount_r:
                data_gap = abs(int(amount) - int(amount_r))
                notnull_dict(str(data_gap), a_dict, 'data_gap')

            timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            notnull_dict(timeNow, a_dict, 'update_time')
            d_save.update(table='t_compare', data=a_dict, id=id)
            d_save.commit_insert()
    except:
        # logger.exception(sys.exc_info())
        logger.error(sys.exc_info())
        # print(e,'111111111')


# 获取中国政府采购网前一天的数据量
def save_ccgp_amount():
    dict_url = {}
    #6790
    n = 0
    ip_list = ip_proxy.proxy_ip(1)
    for i in range(1,2):

        try:
            yesterday = (date.today() + timedelta(days=-i)).strftime("%Y:%m:%d")
            print(yesterday)
            keyword = ''
            start_time = yesterday
            end_time = yesterday
            # proxies = ip_proxy.proxy_list(ip_list)
            url = 'http://search.ccgp.gov.cn/bxsearch?searchtype=1'
            if n >= 10:
                ip_list = ip_proxy.proxy_ip(1)
                n = 0
            get_page_url(u=url, date=yesterday, ip_list=ip_list,keyWord=keyword,start_time=start_time,end_time=end_time)
            n+=1
            print(n)
        except Exception as e:
            print(e)

# 获取数据量的xpath语法
def amount_ex(html):
    try:
        amount = etree.HTML(html).xpath('//span[@style="color:#c00000"]/text()')[0]
        # print(title,'tititititi')

        return amount
    except Exception as e:
        print(e)
        return '空'


def response_html(resp):
    if resp.status_code == 200:
        html = resp.content.decode('utf-8', 'ignore').replace(u'\xa9', u'')
        # print(html)
        return html
    else:
        print(resp.status_code)

# 获取易找标中中国政府采购网昨天爬取数量
def yzb_amount():
    # server = SSHTunnelForwarder(ssh_address_or_host=('39.96.69.104', 22), ssh_username='root',
    #                                 ssh_password='vitW0Pks2A*Cf*CH', remote_bind_address=(conf.host, 3306))
    # server.start()
    #
    # d_save = MySQL(host='127.0.0.1', port=server.local_bind_port, user=conf.user, password=conf.password, db=conf.db,
    #                charset=conf.charset)

    for i in range(1,2):
        date_save = (date.today() + timedelta(days=-i)).strftime("%Y:%m:%d")
        date_check = (date.today() + timedelta(days=-i)).strftime("%Y%m%d")
        year = (date.today() + timedelta(days=-i)).strftime("%Y")
        amount = d_save.select_where('count(*)','t_website_page_1','page_url like "%{}%" and mission_id = 7 and is_crawled = 1'.format(date_check))[0][0]
        print(amount)
        save_amount('yzb_amount',amount, date_save)

    # server.close()

# 获取中国政府采购网意向公开数据量
def get_yxgk_count():
    url = 'http://cgyx.ccgp.gov.cn/cgyx/pub/projSearchData'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',

    }
    data = {
        'pageSize': '1',
        'pageNo': '1',
        # 'releaseStar': start_date,
        # 'releaseEnd': end_date,
    }

    text = requests.post(url=url, data=data, headers=headers).json()
    # print(text)
    total = text['total']
    print(total,type(total))
    return int(total)

# 获取易找标意向公开数据量
def get_yxgk_yzb_count():
    count_all = 0
    for i in range(2020,2026):
        count = d_save.select_where('count(*)','t_bid_{}'.format(str(i)),'website_id=27')[0][0]
        # print(count,'--------------')
        count_all += int(count)
    print(count_all,type(count_all))
    return count_all


def main():
    save_ccgp_amount()
    yzb_amount()


if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'cron', hour=11,minute=50)
    print('定时任务启动！')
    scheduler.start()
    # main()
    # intention_ob()
    # get_yxgk_yzb_count()
    # get_yxgk_count()











