#coding=UTF-8
import MySQLdb
from MySQLdb import escape_string
from sshtunnel import SSHTunnelForwarder
import logging
import os.path
import time
import sys
import html
from snow_factory import IdWorker
import snow_settings as sst


# 实例化雪花ID，sst为配置文件
worker = IdWorker(sst.DATACENTER_ID,sst.WORKER_ID,sst.SEQUENCE)


class MySQL():

    def __init__(self,host,port,user,password,db,charset):
        try:
            self.db = MySQLdb.connect(host=host,port=port,user=user,password=password,db=db,charset=charset)
            self.db.ping(True)
            self.cursor = self.db.cursor()
        except Exception as e:
            print(e,'@@@@@@')


    # def insert(self,table,data):
    #     keys = ','.join(data.keys())
    #     # values = ','.join(['%s']*len(data))
    #     values = data.values()
    #     # print(data.values())
    #     sql_query = 'insert into %s(%s) values(%s)'
    #     # print(sql_query)
    #
    #     self.cursor.execute(sql_query,(table,keys,values))
    #     bid_id = self.db.insert_id()
    #
    #     print('1')
    #     return bid_id

    def runSql_select(self,sql):
        sql_query = sql
        self.cursor.execute(sql_query)
        return self.cursor.fetchall()

    def runSql_excute(self,sql):
        sql_query = sql
        # print(sql_query)
        self.cursor.execute(sql_query)

    def insert(self,table,data):
        keys = ','.join(data.keys())
        # values = ','.join(['%s']*len(data))
        values = ','.join(['0' if i == None else i for i in data.values()])
        # print(data.values())
        sql_query = 'insert into %s(%s) values(%s)'%(table,keys,values)
        # print(sql_query)

        self.cursor.execute(sql_query)
        bid_id = self.db.insert_id()

        print('1')
        return bid_id

    def update_money(self,budget_money=None,bid_money=None,update_time=None,bid_id=None):
        # print(index_status,'-----------index_status------------')
        sql_query = 'update t_bid set budget_money = %s ,bid_money = %s ,update_time= %s ,index_status = 2 where id=%s'
        # print(sql_query,'更新money，sql语句')

        self.cursor.execute(sql_query,(budget_money,bid_money,update_time,bid_id))
        print('2')


    def update_url(self,url=None,update_time=None,title=None):
        sql_query = 'update t_bid set page_url = %s ,update_time= %s ,index_status = 2 where title = %s and website_id = 38'

        self.cursor.execute(sql_query, (url, update_time, title))
        print('2')


    def update_url_zj(self,url=None,update_time=None,page_id=None):
        sql_query = 'update t_bid set page_url = %s ,update_time= %s ,index_status = 2 where page_id = %s and website_id = 33'

        self.cursor.execute(sql_query, (url, update_time, page_id))
        print('2')


    def update(self,table=None,data=None,id=None):
        keys = data.keys()
        # values = ','.join(['%s']*len(data))
        values = data.values()
        # print(data.values())
        set_values = ','.join(list(map(lambda x,y:x+'='+y,keys,values)))
        # print(set_values)
        sql_query = 'update %s set %s where id=%s'%(table, set_values,id)
        # print(sql_query,type(sql_query))

        self.cursor.execute(sql_query)
        print('2')


    def batchinsert(self,table,field,data_list):
        self.cursor.executemany('insert into ''(字段名) values(%s,%s,%s,%s)',data_list)




    def select_all(self,sth,table):
        sql_query = 'select %s from %s'%(sth,table)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_where(self,sth,table,condition):
        sql_query = 'select %s from %s where %s' % (sth,table,condition)
        # print(sql_query)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_bid_id(self,title,project_num=''):
        sql_query = 'select id,project_date from t_bid where title= "%s" and project_code = "%s"'%(title,project_num)
        # print(sql_query)
        try:
            self.cursor.execute(sql_query)
            result = self.cursor.fetchall()[0]
            print(result,'xxxxxxxxxx')
            return result[0],result[1]
        except Exception as e:
            print(e)

    def select_type(self,start,end):
        sql_query = 'select a.id,a.title,b.pure_content from t_bid as a left join t_bid_content as b on a.id = b.bid_id where a.id between %s and %s' %(start,end)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_p_num(self):
        sql_query = 'select a.id,b.pure_content from t_bid as a left join t_bid_content as b on a.id = b.bid_id where project_code="SDGP3700002"'
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_c_num(self):
        sql_query = 'select c.id from t_bid as a left join t_bid_content as b on a.id = b.bid_id left join t_website_page as c on a.page_id = c.id where b.content is Null'
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_c_clean(self):
        sql_query = 'select b.id,a.page_url from t_bid as a left join t_bid_content as b on a.id = b.bid_id where a.id = 4165457'
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_date(self,start,end):
        sql_query = 'select a.id,a.page_url,b.pure_content from t_bid as a left join t_bid_content as b on a.id = b.bid_id where a.id between %s and %s' %(start,end)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_c_date(self,start):
        sql_query = 'select page_id,project_date from t_bid where page_id > %s' %(start)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_web(self,start,end):
        sql_query = 'select a.id,c.website_id from t_bid as a left join t_website_page as b on a.page_id = b.id left join t_website_mission as c on b.mission_id = c.id where a.id between %s and %s'%(start,end)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_ccgp_where(self,date):
        sql_query = 'select page_url,page_id from t_bid where province is NULL and website_id = 1 and page_url like "%s"'%(date)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)


    def select_ccgp_where_big(self,date):
        sql_query = 'select page_url,page_id from t_bid where  website_id = 1 and (bid_money > 100000000000 or budget_money > 100000000000) and page_url like "%s"'%(date)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_ccgp_where_null(self,date):
        sql_query = 'select page_url,page_id from t_bid where  website_id = 1 and bid_money is NULL and budget_money is NULL and page_url like "%s"'%(date)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_web_where(self,condition):
        '''
        从数据库搜索相关网站爬虫的详情页url（page_url）
        '''
        sql_query = 'select a.page_url,a.id,b.website_id from t_website_page as a left join t_website_mission as b on a.mission_id = b.id where %s' %(condition)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)


    def select_web_from_bid(self):
        sql_query = 'select a.page_url,a.id,b.website_id from t_website_page as a left join t_bid as b on a.id = b.page_id where b.project_date > "2020-08-08" and website_id = 41'
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_web_where_hb(self,condition):
        '''
        带有额外信息（extra）的page_url用此方法
        '''
        sql_query = 'select a.page_url,a.id,a.extra,b.website_id from t_website_page as a left join t_website_mission as b on a.mission_id = b.id where %s' %(condition)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_repeat_bid_id(self):
        sql_query = 'select id,bid_id from t_bid_content where bid_id in (select bid_id from t_bid_content group by bid_id having count(bid_id) > 1)'
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_text(self,start,end):
        sql_query = 'select a.id,b.pure_content,b.content,a.page_url from t_bid as a left join t_bid_content as b on a.id = b.bid_id where a.bid_money is NULL and a.budget_money is NULL and (a.website_id = 15 or a.website_id = 16) and a.id between %s and %s'%(start,end)
        print(sql_query)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_title_ca(self,start,end):
        sql_query = 'select id,company_address,title from t_bid where province is NULL and (website_id == 15 or website_id == 16) and id between %s and %s'%(start,end)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_big(self,date):
        sql_query = 'select id,budget_money,bid_money from t_bid where  website_id = 1 and (bid_money > 100000000000 or budget_money > 100000000000) and page_url like "%s"' %(date)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_repeat(self):
        sql_query = 'select id from t_bid where id not in (select dt.minno from(select max(id) as minno from t_bid group by title) dt )'
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def select_limit(self,sth,table,condition):
        sql_query = 'select %s from %s where %s' % (sth, table, condition)
        try:
            self.cursor.execute(sql_query)
            return self.cursor.fetchall()
        except Exception as e:
            print(e)

    def update_one(self,table,new,where):
        sql_query = 'update %s set  %s where %s' % (table,new, where)
        # print(sql_query,'update_one')
        try:
            self.cursor.execute(sql_query)
            # self.db.commit()
        except Exception as e:
            print(e)


    def update_spider_status(self,status,program_name):
        sql_query = 'update t_website set running_status = %s where program_name=%s'%(status,'"'+program_name+'"')
        try:
            self.cursor.execute(sql_query)
            self.db.commit()
        except Exception as e:
            print(e)

    def update_date(self,status,timeNow,program_name):
        sql_query = 'update t_website set {} = {} where program_name={}'.format(status,'"'+timeNow+'"','"'+program_name+'"')
        try:
            self.cursor.execute(sql_query)
            self.db.commit()
        except Exception as e:
            print(e)

    def update_state(self,status,timeNow,program_name):
        sql_query = 'update t_website set {} = {} where program_name={}'.format(status,timeNow,'"'+program_name+'"')
        try:
            self.cursor.execute(sql_query)
            self.db.commit()
        except Exception as e:
            print(e)

    def delete_where(self,table,field,sth):
        sql_query = 'delete from %s where %s = %s'%(table,field,sth)
        try:
            self.cursor.execute(sql_query)
            # self.db.commit()
            print('删除成功')
        except Exception as e:
            print(e)

    def start_status(self,p_name):
        try:
            sql_query = 'update t_website set running_status= 1 where program_name={}'.format('"' + p_name + '"')
            # print(sql_query)
            timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            sql_query2 = 'update t_website set start_time = {} where program_name={}'.format('"' + timeNow + '"',
                                                                                             '"' + p_name + '"')
            self.cursor.execute(sql_query)
            self.cursor.execute(sql_query2)
        except Exception as e:
            print(e)


    def stop_status(self,p_name):
        try:
            sql_query = 'update t_website set running_status= 0 where program_name={}'.format('"' + p_name + '"')
            timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            sql_query2 = 'update t_website set stop_time = {} where program_name={}'.format('"' + timeNow + '"',
                                                                                            '"' + p_name + '"')
            self.cursor.execute(sql_query)
            self.cursor.execute(sql_query2)
        except Exception as e:
            print(e)


    def commit_insert(self):
        self.db.commit()


    def roll_back_datebase(self):
        self.db.rollback()


    def close_db(self):
        try:
            self.cursor.close()
        except:
            pass
        finally:
            self.db.close()






