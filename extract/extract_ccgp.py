# coding=utf-8
# 中国政府采购网
import requests
import sys
from yzb_tag_extract import *
from yzb_db_connect import *
import datetime
import AguaSpider
import json
from yzb_conf import config as conf
from sshtunnel import SSHTunnelForwarder
import os
from datetime import datetime, date, timedelta
import random
import time
import html
from yzb_remote_control import ControPy
from yzb_remote_control import ControPy_linux
import yzb_ip_proxy
from retrying import retry
from yzb_ml_code.purchaser_sort import purchersSort
from yzb_ml_code.purchaser_sort import itemSort
from snow_factory import IdWorker
import snow_settings as sst
import yzb_pkg_update

# 实例化雪花ID，sst为配置文件
worker = IdWorker(sst.DATACENTER_ID,sst.WORKER_ID,sst.SEQUENCE)


# dict_save = {}
# dict_content = {}


# server = SSHTunnelForwarder(ssh_address_or_host=('39.96.69.104',22),ssh_username='root',ssh_password='vitW0Pks2A*Cf*CH',remote_bind_address=(conf.host,3306))
# server.start()
logger = Logger()


# d_save = MySQL(host='127.0.0.1', port=server.local_bind_port, user=conf.user, password=conf.password, db=conf.db,
#                    charset=conf.charset)

d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                   charset=conf.charset)


dict_url = {}
# dict_save = {}
# dict_content = {}
dict_MQ = []
url_tag = 'ccgp.gov.cn'



def item_dict():
    try:
        d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                       charset=conf.charset)

        item_list = d_save.select_all('name,code', 't_item')
        # print(item_list)
        item_dict = dict(item_list)
        return item_dict
    except Exception as e:
        print(e)


item_dict = item_dict()




def word_ex(table_str,key_word):
    try:
        result = table_str[table_str.index(key_word) + 1]
        if result == '详见公告正文':
            return '空'
        return result
    except:
        return '空'


def budget_amount_special_ex(content):
    try:
        # 单位是 万元 的，转换为元
        rule = '\d+.\d+.\d+.\d+.\d+|\d+.\d+.\d+.\d+|\d+.\d+.\d+|\d+.\d+'
        if re.search(rule,content, re.I | re.S):
            print(re.findall(rule, content)[0],'ooooooooo')
            # print(rule,'wwwwwwwww')
            thousand = decimal.Decimal(re.findall(rule, content)[0].strip())*1000000
            # print(thousand,len(thousand))
            return str(thousand)
        return '空'
    except:
        return '空'

def save_error_item(item_name,page_id):
    try:
        with open('item_issue.txt', mode='a', encoding='utf-8') as a:
            a.write('\n')
            a.write('page_id:'+str(page_id)+'    ')
            a.write('item_name:'+str(item_name))

    except Exception as e:
        print(e)

def switch_to_code(item,page_id):
    # 将品目中文转换为品目标号


    # print(item_dict)
    code_list = []
    i_list = item.split(',')
    for i in i_list:
        try:
            if i == '采购单位':
                continue
            item_name = i.split('/').pop()
            print(item_name)
            code = item_dict[item_name]
            code_list.append(code)
        except:
            save_error_item(i,page_id)
    return list(set(code_list))
    # print(code_list)

    # print(item_dict['服务/其他服务'])


def date_switch(date_str):
    try:
        a = re.findall('\d{2,4}-\d{1,2}-\d{1,2}\s*\d{1,2}:\d{1,2}|\d{2,4}-\d{1,2}-\d{1,2}',
                   str(date_str).strip().replace('年', '-').replace('月', '-').replace('日', ''),
                   re.I | re.S)[0]
        return re.sub('\s+',' ',a)
    except Exception as e:
        print(e)
        return '空'

