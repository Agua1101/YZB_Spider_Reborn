from lxml import etree
import sys





class UrlListEX():

    def __init__(self,url_tag=None,text=None):
        self.url_tag = url_tag
        self.text = text


    def url_ex(self):
        try:
            tag_dict = {'ggzyjy_gansu': self.ggzyjy_gansu,

                        }
            return tag_dict[self.url_tag]()
        except:
            return None

    def ggzyjy_gansu(self):
        url_list = etree.HTML(self.text).xpath('//div[@class="sTradingInformationSelectedBtoList"]//a/@onclick')
        title_list = etree.HTML(self.text).xpath(
            '//div[@class="sTradingInformationSelectedBtoList"]//a/text()')
        date_list = etree.HTML(self.text).xpath('//div[@class="sTradingInformationSelectedBtoList"]//i/text()')
        url_list = list(zip(url_list, title_list,date_list))
        return url_list