class Logger(object):
    def __init__(self,file_path=''):
        '''''
            指定保存日志的文件路径，日志级别，以及调用文件
            将日志存入到指定的文件中
        '''
        project_path = '.'  # 定义项目目录
        current_time=time.strftime('%Y%m%d%H%M',
                                   time.localtime(time.time()))  # 返回当前时间
        current_path=os.path.dirname(os.path.abspath(project_path))  # 返回当前目录
        path1=current_path.split(project_path)  #指定分隔符对字符串进行切片
        path2=[path1[0], project_path]
        path3=''
        new_name=path3.join(path2) + '/logs/'+file_path #在该路径下新建下级目录

        dir_time = time.strftime('%Y%m%d', time.localtime(time.time()))  #返回当前时间的年月日作为目录名称
        isExists=os.path.exists(new_name + dir_time)   #判断该目录是否存在
        if not isExists:
            os.makedirs(new_name + dir_time)
            print(new_name + dir_time + "目录创建成功")

        else:
            # 如果目录存在则不创建，并提示目录已存在
            print(new_name + "目录 %s 已存在" % dir_time)


        try:
            # 创建一个logger(初始化logger)
            self.log = logging.getLogger()
            self.log.setLevel(logging.DEBUG)

            # 创建一个handler，用于写入日志文件


            # 如果case组织结构式 /testsuit/featuremodel/xxx.py ， 那么得到的相对路径的父路径就是项目根目录
            log_name = new_name  + dir_time + '/' + current_time + '.log'  #定义日志文件的路径以及名称

            fh = logging.FileHandler(log_name)
            fh.setLevel(logging.INFO)

            # 再创建一个handler，用于输出到控制台
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # 定义handler的输出格式
            formatter = logging.Formatter('[%(asctime)s] - %(name)s - %(levelname)s - %(message)s')
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            # 给logger添加handler
            self.log.addHandler(fh)
            self.log.addHandler(ch)
        except Exception as e:
            print("输出日志失败！ %s" % e)

    # 日志接口，用户只需调用这里的接口即可，这里只定位了INFO, WARNING, ERROR三个级别的日志，可根据需要定义更多接口

    def info(cls,msg):
        cls.log.info(msg)
        # cls.log.exception(msg)
        return


    def warning(cls,msg):
        cls.log.warning(msg)
        return


    def error(cls, msg):
        cls.log.error(msg)
        cls.log.exception(msg)
        return


