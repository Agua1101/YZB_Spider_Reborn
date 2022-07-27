# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from yzb_tools.yzb_db_connect import *
from yzb_conf import config as conf

d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                   charset=conf.charset)




class CcgpGovCnPipeline:
    def __init__(self):
        self.d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                       charset=conf.charset)



    def process_item(self, item, spider):
        dict_save = {}
        dict_content_save = {}
        notnull_dict(item['title'], dict_save, 'title')
        notnull_dict(item['date'], dict_save, 'date')


        self.d_save.insert('t_bid', dict_save)
        self.d_save.commit_insert()

        notnull_dict(item['html'], dict_content_save, 'html')
        self.d_save.insert('t_bid_content', dict_content_save)
        self.d_save.commit_insert()


        return item