# 提取中国政府采购网表格中的内容
def ccgp_table_ex(dict_save,det_html,page_id):
    try:

        table_str = etree.HTML(det_html).xpath('//div[@class="table"]//tr//text()')
        project_name = word_ex(table_str,'采购项目名称')
        #品目需要处理
        item = word_ex(table_str, '品目')
        if item:
            items = switch_to_code(item,page_id)
        # 地区需要处理
        address = word_ex(table_str, '行政区域')
        if address != '市辖区':
            address_list = province_ex_all([[address]],'')
            province = province_s(address_list)
            # print(province, 'province')
            city = city_s(address_list)
            # print(city, 'city')
            town = town_s(address_list)
            # print(town,'town')
            notnull_dict(province, dict_save, 'province')
            notnull_dict(city, dict_save, 'city')
            notnull_dict(town, dict_save, 'town')
        date = date_switch(word_ex(table_str, '公告时间'))
        pro = word_ex(table_str, '评审专家名单')[:32]
        # 金额需要处理

        win_money = budget_amount_special_ex(word_ex(table_str, '总中标金额'))
        deal_money = budget_amount_special_ex(word_ex(table_str, '总成交金额'))
        c_man = word_ex(table_str, '项目联系人')
        c_name = word_ex(table_str, '采购单位')[:128]
        c_address = word_ex(table_str, '采购单位地址')[:128]
        c_num = word_ex(table_str, '采购单位联系方式')[:64]
        a_name = word_ex(table_str, '代理机构名称')
        a_address = word_ex(table_str, '代理机构地址')
        a_num = word_ex(table_str, '代理机构联系方式')
        bid_opening_time = date_switch(word_ex(table_str, '开标时间'))
        bid_opening_address = word_ex(table_str, '开标地点')[:255]
        win_date = date_switch(word_ex(table_str, '中标日期'))
        change_date = date_switch(word_ex(table_str, '更正日期'))

        get_bid_doc_time = word_ex(table_str, '获取招标文件时间')
        get_bid_doc_address = word_ex(table_str, '获取招标文件时间')
        budget_money = budget_amount_special_ex(word_ex(table_str, '预算金额'))


        # print('-------------------table-----------------------')
        # print(table_str,'table_str')
        # print(project_name,'project_name')
        # print(item,'item')
        # print(address,'address')
        # print(date,'date')
        # print(pro,'pro')
        # print(win_money,'win_money')
        # print(deal_money,'win_money')
        # print(c_man,'c_man')
        # print(c_name,'c_name')
        # print(c_address,'c_address')
        # print(c_num,'c_num')
        # print(a_name,'a_name')
        # print(a_address,'a_address')
        # print(a_num,'a_num')
        # print(get_bid_doc_time,'get_bid_doc_time')
        # print(get_bid_doc_address,'get_bid_doc_address')
        # print(budget_money,'budget_money')
        # print('-----------------------------------------------')

        notnull_dict(project_name, dict_save, 'project_name')
        notnull_dict(c_num, dict_save, 'company_tel')
        notnull_dict(c_name, dict_save, 'company_name')
        notnull_dict(a_name, dict_save, 'agency_name')
        notnull_dict(date, dict_save, 'project_date')
        notnull_dict(pro, dict_save, 'expert')

        if win_money and win_money != '空':
            notnull_dict(win_money, dict_save, 'bid_money')
        else:
            notnull_dict(deal_money, dict_save, 'bid_money')
        notnull_dict(c_man, dict_save, 'company_contact')
        notnull_dict(c_address, dict_save, 'company_address')
        notnull_dict(a_address, dict_save, 'agency_address')
        notnull_dict(a_num, dict_save, 'agency_tel')
        notnull_dict(budget_money, dict_save, 'budget_money')
        notnull_dict(get_bid_doc_time, dict_save, 'get_bid_doc_time')
        notnull_dict(get_bid_doc_address, dict_save, 'get_bid_doc_address')
        notnull_dict(bid_opening_time, dict_save, 'bid_opening_time')
        notnull_dict(bid_opening_address, dict_save, 'bid_opening_address')
        notnull_dict(win_date, dict_save, 'win_date')
        notnull_dict(change_date, dict_save, 'change_date')


        # print(dict_save)
        if items:
            return dict_save,items
        return dict_save,''
    except Exception as e:
        print(e,'ccgp_table_ex')
        return {},''

