from yzb_db_connect import *


class SavePart():

    def __init__(self, d_save=None, dict_url=None, dict_content=None, logger=logger, url_list=None, web_id=None):
        self.d_save = d_save
        self.dict_url = dict_url
        self.dict_content = dict_content
        self.logger = logger
        self.url_list = url_list
        self.web_id = web_id

    # 详情页url存储逻辑
    def url_save_part(self, det_url='', mission_id='', dict_url=None, web_table=None, page_id=None,extra=None):
        try:

            # print(id)
            notnull_dict(str(page_id), dict_url, 'id')
            notnull_dict(det_url, dict_url, 'page_url')
            notnull_dict(str(mission_id), dict_url, 'mission_id')
            if extra:
                notnull_dict(str(extra), dict_url, 'extra')
            try:
                # 在分表中去重，通过查询有没有
                count = self.d_save.select_where('count(*)', web_table, 'page_url=' + '"' + det_url + '"')[0][0]
                if not count:
                    # 在临时表中去重，存不进去会报错
                    self.d_save.insert('t_website_page', dict_url)
                    # self.d_save.commit_insert()
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
                return url_id
                # self.d_save.commit_insert()
        except:
            # logger.exception(sys.exc_info())
            self.logger.error(sys.exc_info())
            # print(e,'111111111')