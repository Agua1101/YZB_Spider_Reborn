import scrapy
import time
from datetime import datetime, date, timedelta
from yzb_tools.yzb_tag_extract import *
from ..items import CcgpGovCnItem
import yzb_ip_proxy


class CcgpGovCnSpiderSpider(scrapy.Spider):
    name = 'ccgp_gov_cn_spider'

    def __init__(self):
        super().__init__()
        self.headers = {
            # 'Cookie': 'JSESSIONID=EgPd86-6id_etA2QDV31Kks3FrNs-4gwHMoSmEZvnEktWIakHbV3!354619916; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; td_cookie=2144571454; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1545611064,1545618402,1545618414; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1545618495',
            'Cookie': 'Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1657159792; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1658819877; JSESSIONID=O4I50r8VN81k8-VOQ_PueAuF1NDX2xOBJHgSvSe-rDpQYgd7UQ-e!1179140079; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1658827822; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1658827872',
            'Host': 'search.ccgp.gov.cn',
            # 'referer': 'https://search.ccgp.gov.cn/bxsearch',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.8 Safari/537.36',
            'keep-alive':'False',
        }
        self.url_tag = 'ccgp.gov.cn'


    def get_date(self):
        year = time.strftime('%Y', time.localtime(time.time()))
        today = time.strftime(':%m:%d', time.localtime(time.time()))
        yesterday = (date.today() + timedelta(days=-1)).strftime(":%m:%d")

        start_time = str(year) + yesterday
        end_time = str(year) + today

        return start_time,end_time

    def start_requests(self):
        url = 'http://search.ccgp.gov.cn/bxsearch'


        start_time, end_time = self.get_date()
        for i in range(1,10):
            params = {
                'searchtype': '1',
                'page_index': str(i),
                'bidSort': '0',
                'pinMu': '0',
                'bidType': '0',
                'kw': '',
                'start_time': '2022:08:02',
                'end_time': '2022:08:02',
                'timeType': '6'
            }
            # headers = {
            #     'Cookie': 'JSESSIONID=EgPd86-6id_etA2QDV31Kks3FrNs-4gwHMoSmEZvnEktWIakHbV3!354619916; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1545618390; td_cookie=2144571454; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1545611064,1545618402,1545618414; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1545618495',
            #     # 'Cookie': 'UM_distinctid=16b882cb78b7f6-04ea86bf03217f-5a40201d-1fa400-16b882cb78c990; Hm_lvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1569467097,1569476101,1569479884,1569479974; Hm_lpvt_9f8bda7a6bb3d1d7a9c7196bfed609b5=1569480034; JSESSIONID=231sWvpmQV90biZXbmgczIedW5cI-y7ummVBIoxhOFix7JPNySGz!-1490526721; Hm_lvt_9459d8c503dd3c37b526898ff5aacadd=1569399637,1569400221,1569476103,1569480964; Hm_lpvt_9459d8c503dd3c37b526898ff5aacadd=1569481021',
            #     'Host': 'search.ccgp.gov.cn',
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3141.8 Safari/537.36'
            # }


            yield scrapy.FormRequest(url=url, headers=self.headers, formdata=params,callback=self.list_parse,dont_filter=True,)



    def list_parse(self, response):
        item = CcgpGovCnItem()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
        }
        url_list = response.xpath('//ul[@class="vT-srch-result-list-bid"]//a/@href').getall()
        for det_url in url_list:
            if det_url.startswith('http'):
                print(det_url)
                item['page_url'] = det_url

                yield scrapy.Request(url=det_url,headers=headers,callback=self.page_parse)


    def page_parse(self,response):
        item = CcgpGovCnItem()

        det_html = response.text
        det_url = response.url
        print(det_url,'det_url')

        # html = content_html_ex(det_html,self.url_tag,det_url)
        # print(det_html,'html')

        title = title_ex_total('', det_html)
        print(title,'title')
        date = date_ex(det_html, '')
        print(date,'date')

        item['title'] = title
        item['html'] = det_html
        item['date'] = date
        item['page_url'] = det_url


        yield item




