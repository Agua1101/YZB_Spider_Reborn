from yzb_db_connect import *
from yzb_conf import config as conf
import requests


# 修改易找标数据时所用方法
class RepairMethod():

    def __init__(self,d_save=None):
        self.d_save = d_save

    # 删除es中的数据
    def delete_es(self,id):
        if conf.db == 'bid':
            url = 'https://yzb.caigou2003.com/bid/py/update/byId'
        else:
            url = 'https://testyzb.caigou2003.com/bid/py/update/byId'

        # id_list = []

        print(id)
        response = requests.post(url, json=id)
        resp_dict = response.json()
        resp_status = resp_dict['status']
        print(response)
        today = time.strftime('%Y:%m:%d', time.localtime(time.time()))
        if response.status_code != 200:
            with open('wrong_id.txt', 'a') as a:
                a.write(today + '---' + str(id) + '\n')
            return
        elif resp_status == 500:
            with open('wrong_id.txt', 'a') as a:
                a.write(today + '---500---' + str(id) + '\n')
            return
        return id

    # 将更改后的数据移动到临时表中
    def move_delete_date(self,id,year):
        d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                       charset=conf.charset)

        # date = d_save.runSql_select('select project_date from t_bid_0000 where id =' + str(id))[0][0]
        # print(str(date))
        # year = str(date)[:4]
        # print(year)
        title = d_save.runSql_select(f'select title from t_bid_{year} where id = {id}')[0][0]
        d_save.runSql_excute(f'update t_bid_{year} set index_status = 0 where id = {id}')
        d_save.runSql_excute(f'update t_bid_{year} set index_status_reindex = 0 where id = {id}')
        d_save.runSql_excute(f'insert into t_bid select * from t_bid_{year} where id = {id}')
        d_save.runSql_excute(
            f'insert into t_bid_content select * from t_bid_content_{year} where bid_id = {id}')
        d_save.runSql_excute(
            f'insert into t_bid_item_ai select * from t_bid_item_ai_{year} where bid_id = {id}')
        d_save.runSql_excute(f'delete from t_bid_{year} where id = {id}')
        d_save.runSql_excute(f'delete from t_bid_content_{year} where bid_id = {id}')
        d_save.runSql_excute(f'delete from t_bid_item_ai_{year} where bid_id = {id}')
        d_save.commit_insert()
        print(f'complete id:{id} title:{title}')


    def move(self,id,year):
        '''
        将分表数据移动到临时表

        '''
        # bid表
        self.d_save.runSql_excute(f'insert into t_bid select * from t_bid_{year} where id = {id}')
        # bid_content表
        self.d_save.runSql_excute(
            f'insert into t_bid_content select * from t_bid_content_{year} where bid_id = {id}')
        # bid_item_ai表
        self.d_save.runSql_excute(
            f'insert into t_bid_item_ai select * from t_bid_item_ai_{year} where bid_id = {id}')
        # bid_pkg表
        self.d_save.runSql_excute(
            f'insert into t_bid_pkg select * from t_bid_pkg_{year} where bid_id = {id}')
        # self.d_save.commit_insert()

    def delete_data(self,id,year):
        '''
        删除分表的数据
        '''
        self.d_save.runSql_excute(f'delete from t_bid_{year} where id = {id}')
        self.d_save.runSql_excute(f'delete from t_bid_content_{year} where bid_id = {id}')
        self.d_save.runSql_excute(f'delete from t_bid_item_ai_{year} where bid_id = {id}')
        self.d_save.runSql_excute(f'delete from t_bid_pkg_{year} where bid_id = {id}')
        # self.d_save.commit_insert()


    def execute(self,id=None,year=None):

        # id = self.delete_es(id)
        # if not id:
        #     return
        # 将更改后的数据移动到临时表中
        self.move_delete_date(id,year)
