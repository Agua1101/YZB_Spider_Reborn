#coding=UTF-8
import MySQLdb
from yzb_conf import config as conf
from sshtunnel import SSHTunnelForwarder


# def mq_dict():
#     list_mq = []
#     cursor = conn.cursor()
#     sql_query = 'select region_code,region_name from {} where region_level= 1'.format('t_region')
#     cursor.execute(sql_query)
#     province_list = cursor.fetchall()


def local_dict():
    # server = SSHTunnelForwarder(ssh_address_or_host=('39.96.69.104', 22), ssh_username='root',
    #                             ssh_password='vitW0Pks2A*Cf*CH', remote_bind_address=(conf.host, 3306))
    # server.start()
    # conn = MySQLdb.connect(
    #     host='127.0.0.1',
    #     port=server.local_bind_port,
    #     user='develop',
    #     password='X02b8H5^FhXOr5Tq',
    #     db='bid',
    #     charset='utf8'
    # )

    # conn = MySQLdb.connect()
    conn = MySQLdb.connect(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                   charset=conf.charset)

    local_table = {}
    
    cursor = conn.cursor()
    sql_query = 'select region_code,region_name from {} where region_level= 1'.format('t_region')
    cursor.execute(sql_query)
    province_list = cursor.fetchall()
    for province in province_list:
        sql_query = 'select region_code,region_name from {} where region_level= 2 and parent_code= {}'.format('t_region',province[0])
        cursor.execute(sql_query)
        city_tuple = cursor.fetchall()
        city_list = [i[1] for i in city_tuple]
        province_str = province[1].replace('\u3000','')
        local_table.update({province_str: {}})
        for city in city_tuple:
            sql_query = 'select region_code,region_name from {} where region_level= 3 and parent_code= {}'.format(
                't_region', city[0])
            cursor.execute(sql_query)
            town_tuple = cursor.fetchall()
            town_list = [i[1].replace('\u3000','') for i in town_tuple]
            local_table[province_str].update({city[1].replace('\u3000',''):town_list})

    conn.close()
    # server.close()
    return local_table

# conn.close()
# server.close()
if __name__ == '__main__':

    print(local_dict())
    # print(local_table)
# local_table = {}
# values = set()
# words = []
# for row in local_list:
#     word = row[1]
#     words.append(word)

    # if local_table.get(keys_province):
    #     if local_table[keys_province].get(keys_city):
    #         local_table[keys_province][keys_city].update({row[5]:row[6]})
    #     else:
    #         local_table[keys_province][keys_city] = {row[5]:row[6]}
        # print({row[i] for i in range(2,7)})
    # else:
    #     local_table[keys_province] = {keys_city:{row[5]:row[6]}}
        # if local_table[keys_province].get(keys_city):
        #     local_table[keys_province][keys_city].update({row[5],row[6]})
        # else:
        #     local_table[keys_province] = {keys_city:{row[5],row[6]}}
    # print(local_keys)
# print(words)

# local_table = {keys_province:{keys_city:{1231231}}}
