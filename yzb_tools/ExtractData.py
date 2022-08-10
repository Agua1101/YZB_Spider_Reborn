# coding=UTF-8
from yzb_db_connect import *
from yzb_tag_extract import *
import requests
import random
from yzb_ml_code.purchaser_sort import purchersSort
from yzb_ml_code.purchaser_sort import itemSort
import html
import yzb_ip_proxy
from snow_factory import IdWorker
import snow_settings as sst
from retrying import retry
import json
import ast

# 实例化雪花ID，sst为配置文件
worker = IdWorker(sst.DATACENTER_ID, sst.WORKER_ID, sst.SEQUENCE)

logger = Logger()


class Save_data():

    def __init__(self, d_save=None, url_tag=None, logger=None, url_list=None, web_id=None,
                 table_name='id="zhongbiaoxinxi"'):
        self.d_save = d_save
        self.url_tag = url_tag
        self.logger = logger
        self.url_list = url_list
        self.web_id = web_id
        self.table_name = table_name

    # 详情页字段拆分和存储
    def save_page(self):
        global dict_MQ

        mq_list = []
        u_list = [[i[0], i[1], i[2]] for i in self.url_list]
        for u_l in u_list:
            print(u_l[0])
            flag = 0
            # task_list = requests.get(u_l[0])
            # for i in task_list:
            try:
                dict_save = {}
                dict_content = {}
                headers = {}
                user_agent_list = [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                ]
                headers['User-Agent'] = random.choice(user_agent_list)

                try:
                    # print(u_l[0],'ulululul')
                    det_html = requests.get(u_l[0], headers=headers, verify=False, timeout=5).content.decode('utf-8')
                    det_html = html.unescape(det_html)
                except:
                    det_html = requests.get(u_l[0], headers=headers, verify=False, timeout=5).content.decode('GB18030')
                    det_html = html.unescape(det_html)

                # print(det_html,f'------------------{det_html}--------------------')

                content, pre_content = content_ex(det_html, key=0, url_tag=self.url_tag)

                title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                project_num = project_num_ex(content, url_tag=self.url_tag, det_html=det_html)

                date = date_ex(det_html, content)
                print(date)
                # date = '0000-00-00'

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[comp_address], [title], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag, self.table_name)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)
                print(win_money, 'win_money')

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, project_name))
                page_id = u_l[1]

                project_id = proj_id_ex(u_l[0], self.url_tag, type)

                # print(det_html)
                # print(content, '\n')
                # print(title, 'title')
                # print(project_name, '22222222222')
                # print(project_num, '33333333333')
                # print(type, '55555555')
                # print(method, '666666666')
                # print(project_intro, 'introduction')
                # print(comp_address, 'c_address')
                # print(province, 'province')
                # print(city, 'city')
                # print(town, 'town')
                print(budget_amount, 'b_amount')
                # print(comp_name, 'c_name')
                # print(comp_contact, 'c_man')
                # print(comp_tell, 'c_num')
                # print(agency_address, 'agency_address')
                # print(agency_name, 'agency_name')
                # print(agency_contact, 'agency_contact')
                # print(agency_tel, 'agency_tell')
                # print(win_money, 'win_money')
                # print(subject, 'subject')
                # print(subcontract, 'subcontract')
                # print(win_bider, 'win_bider')
                # print(pro, 'pro')
                # print(page_id, 'page_id')
                # print(purchasers,'purchaser')

                notnull_dict(title, dict_save, 'title')
                notnull_dict(project_name, dict_save, 'project_name')
                notnull_dict(project_num, dict_save, 'project_code')
                notnull_dict(date, dict_save, 'project_date')
                notnull_dict(pro, dict_save, 'expert')
                notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
                notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
                # notnull_dict(purchaser_class,dict_save,'purchaser_class')
                notnull_dict(project_intro, dict_save, 'project_intro')
                notnull_dict(win_money, dict_save, 'bid_money')
                # notnull_dict(items, dict_save, 'item')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')
                notnull_dict(subcontract, dict_save, 'subcontract')
                notnull_dict(budget_amount, dict_save, 'budget_money')
                notnull_dict(comp_name, dict_save, 'company_name')
                notnull_dict(comp_contact, dict_save, 'company_contact')
                notnull_dict(comp_address, dict_save, 'company_address')
                notnull_dict(comp_tell, dict_save, 'company_tel')
                notnull_dict(agency_name, dict_save, 'agency_name')
                notnull_dict(agency_contact, dict_save, 'agency_contact')
                notnull_dict(agency_address, dict_save, 'agency_address')
                notnull_dict(agency_tel, dict_save, 'agency_tel')
                notnull_dict(win_bider, dict_save, 'winning_bidder')
                notnull_dict(subject, dict_save, 'subject')
                notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
                notnull_dict(u_l[0], dict_save, 'page_url')
                notnull_dict(str(page_id), dict_save, 'page_id')
                notnull_dict(str(u_l[2]), dict_save, 'website_id')
                notnull_dict(project_id, dict_save, 'project_id')
                # notnull_dict(u_l[1],dict_save,'page_id')
                # self.d_save.delete_where('t_bid', 'title', title)
                # print(dict_save,'aaaaaaaaa')

                try:

                    # 将插入t_bid表
                    bid_id = worker.get_id()
                    notnull_dict(str(bid_id), dict_save, 'id')
                    self.d_save.insert('t_bid', dict_save)
                    # self.d_save.commit_insert()
                    print(bid_id)

                    # 日期在一个月以内存入MQ
                    date_tag = self.date_limit(date)
                    if date_tag == 1:
                        flag = 1

                    # print(bid_id)
                except:
                    flag = 0
                    bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                         project_num)
                    # self.d_save.commit_insert()
                    if project_date_old:

                        if latest_date(project_date_old, date):
                            continue

                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    del dict_save['id']
                    notnull_dict(timeNow, dict_save, 'update_time')
                    notnull_dict('2', dict_save, 'index_status')
                    notnull_dict('0', dict_save, 'index_status_reindex')
                    self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

                if type == 3 or type == 4:
                    pkg_ex(pre_content, bid_id, self.d_save)

                # 品目标签
                itemSort(title, self.d_save, bid_id)

                # try:
                #     bid_id = d_save.select_where('id','t_bid','title='+'"'+title+'"')[0][0]
                #     print(bid_id)
                # except:
                #     bid_id = None
                # self.d_save.delete_where('t_bid_content', 'title', title)

                c_html = content_html_ex(det_html, self.url_tag, page_url=u_l[0])
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
                    self.d_save.insert('t_bid_content', dict_content)
                    self.d_save.commit_insert()
                    print(content_id, 'content_id')
                except:
                    # self.logger.error(sys.exc_info())
                    content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
                    # self.d_save.commit_insert()
                    del dict_content['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_content, 'update_time')

                    self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                    self.d_save.commit_insert()

                print(111111)
                try:
                    # website_page分表逻辑
                    self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    # self.d_save.commit_insert()
                    self.d_save.runSql_excute(
                        'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                            str(self.web_id), str(page_id)))

                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                except:
                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                print(222222)
                with open('log.txt', 'w') as w:
                    w.writelines(['page:' + str(u_l[0]) + '\n'])
                print('---------------------------------`--------------------')
            except Exception as e:
                self.logger.error(sys.exc_info())
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task',{'fail_page_id':str(u_l[1])})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()

        # 如果数据爬完mq_list中不足500条，直接推送
        # ms = RabbitMQ('admin1', 'admin1', 'subscribe_queue-t')
        # ms.message_send(mq_list)

    def save_lnggzy(self):
        global dict_MQ

        mq_list = []
        u_list = [[i[0], i[1], i[2]] for i in self.url_list]
        for u_l in u_list:
            page_url = u_l[0]
            page_id = u_l[1]
            website_id = u_l[2]
            print(u_l[0])
            flag = 0
            # task_list = requests.get(u_l[0])
            # for i in task_list:
            try:
                dict_save = {}
                dict_content = {}
                headers = {}
                user_agent_list = [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                ]
                headers['User-Agent'] = random.choice(user_agent_list)

                try:
                    # print(u_l[0],'ulululul')
                    det_html = requests.get(u_l[0], headers=headers, verify=False, timeout=5).content.decode('utf-8')
                    det_html = html.unescape(det_html)
                except:
                    det_html = requests.get(u_l[0], headers=headers, verify=False, timeout=5).content.decode('GB18030')
                    det_html = html.unescape(det_html)

                # print(det_html, f'------------------{det_html}--------------------')

                content, pre_content = content_ex(det_html, key=0)

                title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                project_num = project_num_ex(content, url_tag=self.url_tag, det_html=det_html)

                date = date_ex(det_html, content)
                print(date)
                # date = '0000-00-00'

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag, self.table_name)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, comp_name))

                project_id = proj_id_ex(page_url, self.url_tag, type)

                self.save_part(dict_save=dict_save, title=title, project_name=project_name, project_num=project_num,
                               date=date, pro=pro, method=method, type=type,
                               project_intro=project_intro, win_money=win_money, province=province, city=city,
                               town=town,
                               subcontract=subcontract, budget_amount=budget_amount, comp_name=comp_name,
                               comp_contact=comp_contact, comp_address=comp_address, comp_tell=comp_tell,
                               agency_name=agency_name, agency_contact=agency_contact, agency_address=agency_address,
                               agency_tel=agency_tel, win_bider=win_bider, subject=subject, purchasers=purchasers,
                               page_url=page_url, page_id=page_id, project_id=project_id,
                               det_html=det_html, dict_content=dict_content, content=content, website_id=website_id,
                               pre_content=pre_content)

            except Exception as e:
                self.logger.error(sys.exc_info())
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task', {'fail_page_id': str(page_id)})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()

    def save_ggzyjy_gansu(self):
        global dict_MQ

        mq_list = []
        u_list = [[i[0], i[1], i[2], i[3]] for i in self.url_list]
        for u_l in u_list:
            print(u_l[0])
            flag = 0

            page_url = u_l[0]
            page_id = u_l[1]
            website_id = u_l[3]
            try:

                extra = ast.literal_eval(u_l[2])
                title = extra['title']
                date = extra['date']
                flow_data = extra['flow_data']
                flow_url = extra['flow_url']

                dict_save = {}
                dict_content = {}
                headers = {}
                user_agent_list = [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                ]
                headers['User-Agent'] = random.choice(user_agent_list)

                det_html = requests.post(url=flow_url, headers=headers, data=flow_data).text

                content, pre_content = content_ex(det_html, key=1)
                if not title:
                    title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                project_num = project_num_ex(content, url_tag=self.url_tag, det_html=det_html)

                if not date:
                    date = date_ex(det_html, content)
                print(date)
                # date = '0000-00-00'

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag, self.table_name)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, comp_name))

                project_id = proj_id_ex(page_url, self.url_tag, type)

                self.save_part(dict_save=dict_save, title=title, project_name=project_name, project_num=project_num,
                               date=date, pro=pro, method=method, type=type,
                               project_intro=project_intro, win_money=win_money, province=province, city=city,
                               town=town,
                               subcontract=subcontract, budget_amount=budget_amount, comp_name=comp_name,
                               comp_contact=comp_contact, comp_address=comp_address, comp_tell=comp_tell,
                               agency_name=agency_name, agency_contact=agency_contact, agency_address=agency_address,
                               agency_tel=agency_tel, win_bider=win_bider, subject=subject, purchasers=purchasers,
                               page_url=page_url, page_id=page_id, project_id=project_id,
                               det_html=det_html, dict_content=dict_content, content=content, website_id=website_id,
                               pre_content=pre_content)

            except Exception as e:
                self.logger.error(sys.exc_info())
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task',{'fail_page_id':str(page_id)})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()

    def save_part(self, dict_save=None, title=None, project_name=None, project_num=None, date=None, pro=None,
                  method=None, type=None,
                  project_intro=None, win_money=None, province=None, city=None, town=None,
                  subcontract=None, budget_amount=None, comp_name=None, comp_contact=None, comp_address=None,
                  comp_tell=None,
                  agency_name=None, agency_contact=None, agency_address=None,
                  agency_tel=None, win_bider=None, subject=None, purchasers=None, page_url=None, page_id=None,
                  project_id=None,
                  det_html=None, dict_content=None, content=None, website_id=None, pre_content=None):
        # print(det_html)
        # print(content, '\n')
        # print(title, 'title')
        # print(project_name, '22222222222')
        # print(project_num, '33333333333')
        # print(type, '55555555')
        # print(method, '666666666')
        # print(project_intro, 'introduction')
        # print(comp_address, 'c_address')
        # print(province, 'province')
        # print(city, 'city')
        # print(town, 'town')
        print(budget_amount, 'b_amount')
        # print(comp_name, 'c_name')
        # print(comp_contact, 'c_man')
        # print(comp_tell, 'c_num')
        # print(agency_address, 'agency_address')
        # print(agency_name, 'agency_name')
        # print(agency_contact, 'agency_contact')
        # print(agency_tel, 'agency_tell')
        # print(win_money, 'win_money')
        # print(subject, 'subject')
        # print(subcontract, 'subcontract')
        # print(win_bider, 'win_bider')
        # print(pro, 'pro')
        # print(page_id, 'page_id')
        # print(purchasers,'purchaser')

        notnull_dict(title, dict_save, 'title')
        notnull_dict(project_name, dict_save, 'project_name')
        notnull_dict(project_num, dict_save, 'project_code')
        notnull_dict(date, dict_save, 'project_date')
        notnull_dict(pro, dict_save, 'expert')
        notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
        notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
        # notnull_dict(purchaser_class,dict_save,'purchaser_class')
        notnull_dict(project_intro, dict_save, 'project_intro')
        notnull_dict(win_money, dict_save, 'bid_money')
        # notnull_dict(items, dict_save, 'item')
        notnull_dict(province, dict_save, 'province')
        notnull_dict(city, dict_save, 'city')
        notnull_dict(town, dict_save, 'town')
        notnull_dict(subcontract, dict_save, 'subcontract')
        notnull_dict(budget_amount, dict_save, 'budget_money')
        notnull_dict(comp_name, dict_save, 'company_name')
        notnull_dict(comp_contact, dict_save, 'company_contact')
        notnull_dict(comp_address, dict_save, 'company_address')
        notnull_dict(comp_tell, dict_save, 'company_tel')
        notnull_dict(agency_name, dict_save, 'agency_name')
        notnull_dict(agency_contact, dict_save, 'agency_contact')
        notnull_dict(agency_address, dict_save, 'agency_address')
        notnull_dict(agency_tel, dict_save, 'agency_tel')
        notnull_dict(win_bider, dict_save, 'winning_bidder')
        notnull_dict(subject, dict_save, 'subject')
        notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
        notnull_dict(page_url, dict_save, 'page_url')
        notnull_dict(str(page_id), dict_save, 'page_id')
        notnull_dict(str(website_id), dict_save, 'website_id')
        notnull_dict(project_id, dict_save, 'project_id')
        # notnull_dict(u_l[1],dict_save,'page_id')
        # self.d_save.delete_where('t_bid', 'title', title)
        # print(dict_save,'aaaaaaaaa')

        try:
            count = self.d_save.select_where('count(*)', 't_bid',
                                             'title= "{}" and project_code = "{}" and website_id = 1'.format(
                                                 MySQLdb.escape_string(title).decode('utf-8'), project_num))[0][0]
            if count:
                try:
                    # print(page_id,'page_id')
                    self.logger.info('数据库中已存在')
                    self.d_save.runSql_excute(
                        'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                            str(self.web_id), str(page_id)))
                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    self.d_save.commit_insert()
                    print(count)

                except:
                    self.d_save.roll_back_datebase()
                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    self.d_save.commit_insert()

                return

            # 将插入t_bid表
            bid_id = worker.get_id()
            notnull_dict(str(bid_id), dict_save, 'id')
            self.d_save.insert('t_bid', dict_save)
            # self.d_save.commit_insert()
            print(bid_id)

            if type == 3 or type == 4:
                pkg_ex(pre_content, bid_id, self.d_save)

            # 日期在一个月以内存入MQ
            date_tag = self.date_limit(date)
            if date_tag == 1:
                flag = 1

            # print(bid_id)
        except:
            flag = 0
            bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                 project_num)
            # self.d_save.commit_insert()
            if project_date_old:

                if latest_date(project_date_old, date):
                    return

            timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            del dict_save['id']
            notnull_dict(timeNow, dict_save, 'update_time')
            notnull_dict('2', dict_save, 'index_status')
            notnull_dict('0', dict_save, 'index_status_reindex')
            self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

        # 品目标签
        itemSort(title, self.d_save, bid_id)

        # try:
        #     bid_id = d_save.select_where('id','t_bid','title='+'"'+title+'"')[0][0]
        #     print(bid_id)
        # except:
        #     bid_id = None
        # self.d_save.delete_where('t_bid_content', 'title', title)

        c_html = content_html_ex(det_html, self.url_tag, page_url=page_url)
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
            self.d_save.insert('t_bid_content', dict_content)
            self.d_save.commit_insert()
            print(content_id, 'content_id')
        except:
            # self.logger.error(sys.exc_info())
            content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
            # self.d_save.commit_insert()
            del dict_content['id']
            timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            notnull_dict(timeNow, dict_content, 'update_time')

            self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
            self.d_save.commit_insert()

        print(111111)
        try:
            # website_page分表逻辑
            self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
            # self.d_save.commit_insert()
            self.d_save.runSql_excute(
                'insert into t_website_page_{} select * from t_website_page where id = {}'.format(str(self.web_id),
                                                                                                  str(page_id)))

            self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
            self.d_save.commit_insert()
        except:
            self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
            self.d_save.commit_insert()
        print(222222)
        with open('log.txt', 'w') as w:
            w.writelines(['page:' + str(page_url) + '\n'])
        print('---------------------------------`--------------------')

    def save_page_guizhou(self):
        global dict_MQ

        mq_list = []
        u_list = [[i[0], i[1], i[2]] for i in self.url_list]
        for u_l in u_list:
            print(u_l[0])
            flag = 0
            det_url = 'http://ggzy.guizhou.gov.cn/igs/front/search/list.html?pageNumber=1&pageSize=1&siteId=500483&index=trades&type=infomation_v6&filter[MetaDataId]=' + \
                      u_l[0].split('=').pop()
            # task_list = requests.get(u_l[0])
            # for i in task_list:
            try:
                dict_save = {}
                dict_content = {}
                headers = {}
                user_agent_list = [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                ]
                headers['User-Agent'] = random.choice(user_agent_list)

                det_dict = requests.get(url=det_url, headers=headers).json()['page']['content'][0]
                # print(det_dict)

                det_html = det_dict['docContent']
                date = det_dict['docRelTime']
                project_num_from_json = det_dict['tenderProjectCode']
                title = det_dict['docTitle']

                content, pre_content = content_ex(det_html, key=1)

                if not title:
                    title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                project_num = project_num_ex(content, self.url_tag, det_html)
                if not project_num:
                    project_num = project_num_filter(project_num_from_json)

                if not date:
                    date = date_ex(det_html, content)
                print(date)
                # date = '0000-00-00'

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag, self.table_name)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, project_name))
                page_id = u_l[1]

                project_id = proj_id_ex(det_url, self.url_tag, type)

                # print(det_html)
                # print(content, '\n')
                # print(title, 'title')
                # print(project_name, '22222222222')
                # print(project_num, '33333333333')
                # print(type, '55555555')
                # print(method, '666666666')
                # print(project_intro, 'introduction')
                # print(comp_address, 'c_address')
                # print(province, 'province')
                # print(city, 'city')
                # print(town, 'town')
                print(budget_amount, 'b_amount')
                # print(comp_name, 'c_name')
                # print(comp_contact, 'c_man')
                # print(comp_tell, 'c_num')
                # print(agency_address, 'agency_address')
                # print(agency_name, 'agency_name')
                # print(agency_contact, 'agency_contact')
                # print(agency_tel, 'agency_tell')
                # print(win_money, 'win_money')
                # print(subject, 'subject')
                # print(subcontract, 'subcontract')
                # print(win_bider, 'win_bider')
                # print(pro, 'pro')
                # print(page_id, 'page_id')
                # print(purchasers,'purchaser')

                notnull_dict(title, dict_save, 'title')
                notnull_dict(project_name, dict_save, 'project_name')
                notnull_dict(project_num, dict_save, 'project_code')
                notnull_dict(date, dict_save, 'project_date')
                notnull_dict(pro, dict_save, 'expert')
                notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
                notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
                # notnull_dict(purchaser_class,dict_save,'purchaser_class')
                notnull_dict(project_intro, dict_save, 'project_intro')
                notnull_dict(win_money, dict_save, 'bid_money')
                # notnull_dict(items, dict_save, 'item')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')
                notnull_dict(subcontract, dict_save, 'subcontract')
                notnull_dict(budget_amount, dict_save, 'budget_money')
                notnull_dict(comp_name, dict_save, 'company_name')
                notnull_dict(comp_contact, dict_save, 'company_contact')
                notnull_dict(comp_address, dict_save, 'company_address')
                notnull_dict(comp_tell, dict_save, 'company_tel')
                notnull_dict(agency_name, dict_save, 'agency_name')
                notnull_dict(agency_contact, dict_save, 'agency_contact')
                notnull_dict(agency_address, dict_save, 'agency_address')
                notnull_dict(agency_tel, dict_save, 'agency_tel')
                notnull_dict(win_bider, dict_save, 'winning_bidder')
                notnull_dict(subject, dict_save, 'subject')
                notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
                notnull_dict(u_l[0], dict_save, 'page_url')
                notnull_dict(str(page_id), dict_save, 'page_id')
                notnull_dict(str(u_l[2]), dict_save, 'website_id')
                notnull_dict(project_id, dict_save, 'project_id')
                # notnull_dict(u_l[1],dict_save,'page_id')
                # self.d_save.delete_where('t_bid', 'title', title)
                # print(dict_save,'aaaaaaaaa')

                try:

                    # 将插入t_bid表
                    bid_id = worker.get_id()
                    notnull_dict(str(bid_id), dict_save, 'id')
                    self.d_save.insert('t_bid', dict_save)
                    # self.d_save.commit_insert()
                    print(bid_id)

                    if type == 3 or type == 4:
                        pkg_ex(pre_content, bid_id, self.d_save)

                    # 日期在一个月以内存入MQ
                    date_tag = self.date_limit(date)
                    if date_tag == 1:
                        flag = 1

                    # print(bid_id)
                except:
                    flag = 0
                    bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                         project_num)
                    # self.d_save.commit_insert()
                    if project_date_old:

                        if latest_date(project_date_old, date):
                            continue

                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    del dict_save['id']
                    notnull_dict(timeNow, dict_save, 'update_time')
                    notnull_dict('2', dict_save, 'index_status')
                    notnull_dict('0', dict_save, 'index_status_reindex')
                    self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

                # 品目标签
                itemSort(title, self.d_save, bid_id)

                c_html = content_html_ex(det_html, self.url_tag, page_url=det_url)
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
                    self.d_save.insert('t_bid_content', dict_content)
                    self.d_save.commit_insert()
                    print(content_id, 'content_id')
                except:
                    # self.logger.error(sys.exc_info())
                    content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
                    # self.d_save.commit_insert()
                    del dict_content['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_content, 'update_time')

                    self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                    self.d_save.commit_insert()

                print(111111)
                try:
                    # website_page分表逻辑
                    self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    # self.d_save.commit_insert()
                    self.d_save.runSql_excute(
                        'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                            str(self.web_id), str(page_id)))

                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                except:
                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                print(222222)
                with open('log.txt', 'w') as w:
                    w.writelines(['page:' + str(u_l[0]) + '\n'])
                print('---------------------------------`--------------------')
            except Exception as e:
                self.logger.error(sys.exc_info())
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task',{'fail_page_id':str(u_l[1])})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()

    def save_page_chongqing(self):
        global dict_MQ
        n = 0
        ip_list = ip_proxy.proxy_ip2()
        mq_list = []
        u_list = [[i[0], i[1], i[2], i[3]] for i in self.url_list]
        for u_l in u_list:
            print(u_l[0])
            flag = 0
            # task_list = requests.get(u_l[0])
            # for i in task_list:
            project_num = u_l[2]

            try:
                dict_save = {}
                dict_content = {}
                headers = {}
                if n >= 30:
                    ip_list = ip_proxy.proxy_ip2()
                    n = 0
                user_agent_list = [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                ]
                headers['User-Agent'] = random.choice(user_agent_list)

                # print(u_l[0],'ulululul')
                det_html = self.html_retry(url=u_l[0], n=n, ip_list=ip_list)
                det_html = html.unescape(det_html)

                content, pre_content = content_ex(det_html, key=0, url_tag=self.url_tag)

                title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                if not project_num:
                    project_num = project_num_ex(content, url_tag=self.url_tag, det_html=det_html)

                date = date_ex(det_html, content)
                print(date)
                # date = '0000-00-00'

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag, self.table_name)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, project_name))
                page_id = u_l[1]

                project_id = proj_id_ex(u_l[0], self.url_tag, type)

                # print(det_html)
                # print(content, '\n')
                # print(title, 'title')
                # print(project_name, '22222222222')
                # print(project_num, '33333333333')
                # print(type, '55555555')
                # print(method, '666666666')
                # print(project_intro, 'introduction')
                # print(comp_address, 'c_address')
                # print(province, 'province')
                # print(city, 'city')
                # print(town, 'town')
                print(budget_amount, 'b_amount')
                # print(comp_name, 'c_name')
                # print(comp_contact, 'c_man')
                # print(comp_tell, 'c_num')
                # print(agency_address, 'agency_address')
                # print(agency_name, 'agency_name')
                # print(agency_contact, 'agency_contact')
                # print(agency_tel, 'agency_tell')
                # print(win_money, 'win_money')
                # print(subject, 'subject')
                # print(subcontract, 'subcontract')
                # print(win_bider, 'win_bider')
                # print(pro, 'pro')
                # print(page_id, 'page_id')
                # print(purchasers,'purchaser')

                notnull_dict(title, dict_save, 'title')
                notnull_dict(project_name, dict_save, 'project_name')
                notnull_dict(project_num, dict_save, 'project_code')
                notnull_dict(date, dict_save, 'project_date')
                notnull_dict(pro, dict_save, 'expert')
                notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
                notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
                # notnull_dict(purchaser_class,dict_save,'purchaser_class')
                notnull_dict(project_intro, dict_save, 'project_intro')
                notnull_dict(win_money, dict_save, 'bid_money')
                # notnull_dict(items, dict_save, 'item')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')
                notnull_dict(subcontract, dict_save, 'subcontract')
                notnull_dict(budget_amount, dict_save, 'budget_money')
                notnull_dict(comp_name, dict_save, 'company_name')
                notnull_dict(comp_contact, dict_save, 'company_contact')
                notnull_dict(comp_address, dict_save, 'company_address')
                notnull_dict(comp_tell, dict_save, 'company_tel')
                notnull_dict(agency_name, dict_save, 'agency_name')
                notnull_dict(agency_contact, dict_save, 'agency_contact')
                notnull_dict(agency_address, dict_save, 'agency_address')
                notnull_dict(agency_tel, dict_save, 'agency_tel')
                notnull_dict(win_bider, dict_save, 'winning_bidder')
                notnull_dict(subject, dict_save, 'subject')
                notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
                notnull_dict(u_l[0], dict_save, 'page_url')
                notnull_dict(str(page_id), dict_save, 'page_id')
                notnull_dict(str(u_l[3]), dict_save, 'website_id')
                notnull_dict(project_id, dict_save, 'project_id')
                # notnull_dict(u_l[1],dict_save,'page_id')
                # self.d_save.delete_where('t_bid', 'title', title)
                # print(dict_save,'aaaaaaaaa')

                try:
                    # count = self.d_save.select_where('count(*)', 't_bid', 'title= "{}" and project_code = "{}" and website_id = 1'.format(MySQLdb.escape_string(title).decode('utf-8'),project_num))[0][0]
                    # if count:
                    #     try:
                    #         # print(page_id,'page_id')
                    #         self.logger.info('数据库中已存在')
                    #         self.d_save.runSql_excute(
                    #             'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                    #                 str(self.web_id), str(page_id)))
                    #         self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    #         # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    #         self.d_save.commit_insert()
                    #         print(count)
                    #
                    #     except:
                    #         self.d_save.roll_back_datebase()
                    #         self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    #         # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    #         self.d_save.commit_insert()
                    #
                    #     continue

                    # 将插入t_bid表
                    bid_id = worker.get_id()
                    notnull_dict(str(bid_id), dict_save, 'id')
                    self.d_save.insert('t_bid', dict_save)
                    # self.d_save.commit_insert()
                    print(bid_id)

                    if type == 3 or type == 4:
                        pkg_ex(pre_content, bid_id, self.d_save)

                    # 日期在一个月以内存入MQ
                    date_tag = self.date_limit(date)
                    if date_tag == 1:
                        flag = 1

                    # print(bid_id)
                except:
                    flag = 0
                    bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                         project_num)
                    # self.d_save.commit_insert()
                    if project_date_old:

                        if latest_date(project_date_old, date):
                            continue

                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    del dict_save['id']
                    notnull_dict(timeNow, dict_save, 'update_time')
                    notnull_dict('2', dict_save, 'index_status')
                    notnull_dict('0', dict_save, 'index_status_reindex')
                    self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

                # 品目标签
                itemSort(title, self.d_save, bid_id)

                c_html = content_html_ex(det_html, self.url_tag, page_url=u_l[0])
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
                    self.d_save.insert('t_bid_content', dict_content)
                    self.d_save.commit_insert()
                    print(content_id, 'content_id')
                except:
                    # self.logger.error(sys.exc_info())
                    content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
                    # self.d_save.commit_insert()
                    del dict_content['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_content, 'update_time')

                    self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                    self.d_save.commit_insert()

                print(111111)
                try:
                    # website_page分表逻辑
                    self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    # self.d_save.commit_insert()
                    self.d_save.runSql_excute(
                        'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                            str(self.web_id), str(page_id)))

                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                except:
                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                print(222222)
                with open('log.txt', 'w') as w:
                    w.writelines(['page:' + str(u_l[0]) + '\n'])
                print('---------------------------------`--------------------')
                n += 1
            except Exception as e:
                self.logger.error(sys.exc_info())
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task',{'fail_page_id':str(u_l[1])})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()
                n += 1

    def save_page_hubei(self):
        global dict_MQ

        mq_list = []
        u_list = [[i[0], i[1], i[2]] for i in self.url_list]
        for u_l in u_list:
            print(u_l[0])
            flag = 0
            # task_list = requests.get(u_l[0])
            # for i in task_list:
            try:
                dict_save = {}
                dict_content = {}
                headers = {}
                user_agent_list = [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                ]
                headers['User-Agent'] = random.choice(user_agent_list)

                det_html = requests.get(url=u_l[0], headers=headers, verify=False, timeout=5).text
                # print(det_html)
                project_num = etree.HTML(det_html).xpath('//input[@id="purchaseProjectCode"]/@value')[0]
                print(project_num)
                url_dict = {0: 'https://www.hbggzyfwpt.cn/jyxxAjax/zfcg/zfcgCgggLiDetail',
                            1: 'https://www.hbggzyfwpt.cn/jyxxAjax/zfcg/zfcgGzsxLiDetail',
                            2: 'https://www.hbggzyfwpt.cn/jyxxAjax/zfcg/zfcgCgjgLiDetail',
                            3: 'https://www.hbggzyfwpt.cn/jyxxAjax/zfcg/zfcgCghtLiDetail',
                            }
                sonFlag = etree.HTML(det_html).xpath('//input[@id="sonFlag"]/@value')
                sonFlag = int(sonFlag[0]) if sonFlag else 0
                # print(url_dict[sonFlag])

                det_json = requests.post(url=url_dict[sonFlag], data={'purchaseProjectCode': str(project_num)},
                                         headers=headers, verify=False, timeout=5).json()['list'][0]
                # print(det_json)
                win_money = None
                if sonFlag == 0:
                    det_html = det_json['bulletinContent']
                    title = det_json['bulletinTitle']
                    date = det_json['bulletinStartTime']
                elif sonFlag == 1:
                    det_html = det_json['terminationBulletinContent']
                    title = det_json['terminationBulletinTitle']
                    date = det_json['modificationStartTime']
                else:
                    det_html = det_json['winBidBulletinContent']
                    title = det_json['winBidBulletinTitle']
                    date = det_json['winBidBulletinStartTime']
                    win_money = det_json['winBidPrice']
                    if win_money:
                        win_money = str(int(win_money * 1000000))

                content, pre_content = content_ex(det_html, key=1)
                if not title:
                    title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                project_num = project_num_ex(content, url_tag=self.url_tag, det_html=det_html)
                if not date:
                    date = date_ex(det_html, content)
                print(date)

                is_date = re.search('\d{4}-\d{1,2}-\d{1,2}', date)
                if not is_date:
                    date = None

                # date = '0000-00-00'

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag, self.table_name)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                if not win_money:
                    win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, project_name))
                page_id = u_l[1]

                project_id = proj_id_ex(u_l[0], self.url_tag, type)

                # print(det_html)
                # print(content, '\n')
                # print(title, 'title')
                # print(project_name, '22222222222')
                # print(project_num, '33333333333')
                # print(type, '55555555')
                # print(method, '666666666')
                # print(project_intro, 'introduction')
                # print(comp_address, 'c_address')
                # print(province, 'province')
                # print(city, 'city')
                # print(town, 'town')
                print(budget_amount, 'b_amount')
                # print(comp_name, 'c_name')
                # print(comp_contact, 'c_man')
                # print(comp_tell, 'c_num')
                # print(agency_address, 'agency_address')
                # print(agency_name, 'agency_name')
                # print(agency_contact, 'agency_contact')
                # print(agency_tel, 'agency_tell')
                # print(win_money, 'win_money')
                # print(subject, 'subject')
                # print(subcontract, 'subcontract')
                # print(win_bider, 'win_bider')
                # print(pro, 'pro')
                # print(page_id, 'page_id')
                # print(purchasers,'purchaser')

                notnull_dict(title, dict_save, 'title')
                notnull_dict(project_name, dict_save, 'project_name')
                notnull_dict(project_num, dict_save, 'project_code')
                notnull_dict(date, dict_save, 'project_date')
                notnull_dict(pro, dict_save, 'expert')
                notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
                notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
                # notnull_dict(purchaser_class,dict_save,'purchaser_class')
                notnull_dict(project_intro, dict_save, 'project_intro')
                notnull_dict(win_money, dict_save, 'bid_money')
                # notnull_dict(items, dict_save, 'item')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')
                notnull_dict(subcontract, dict_save, 'subcontract')
                notnull_dict(budget_amount, dict_save, 'budget_money')
                notnull_dict(comp_name, dict_save, 'company_name')
                notnull_dict(comp_contact, dict_save, 'company_contact')
                notnull_dict(comp_address, dict_save, 'company_address')
                notnull_dict(comp_tell, dict_save, 'company_tel')
                notnull_dict(agency_name, dict_save, 'agency_name')
                notnull_dict(agency_contact, dict_save, 'agency_contact')
                notnull_dict(agency_address, dict_save, 'agency_address')
                notnull_dict(agency_tel, dict_save, 'agency_tel')
                notnull_dict(win_bider, dict_save, 'winning_bidder')
                notnull_dict(subject, dict_save, 'subject')
                notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
                notnull_dict(u_l[0], dict_save, 'page_url')
                notnull_dict(str(page_id), dict_save, 'page_id')
                notnull_dict(str(u_l[2]), dict_save, 'website_id')
                notnull_dict(project_id, dict_save, 'project_id')
                # notnull_dict(u_l[1],dict_save,'page_id')
                # self.d_save.delete_where('t_bid', 'title', title)
                # print(dict_save,'aaaaaaaaa')

                try:
                    # count = self.d_save.select_where('count(*)', 't_bid', 'title= "{}" and project_code = "{}" and website_id = 1'.format(MySQLdb.escape_string(title).decode('utf-8'),project_num))[0][0]
                    # if count:
                    #     try:
                    #         # print(page_id,'page_id')
                    #         self.logger.info('数据库中已存在')
                    #         self.d_save.runSql_excute(
                    #             'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                    #                 str(self.web_id), str(page_id)))
                    #         self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    #         # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    #         self.d_save.commit_insert()
                    #         print(count)
                    #
                    #     except:
                    #         self.d_save.roll_back_datebase()
                    #         self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    #         # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    #         self.d_save.commit_insert()
                    #
                    #     continue

                    # 将插入t_bid表
                    bid_id = worker.get_id()
                    notnull_dict(str(bid_id), dict_save, 'id')
                    self.d_save.insert('t_bid', dict_save)
                    # self.d_save.commit_insert()
                    print(bid_id)

                    if type == 3 or type == 4:
                        pkg_ex(pre_content, bid_id, self.d_save)

                    # 日期在一个月以内存入MQ
                    date_tag = self.date_limit(date)
                    if date_tag == 1:
                        flag = 1

                    # print(bid_id)
                except:
                    flag = 0
                    bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                         project_num)
                    # self.d_save.commit_insert()
                    if project_date_old:

                        if latest_date(project_date_old, date):
                            continue

                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    del dict_save['id']
                    notnull_dict(timeNow, dict_save, 'update_time')
                    notnull_dict('2', dict_save, 'index_status')
                    notnull_dict('0', dict_save, 'index_status_reindex')
                    self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

                # 品目标签
                itemSort(title, self.d_save, bid_id)

                c_html = content_html_ex(det_html, self.url_tag, page_url=u_l[0])
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
                    self.d_save.insert('t_bid_content', dict_content)
                    self.d_save.commit_insert()
                    print(content_id, 'content_id')
                except:
                    # self.logger.error(sys.exc_info())
                    content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
                    # self.d_save.commit_insert()
                    del dict_content['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_content, 'update_time')

                    self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                    self.d_save.commit_insert()

                print(111111)
                try:
                    # website_page分表逻辑
                    self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    # self.d_save.commit_insert()
                    self.d_save.runSql_excute(
                        'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                            str(self.web_id), str(page_id)))

                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                except:
                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                print(222222)
                with open('log.txt', 'w') as w:
                    w.writelines(['page:' + str(u_l[0]) + '\n'])
                print('---------------------------------`--------------------')
            except Exception as e:
                self.logger.error(sys.exc_info())
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task',{'fail_page_id':str(u_l[1])})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()

    @staticmethod
    def date_limit(date):
        try:
            if date == None or date == '空':
                return 0

            try:
                date_mk = time.mktime(time.strptime(date, '%Y-%m-%d %H:%M'))
                date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
                date_now_mk = time.mktime(time.strptime(date_now, "%Y-%m-%d %H:%M"))
            except:
                date_mk = time.mktime(time.strptime(date, '%Y-%m-%d'))
                date_now = datetime.datetime.now().strftime('%Y-%m-%d')
                date_now_mk = time.mktime(time.strptime(date_now, "%Y-%m-%d"))

            compare = int(date_now_mk) - int(date_mk)

            # 比较日期是否小于30天
            if compare < 2592000:
                return 1

        except Exception as e:
            print(e)

    @retry(stop_max_attempt_number=2)
    def html_retry(self, url='', n=0, ip_list=None):
        # time.sleep(0.5)
        proxies = ip_proxy.proxy_amount(ip_list)
        logger.info(proxies)

        headers = {}
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]
        headers['User-Agent'] = random.choice(user_agent_list)
        response = requests.get(url, headers=headers, proxies=proxies, verify=False, timeout=5)
        # print(response)
        try:
            all_html = response.content.decode('utf-8')
        except:
            all_html = response.content.decode('GB18030')

        # print(det_dict)

        print(n, 'xxxxxxxx')
        return all_html

    def save_zcy(self):
        n = 0
        ip_list = ip_proxy.proxy_ip2()
        mq_list = []

        u_list = [[i[0], i[1], i[2]] for i in self.url_list]
        for u_l in u_list:
            print(u_l[0])
            flag = 0
            # task_list = requests.get(u_l[0])
            # for i in task_list:
            try:
                dict_save = {}
                dict_content = {}

                if n >= 40:
                    ip_list = ip_proxy.proxy_ip2()
                    n = 0
                all_html = self.html_retry(url=u_l[0], n=n, ip_list=ip_list)

                det_json = etree.HTML(all_html).xpath('//input[@name="articleDetail"]/@value')[0]
                det_dict = json.loads(det_json)

                det_html = det_dict['content']
                # print(det_html)

                content, pre_content = content_ex(det_html, key=1)
                # print(content)
                title = det_dict['title']
                print(title)
                date = det_dict['publishDate']
                print(date)
                project_num_d = det_dict['projectCode']
                print(project_num_d)

                if not content:
                    content, pre_content = content_ex(det_html, key=0, url_tag=self.url_tag)

                if not title:
                    title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                project_num = project_num_ex(content, self.url_tag, det_html)
                if not project_num:
                    project_num = project_num_d

                if not date or valid_date(date) == 0:
                    date = date_ex(det_html, content)
                    print(date)

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, comp_name))
                page_id = u_l[1]
                page_url = u_l[0]

                project_id = proj_id_ex(u_l[0], self.url_tag, type)
                # print(det_html)
                # print(content, '\n')
                # print(title, 'title')
                # print(project_name, '22222222222')
                # print(project_num, '33333333333')
                # print(type, '55555555')
                # print(method, '666666666')
                # print(project_intro, 'introduction')
                # print(comp_address, 'c_address')
                # print(province, 'province')
                # print(city, 'city')
                # print(town, 'town')
                # print(budget_amount, 'b_amount')
                # print(comp_name, 'c_name')
                # print(comp_contact, 'c_man')
                # print(comp_tell, 'c_num')
                # print(agency_address, 'agency_address')
                # print(agency_name, 'agency_name')
                # print(agency_contact, 'agency_contact')
                # print(agency_tel, 'agency_tell')
                # print(win_money, 'win_money')
                # print(subject, 'subject')
                # print(subcontract, 'subcontract')
                # print(win_bider, 'win_bider')
                # print(pro, 'pro')
                # print(page_id, 'page_id')
                # print(purchasers,'purchaser')

                notnull_dict(title, dict_save, 'title')
                notnull_dict(project_name, dict_save, 'project_name')
                notnull_dict(project_num, dict_save, 'project_code')
                notnull_dict(date, dict_save, 'project_date')
                notnull_dict(pro, dict_save, 'expert')
                notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
                notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
                # notnull_dict(purchaser_class,dict_save,'purchaser_class')
                notnull_dict(project_intro, dict_save, 'project_intro')
                notnull_dict(win_money, dict_save, 'bid_money')
                # notnull_dict(items, dict_save, 'item')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')
                notnull_dict(subcontract, dict_save, 'subcontract')
                notnull_dict(budget_amount, dict_save, 'budget_money')
                notnull_dict(comp_name, dict_save, 'company_name')
                notnull_dict(comp_contact, dict_save, 'company_contact')
                notnull_dict(comp_address, dict_save, 'company_address')
                notnull_dict(comp_tell, dict_save, 'company_tel')
                notnull_dict(agency_name, dict_save, 'agency_name')
                notnull_dict(agency_contact, dict_save, 'agency_contact')
                notnull_dict(agency_address, dict_save, 'agency_address')
                notnull_dict(agency_tel, dict_save, 'agency_tel')
                notnull_dict(win_bider, dict_save, 'winning_bidder')
                notnull_dict(subject, dict_save, 'subject')
                notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
                notnull_dict(page_url, dict_save, 'page_url')
                notnull_dict(str(page_id), dict_save, 'page_id')
                notnull_dict(str(u_l[2]), dict_save, 'website_id')
                notnull_dict(project_id, dict_save, 'project_id')
                # notnull_dict(u_l[1],dict_save,'page_id')
                # d_save.delete_where('t_bid', 'title', title)
                # print(dict_save,'aaaaaaaaa')

                # try:
                # count = self.d_save.select_where('count(*)', 't_bid',
                #                             'title= "{}" and project_code = "{}" and website_id = 1'.format(
                #                                 MySQLdb.escape_string(title).decode('utf-8'), project_num))[0][0]
                # if count:
                #     logger.info('数据库中已存在')
                #     self.d_save.runSql_excute(
                #         'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                #             '50', str(page_id)))
                #     self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                #     self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                #     self.d_save.commit_insert()
                #     print(count)
                #
                #     continue
                print(dict_save)
                bid_id = worker.get_id()
                notnull_dict(str(bid_id), dict_save, 'id')
                self.d_save.insert('t_bid', dict_save)
                # d_save.commit_insert()
                print(bid_id)
                flag = 1

                if type == 3 or type == 4:
                    pkg_ex(pre_content, bid_id, self.d_save)

                    # print(bid_id)
                # except:
                #     flag = 0
                #     bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                #                                                     project_num)
                #     if latest_date(project_date_old, date):
                #         continue
                #     del dict_save['id']
                #     # d_save.commit_insert()
                #     timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                #     notnull_dict(timeNow, dict_save, 'update_time')
                #     notnull_dict('2', dict_save, 'index_status')
                #     notnull_dict('0', dict_save, 'index_status_reindex')
                #     self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

                # 品目标签
                itemSort(title, self.d_save, bid_id)

                # try:
                #     bid_id = d_save.select_where('id','t_bid','title='+'"'+title+'"')[0][0]
                #     print(bid_id)
                # except:
                #     bid_id = None
                # d_save.delete_where('t_bid_content', 'title', title)
                c_html = content_html_ex(det_html, self.url_tag)
                # print(c_html)
                # c_html = content_html_ex(det_html, url_tag)
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
                    self.d_save.insert('t_bid_content', dict_content)
                    self.d_save.commit_insert()
                    print(content_id, 'content_id')
                except:
                    # logger.error(sys.exc_info())
                    content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
                    # d_save.commit_insert()
                    del dict_content['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_content, 'update_time')

                    self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                    self.d_save.commit_insert()

                # if flag == 1:
                #     # 消息队列
                #     mq_list.append(bid_id)
                #     if len(mq_list) >= 500:
                #         ms = RabbitMQ('admin1', 'admin1', 'subscribe_queue-t')
                #         ms.message_send(mq_list)
                #         mq_list = []

                # website_page分表逻辑
                self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                self.d_save.runSql_excute(
                    'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                        self.web_id, str(page_id)))
                # self.d_save.commit_insert()
                self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                self.d_save.commit_insert()
                with open('log.txt', 'w') as w:
                    w.writelines(['page:' + str(u_l[0]) + '\n'])
                print('---------------------------------`--------------------')
                n += 1
            except Exception as e:
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task', {'fail_page_id': str(u_l[1])})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id = 42')
                self.d_save.commit_insert()
                logger.error(sys.exc_info())
                n += 1

    def save_nmg(self):
        import base64
        global dict_MQ

        mq_list = []
        u_list = [[i[0], i[1], i[2]] for i in self.url_list]
        for u_l in u_list:
            print(u_l[0])
            flag = 0
            # task_list = requests.get(u_l[0])
            # for i in task_list:
            try:
                dict_save = {}
                dict_content = {}
                headers = {}
                user_agent_list = [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                ]
                headers['User-Agent'] = random.choice(user_agent_list)

                try:
                    # print(u_l[0],'ulululul')
                    det_html = requests.get(u_l[0], headers=headers, verify=False, timeout=5).content.decode('utf-8')
                    det_html = html.unescape(det_html)
                except:
                    det_html = requests.get(u_l[0], headers=headers, verify=False, timeout=5).content.decode('GB18030')
                    det_html = html.unescape(det_html)

                content, pre_content = content_ex(det_html, key=0, url_tag=self.url_tag)
                # print(content)

                if 'gzsx' in u_l[0]:
                    content_b64 = content_ex(det_html, key=0)
                    # print(content_b64)
                    aaa = base64.b64decode(content_b64).decode("utf-8")
                    content_html = re.sub('<style type="text/css">[\s\S]*?</style>', '', aaa)
                    # print(content_html)
                    det_html = re.sub('<div class="detail_contect">([\s\S]*?)</div>', content_html, det_html)
                    # print(det_html)
                    content, pre_content = content_ex(content_html, key=1)
                    print(content, 'content')

                title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                project_num = project_num_ex(content, url_tag=self.url_tag, det_html=det_html)

                date = date_ex(det_html, content)
                print(date)
                # date = '0000-00-00'

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag, self.table_name)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, comp_name))
                page_id = u_l[1]

                project_id = proj_id_ex(u_l[0], self.url_tag, type)

                # print(det_html)
                # print(content, '\n')
                # print(title, 'title')
                # print(project_name, '22222222222')
                # print(project_num, '33333333333')
                # print(type, '55555555')
                # print(method, '666666666')
                # print(project_intro, 'introduction')
                # print(comp_address, 'c_address')
                # print(province, 'province')
                # print(city, 'city')
                # print(town, 'town')
                print(budget_amount, 'b_amount')
                # print(comp_name, 'c_name')
                # print(comp_contact, 'c_man')
                # print(comp_tell, 'c_num')
                # print(agency_address, 'agency_address')
                # print(agency_name, 'agency_name')
                # print(agency_contact, 'agency_contact')
                # print(agency_tel, 'agency_tell')
                # print(win_money, 'win_money')
                # print(subject, 'subject')
                # print(subcontract, 'subcontract')
                # print(win_bider, 'win_bider')
                # print(pro, 'pro')
                # print(page_id, 'page_id')
                # print(purchasers,'purchaser')

                notnull_dict(title, dict_save, 'title')
                notnull_dict(project_name, dict_save, 'project_name')
                notnull_dict(project_num, dict_save, 'project_code')
                notnull_dict(date, dict_save, 'project_date')
                notnull_dict(pro, dict_save, 'expert')
                notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
                notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
                # notnull_dict(purchaser_class,dict_save,'purchaser_class')
                notnull_dict(project_intro, dict_save, 'project_intro')
                notnull_dict(win_money, dict_save, 'bid_money')
                # notnull_dict(items, dict_save, 'item')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')
                notnull_dict(subcontract, dict_save, 'subcontract')
                notnull_dict(budget_amount, dict_save, 'budget_money')
                notnull_dict(comp_name, dict_save, 'company_name')
                notnull_dict(comp_contact, dict_save, 'company_contact')
                notnull_dict(comp_address, dict_save, 'company_address')
                notnull_dict(comp_tell, dict_save, 'company_tel')
                notnull_dict(agency_name, dict_save, 'agency_name')
                notnull_dict(agency_contact, dict_save, 'agency_contact')
                notnull_dict(agency_address, dict_save, 'agency_address')
                notnull_dict(agency_tel, dict_save, 'agency_tel')
                notnull_dict(win_bider, dict_save, 'winning_bidder')
                notnull_dict(subject, dict_save, 'subject')
                notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
                notnull_dict(u_l[0], dict_save, 'page_url')
                notnull_dict(str(page_id), dict_save, 'page_id')
                notnull_dict(str(u_l[2]), dict_save, 'website_id')
                notnull_dict(project_id, dict_save, 'project_id')
                # notnull_dict(u_l[1],dict_save,'page_id')
                # self.d_save.delete_where('t_bid', 'title', title)
                # print(dict_save,'aaaaaaaaa')

                try:
                    count = self.d_save.select_where('count(*)', 't_bid',
                                                     'title= "{}" and project_code = "{}" and website_id = 1'.format(
                                                         MySQLdb.escape_string(title).decode('utf-8'), project_num))[0][
                        0]
                    if count:
                        try:
                            # print(page_id,'page_id')
                            self.logger.info('数据库中已存在')
                            self.d_save.runSql_excute(
                                'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                                    str(self.web_id), str(page_id)))
                            self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                            # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                            self.d_save.commit_insert()
                            print(count)

                        except:
                            self.d_save.roll_back_datebase()
                            self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                            # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                            self.d_save.commit_insert()

                        continue

                    # 将插入t_bid表
                    bid_id = worker.get_id()
                    notnull_dict(str(bid_id), dict_save, 'id')
                    self.d_save.insert('t_bid', dict_save)
                    # self.d_save.commit_insert()
                    print(bid_id)

                    # 日期在一个月以内存入MQ
                    date_tag = self.date_limit(date)
                    if date_tag == 1:
                        flag = 1

                    # print(bid_id)
                except:
                    flag = 0
                    bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                         project_num)
                    # self.d_save.commit_insert()
                    if project_date_old:

                        if latest_date(project_date_old, date):
                            continue

                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    del dict_save['id']
                    notnull_dict(timeNow, dict_save, 'update_time')
                    notnull_dict('2', dict_save, 'index_status')
                    notnull_dict('0', dict_save, 'index_status_reindex')
                    self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

                # 品目标签
                itemSort(title, self.d_save, bid_id)

                # try:
                #     bid_id = d_save.select_where('id','t_bid','title='+'"'+title+'"')[0][0]
                #     print(bid_id)
                # except:
                #     bid_id = None
                # self.d_save.delete_where('t_bid_content', 'title', title)

                c_html = content_html_ex(det_html, self.url_tag, page_url=u_l[0])
                # print(c_html, 'c_html')
                # print(content,'content')
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
                    self.d_save.insert('t_bid_content', dict_content)
                    self.d_save.commit_insert()
                    print(content_id, 'content_id')
                except:
                    # self.logger.error(sys.exc_info())
                    content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
                    # self.d_save.commit_insert()
                    del dict_content['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_content, 'update_time')

                    self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                    self.d_save.commit_insert()

                # else:
                #     # self.d_save.delete_where('t_bid_content', 'title', title)
                #     c_html = content_html_ex(det_html, self.url_tag)
                #     # print(c_html, 'c_html')
                #     # print(c_html)
                #     bid_id = self.d_save.select_where('id', 't_bid', 'title=' + '"' + title + '"')[0][0]
                #     notnull_dict(MySQLdb.escape_string(c_html).decode('utf-8'), dict_content, 'content')
                #     notnull_dict(MySQLdb.escape_string(content).decode('utf-8'), dict_content, 'pure_content')
                #     notnull_dict(str(bid_id), dict_content, 'bid_id')
                #     notnull_dict(title, dict_content, 'title')
                #     # print(dict_content, 'xxxxxxx')
                #     self.d_save.insert('t_bid_content', dict_content)
                # self.d_save.commit_insert()
                # if flag == 1:
                #     # 消息队列
                #     mq_list.append(bid_id)
                #     if len(mq_list) >= 500:
                #         ms = RabbitMQ('admin1', 'admin1', 'subscribe_queue-t')
                #         ms.message_send(mq_list)
                #         mq_list = []

                print(111111)
                try:
                    # website_page分表逻辑
                    self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    # self.d_save.commit_insert()
                    self.d_save.runSql_excute(
                        'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                            str(self.web_id), str(page_id)))

                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                except:
                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                print(222222)
                with open('log.txt', 'w') as w:
                    w.writelines(['page:' + str(u_l[0]) + '\n'])
                print('---------------------------------`--------------------')
            except Exception as e:
                self.logger.error(sys.exc_info())
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task', {'fail_page_id': str(u_l[1])})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()

    def save_page_proxy(self):
        global dict_MQ

        u_list = [[i[0], i[1], i[2]] for i in self.url_list]
        for u_l in u_list:
            print(u_l[0])
            url = u_l[0]
            try:
                dict_save = {}
                dict_content = {}
                headers = {}
                user_agent_list = [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                ]
                headers['User-Agent'] = random.choice(user_agent_list)

                response = self.getHtml(url=url, headers=headers)

                try:
                    # print(u_l[0],'ulululul')
                    det_html = response.content.decode('utf-8')
                    det_html = html.unescape(det_html)
                except:
                    det_html = response.content.decode('GB18030')
                    det_html = html.unescape(det_html)

                # try:
                #     # print(u_l[0],'ulululul')
                #     det_html = requests.get(url=url,headers=headers).content.decode('utf-8')
                #     det_html = html.unescape(det_html)
                # except:
                #     det_html = requests.get(url=url,headers=headers).content.decode('GB18030')
                #     det_html = html.unescape(det_html)

                # print(det_html)

                content, pre_content = content_ex(det_html, key=0, url_tag=self.url_tag)

                title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                project_num = project_num_ex(content, url_tag=self.url_tag, det_html=det_html)

                date = date_ex(det_html, content)
                print(date)
                # date = '0000-00-00'

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag, self.table_name)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, project_name))
                page_id = u_l[1]

                project_id = proj_id_ex(u_l[0], self.url_tag, type)

                # print(det_html)
                print(content, '\n')
                # print(title, 'title')
                # print(project_name, '22222222222')
                # print(project_num, '33333333333')
                # print(type, '55555555')
                # print(method, '666666666')
                # print(project_intro, 'introduction')
                # print(comp_address, 'c_address')
                # print(province, 'province')
                # print(city, 'city')
                # print(town, 'town')
                print(budget_amount, 'b_amount')
                # print(comp_name, 'c_name')
                # print(comp_contact, 'c_man')
                # print(comp_tell, 'c_num')
                # print(agency_address, 'agency_address')
                # print(agency_name, 'agency_name')
                # print(agency_contact, 'agency_contact')
                # print(agency_tel, 'agency_tell')
                # print(win_money, 'win_money')
                # print(subject, 'subject')
                # print(subcontract, 'subcontract')
                # print(win_bider, 'win_bider')
                # print(pro, 'pro')
                # print(page_id, 'page_id')
                # print(purchasers,'purchaser')

                notnull_dict(title, dict_save, 'title')
                notnull_dict(project_name, dict_save, 'project_name')
                notnull_dict(project_num, dict_save, 'project_code')
                notnull_dict(date, dict_save, 'project_date')
                notnull_dict(pro, dict_save, 'expert')
                notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
                notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
                # notnull_dict(purchaser_class,dict_save,'purchaser_class')
                notnull_dict(project_intro, dict_save, 'project_intro')
                notnull_dict(win_money, dict_save, 'bid_money')
                # notnull_dict(items, dict_save, 'item')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')
                notnull_dict(subcontract, dict_save, 'subcontract')
                notnull_dict(budget_amount, dict_save, 'budget_money')
                notnull_dict(comp_name, dict_save, 'company_name')
                notnull_dict(comp_contact, dict_save, 'company_contact')
                notnull_dict(comp_address, dict_save, 'company_address')
                notnull_dict(comp_tell, dict_save, 'company_tel')
                notnull_dict(agency_name, dict_save, 'agency_name')
                notnull_dict(agency_contact, dict_save, 'agency_contact')
                notnull_dict(agency_address, dict_save, 'agency_address')
                notnull_dict(agency_tel, dict_save, 'agency_tel')
                notnull_dict(win_bider, dict_save, 'winning_bidder')
                notnull_dict(subject, dict_save, 'subject')
                notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
                notnull_dict(u_l[0], dict_save, 'page_url')
                notnull_dict(str(page_id), dict_save, 'page_id')
                notnull_dict(str(u_l[2]), dict_save, 'website_id')
                notnull_dict(project_id, dict_save, 'project_id')
                # notnull_dict(u_l[1],dict_save,'page_id')
                # self.d_save.delete_where('t_bid', 'title', title)
                # print(dict_save,'aaaaaaaaa')

                try:
                    # count = self.d_save.select_where('count(*)', 't_bid', 'title= "{}" and project_code = "{}" and website_id = 1'.format(MySQLdb.escape_string(title).decode('utf-8'),project_num))[0][0]
                    # if count:
                    #     try:
                    #         # print(page_id,'page_id')
                    #         self.logger.info('数据库中已存在')
                    #         self.d_save.runSql_excute(
                    #             'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                    #                 str(self.web_id), str(page_id)))
                    #         self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    #         # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    #         self.d_save.commit_insert()
                    #         print(count)
                    #
                    #     except:
                    #         self.d_save.roll_back_datebase()
                    #         self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    #         # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    #         self.d_save.commit_insert()
                    #
                    #     continue

                    # 将插入t_bid表
                    bid_id = worker.get_id()
                    notnull_dict(str(bid_id), dict_save, 'id')
                    self.d_save.insert('t_bid', dict_save)
                    # self.d_save.commit_insert()
                    print(bid_id)

                    # 日期在一个月以内存入MQ
                    date_tag = self.date_limit(date)
                    if date_tag == 1:
                        flag = 1

                    # print(bid_id)
                except:
                    flag = 0
                    bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                         project_num)
                    # self.d_save.commit_insert()
                    if project_date_old:

                        if latest_date(project_date_old, date):
                            continue

                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    del dict_save['id']
                    notnull_dict(timeNow, dict_save, 'update_time')
                    notnull_dict('2', dict_save, 'index_status')
                    notnull_dict('0', dict_save, 'index_status_reindex')
                    self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

                # 品目标签
                itemSort(title, self.d_save, bid_id)

                c_html = content_html_ex(det_html, self.url_tag, page_url=u_l[0])
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
                    self.d_save.insert('t_bid_content', dict_content)
                    self.d_save.commit_insert()
                    print(content_id, 'content_id')
                except:
                    # self.logger.error(sys.exc_info())
                    content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
                    # self.d_save.commit_insert()
                    del dict_content['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_content, 'update_time')

                    self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                    self.d_save.commit_insert()

                print(111111)
                try:
                    # website_page分表逻辑
                    self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    # self.d_save.commit_insert()
                    self.d_save.runSql_excute(
                        'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                            str(self.web_id), str(page_id)))

                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                except:
                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                print(222222)
                with open('log.txt', 'w') as w:
                    w.writelines(['page:' + str(u_l[0]) + '\n'])
                print('---------------------------------`--------------------')
            except Exception as e:
                self.logger.error(sys.exc_info())
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task',{'fail_page_id':str(u_l[1])})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()

    def get_proxy(self):
        return requests.get("http://127.0.0.1:5010/get/").json()

    def delete_proxy(self, proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

    def getHtml(self, url=None, headers=None, params=None):
        # print(url,'url')
        retry_count = 5
        proxy = self.get_proxy().get("proxy")
        print(proxy, 'proxy')
        while retry_count > 0:
            try:
                html = requests.get(url='http://ggzy.zwfwb.tj.gov.cn/jyxxcggg/dkBG93glahi39LLLm22MJA.jhtml',
                                    headers=headers, params=params, proxies={"http": f"http://{proxy}"}, timeout=10)
                # 使用代理访问
                # print(html,'html')
                code = html.status_code
                if code == '200':
                    return html
                retry_count -= 1
            except Exception:
                # print(sys.exc_info())
                retry_count -= 1
        # 删除代理池中代理
        self.delete_proxy(proxy)
        return None

    def jiagsu_contract(self, data):
        from bs4 import BeautifulSoup

        #
        projNumber = data.get('projNumber')  # 项目编号
        contractName = data['extend'].get('contractName')  # 标题
        projName = data.get('projName')  # 项目名称
        buyerName = data.get('buyerName')  # 采购人名称
        purchaserAddr = data['extend'].get('buyerAddr')  # 采购人地区
        purchaserContact = data['extend'].get('buyerContact')  # 采购人联系方式
        supplyName = data['extend'].get('supplyName')  # 供应商名称
        supplyAddr = data['extend'].get('supplyAddr')  # 供应商地址
        supplyContact = data['extend'].get('supplyContact')  # 供应商联系方式
        objectName = data['extend'].get('objectName')  # 主要标的信息
        objectModel = data['extend'].get('objectModel')  # 规格型号，服务要求
        objectNum = data['extend'].get('objectNum')  # 标的数量
        objectUnitPrice = data['extend'].get('objectUnitPrice')  # 标的单价
        contractMoney = str(data['extend'].get('contractMoney'))  # 合同金额
        perForm = data['extend'].get('perForm')  # 履约地点
        publishDate = data.get('publishDate')  # 公告日期
        signDate = data['extend'].get('signDate')  # 签订日期

        with open('jiangsu_hetong.html', 'r') as r:
            html_null = r.read()
        soup = BeautifulSoup(html_null, 'html.parser')
        span_list = soup.find_all('span')
        for tag_span in span_list:
            if tag_span['id'] == 'contractCode':
                tag_span.append(projNumber)
            elif tag_span['id'] == 'contractName':
                tag_span.append(contractName)
            elif tag_span['id'] == 'htProjNumber':
                tag_span.append(projNumber)
            elif tag_span['id'] == 'htProjName':
                tag_span.append(projName)
            elif tag_span['id'] == 'htbuyerName':
                tag_span.append(buyerName)
            elif tag_span['id'] == 'buyerAddress':
                tag_span.append(purchaserAddr)
            elif tag_span['id'] == 'buyerPhone':
                tag_span.append(purchaserContact)
            elif tag_span['id'] == 'supplyName':
                tag_span.append(supplyName)
            elif tag_span['id'] == 'supplyAddress':
                tag_span.append(supplyAddr)
            elif tag_span['id'] == 'supplyPhone':
                tag_span.append(supplyContact)
            elif tag_span['id'] == 'htmainMsg':
                tag_span.append(objectName)
            elif tag_span['id'] == 'htsize':
                tag_span.append(objectModel)
            elif tag_span['id'] == 'htpnone':
                tag_span.append(supplyContact)
            elif tag_span['id'] == 'htnum':
                tag_span.append(objectNum)
            elif tag_span['id'] == 'heprice':
                tag_span.append(objectUnitPrice)
            elif tag_span['id'] == 'contractMoney':
                tag_span.append(contractMoney)
            elif tag_span['id'] == 'htEdDate':
                tag_span.append(perForm)
            elif tag_span['id'] == 'purchaseWay':
                tag_span.append('定点采购')
            elif tag_span['id'] == 'signDate':
                tag_span.append(signDate)
            elif tag_span['id'] == 'htggrq':
                tag_span.append(publishDate)
        return str(soup)

    def save_jiangsu(self):
        global dict_MQ

        mq_list = []
        u_list = [[i[0], i[1], i[2]] for i in self.url_list]
        for u_l in u_list:
            print(u_l[0])
            page_url = u_l[0]
            ggid = page_url.split('ggid=').pop()
            print(ggid, 'ggid')

            flag = 0
            # task_list = requests.get(u_l[0])
            # for i in task_list:
            try:
                dict_save = {}
                dict_content = {}
                headers = {}
                user_agent_list = [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                ]
                headers['User-Agent'] = random.choice(user_agent_list)
                url = 'http://www.ccgp-jiangsu.gov.cn/pss/jsp/relevantCgggGetById.jsp'
                data = {'ggid': str(ggid)}
                # print(u_l[0],'ulululul')
                data = requests.post(url, headers=headers, data=data, verify=False, timeout=5).json()['data']
                # print(data)
                det_html = data.get('content')
                if det_html == None:
                    det_html = self.jiagsu_contract(data)
                det_html = html.unescape(det_html)
                title = data['title']
                date = data['publishDate']
                annex_list = data.get('files')

                content, pre_content = content_ex(det_html, key=1)
                if not title:
                    title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                project_num = project_num_ex(content, url_tag=self.url_tag, det_html=det_html)
                if not date:
                    date = date_ex(det_html, content)
                print(date)
                # date = '0000-00-00'

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[comp_address], [title], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag, self.table_name)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, comp_name))
                page_id = u_l[1]

                project_id = proj_id_ex(u_l[0], self.url_tag, type)

                # print(det_html)
                # print(content, '\n')
                # print(title, 'title')
                # print(project_name, '22222222222')
                # print(project_num, '33333333333')
                # print(type, '55555555')
                # print(method, '666666666')
                # print(project_intro, 'introduction')
                # print(comp_address, 'c_address')
                # print(province, 'province')
                # print(city, 'city')
                # print(town, 'town')
                print(budget_amount, 'b_amount')
                # print(comp_name, 'c_name')
                # print(comp_contact, 'c_man')
                # print(comp_tell, 'c_num')
                # print(agency_address, 'agency_address')
                # print(agency_name, 'agency_name')
                # print(agency_contact, 'agency_contact')
                # print(agency_tel, 'agency_tell')
                # print(win_money, 'win_money')
                # print(subject, 'subject')
                # print(subcontract, 'subcontract')
                # print(win_bider, 'win_bider')
                # print(pro, 'pro')
                # print(page_id, 'page_id')
                # print(purchasers,'purchaser')

                notnull_dict(title, dict_save, 'title')
                notnull_dict(project_name, dict_save, 'project_name')
                notnull_dict(project_num, dict_save, 'project_code')
                notnull_dict(date, dict_save, 'project_date')
                notnull_dict(pro, dict_save, 'expert')
                notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
                notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
                # notnull_dict(purchaser_class,dict_save,'purchaser_class')
                notnull_dict(project_intro, dict_save, 'project_intro')
                notnull_dict(win_money, dict_save, 'bid_money')
                # notnull_dict(items, dict_save, 'item')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')
                notnull_dict(subcontract, dict_save, 'subcontract')
                notnull_dict(budget_amount, dict_save, 'budget_money')
                notnull_dict(comp_name, dict_save, 'company_name')
                notnull_dict(comp_contact, dict_save, 'company_contact')
                notnull_dict(comp_address, dict_save, 'company_address')
                notnull_dict(comp_tell, dict_save, 'company_tel')
                notnull_dict(agency_name, dict_save, 'agency_name')
                notnull_dict(agency_contact, dict_save, 'agency_contact')
                notnull_dict(agency_address, dict_save, 'agency_address')
                notnull_dict(agency_tel, dict_save, 'agency_tel')
                notnull_dict(win_bider, dict_save, 'winning_bidder')
                notnull_dict(subject, dict_save, 'subject')
                notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
                notnull_dict(u_l[0], dict_save, 'page_url')
                notnull_dict(str(page_id), dict_save, 'page_id')
                notnull_dict(str(u_l[2]), dict_save, 'website_id')
                notnull_dict(project_id, dict_save, 'project_id')
                # notnull_dict(u_l[1],dict_save,'page_id')
                # self.d_save.delete_where('t_bid', 'title', title)
                # print(dict_save,'aaaaaaaaa')

                try:
                    count = self.d_save.select_where('count(*)', 't_bid',
                                                     'title= "{}" and project_code = "{}" and website_id = 1'.format(
                                                         MySQLdb.escape_string(title).decode('utf-8'), project_num))[0][
                        0]
                    if count:
                        try:
                            # print(page_id,'page_id')
                            self.logger.info('数据库中已存在')
                            self.d_save.runSql_excute(
                                'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                                    str(self.web_id), str(page_id)))
                            self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                            # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                            self.d_save.commit_insert()
                            print(count)

                        except:
                            self.d_save.roll_back_datebase()
                            self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                            # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                            self.d_save.commit_insert()

                        continue

                    # 将插入t_bid表
                    bid_id = worker.get_id()
                    notnull_dict(str(bid_id), dict_save, 'id')
                    self.d_save.insert('t_bid', dict_save)
                    # self.d_save.commit_insert()
                    print(bid_id)

                    # 日期在一个月以内存入MQ
                    date_tag = self.date_limit(date)
                    if date_tag == 1:
                        flag = 1

                    # print(bid_id)
                except:
                    flag = 0
                    bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                         project_num)
                    # self.d_save.commit_insert()
                    if project_date_old:

                        if latest_date(project_date_old, date):
                            continue

                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    del dict_save['id']
                    notnull_dict(timeNow, dict_save, 'update_time')
                    notnull_dict('2', dict_save, 'index_status')
                    notnull_dict('0', dict_save, 'index_status_reindex')
                    self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

                # 品目标签
                itemSort(title, self.d_save, bid_id)

                # try:
                #     bid_id = d_save.select_where('id','t_bid','title='+'"'+title+'"')[0][0]
                #     print(bid_id)
                # except:
                #     bid_id = None
                # self.d_save.delete_where('t_bid_content', 'title', title)

                c_html = content_html_ex(det_html, self.url_tag, page_url=u_l[0], extra=annex_list)
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
                    self.d_save.insert('t_bid_content', dict_content)
                    self.d_save.commit_insert()
                    print(content_id, 'content_id')
                except:
                    # self.logger.error(sys.exc_info())
                    content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
                    # self.d_save.commit_insert()
                    del dict_content['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_content, 'update_time')

                    self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                    self.d_save.commit_insert()

                print(111111)
                try:
                    # website_page分表逻辑
                    self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    # self.d_save.commit_insert()
                    self.d_save.runSql_excute(
                        'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                            str(self.web_id), str(page_id)))

                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                except:
                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                print(222222)
                with open('log.txt', 'w') as w:
                    w.writelines(['page:' + str(u_l[0]) + '\n'])
                print('---------------------------------`--------------------')
            except Exception as e:
                self.logger.error(sys.exc_info())
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task', {'fail_page_id': str(u_l[1])})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()

    def save_page_ah(self):
        global dict_MQ

        mq_list = []
        u_list = [[i[0], i[1], i[2], i[3]] for i in self.url_list]
        for u_l in u_list:
            print(u_l[0])

            det_url = 'http://ggzy.ah.gov.cn/zfcg/newDetailSub'

            extra = ast.literal_eval(u_l[2])
            url = extra['url']
            title = extra['title']
            date = extra['date']
            bulletinNature = extra['bulletinNature']
            guid = re.findall('guid=(.*?)&', url)[0]
            type = 'bulletin' if bulletinNature == '1' else 'zbjg'
            det_data = {
                'type': type,
                'bulletinNature': bulletinNature,
                'guid': guid,
                'statusGuid': '',
            }

            try:
                dict_save = {}
                dict_content = {}
                headers = {}
                user_agent_list = [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                ]
                headers['User-Agent'] = random.choice(user_agent_list)

                try:
                    # print(u_l[0],'ulululul')
                    det_html = requests.post(url=det_url, headers=headers, data=det_data, verify=False,
                                             timeout=5).content.decode('utf-8')
                    det_html = html.unescape(det_html)
                except:
                    det_html = requests.post(url=det_url, headers=headers, data=det_data, verify=False,
                                             timeout=5).content.decode('GB18030')
                    det_html = html.unescape(det_html)

                content, pre_content = content_ex(det_html, key=1)

                if not title:
                    title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                project_num = project_num_ex(content, url_tag=self.url_tag, det_html=det_html)

                if not date:
                    date = date_ex(det_html, content)
                print(date)
                # date = '0000-00-00'

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag, self.table_name)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, project_name))
                page_id = u_l[1]

                project_id = proj_id_ex(u_l[0], self.url_tag, type)

                # print(det_html)
                # print(content, '\n')
                # print(title, 'title')
                # print(project_name, '22222222222')
                # print(project_num, '33333333333')
                # print(type, '55555555')
                # print(method, '666666666')
                # print(project_intro, 'introduction')
                # print(comp_address, 'c_address')
                # print(province, 'province')
                # print(city, 'city')
                # print(town, 'town')
                # print(budget_amount, 'b_amount')
                # print(comp_name, 'c_name')
                # print(comp_contact, 'c_man')
                # print(comp_tell, 'c_num')
                # print(agency_address, 'agency_address')
                # print(agency_name, 'agency_name')
                # print(agency_contact, 'agency_contact')
                # print(agency_tel, 'agency_tell')
                # print(win_money, 'win_money')
                # print(subject, 'subject')
                # print(subcontract, 'subcontract')
                # print(win_bider, 'win_bider')
                # print(pro, 'pro')
                # print(page_id, 'page_id')
                # print(purchasers,'purchaser')

                notnull_dict(title, dict_save, 'title')
                notnull_dict(project_name, dict_save, 'project_name')
                notnull_dict(project_num, dict_save, 'project_code')
                notnull_dict(date, dict_save, 'project_date')
                notnull_dict(pro, dict_save, 'expert')
                notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
                notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
                # notnull_dict(purchaser_class,dict_save,'purchaser_class')
                notnull_dict(project_intro, dict_save, 'project_intro')
                notnull_dict(win_money, dict_save, 'bid_money')
                # notnull_dict(items, dict_save, 'item')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')
                notnull_dict(subcontract, dict_save, 'subcontract')
                notnull_dict(budget_amount, dict_save, 'budget_money')
                notnull_dict(comp_name, dict_save, 'company_name')
                notnull_dict(comp_contact, dict_save, 'company_contact')
                notnull_dict(comp_address, dict_save, 'company_address')
                notnull_dict(comp_tell, dict_save, 'company_tel')
                notnull_dict(agency_name, dict_save, 'agency_name')
                notnull_dict(agency_contact, dict_save, 'agency_contact')
                notnull_dict(agency_address, dict_save, 'agency_address')
                notnull_dict(agency_tel, dict_save, 'agency_tel')
                notnull_dict(win_bider, dict_save, 'winning_bidder')
                notnull_dict(subject, dict_save, 'subject')
                notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
                notnull_dict(u_l[0], dict_save, 'page_url')
                notnull_dict(str(page_id), dict_save, 'page_id')
                notnull_dict(str(u_l[3]), dict_save, 'website_id')
                notnull_dict(project_id, dict_save, 'project_id')
                # notnull_dict(u_l[1],dict_save,'page_id')
                # self.d_save.delete_where('t_bid', 'title', title)
                # print(dict_save,'aaaaaaaaa')

                try:
                    # count = self.d_save.select_where('count(*)', 't_bid', 'title= "{}" and project_code = "{}" and website_id = 1'.format(MySQLdb.escape_string(title).decode('utf-8'),project_num))[0][0]
                    # if count:
                    #     try:
                    #         # print(page_id,'page_id')
                    #         self.logger.info('数据库中已存在')
                    #         self.d_save.runSql_excute(
                    #             'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                    #                 str(self.web_id), str(page_id)))
                    #         self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    #         # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    #         self.d_save.commit_insert()
                    #         print(count)
                    #
                    #     except:
                    #         self.d_save.roll_back_datebase()
                    #         self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    #         # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    #         self.d_save.commit_insert()
                    #
                    #     continue

                    # 将插入t_bid表
                    bid_id = worker.get_id()
                    notnull_dict(str(bid_id), dict_save, 'id')
                    self.d_save.insert('t_bid', dict_save)
                    # self.d_save.commit_insert()
                    print(bid_id)

                    # 日期在一个月以内存入MQ
                    date_tag = self.date_limit(date)
                    if date_tag == 1:
                        flag = 1

                    # print(bid_id)
                except:
                    flag = 0
                    bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                         project_num)
                    # self.d_save.commit_insert()
                    if project_date_old:

                        if latest_date(project_date_old, date):
                            continue

                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    del dict_save['id']
                    notnull_dict(timeNow, dict_save, 'update_time')
                    notnull_dict('2', dict_save, 'index_status')
                    notnull_dict('0', dict_save, 'index_status_reindex')
                    self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

                # 品目标签
                itemSort(title, self.d_save, bid_id)

                # try:
                #     bid_id = d_save.select_where('id','t_bid','title='+'"'+title+'"')[0][0]
                #     print(bid_id)
                # except:
                #     bid_id = None
                # self.d_save.delete_where('t_bid_content', 'title', title)

                c_html = content_html_ex(det_html, self.url_tag, page_url=u_l[0])
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
                    self.d_save.insert('t_bid_content', dict_content)
                    self.d_save.commit_insert()
                    print(content_id, 'content_id')
                except:
                    # self.logger.error(sys.exc_info())
                    content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
                    # self.d_save.commit_insert()
                    del dict_content['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_content, 'update_time')

                    self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                    self.d_save.commit_insert()

                print(111111)
                try:
                    # website_page分表逻辑
                    self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    # self.d_save.commit_insert()
                    self.d_save.runSql_excute(
                        'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                            str(self.web_id), str(page_id)))

                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                except:
                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                print(222222)
                with open('log.txt', 'w') as w:
                    w.writelines(['page:' + str(u_l[0]) + '\n'])
                print('---------------------------------`--------------------')
            except Exception as e:
                self.logger.error(sys.exc_info())
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task',{'fail_page_id':str(u_l[1])})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()

    def merge_crypto(self, data):
        import base64
        import hashlib

        data_str = json.dumps(data).encode()
        # print(data_str)
        data_64 = base64.b64encode(data_str)
        # print(data_64)
        r_data = os.popen(f'node ./js_file/ggzy_fujian.js {data_64.decode()}')
        data_end = r_data.read()
        # print(data_end)
        data_md5 = hashlib.md5(data_end.encode().strip()).hexdigest()
        # print(data_md5)

        return data_md5

    def get_headers(self, portal_sign=None,
                    cookies='__root_domain_v=.fj.gov.cn; _qddaz=QD.656131952951040; ASP.NET_SessionId=00ddelay1jpd0atolbfpxapc; _qdda=4-1.3b9a47; _qddab=4-jc9g9v.ktwmhbbj'):

        return {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh,zh-TW;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6',
            'Connection': 'keep-alive',
            'Content-Length': '70',
            'Content-Type': 'application/json;charset=UTF-8',
            'Cookie': cookies,
            'Host': 'ggzyfw.fj.gov.cn',
            'Origin': 'https://ggzyfw.fj.gov.cn',
            'portal-sign': portal_sign,
            'Referer': 'https://ggzyfw.fj.gov.cn/web/index.html',
            'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
        }

    def save_page_fj(self):
        from tools_monitor import AES_code
        global dict_MQ

        mq_list = []
        u_list = [[i[0], i[1], i[2], i[3]] for i in self.url_list]
        for u_l in u_list:
            print(u_l[0])

            det_url = 'https://ggzyfw.fj.gov.cn/Trade/TradeInfoContent'

            extra = ast.literal_eval(u_l[2])
            GGTYPE = extra['GGTYPE']
            title = extra['title']
            date = extra['date']
            M_ID = extra['M_ID']
            # time_st = extra['time_st']
            time_st = int(round(time.time() * 1000))
            content_type = {
                '1': 'PURCHASE_QUALI_INQUERY_ANN',
                '2': 'BID_DEAL_ANNOUNCE'
            }

            tradeInfo_content_data = {
                "m_id": int(M_ID),
                "ts": time_st,
                "type": content_type[GGTYPE]
            }

            try:
                dict_save = {}
                dict_content = {}

                tradeInfo_content_md5 = self.merge_crypto(tradeInfo_content_data)
                headers_content = self.get_headers(
                    portal_sign=tradeInfo_content_md5,
                    cookies='__root_domain_v=.fj.gov.cn; _qddaz=QD.656131952951040; ASP.NET_SessionId=00ddelay1jpd0atolbfpxapc; _qdda=4-1.3b9a47; _qddab=4-jc9g9v.ktwmhbbj'
                )

                # print(headers_content,tradeInfo_content_data)
                det_html = requests.post(url=det_url, headers=headers_content, json=tradeInfo_content_data,
                                         verify=False,
                                         timeout=5).json()
                # print(det_html,'det_html')
                det_html_AES = det_html['Data']
                real_html = re.sub('}(.*?)$', '}', AES_code.decrypt(det_html_AES))

                # print(real_html)
                real_html = json.loads(real_html)
                det_html = real_html['Contents']

                content, pre_content = content_ex(det_html, key=1)

                if not title:
                    title = title_ex_total(content, det_html)

                project_name = project_name_ex(content, title)

                project_num = project_num_ex(content, url_tag=self.url_tag, det_html=det_html)

                if not date:
                    date = date_ex(det_html, content)
                print(date)
                # date = '0000-00-00'

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html, self.url_tag, self.table_name)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, comp_name))
                page_id = u_l[1]

                project_id = proj_id_ex(u_l[0], self.url_tag, type)

                # print(det_html)
                # print(content, '\n')
                # print(title, 'title')
                # print(project_name, '22222222222')
                # print(project_num, '33333333333')
                # print(type, '55555555')
                # print(method, '666666666')
                # print(project_intro, 'introduction')
                # print(comp_address, 'c_address')
                # print(province, 'province')
                # print(city, 'city')
                # print(town, 'town')
                # print(budget_amount, 'b_amount')
                # print(comp_name, 'c_name')
                # print(comp_contact, 'c_man')
                # print(comp_tell, 'c_num')
                # print(agency_address, 'agency_address')
                # print(agency_name, 'agency_name')
                # print(agency_contact, 'agency_contact')
                # print(agency_tel, 'agency_tell')
                # print(win_money, 'win_money')
                # print(subject, 'subject')
                # print(subcontract, 'subcontract')
                # print(win_bider, 'win_bider')
                # print(pro, 'pro')
                # print(page_id, 'page_id')
                # print(purchasers,'purchaser')

                notnull_dict(title, dict_save, 'title')
                notnull_dict(project_name, dict_save, 'project_name')
                notnull_dict(project_num, dict_save, 'project_code')
                notnull_dict(date, dict_save, 'project_date')
                notnull_dict(pro, dict_save, 'expert')
                notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
                notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
                # notnull_dict(purchaser_class,dict_save,'purchaser_class')
                notnull_dict(project_intro, dict_save, 'project_intro')
                notnull_dict(win_money, dict_save, 'bid_money')
                # notnull_dict(items, dict_save, 'item')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')
                notnull_dict(subcontract, dict_save, 'subcontract')
                notnull_dict(budget_amount, dict_save, 'budget_money')
                notnull_dict(comp_name, dict_save, 'company_name')
                notnull_dict(comp_contact, dict_save, 'company_contact')
                notnull_dict(comp_address, dict_save, 'company_address')
                notnull_dict(comp_tell, dict_save, 'company_tel')
                notnull_dict(agency_name, dict_save, 'agency_name')
                notnull_dict(agency_contact, dict_save, 'agency_contact')
                notnull_dict(agency_address, dict_save, 'agency_address')
                notnull_dict(agency_tel, dict_save, 'agency_tel')
                notnull_dict(win_bider, dict_save, 'winning_bidder')
                notnull_dict(subject, dict_save, 'subject')
                notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
                notnull_dict(u_l[0], dict_save, 'page_url')
                notnull_dict(str(page_id), dict_save, 'page_id')
                notnull_dict(str(u_l[3]), dict_save, 'website_id')
                notnull_dict(project_id, dict_save, 'project_id')
                # notnull_dict(u_l[1],dict_save,'page_id')
                # self.d_save.delete_where('t_bid', 'title', title)
                # print(dict_save,'aaaaaaaaa')

                try:
                    count = self.d_save.select_where('count(*)', 't_bid',
                                                     'title= "{}" and project_code = "{}" and website_id = 1'.format(
                                                         MySQLdb.escape_string(title).decode('utf-8'), project_num))[0][
                        0]
                    if count:
                        try:
                            # print(page_id,'page_id')
                            self.logger.info('数据库中已存在')
                            self.d_save.runSql_excute(
                                'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                                    str(self.web_id), str(page_id)))
                            self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                            # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                            self.d_save.commit_insert()
                            print(count)

                        except:
                            self.d_save.roll_back_datebase()
                            self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                            # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                            self.d_save.commit_insert()

                        continue

                    # 将插入t_bid表
                    bid_id = worker.get_id()
                    notnull_dict(str(bid_id), dict_save, 'id')
                    self.d_save.insert('t_bid', dict_save)
                    # self.d_save.commit_insert()
                    print(bid_id)

                    # 日期在一个月以内存入MQ
                    date_tag = self.date_limit(date)
                    if date_tag == 1:
                        flag = 1

                    # print(bid_id)
                except:
                    flag = 0
                    bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                         project_num)
                    # self.d_save.commit_insert()
                    if project_date_old:

                        if latest_date(project_date_old, date):
                            continue

                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    del dict_save['id']
                    notnull_dict(timeNow, dict_save, 'update_time')
                    notnull_dict('2', dict_save, 'index_status')
                    notnull_dict('0', dict_save, 'index_status_reindex')
                    self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

                # 品目标签
                itemSort(title, self.d_save, bid_id)

                # try:
                #     bid_id = d_save.select_where('id','t_bid','title='+'"'+title+'"')[0][0]
                #     print(bid_id)
                # except:
                #     bid_id = None
                # self.d_save.delete_where('t_bid_content', 'title', title)

                c_html = content_html_ex(det_html, self.url_tag, page_url=u_l[0])
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
                    self.d_save.insert('t_bid_content', dict_content)
                    self.d_save.commit_insert()
                    print(content_id, 'content_id')
                except:
                    # self.logger.error(sys.exc_info())
                    content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
                    # self.d_save.commit_insert()
                    del dict_content['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_content, 'update_time')

                    self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                    self.d_save.commit_insert()

                print(111111)
                try:
                    # website_page分表逻辑
                    self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    # self.d_save.commit_insert()
                    self.d_save.runSql_excute(
                        'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                            str(self.web_id), str(page_id)))

                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                except:
                    self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    self.d_save.commit_insert()
                print(222222)
                with open('log.txt', 'w') as w:
                    w.writelines(['page:' + str(u_l[0]) + '\n'])
                print('---------------------------------`--------------------')
            except Exception as e:
                self.logger.error(sys.exc_info())
                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task', {'fail_page_id': str(u_l[1])})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()


# 详情页字段拆分和存储（需要代理IP）
class Save_data_proxy():

    def __init__(self, d_save=None, url_tag=None, logger=None, url_list=None, web_id=None):
        self.d_save = d_save
        self.url_tag = url_tag
        self.logger = logger
        self.url_list = url_list
        self.web_id = web_id

    def get_response(self, u='', proxy=None, timeout=5):
        headers = {}
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]

        headers['User-Agent'] = random.choice(user_agent_list)
        url = u
        # print(url)
        retry_count = 3
        # ip_list = ip_proxy.proxy_ip(1)
        # proxies = ip_proxy.proxy_amount(ip_list)
        print(proxy)
        proxies = proxy
        if proxies:
            while retry_count > 0:
                try:
                    response = requests.get(url=url, headers=headers, proxies=proxies, verify=False, timeout=timeout)
                    # 使用代理访问
                    retry_count = 3
                    return response
                except Exception:
                    print('出错啦')
                    # logger.error(sys.exc_info())
                    ip_list = ip_proxy.proxy_ip(1)
                    proxies = ip_proxy.proxy_amount(ip_list)
                    retry_count -= 1

        else:
            response = requests.get(url=url, headers=headers, verify=False, timeout=timeout)
            return response
            # 出错3次, 删除代理池中代理
            # ip_proxy.delete_proxy(proxy)
        # ip_list = ip_proxy.proxy_ip(1)
        # proxies = ip_proxy.proxy_amount(ip_list)
        # self.get_response(u=url,proxy=proxies)

    def save_page(self):
        global dict_MQ
        mq_list = []
        u_list = [[i[0], i[1], i[2]] for i in self.url_list]

        ip_list = ip_proxy.proxy_ip(10)
        proxies = ip_proxy.proxy_amount(ip_list)
        for u_l in u_list:
            print(u_l[0])
            flag = 0
            # task_list = requests.get(u_l[0])
            # for i in task_list:
            try:
                dict_save = {}
                dict_content = {}
                headers = {}
                user_agent_list = [
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
                ]
                headers['User-Agent'] = random.choice(user_agent_list)

                response = self.get_response(u=u_l[0].encode(), proxy=proxies)
                try:
                    # print(u_l[0],'ulululul')
                    det_html = response.content.decode('utf-8')
                    det_html = html.unescape(det_html)
                except:
                    det_html = response.content.decode('GB18030')
                    det_html = html.unescape(det_html)

                # print(det_html,'------------------det_html--------------------')

                content, pre_content = content_ex(det_html, key=0, url_tag=self.url_tag)
                # print(content,'content')
                title = title_ex_total(content, det_html)
                # print(title,'title')

                project_name = project_name_ex(content, title)
                # print(project_name,'project_name')

                project_num = project_num_ex(content, self.url_tag, det_html)
                # print(project_num,'project_num')

                date = date_ex(det_html, content)
                print(date)

                # type = type_ex(title, content)

                method = method_ex(title, content)

                project_intro = project_intro_ex(content)

                comp_address = comp_address_ex(content)

                comp_name = comp_name_ex(content)

                address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
                province = province_s(address)

                city = city_s(address)

                town = town_s(address)

                budget_amount = budget_amount_ex(content, det_html)

                comp_contact = comp_contact_ex(content)

                comp_tell = comp_tell_ex(content)

                agency_all = agency_all_ex(content)
                # print(agency_all)
                agency_address = agency_all[1]

                agency_name = agency_all[0]

                agency_contact = agency_all[2]

                agency_tel = agency_all[3]

                # table = table_ex(det_html)
                # print(table, 'table')
                win_money = win_money_all(content, det_html, self.url_tag)

                type = type_ex(title, content, win_money)

                # items = items_ex(title)
                # print(items, 'items')
                subject = subject_ex(title)

                subcontract = subcontract_ex(content)

                win_bider = winning_bidder_all(content, det_html, self.url_tag)

                pro = pro_ex(content)

                purchasers = str(purchersSort(title, project_name))
                page_id = u_l[1]
                # print(det_html)
                # print(content, '\n')
                print(title, 'title')
                # print(project_name, '22222222222')
                # print(project_num, '33333333333')
                # print(type, '55555555')
                # print(method, '666666666')
                # print(project_intro, 'introduction')
                # print(comp_address, 'c_address')
                # print(province, 'province')
                # print(city, 'city')
                # print(town, 'town')
                # print(budget_amount, 'b_amount')
                # print(comp_name, 'c_name')
                # print(comp_contact, 'c_man')
                # print(comp_tell, 'c_num')
                # print(agency_address, 'agency_address')
                # print(agency_name, 'agency_name')
                # print(agency_contact, 'agency_contact')
                # print(agency_tel, 'agency_tell')
                # print(win_money, 'win_money')
                # print(subject, 'subject')
                # print(subcontract, 'subcontract')
                # print(win_bider, 'win_bider')
                # print(pro, 'pro')
                # print(page_id, 'page_id')
                # print(purchasers,'purchaser')

                notnull_dict(title, dict_save, 'title')
                notnull_dict(project_name, dict_save, 'project_name')
                notnull_dict(project_num, dict_save, 'project_code')
                notnull_dict(date, dict_save, 'project_date')
                notnull_dict(pro, dict_save, 'expert')
                notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
                notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
                # notnull_dict(purchaser_class,dict_save,'purchaser_class')
                notnull_dict(project_intro, dict_save, 'project_intro')
                notnull_dict(win_money, dict_save, 'bid_money')
                # notnull_dict(items, dict_save, 'item')
                notnull_dict(province, dict_save, 'province')
                notnull_dict(city, dict_save, 'city')
                notnull_dict(town, dict_save, 'town')
                notnull_dict(subcontract, dict_save, 'subcontract')
                notnull_dict(budget_amount, dict_save, 'budget_money')
                notnull_dict(comp_name, dict_save, 'company_name')
                notnull_dict(comp_contact, dict_save, 'company_contact')
                notnull_dict(comp_address, dict_save, 'company_address')
                notnull_dict(comp_tell, dict_save, 'company_tel')
                notnull_dict(agency_name, dict_save, 'agency_name')
                notnull_dict(agency_contact, dict_save, 'agency_contact')
                notnull_dict(agency_address, dict_save, 'agency_address')
                notnull_dict(agency_tel, dict_save, 'agency_tel')
                notnull_dict(win_bider, dict_save, 'winning_bidder')
                notnull_dict(subject, dict_save, 'subject')
                notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
                notnull_dict(u_l[0], dict_save, 'page_url')
                notnull_dict(str(page_id), dict_save, 'page_id')
                notnull_dict(str(u_l[2]), dict_save, 'website_id')

                try:
                    # count = self.d_save.select_where('count(*)', 't_bid', 'title= "{}" and project_code = "{}" and website_id = 1'.format(MySQLdb.escape_string(title).decode('utf-8'),project_num))[0][0]
                    # if count:
                    #     self.logger.info('数据库中已存在')
                    #     self.d_save.runSql_excute(
                    #         'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                    #             str(self.web_id), str(page_id)))
                    #     self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                    #     # self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                    #     self.d_save.commit_insert()
                    #     print(count)
                    #
                    #     continue
                    bid_id = worker.get_id()
                    notnull_dict(str(bid_id), dict_save, 'id')
                    self.d_save.insert('t_bid', dict_save)
                    # self.d_save.commit_insert()
                    print(bid_id)
                    flag = 1

                    # print(bid_id)
                except:
                    flag = 0

                    bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                         project_num)
                    # self.d_save.commit_insert()
                    if latest_date(project_date_old, date):
                        continue
                    del dict_save['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_save, 'update_time')
                    notnull_dict('2', dict_save, 'index_status')
                    notnull_dict('0', dict_save, 'index_status_reindex')
                    self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

                # 品目标签
                itemSort(title, self.d_save, bid_id)

                c_html = content_html_ex(det_html, self.url_tag)
                if c_html == '空':
                    c_html = None

                notnull_dict(html.escape(c_html), dict_content, 'content')
                notnull_dict(html.escape(content), dict_content, 'pure_content')
                # notnull_dict(title, dict_content, 'title')
                notnull_dict(str(bid_id), dict_content, 'bid_id')
                # print(dict_content,'oooooo')
                try:
                    content_id = worker.get_id()
                    notnull_dict(str(content_id), dict_content, 'id')
                    self.d_save.insert('t_bid_content', dict_content)
                    self.d_save.commit_insert()
                    print(content_id, 'content_id')
                except:
                    # self.logger.error(sys.exc_info())
                    content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
                    # self.d_save.commit_insert()
                    del dict_content['id']
                    timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    notnull_dict(timeNow, dict_content, 'update_time')

                    self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
                    self.d_save.commit_insert()

                # if flag == 1:
                #     # 消息队列
                #     mq_list.append(bid_id)
                #     if len(mq_list) >= 500:
                #         ms = RabbitMQ('admin1', 'admin1', 'subscribe_queue-t')
                #         ms.message_send(mq_list)
                #         mq_list = []

                # website_page分表逻辑
                self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
                self.d_save.runSql_excute(
                    'insert into t_website_page_{} select * from t_website_page where id = {}'.format(
                        str(self.web_id), str(page_id)))
                # self.d_save.commit_insert()
                self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
                self.d_save.commit_insert()
                with open('log.txt', 'w') as w:
                    w.writelines(['page:' + str(u_l[0]) + '\n'])
                print('---------------------------------`--------------------')
            except Exception as e:

                self.d_save.roll_back_datebase()
                # self.d_save.insert('t_fail_task',{'fail_page_id':str(u_l[1])})
                self.d_save.update_one('t_website', 'mistake_num=mistake_num + 1', 'id =' + self.web_id)
                self.d_save.commit_insert()
                self.logger.error(sys.exc_info())
        # 如果数据爬完mq_list中不足500条，直接推送
        # ms = RabbitMQ('admin1', 'admin1', 'subscribe_queue-t')
        # ms.message_send(mq_list)

    def save_page_nmg_in(self):
        global dict_MQ
        mq_list = []
        u_list = [[i[0], i[1], i[2]] for i in self.url_list]

        # ip_list = ip_proxy.proxy_ip(10)
        # proxies = ip_proxy.proxy_amount(ip_list)
        for u_l in u_list:

            page_url = u_l[0]
            print(page_url)

            website_id = u_l[2]

            dict_save = {}
            dict_content = {}
            headers = {}
            user_agent_list = [
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
                "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
                "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
            ]
            headers['User-Agent'] = random.choice(user_agent_list)

            response = self.get_response(u=page_url.encode(), timeout=20)
            try:
                # print(u_l[0],'ulululul')
                det_html = response.content.decode('utf-8')
                det_html = html.unescape(det_html)
            except:
                det_html = response.content.decode('GB18030')
                det_html = html.unescape(det_html)

            # print(det_html,'------------------det_html--------------------')

            content, pre_content = content_ex(det_html, key=0, url_tag=self.url_tag)
            # print(content,'content')
            title = title_ex_total(content, det_html)
            # print(title,'title')

            project_name = project_name_ex(content, title)
            # print(project_name,'project_name')

            project_num = project_num_ex(content, self.url_tag, det_html)
            # print(project_num,'project_num')

            date = date_ex(det_html, content)
            print(date)

            # type = type_ex(title, content)

            method = method_ex(title, content)

            project_intro = project_intro_ex(content)

            comp_address = comp_address_ex(content)

            comp_name = comp_name_ex(content)

            address = province_ex_all([[title], [comp_address], [comp_name]], self.url_tag)
            province = province_s(address)

            city = city_s(address)

            town = town_s(address)

            budget_amount = budget_amount_ex(content, det_html)

            comp_contact = comp_contact_ex(content)

            comp_tell = comp_tell_ex(content)

            agency_all = agency_all_ex(content)
            # print(agency_all)
            agency_address = agency_all[1]

            agency_name = agency_all[0]

            agency_contact = agency_all[2]

            agency_tel = agency_all[3]

            # table = table_ex(det_html)
            # print(table, 'table')
            win_money = win_money_all(content, det_html, self.url_tag)

            type = type_ex(title, content, win_money)

            # items = items_ex(title)
            # print(items, 'items')
            subject = subject_ex(title)

            subcontract = subcontract_ex(content)

            win_bider = winning_bidder_all(content, det_html, self.url_tag)

            pro = pro_ex(content)

            purchasers = str(purchersSort(title, project_name))
            page_id = u_l[1]

            project_id = proj_id_ex(page_url, self.url_tag, type)

            self.save_part(dict_save=dict_save, title=title, project_name=project_name, project_num=project_num,
                           date=date, pro=pro, method=method, type=type,
                           project_intro=project_intro, win_money=win_money, province=province, city=city, town=town,
                           subcontract=subcontract, budget_amount=budget_amount, comp_name=comp_name,
                           comp_contact=comp_contact, comp_address=comp_address, comp_tell=comp_tell,
                           agency_name=agency_name, agency_contact=agency_contact, agency_address=agency_address,
                           agency_tel=agency_tel, win_bider=win_bider, subject=subject, purchasers=purchasers,
                           page_url=page_url, page_id=page_id, project_id=project_id,
                           det_html=det_html, dict_content=dict_content, content=content, website_id=website_id,
                           pre_content=pre_content)

    def save_part(self, dict_save=None, title=None, project_name=None, project_num=None, date=None, pro=None,
                  method=None, type=None,
                  project_intro=None, win_money=None, province=None, city=None, town=None,
                  subcontract=None, budget_amount=None, comp_name=None, comp_contact=None, comp_address=None,
                  comp_tell=None,
                  agency_name=None, agency_contact=None, agency_address=None,
                  agency_tel=None, win_bider=None, subject=None, purchasers=None, page_url=None, page_id=None,
                  project_id=None,
                  det_html=None, dict_content=None, content=None, website_id=None, pre_content=None):
        # print(det_html)
        # print(content, '\n')
        # print(title, 'title')
        # print(project_name, '22222222222')
        # print(project_num, '33333333333')
        # print(type, '55555555')
        # print(method, '666666666')
        # print(project_intro, 'introduction')
        # print(comp_address, 'c_address')
        # print(province, 'province')
        # print(city, 'city')
        # print(town, 'town')
        print(budget_amount, 'b_amount')
        # print(comp_name, 'c_name')
        # print(comp_contact, 'c_man')
        # print(comp_tell, 'c_num')
        # print(agency_address, 'agency_address')
        # print(agency_name, 'agency_name')
        # print(agency_contact, 'agency_contact')
        # print(agency_tel, 'agency_tell')
        # print(win_money, 'win_money')
        # print(subject, 'subject')
        # print(subcontract, 'subcontract')
        # print(win_bider, 'win_bider')
        # print(pro, 'pro')
        # print(page_id, 'page_id')
        # print(purchasers,'purchaser')

        notnull_dict(title, dict_save, 'title')
        notnull_dict(project_name, dict_save, 'project_name')
        notnull_dict(project_num, dict_save, 'project_code')
        notnull_dict(date, dict_save, 'project_date')
        notnull_dict(pro, dict_save, 'expert')
        notnull_dict(str(method), dict_save, 'dictionary_purchase_id')
        notnull_dict(str(type), dict_save, 'dictionary_announcement_id')
        # notnull_dict(purchaser_class,dict_save,'purchaser_class')
        notnull_dict(project_intro, dict_save, 'project_intro')
        notnull_dict(win_money, dict_save, 'bid_money')
        # notnull_dict(items, dict_save, 'item')
        notnull_dict(province, dict_save, 'province')
        notnull_dict(city, dict_save, 'city')
        notnull_dict(town, dict_save, 'town')
        notnull_dict(subcontract, dict_save, 'subcontract')
        notnull_dict(budget_amount, dict_save, 'budget_money')
        notnull_dict(comp_name, dict_save, 'company_name')
        notnull_dict(comp_contact, dict_save, 'company_contact')
        notnull_dict(comp_address, dict_save, 'company_address')
        notnull_dict(comp_tell, dict_save, 'company_tel')
        notnull_dict(agency_name, dict_save, 'agency_name')
        notnull_dict(agency_contact, dict_save, 'agency_contact')
        notnull_dict(agency_address, dict_save, 'agency_address')
        notnull_dict(agency_tel, dict_save, 'agency_tel')
        notnull_dict(win_bider, dict_save, 'winning_bidder')
        notnull_dict(subject, dict_save, 'subject')
        notnull_dict(purchasers, dict_save, 'dictionary_purchaser_id')
        notnull_dict(page_url, dict_save, 'page_url')
        notnull_dict(str(page_id), dict_save, 'page_id')
        notnull_dict(str(website_id), dict_save, 'website_id')
        notnull_dict(project_id, dict_save, 'project_id')
        # notnull_dict(u_l[1],dict_save,'page_id')
        # self.d_save.delete_where('t_bid', 'title', title)
        # print(dict_save,'aaaaaaaaa')

        try:

            # 将插入t_bid表
            bid_id = worker.get_id()
            notnull_dict(str(bid_id), dict_save, 'id')
            self.d_save.insert('t_bid', dict_save)
            # self.d_save.commit_insert()
            print(bid_id)

            if type == 3 or type == 4:
                pkg_ex(pre_content, bid_id, self.d_save)

            # print(bid_id)
        except:
            bid_id, project_date_old = self.d_save.select_bid_id(MySQLdb.escape_string(title).decode('utf-8'),
                                                                 project_num)
            # self.d_save.commit_insert()
            if project_date_old:

                if latest_date(project_date_old, date):
                    return

            timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            del dict_save['id']
            notnull_dict(timeNow, dict_save, 'update_time')
            notnull_dict('2', dict_save, 'index_status')
            notnull_dict('0', dict_save, 'index_status_reindex')
            self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

        # 品目标签
        itemSort(title, self.d_save, bid_id)

        # try:
        #     bid_id = d_save.select_where('id','t_bid','title='+'"'+title+'"')[0][0]
        #     print(bid_id)
        # except:
        #     bid_id = None
        # self.d_save.delete_where('t_bid_content', 'title', title)

        c_html = content_html_ex(det_html, self.url_tag, page_url=page_url)
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
            self.d_save.insert('t_bid_content', dict_content)
            self.d_save.commit_insert()
            print(content_id, 'content_id')
        except:
            # self.logger.error(sys.exc_info())
            content_id = self.d_save.select_where('id', 't_bid_content', 'bid_id=' + str(bid_id))[0][0]
            # self.d_save.commit_insert()
            del dict_content['id']
            timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            notnull_dict(timeNow, dict_content, 'update_time')

            self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
            self.d_save.commit_insert()

        print(111111)
        try:
            # website_page分表逻辑
            self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
            # self.d_save.commit_insert()
            self.d_save.runSql_excute(
                'insert into t_website_page_{} select * from t_website_page where id = {}'.format(str(self.web_id),
                                                                                                  str(page_id)))

            self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
            self.d_save.commit_insert()
        except:
            self.d_save.runSql_excute('delete from t_website_page where id = {}'.format(page_id))
            self.d_save.commit_insert()
        print(222222)
        with open('log.txt', 'w') as w:
            w.writelines(['page:' + str(page_url) + '\n'])
        print('---------------------------------`--------------------')


class SavePart():
    def __init__(self, d_save=None, dict_url=None, dict_content=None, logger=None, url_list=None, web_id=None):
        self.d_save = d_save
        self.dict_url = dict_url
        self.dict_content = dict_content
        self.logger = logger
        self.url_list = url_list
        self.web_id = web_id

    # 详情页url存储逻辑
    def url_save_part(self, det_url='', mission_id='', dict_url=None, web_table=None, extra=None):
        try:
            id = worker.get_id()
            # print(id)
            notnull_dict(str(id), dict_url, 'id')
            notnull_dict(det_url, dict_url, 'page_url')
            notnull_dict(str(mission_id), dict_url, 'mission_id')
            if extra:
                notnull_dict(str(extra), dict_url, 'extra')
            try:

                count = self.d_save.select_where('count(*)', web_table, 'page_url=' + '"' + det_url + '"')[0][0]
                if not count:
                    # 没用？？？
                    self.d_save.insert('t_website_page', dict_url)
                    self.d_save.commit_insert()
                    # print(id)
                # self.d_save.insert('t_website_page', dict_url)
                # self.d_save.commit_insert()
            except:
                # logger.error(sys.exc_traceback)
                url_id = self.d_save.select_where('id', 't_website_page', 'page_url=' + '"' + det_url + '"')[0][0]
                # self.d_save.commit_insert()
                del dict_url['id']
                timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                notnull_dict(timeNow, dict_url, 'update_time')
                self.d_save.update(table='t_website_page', data=dict_url, id=url_id)
                self.d_save.commit_insert()
        except:
            # logger.exception(sys.exc_info())
            self.logger.error(sys.exc_info())
            # print(e,'111111111')

    def bid_save_part(self, dict_save, title):
        try:
            # count = self.d_save.select_where('count(*)','t_bid','title="{}" and website_id <> 1'.format(title))
            #
            # if count:
            #     continue
            bid_id = worker.get_id()
            notnull_dict(str(bid_id), dict_save, 'id')
            self.d_save.insert('t_bid', dict_save)
            # self.self.d_save.commit_insert()
            print(bid_id)
            flag = 1
        except:
            flag = 1
            # self.logger.error(sys.exc_info())
            bid_id = self.d_save.select_where('id', 't_bid',
                                              'title=' + '"' + title + '"' + ' and ' + 'project_id=' + '"' + projid + '"')[
                0][0]
            # self.self.d_save.commit_insert()
            timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            del dict_save['id']
            notnull_dict(timeNow, dict_save, 'update_time')
            notnull_dict('2', dict_save, 'index_status')
            notnull_dict('0', dict_save, 'index_status_reindex')
            self.d_save.update(table='t_bid', data=dict_save, id=bid_id)

        # 品目标签
        item_save(items, self.d_save, bid_id)

        # try:
        #     bid_id = self.d_save.select_where('id','t_bid','title='+'"'+title+'"')[0][0]
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
            self.d_save.insert('t_bid_content', dict_content)
            self.d_save.commit_insert()
            print(content_id, 'content_id')
        except:
            # self.logger.error(sys.exc_info())
            content_id = self.d_save.select_where('id', 't_bid_content',
                                                  'bid_id=' + str(bid_id))[
                0][0]
            # self.self.d_save.commit_insert()
            del dict_content['id']
            timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            notnull_dict(timeNow, dict_content, 'update_time')
            self.d_save.update(table='t_bid_content', data=dict_content, id=content_id)
            self.d_save.commit_insert()
        if flag == 1:
            # 消息队列
            mq_list.append(bid_id)
            if len(mq_list) >= 500:
                ms = RabbitMQ('admin1', 'admin1', 'subscribe_queue-t')
                ms.message_send(mq_list)
                mq_list = []
        self.d_save.update_one('t_website_page', 'is_crawled=1', 'id=' + str(page_id))
        with open('page_log.txt', 'w') as w:
            w.writelines(['page:' + str(u_l[1]) + '\n'])
        print('---------------------------------`--------------------')
        n += 1


if __name__ == '__main__':
    s = Save_data()
    s.jiagsu_contract('s')