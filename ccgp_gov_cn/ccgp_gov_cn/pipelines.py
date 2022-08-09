# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from yzb_tools.yzb_db_connect import *
from yzb_conf import config as conf
worker = IdWorker(sst.DATACENTER_ID,sst.WORKER_ID,sst.SEQUENCE)



class CcgpGovCnPipeline():
    def __init__(self):
        # self.d_save = MySQL(host=spider.settings.get('host'), port=spider.settings.get('port'), user=spider.settings.get('user'), password=spider.settings.get('password'), db=spider.settings.get('db'),
        #                charset=spider.settings.get('charset'))

        self.d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                       charset=conf.charset)



    def process_item(self, item, spider):
        dict_url_save = {}
        dict_html_save = {}
        id = worker.get_id()


        notnull_dict(item['page_url'], dict_url_save, 'page_url')
        notnull_dict(str(id), dict_url_save, 'id')
        notnull_dict('7', dict_url_save, 'mission_id')
        self.d_save.insert('t_website_page',dict_url_save)

        notnull_dict(item['title'], dict_html_save, 'title')
        notnull_dict(item['date'], dict_html_save, 'date')
        # notnull_dict(item['html'], dict_html_save, 'html')
        self.d_save.insert('t_bid_html', dict_html_save)
        self.d_save.commit_insert()

        print('数据保存成功')
        return item


    def close_spider(self,spider):
        self.d_save.close_db()
