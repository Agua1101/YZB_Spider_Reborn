import regex as re
from lxml import etree


class ContentSpecialEx():

    def __init__(self,url_tag=None,det_html=None,extra=None):
        self.url_tag = url_tag
        self.det_html = det_html
        self.extra = extra

    def special_ex(self):
        tag_dict = {'ggzyjy_sc':self.ggzyjy_sc,
                    }
        return tag_dict[self.url_tag]()


    def ggzyjy_sc(self):
        result_list = etree.HTML(self.det_html).xpath(f'//div[@id="tab-55{self.extra}"]//div[@class="clearfix"]//text()')
        print(result_list)
        return result_list