# 存储品目
def item_save(items,d_save,bid_id):
    dict_item = {}
    dict_save = {}

    id = d_save.select_where('id', 't_bid_item_ai', 'bid_id=' + str(bid_id))
    if id:
        d_save.delete_where('t_bid_item_ai', 'bid_id', bid_id)
        notnull_dict('2', dict_save, 'index_status')
        notnull_dict('0', dict_save, 'index_status_reindex')
        d_save.update(table='t_bid', data=dict_save, id=bid_id)
    for j in items:
        item_id = worker.get_id()
        print(item_id)
        notnull_dict_num(item_id, dict_item, 'id')
        notnull_dict_num(bid_id, dict_item, 'bid_id')
        notnull_dict(str(j), dict_item, 'item_code')
        d_save.insert('t_bid_item_ai', dict_item)

    print('------------done-------------')

# 金额筛选逻辑
def money_filter(table_money=None,content=None,det_html=None,dict_save=None,
                 table_class_name = 'bid_money',content_money=None):

    print(table_money,'table_money')
    print(content_money,'content_money')

    if table_money == 'null' or table_money == None:
        if content_money == '空':
            try:
                # print(dict_save['budget_money'],'------------------------')
                notnull_dict('空', dict_save, table_class_name)
            except:
                logger.error(sys.exc_info())
        # ppp项目金额本来就大
        # elif float(win_money) > 100000000000:
        #     win_money = str(float(win_money)/10000)
        #     notnull_dict(win_money, dict_save, 'bid_money')
        else:
            notnull_dict(content_money, dict_save, table_class_name)
    else:
        print(table_money, f'--------------{table_class_name}----------------2')
        if content_money == '空' or content_money == None or content_money == '0':
            notnull_dict(table_money.strip('"'), dict_save, table_class_name)

        elif float(table_money.strip('"')) == float(0):
            notnull_dict(content_money, dict_save, table_class_name)

        elif 0 < abs((float(table_money.strip('"')) / float(content_money)) - 10000) < 10 or 0 < abs((float(table_money.strip('"')) / float(content_money)) - 1000) < 10:

            notnull_dict(content_money, dict_save, table_class_name)

        else:
            notnull_dict(content_money.strip('"'), dict_save, table_class_name)



def get_html(page_id):
    html = d_save.runSql_select(f'select html from t_bid_html where page_id = {page_id}')
    # print(html,'html')
    if html != ():
        return html[0][0]



