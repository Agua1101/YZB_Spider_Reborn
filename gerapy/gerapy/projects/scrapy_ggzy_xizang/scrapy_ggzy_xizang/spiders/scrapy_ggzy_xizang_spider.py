import json

import scrapy
import time
from datetime import datetime, date, timedelta
from yzb_tools.yzb_tag_extract import *
from ..items import ScrapyGgzyXizangItem
import yzb_ip_proxy


class ScrapyGgzyXizangSpider(scrapy.Spider):
    name = 'ccgp_gov_cn_spider'

    def __init__(self,name=None, **kwargs):
        kwargs.pop('_job')#删除job
        super(ScrapyGgzyXizangSpider, self).__init__(name, **kwargs)#对两个变量进行使用
        self.headers = {
                'Host': 'ggzy.xizang.gov.cn',
                'Referer': 'http://ggzy.xizang.gov.cn/jyxxzc_3.jhtml',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36',
            }
        self.url_tag = 'ggzy_xizang'

    def start_requests(self):
        for page in range(1,20):
            url = f'http://ggzy.xizang.gov.cn/jyxxzc_{page}.jhtml'

            yield scrapy.FormRequest(url=url, headers=self.headers, callback=self.list_parse,
                                     dont_filter=True)



    def list_parse(self, response):
        item = ScrapyGgzyXizangItem()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        text = response.text
        url_list = url_ex(text)
        for i in url_list:
            det_url = 'http://ggzy.xizang.gov.cn' + re.findall("window.open\('(.*?)'\)", i)[0]
            item['page_url'] = det_url
            yield item

            yield scrapy.Request(url=det_url,headers=headers,callback=self.page_parse)


    def page_parse(self,response):
        det_html = response.text
        det_url = response.url
        print(det_url,'det_url')

        project_num = re.findall('招标编号：(.*?)</p>', det_html)
        # print(project_num)
        path = etree.HTML(det_html).xpath('//li[@class="layui-this"]/@id')
        if project_num != []:
            project_num = project_num[0]
        if path != []:
            path = path[0]

        detail_url = 'http://ggzy.xizang.gov.cn/personalitySearch/initDetailbyProjectCode'
        data = {
            'path': path,
            'projectCode': project_num,
            'sId': 22
        }

        yield scrapy.Request(url=detail_url, headers=self.headers,body=json.dumps(data),method='POST', callback=self.save_parse)


    def save_parse(self,response):
        item = ScrapyGgzyXizangItem()
        detail = response.json()
        det_html = detail['data']['listData'][0]['txt']
        date = detail['data']['listData'][0]['publishTime']
        title = detail['data']['listData'][0]['title']

        item['title'] = title
        item['html'] = det_html
        item['date'] = date

        yield item
