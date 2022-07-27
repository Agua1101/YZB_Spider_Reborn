#coding=UTF-8
from yzb_db_connect import *
from yzb_conf import config as conf
from sshtunnel import SSHTunnelForwarder

class Dictionary():

    @staticmethod
    def dictionary():
        # server = SSHTunnelForwarder(ssh_address_or_host=('39.96.69.104', 22), ssh_username='root',
        #                             ssh_password='vitW0Pks2A*Cf*CH', remote_bind_address=(conf.host, 3306))
        # server.start()
        # d_save = MySQL(host='127.0.0.1', port=server.local_bind_port, user=conf.user, password=conf.password, db=conf.db,
        #                charset=conf.charset)
        d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                       charset=conf.charset)

        #更正/澄清
        gzcq = d_save.select_where('id','t_bid_dictionary','constant_type = 1 and constant_name = "澄清/更正"')[0][0]
        fblb = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "废标"')[0][0]
        zhongbgg = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "中标公告"')[0][0]
        cjgg = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "成交公告"')[0][0]
        xqgg = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "需求公告"')[0][0]
        tpgg = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "谈判公告"')[0][0]
        csgg = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "磋商公告"')[0][0]
        yqzbgg = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "邀请招标公告"')[0][0]
        xjgg = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "询价公告"')[0][0]
        dylygs = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "单一来源公示"')[0][0]
        zgys = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "资格预审"')[0][0]
        zhaobgg = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "公开招标公告"')[0][0]
        qtgs = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "其他公示"')[0][0]
        qtgg = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "其他公告"')[0][0]
        dyly = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 2 and constant_name = "单一来源"')[0][0]
        xj = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 2 and constant_name = "询价"')[0][0]
        jzxtp = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 2 and constant_name = "竞争性谈判"')[0][0]
        jzxcs = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 2 and constant_name = "竞争性磋商"')[0][0]
        yqzb = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 2 and constant_name = "邀请招标"')[0][0]
        gkzb = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 2 and constant_name = "公开招标"')[0][0]
        qtcg = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 2 and constant_name = "其他采购方式"')[0][0]
        cgyx = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "采购意向"')[0][0]
        htgg = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "合同公告"')[0][0]
        ggfuxmys = d_save.select_where('id', 't_bid_dictionary', 'constant_type = 1 and constant_name = "公共服务项目验收结果公告"')[0][0]
        # print(gzcq,fblb,zhongbgg,cjgg,xqgg,tpgg,csgg,yqzbgg,xjgg,dylygs,zgys,zhaobgg,qtgs,qtgg,dyly,xj,jzxtp,jzxcs,yqzb,gkzb,qtcg)

        # server.close()
        return gzcq,fblb,zhongbgg,cjgg,xqgg,tpgg,csgg,yqzbgg,xjgg,dylygs,zgys,zhaobgg,qtgs,qtgg,dyly,xj,jzxtp,jzxcs,yqzb,gkzb,qtcg,cgyx,htgg,ggfuxmys





if __name__ == '__main__':

    gzcq, fblb, zhongbgg, cjgg, xqgg, tpgg, csgg, yqzbgg, xjgg, dylygs, zgys, zhaobgg, qtgs, qtgg, dyly, xj, jzxtp, jzxcs, yqzb, gkzb, qtcg = Dictionary.dictionary()
    print(gzcq)