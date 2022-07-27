from lxml import etree
import regex as re


class WinningBidderEx():

    def __init__(self,html=None,url_tag=None,i=None,n=None):
        self.html = html
        self.url_tag = url_tag
        self.i = i
        self.n = n

    def wb_ex(self):
        try:
            tag_dict = {'ccgp-gansu': self.gansu,'ccgp.gov.cn':self.ccgp_gov,'ccgp-hunan':self.ccgp_hunan,
                        'ccgp-chongqing':self.ccgp_chongqing,'ccgp-hebei.gov.cn':self.ccgp_hebei}
            return tag_dict[self.url_tag]()
        except Exception as e:
            # print(e,'xxxxssssss')
            return None,0

    # 甘肃省政府采购网
    def gansu(self):
        aa = etree.HTML(self.html).xpath('//table[@class="MsoTableGrid"][1]//tr[1]//th[{}]//text() | //table[@class="MsoTableGrid"][1]//tr[{}]//td[{}]//text()'.format(str(self.n),str(self.i),str(self.n)))
        return aa,0

    # 中国政府采购网
    def ccgp_gov(self):
        aa = etree.HTML(self.html).xpath('//div[@class="vF_detail_content"]//table[1]//tr[1]//th[{}]//text() | //div[@class="vF_detail_content"]//table[1]//tr[{}]//td[{}]//text()'.format(str(self.n),str(self.i),str(self.n)))
        return aa,0

    # 湖南政府采购网
    def ccgp_hunan(self):
        aa = etree.HTML(self.html).xpath(
            '//table//table[@class="table"][2]//tr[1]//th[{}]//text() | //table//table[@class="table"][2]//tr[{}]//td[{}]//text()'.format(
                str(self.n), str(self.i), str(self.n)))
        return aa,0

    # 重庆政府采购网
    def ccgp_chongqing(self):

        aa = etree.HTML(self.html).xpath(
            '//table[@class="table"]//th[{}]//text() | //table[@class="table"]//tr[{}]//td[{}]//text()'.format(
                str(self.n), str(self.i), str(self.n)))
        # print(aa,'1111111111')
        return aa,0

    # 河北省政府采购网
    def ccgp_hebei(self):
        con = etree.HTML(self.html).xpath('//span[@id="con"]/text()')[0]
        # print(con,'tttttttt')


        con_list = con.split('#_@_@')
        # print(con_list)

        for i in con_list:
            if re.match('[\u4e00-\u9fa5]',i):
                # print(i,'ddddddddddddd')
                return '中标供应商'+ i,2

    # 公共资源交易中心
    def ggzy_gov(self):
        aa = etree.HTML(self.html).xpath(
            '//table//table[@class="table"][2]//tr[1]//th[{}]//text() | //table//table[@class="table"][2]//tr[{}]//td[{}]//text()'.format(
                str(self.n), str(self.i), str(self.n)))
        return aa, 0