def logger():
    logger = Logger()
    return logger


def notnull_dict(str,dict,key):
    if str != '空' :
        if str == None:
            # str为None的时候存储会报错
            # return
            dict[key] = str

        elif str == 'None':
            return
        else:
            str_clean = MySQLdb.escape_string(str).decode('utf-8')
            # print(str_clean,'str_clean')
            dict[key] = '"'+str_clean+'"'
    elif str == '空' and (key == 'project_code' or key == 'title' or key == 'project_date' or key == 'project_id'):
        return 
    else:
        # print(1)
        dict[key] = 'null'


def notnull_dict_num(num,dict,key):
    if num != '空':
        dict[key] = str(num)
    else:
        dict[key] = 'null'


def getListMaxNumIndex(num_list,topk=3):
    import copy
    '''
    获取列表中最大的前n个数值的位置索引
    '''
    tmp_list=copy.deepcopy(num_list)
    tmp_list.sort()
    max_num_index=[num_list.index(one) for one in tmp_list[::-1][:topk]]
    # min_num_index=[num_list.index(one) for one in tmp_list[:topk]]
    return max_num_index


def readPageUrl(txt_name):
    with open(txt_name,'r') as r:
        page=r.readlines()[0].split(':')[1]
        # print(page)
        return int(page)





if __name__ == '__main__':
    # t_test = MySQL(host='39.107.25.250',port=3306,user='root',password='jie8#jlfsjd',db='crawl_test',charset='utf8')
    # t_test.update(table='hehe',data={'aaa':'111','bbb':'222'},condition='abc=123')
    # local_list = gov.select_all('lib_admin_gov')
    # print(local_list)
    # readPageUrl()
    pass