mq_list = []
def save_page(url_list):
    global dict_MQ
    global mq_list
    headers = {
        # 'Cookie': 'JSESSIONID=EgPd86-6id_etA2QDV31Kks3FrNs-4gwHMoSmEZvnEktWIakHbV3!354619916; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; td_cookie=2144571454; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1545611064,1545618402,1545618414; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1545618495',
        'Cookie': 'UM_distinctid=16b882cb78b7f6-04ea86bf03217f-5a40201d-1fa400-16b882cb78c990; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1569467097,1569476101,1569479884,1569479974; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1569480034; JSESSIONID=231sWvpmQV90biZXbmgczIedW5cI-y7ummVBIoxhOFix7JPNySGz!-1490526721; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1569399637,1569400221,1569476103,1569480964; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1569481021',
        'Host': 'search.ccgp.gov.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.8 Safari/537.36'
    }


    u_list = [[i[0], i[1], i[2]] for i in url_list]
    n = 0


    for u_l in u_list:
        flag = 0
        logger.info(u_l[0])

        page_id = u_l[1]

        try:
            dict_save = {}
            dict_content = {}

            # det_html = html_retry(url=u_l[0],n=n,ip_list=ip_list)
            result = d_save.select_html(page_id)
            det_html = result[0]
            title = result[1]
            date = result[2]

            dict_save,items = ccgp_table_ex(dict_save, det_html, page_id)
            # print(items,'items')
            # print(det_html)
            # content1 = re.findall('.*<span.*>(.+)</span>.*',content)
            # print(dict_save,'dddddddddddddddd')
            # print('11111111111111111111')

            content,pre_content = content_ex(det_html,url_tag=url_tag)
            # print('222222222222222222222')
            if not title:
                title = title_ex_total(content, det_html)
            # print(title, 'title')
            project_name = dict_save.get('project_name')
            if project_name == 'null':
                project_name = project_name_ex(content, title)
                notnull_dict(project_name, dict_save, 'project_name')
            # print(project_name, '22222222222')
            project_num = project_num_ex(content,url_tag=url_tag)
            # print(project_num, '33333333333')
            if not date:
                date = dict_save.get('project_date')
                if date == 'null':
                    date = date_ex(det_html, content)
                    notnull_dict(date, dict_save, 'project_date')

            type = type_ex(title, content)
            # print(type, '55555555')
            method = method_ex(title, content)
            # print(method, '666666666')
            project_intro = project_intro_ex(content)
            # print(project_intro, 'introduction')
            comp_address = dict_save.get('company_address')
            if comp_address == 'null':
                comp_address = comp_address_ex(content)
                notnull_dict(comp_address, dict_save, 'company_address')
            # print(comp_address, 'c_address')
            comp_name = dict_save.get('company_name')
            if comp_name == 'null':
                comp_name = comp_name_ex(content)
                notnull_dict(comp_name, dict_save, 'company_name')
            # print(comp_name, 'c_name')
            # print(dict_save.get('province'),'pppppppppppppppppp')
            if dict_save.get('province') == None or dict_save.get('province') == 'null':

                address = province_ex_all([[title],[comp_address],[comp_name]], url_tag)
                province = province_s(address)
                # print(province, 'province')
                city = city_s(address)
                # print(city, 'city')
                town = town_s(address)
                # print(town, 'town')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')

            table_budget = dict_save.get('budget_money')
            content_budget = budget_amount_ex(content, det_html)
            money_filter(table_money=table_budget,content=content,det_html=det_html,dict_save=dict_save,
                 table_class_name = 'budget_money',content_money=content_budget)

            # print(budget_amount, 'b_amount')
            # print(dict_save['budget_money'],'budget_money')
            comp_contact = dict_save.get('company_contact')
            if comp_contact == 'null':
                comp_contact = comp_contact_ex(content)
                notnull_dict(comp_contact, dict_save, 'company_contact')
            # print(comp_contact, 'c_man')
            comp_tell = dict_save.get('company_tel')
            if comp_tell == 'null':
                comp_tell = comp_tell_ex(content)
                notnull_dict(comp_tell, dict_save, 'company_tel')
            # print(comp_tell, 'c_num')

            agency_all = agency_all_ex(content)
            # print(agency_all)
            agency_address = dict_save.get('agency_address')
            if agency_address == 'null':
                agency_address = agency_all[1]
                notnull_dict(agency_address, dict_save, 'agency_address')
            # print(agency_address, 'agency_address')
            agency_name = dict_save.get('agency_name')
            if agency_name == 'null':
                agency_name = agency_all[0]
                notnull_dict(agency_name, dict_save, 'agency_name')
            # print(agency_name, 'agency_name')

            agency_contact = agency_all[2]
            # print(agency_contact, 'agency_contact')
            agency_tel = dict_save.get('agency_tel')
            if agency_tel == 'null':
                agency_tel = agency_all[3]
                notnull_dict(agency_tel, dict_save, 'agency_tel')
            # print(agency_tel, 'agency_tell')
            # table = table_ex(det_html)
            # print(table, 'table')
            # print(dict_save.get('bid_money'), '--------------bid_money----------------1')
            # win_money = dict_save.get('bid_money')

            table_bid = dict_save.get('bid_money')
            content_bid = win_money_all(content, det_html)
            print(table_bid,content_bid,'==========')
            print(content_bid,'content_bid')
            money_filter(table_money=table_bid, content=content, det_html=det_html, dict_save=dict_save,
                         table_class_name='bid_money', content_money=content_bid)



            # items = items_ex(title)
            # print(items, 'items')
            subject = subject_ex(title)
            # print(subject, 'subject')
            subcontract = subcontract_ex(content)
            # print(subcontract, 'subcontract')
            win_bider = winning_bidder_all(content,det_html,url_tag)
            # print(win_bider, 'win_bider')
            pro = pro_ex(content)
            # print(pro, 'pro')
            page_id = u_l[1]
            # print(page_id, 'page_id')
            purchasers = str(purchersSort(title, comp_name))


            # print(det_html)
            # print('---------------------final------------------------')
            # print(content, '\n')
            # print(title, 'title')
            # print(project_name, 'project_name')
            # print(project_num, 'project_num')
            # print(type, 'type')
            # print(method, 'method')
            # print(project_intro, 'project_intro')
            # print(comp_address, 'comp_address')
            # # if province:
            # #     print(province, 'province')
            # # print(city, 'city')
            # # print(town, 'town')
            #
            # # print(budget_amount, 'b_amount')
            # print(comp_name, 'c_name')
            # print(comp_contact, 'c_man')
            # print(comp_tell, 'c_num')
            # print(agency_address, 'agency_address')
            # print(agency_name, 'agency_name')
            # print(agency_contact, 'agency_contact')
            # print(agency_tel, 'agency_tell')
            # # print(win_money, 'win_money')
            # print(subject, 'subject')
            # print(subcontract, 'subcontract')
            # print(win_bider, 'win_bider')
            # print(pro, 'pro')
            # print(page_id, 'page_id')
            # print('--------------------------------------------------')




            notnull_dict(title, dict_save, 'title')
            # notnull_dict(project_name, dict_save, 'project_name')
            notnull_dict(project_num, dict_save, 'project_code')
            # notnull_dict(date, dict_save, 'project_date')
            notnull_dict(pro, dict_save, 'expert')
            notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
            notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
            # notnull_dict(purchaser_class,dict_save,'purchaser_class')
            notnull_dict(project_intro, dict_save, 'project_intro')
            # notnull_dict(items, dict_save, 'item')

            notnull_dict(subcontract, dict_save, 'subcontract')
            # notnull_dict(comp_name, dict_save, 'company_name')
            # notnull_dict(comp_contact, dict_save, 'company_contact')
            # notnull_dict(comp_address, dict_save, 'company_address')
            # notnull_dict(comp_tell, dict_save, 'company_tel')
            # notnull_dict(agency_name, dict_save, 'agency_name')
            notnull_dict(agency_contact, dict_save, 'agency_contact')
            # notnull_dict(agency_address, dict_save, 'agency_address')
            # notnull_dict(agency_tel, dict_save, 'agency_tel')
            # notnull_dict(win_bider, dict_save, 'winning_bidder')
            notnull_dict(subject, dict_save, 'subject')
            notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
            notnull_dict(u_l[0], dict_save, 'page_url')
            notnull_dict(str(page_id), dict_save, 'page_id')
            notnull_dict(str(u_l[2]), dict_save, 'website_id')
            # notnull_dict(str(1), dict_save, 'project_id')
            # notnull_dict(u_l[1],dict_save,'page_id')
            # d_save.delete_where('t_bid', 'title', title)
            # print(dict_save,'aaaaaaaaa')
            # print('1111111111111111111111111111111')

            print(dict_save, 'dict_save')

            # try:
            flag = 1
            bid_id = worker.get_id()

            # 提取分包内容，保存到t_bid_pkg表中
            if type == 3 or type == 4:
                try:
                    # pkg_ex(pre_content,bid_id,d_save)
                    pkg_list = yzb_pkg_update.pkg_ex(pre_content, bid_id)
                    yzb_pkg_update.save_package(pkg_list, d_save)

                    win_bider_pkg = yzb_pkg_update.win_bider_to_str(pkg_list)
                    print(win_bider_pkg,'------------win_bider_pkg-------------')
                    if win_bider_pkg:
                        notnull_dict(win_bider_pkg, dict_save, 'winning_bidder')
                    else:
                        notnull_dict(win_bider, dict_save, 'winning_bidder')
                except:
                    pass



            # print(bid_id,'orgin')
            notnull_dict(str(bid_id), dict_save, 'id')
            d_save.insert('t_bid', dict_save)
            logger.info(bid_id)






            # except:
            #     pass
                # del dict_save['id']
                #
                # flag = 0
                #
                # bid_list = d_save.select_where('id,project_date,website_id', 't_bid', 'title="' + title + '" and project_code="'+project_num+'"')[0]
                #
                # bid_id = bid_list[0]
                #
                # bid_date = bid_list[1]
                #
                # website_id = bid_list[2]
                #
                # if website_id != 1:
                #
                #     timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                #
                #     notnull_dict(timeNow, dict_save, 'update_time')
                #
                #     notnull_dict('2', dict_save, 'index_status')
                #     notnull_dict('0', dict_save, 'index_status_reindex')
                #     # print(bid_id,'xxxxxxx')
                #     d_save.update(table='t_bid', data=dict_save, id=bid_id)
                #
                # else:
                #
                #     old_time = time.mktime(time.strptime(bid_date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))
                #
                #     new_time = time.mktime(time.strptime(date, "%Y-%m-%d %H:%M"))
                #
                #     if int(old_time) - int(new_time) > 0:
                #
                #         print('库中数据较新')
                #         d_save.runSql_excute(
                #             'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                #                 '1', str(page_id)))
                #         d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                #
                #         # d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                #
                #         continue
                #
                #     else:
                #
                #         print('爬取数据较新')
                #         # del dict_url['id']
                #
                #         timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                #
                #         notnull_dict(timeNow, dict_save, 'update_time')
                #
                #         notnull_dict('2', dict_save, 'index_status')
                #         notnull_dict('0', dict_save, 'index_status_reindex')
                #         # print(bid_id, 'ooooooo')
                #         d_save.update(table='t_bid', data=dict_save, id=bid_id)
                #
                #         # bid_id = self.d_save.insert('t_bid', dict_save)
                #
                #         # self.d_save.commit_insert()

            # 品目标签
            if items:
                item_save(items, d_save, bid_id)
                notnull_dict('1', dict_save, 'item_from_ccgp')
                d_save.update(table='t_bid', data=dict_save, id=bid_id)
            else:
                itemSort(title, d_save, bid_id)

            # try:
            #     bid_id = d_save.select_where('id','t_bid','title='+'"'+title+'"')[0][0]
            #     print(bid_id)
            # except:
            #     bid_id = None
            c_html = content_html_ex(det_html, url_tag)
            # print(c_html, 'c_html')
            if c_html == '空':
                c_html = None
            # notnull_dict(date, dict_content, 'project_date')
            notnull_dict(html.escape(c_html), dict_content, 'content')
            notnull_dict(html.escape(content), dict_content, 'pure_content')
            # notnull_dict(title, dict_content, 'title')
            notnull_dict(str(bid_id), dict_content, 'bid_id')
            # print(dict_content,'oooooo')
            try:
                content_id = worker.get_id()
                notnull_dict(str(content_id), dict_content, 'id')
                d_save.insert('t_bid_content', dict_content)
                d_save.commit_insert()
                print(content_id, 'content_id')
            except:
                # self.logger.error(sys.exc_info())
                content_id = d_save.select_where('id', 't_bid_content',
                                                 'bid_id='+str(bid_id))[
                    0][0]
                # self.d_save.commit_insert()
                del dict_content['id']
                timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                notnull_dict(timeNow, dict_content, 'update_time')
                d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                d_save.commit_insert()
            # if flag == 1:
            #     # 消息队列
            #     mq_list.append(bid_id)
            #     if len(mq_list) >= 500:
            #         ms = RabbitMQ('admin1', 'admin1', 'subscribe_queue-t')
            #         ms.message_send(mq_list)
            #         mq_list = []
            # website_page分表逻辑
            try:
                d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                d_save.runSql_excute(
                    'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                        '1', str(page_id)))

                d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                d_save.commit_insert()
            except Exception as e:
                d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                d_save.commit_insert()

            with open('page_log.txt', 'w') as w:
                w.writelines(['page:' + str(u_l[1]) + '\n'])
            logger.info('---------------------------------`--------------------')
            n += 1
        except Exception as e:
            n += 1
            # print(e)
            d_save.roll_back_datebase()
            # d_save.insert('t_fail_task', {'fail_page_id': str(u_l[1])})
            d_save.update_one('t_website','mistake_num=mistake_num + 1','id = 1')
            d_save.commit_insert()
            logger.error(sys.exc_info())
    #如果数据爬完mq_list中不足500条，直接推送
    # ms = RabbitMQ('admin1', 'admin1', 'subscribe_queue-t')
    # ms.message_send(mq_list)


def response_html(resp):
        if resp.status_code == 200:
            html = resp.content.decode('utf-8', 'ignore').replace(u'\xa9', u'')
            # print(html)
            return html
        else:
            print(resp.status_code)
            return 404


class FooError(ValueError):
    pass





def show_time(func):
    def wrapper():
        star = time.process_time()
        func()
        end= time.process_time()
        print('spend_time:',end-star)
    return wrapper





@show_time
def main():
    #先运行save_page_url()爬取page_url再运行save_page(det_url_list)爬详情
    # timeNow = time.strftime('%Y-%m-%d 00:00:00', time.localtime(time.time()))
    d_save.update_one('t_website', 'mistake_num=0', 'id = 1')
    d_save.commit_insert()

    # d_save.runSql_excute('insert into t_website_page (id,page_url,mission_id) values (19000000000000000,"http://www.ccgp.gov.cn/cggg/dfgg/gkzb/202112/t20211224_17440910.htm",7)')
    # d_save.commit_insert()
    # time.sleep(60)
    # page = readPageUrl('page_log.txt')


    # dateNow = time.strftime('%Y%m', time.localtime(time.time()))
    # print(dateNow)
    # det_url_list_new = d_save.select_web_where('page_url like "%/t2022%" and a.is_crawled = 0 and a.mission_id = 7')
    # det_url_list_new = d_save.select_web_where('a.is_crawled = 0 and a.mission_id = 7 and a.id = 1572476722501648384')
    det_url_list_new = d_save.select_web_where('a.is_crawled = 0 and a.mission_id = 7 and page_url like "%/t202211%"')
    save_page(det_url_list_new)

    # det_url_list_old = d_save.select_web_where('page_url like "%/t202108%" and a.is_crawled = 0 and a.mission_id = 7')
    # det_url_list_new = d_save.select_web_where('a.is_crawled = 0 and a.mission_id = 7 and page_url like "%202203%"')
    # save_page(det_url_list_old)

    # dateAfter = (date.today() + timedelta(days=-1)).strftime('%Y%m')
    # print(dateAfter)
    # det_url_list_second = d_save.select_web_where(
    #     'page_url like "%/' + dateAfter + '/%" and a.is_crawled = 0 and a.mission_id = 7')
    # save_page(det_url_list_second)


    # det_url_list_old = d_save.select_web_where('page_url like "%/2021%" and is_crawled = 0 and mission_id  = 7')
    # save_page(det_url_list_old)
    # det_url_list = d_save.select_where('page_url,id', 't_website_page',
    #                                    'is_crawled = 0 and mission_id = 7 and id >' + str(page))
    # save_page(det_url_list)
    # server.close()






if __name__ == '__main__':
    contro = ControPy_linux('request_ccgp_gov_cn', logger, d_save)
    contro.spider_opened()
    main()
    contro.spider_closed()

    # get_html('111')







