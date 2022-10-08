#coding=UTF-8
import re

from yzb_tools.yzb_db_connect import *
from yzb_ml_code.purchaser_ml import myPredict
from yzb_conf import config as conf
# import item_ml
from classifier_multi_label_textcnn import predict
from snow_factory import IdWorker
import snow_settings as sst


# 实例化雪花ID，sst为配置文件
worker = IdWorker(sst.DATACENTER_ID,sst.WORKER_ID,sst.SEQUENCE)


def insert_ps():
    d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                   charset=conf.charset)
    title_list = d_save.select_where('project_name,company_name,id', 't_bid', 'id between 12004 and 570244')
    # print(title_list)
    for t in title_list:
        try:
            sample = str(t[0])+str(t[1])
            result = myPredict(sample)
            d_save.update_one('t_bid','dictionary_purchaser_id="{}"'.format(result),'id={}'.format(t[2]))
            # with open('log2.txt', 'w') as w:
            #     w.writelines(['id:' + str(t[1]),])
        except Exception as e:
            print(e)


def purchers_rules(sample):
    medical = '医院|卫生院|妇幼保健院'
    college = '学院|学校|大学|小学|中学|初中|高中|教育'
    others = '公司|支行|银行'
    judicial = '法院'
    gov = '中心'
    if re.search(f'({medical})$',sample):
        return 25
    elif re.search(f'({college})$',sample):
        return 26
    elif re.search(f'({others})$',sample):
        return 27
    elif re.search(f'({judicial})$',sample):
        return 23
    elif re.search(f'({gov})$',sample):
        return 23
    elif re.search(medical,sample):
        return 25
    elif re.search(college,sample):
        return 26
    elif re.search(college,sample):
        return 27
    elif re.search(judicial,sample):
        return 23
    else:
        return


def purchersSort(title,c_name):
    sample = str(c_name)
    if not sample:
        return 27
    purchers = myPredict(sample)
    # purchers = ''
    rule_purchase = purchers_rules(sample)

    if rule_purchase:
        return rule_purchase
    else:
        return purchers

# 品目分类
def itemSort(title,d_save,bid_id):
    dict_item = {}
    dict_save = {}

    print(title,'title')
    items = predict.get_label(title)
    id = d_save.select_where('id', 't_bid_item_ai', 'bid_id=' + str(bid_id))
    if id:
        d_save.delete_where('t_bid_item_ai','bid_id',bid_id)
        notnull_dict('2', dict_save, 'index_status')
        notnull_dict('0', dict_save, 'index_status_reindex')
        d_save.update(table='t_bid', data=dict_save, id=bid_id)
    for j in items:
        item_id = worker.get_id()
        print(item_id)
        notnull_dict_num(item_id, dict_item, 'id')
        notnull_dict_num(bid_id, dict_item, 'bid_id')
        notnull_dict(str(j), dict_item, 'item_code')
        d_save.insert('t_bid_item_ai',dict_item)

    print('------------done-------------')


# def quan_da():
#     from sshtunnel import SSHTunnelForwarder
#     server = SSHTunnelForwarder(ssh_address_or_host=('39.96.69.104', 22), ssh_username='root',
#                                 ssh_password='vitW0Pks2A*Cf*CH', remote_bind_address=(conf.host, 3306))
#     server.start()
#     dict_item = {}
#     d_save = MySQL(host='127.0.0.1', port=server.local_bind_port, user=conf.user, password=conf.password, db=conf.db,
#                    charset=conf.charset)
#     title_list = d_save.select_where('id,title', 't_bid', 'id > 0')
#     # print(title_list)
#     for i in title_list:
#         items = item_ml.predict(i[1])
#         for j in items:
#             notnull_dict_num(i[0], dict_item, 'bid_id')
#             notnull_dict(str(j), dict_item, 'item_code')
#             d_save.insert('t_bid_item_ai', dict_item)
#             d_save.commit_insert()
#     print('------------done-------------')



# if __name__ == '__main__':
    # quan_da()