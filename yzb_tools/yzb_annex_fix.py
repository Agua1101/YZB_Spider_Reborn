from lxml import etree
import regex as re
from bs4 import BeautifulSoup
import html as htmlpkg
import requests
import html
import random
import base64
from urllib.parse import urlencode
import sys
from datetime import datetime
import traceback

class AnnexFix():

    def __init__(self,det_html=None,tag_url=None,page_url=None,rtnv=None,extra=None):
        self.det_html = det_html
        self.tag_url = tag_url
        self.page_url = page_url
        self.rtnv = rtnv
        self.extra = extra


    # def __Buildcontent(self):




    def ccgp_jiangsu(self):
        if self.extra:
            annex_list = []
            for i in self.extra:
                name = i['name']
                url = i['url']
                a_tag = f'<a href="{url}">{name}</a>'
                annex_list.append(a_tag)
            annex_html = '\n'.join(annex_list)
            self.rtnv.append(annex_html)
            return ''.join(self.rtnv)
        else:
            return ''.join(self.rtnv)

    def hebei_file_ex_ding(self,list_a):
        # print(11111)
        # print(rtnv)
        # print(list_a)
        if list_a != ['']:
            self.rtnv.append(
                "<a href='http://www.ccgp-hebei.gov.cn/BidDingAnncFiles/" + list_a[2] + "." + list_a[
                    1] + "' download>" +
                list_a[0] + "</a><br />")
            print(list_a, 'annex_list')


    def hebei_file_ex_win(self,list_b):

        if list_b != ['']:
            # print(list_b, 'annex_list')
            file_name = list_b.pop()
            file_suffix = list_b.pop()
            file_display = list_b.pop()
            self.rtnv.append(
                "<a href='http://www.ccgp-hebei.gov.cn/BidWinAnncFiles/" + file_name + "." + file_suffix + "' download>" +
                file_display + "</a><br />")

    def hebei_file_ex_contract(self,list_b):
        if list_b != ['']:
            # print(list_b, 'annex_list')
            file_name = list_b.pop()
            file_suffix = list_b.pop()
            file_display = list_b.pop()
            self.rtnv.append(
                "<a href='http://www.ccgp-hebei.gov.cn/ContractAnncFiles/" + file_name + "." + file_suffix + "' download>" +
                file_display + "</a><br />")

    def ccgp_hebei(self):
        self.rtnv.append(
            '\n<script> \nvar amt=document.getElementById("amt").innerText;\nif(amt<0)\n  {\n     document.getElementById("gpamt").innerHTML="";\n  }\n</script>')
        self.rtnv.insert(0, '<body onload="content()">')
        script = etree.HTML(self.det_html).xpath('//head')
        # print(aaa,'aaa')
        for a in script:
            script_b_str = etree.tostring(a, encoding='utf-8')  # 规整html，输出二进制
            script_u_str = str(script_b_str, "utf-8")  # 转换成字符串
            # print(script_u_str,'script_u_str')
            # script_u_str.replace('../../../../..','http://www.ccgp-hebei.gov.cn')
            script_u_str = re.sub('\.\./\.\./\.\./\.\./\.\.','http://www.ccgp-hebei.gov.cn',script_u_str)
            script_u_str = html.unescape(script_u_str)
            # print(type(a),'aaaaaaaaa')
            self.rtnv.insert(0, script_u_str)

        annex_direct = etree.HTML(self.det_html).xpath('//span[@id="fujian"]/text()')
        # print(annex_direct)
        # print(''.join(annex_direct),'xxxxx')
        # print(re.search('^\s+$',''.join(annex_direct)))
        if annex_direct and not re.search('^\s+$',''.join(annex_direct)):
            # print(111111111)
            list_file = ''.join(annex_direct[0].split('#filename#')[1])
            list_ann = list_file.split('@_@')
            for i in list_ann:
                list_b = i.split('#_#')
                self.hebei_file_ex_contract(list_b)
            content = ''.join(self.rtnv)
            p_html = content.replace('<body>', '<body onload="content()">')
            return p_html


        annex_list = etree.HTML(self.det_html).xpath('//span[@id="con"]/text()')
        # print(annex_list,'annex_list')
        if annex_list:
            annex_str = ''.join(annex_list)
            if '#filename#' in annex_str and '#detail#' not in annex_str:
                # print(2222)
                annex_str = annex_str.split('#filename#')[1]
                print(annex_str,'xxxxxxxxxx')
                if annex_str != 'null':
                    if '@_@' in annex_str:
                        list_ann = annex_str.split('@_@')
                        for i in list_ann:
                            list_a = i.split('#_#')
                            self.hebei_file_ex_ding(list_a)
                    else:
                        # print(annex_str,'annex_str')
                        list_a = annex_str.split('#_#')
                        self.hebei_file_ex_ding(list_a)
            else:
                # print(33333)

                annex_str = ''.join(annex_list).split('#detail#')[1]
                # print(annex_str)
                if annex_str != 'null':
                    if '#filename#' not in annex_str:
                        if '@_@' in annex_str:
                            list_ann = annex_str.split('@_@')
                            for i in list_ann:
                                list_a = i.split('#_#')
                                self.hebei_file_ex_ding(list_a)
                        else:
                            print(annex_str,'annex_str')
                            list_a = annex_str.split('#_#')
                            self.hebei_file_ex_ding(list_a)

                    else:
                        list_file = ''.join(annex_str.split('#filename#')[1])
                        list_ann = list_file.split('@_@')
                        for i in list_ann:
                            list_b = i.split('#_#')
                            self.hebei_file_ex_win(list_b)

            # if '#filename#' not in annex_str:
            #     # print(rtnv)
            #     # print(list_a)
            #     self.rtnv.append(
            #         "<a id='files' href='http://www.ccgp-hebei.gov.cn/BidDingAnncFiles/" + list_a[2] + "." + list_a[1] + "'   class='blue' download>" +
            #         list_a[0] + "</a><br />")
            #     print(list_a, 'annex_list')
            # else:
            #     list_b = ''.join(annex_str.split('#filename#')[1])
            #     print(list_b)
            #     list_b = list_b.replace('@_@','').split('#_#')
            #     print(list_b, 'annex_list')
            #     file_name = list_b.pop()
            #     file_suffix = list_b.pop()
            #     file_display = list_b.pop()
            #     self.rtnv.append(
            #         "<a id='files' href='http://www.ccgp-hebei.gov.cn/BidWinAnncFiles/" + file_name + "." + file_suffix + "'   class='blue' download>" +
            #         file_display + "</a><br />")


        self.rtnv.insert(0, '</body>')
        content = ''.join(self.rtnv)
        # re.sub(etree.HTML(self.det_html).xpath('//span[@id="con"]/text()'),'',content)

        # ccc = re.findall('<table[\s\S]*bgcolor="#E4E4E4">[\s\S]*?</table>',content)

        # if ccc:
        #     content = re.sub(ccc[0],'',content)
        # content = re.sub('<table[\s\S]*bgcolor="#bfdff1">[\s\S]*?</table>','',content)
        content = re.sub('<td[\s\S]*bgcolor="#EAEAEA">[\s\S]*?</td>','',content)
        content = re.sub('<form.*>[\s\S]*?</form>','',content)

        p_html = content.replace('<body>', '<body onload="content()">')
        # print(p_html,'p_html')
        return p_html

    def hnggzy(self):
        # print(self.det_html)
        # p_html = re.sub(r'<script.*"/>', '', content)
        annex_html = re.findall('<p><a.*</a><p>',self.det_html)
        print(annex_html,'annex_html')
        for i in annex_html:

            self.rtnv.append(i)
        content = ''.join(self.rtnv)
        return content

    def jxsggzy_cn(self):
        # 添加附件
        annex_html = etree.HTML(self.det_html).xpath('//div[@class="con attach"]')
        if annex_html:
            script_b_str = etree.tostring(annex_html[0], encoding='utf-8')  # 规整html，输出二进制
            script_u_str = str(script_b_str, "utf-8")  # 转换成字符串
            self.rtnv.append(script_u_str)
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            if a.get('href'):
                a['href'] = 'https://www.jxsggzy.cn' + a['href']
        content = htmlpkg.unescape(str(soup))
        # 去除正文中蓝色按钮
        # content = ''.join(self.rtnv)
        dirt_text = re.findall(r'<div style="width: 300px; margin-left:.*</a></div>', content, re.S | re.M)
        print(dirt_text, 'hhhhhhhhhhhhhhh')
        if dirt_text:
            dirt_text = dirt_text[0]
        else:
            return content
        # print(dirt_text,'aaaaaaaaaaa')
        p_html = content.replace(dirt_text, '')
        return p_html

    def ccgp_jiangxi(self):
        annex_html = etree.HTML(self.det_html).xpath('//div[@class="con attach"]')
        # print(annex_html,'a_html')
        if annex_html:
            script_b_str = etree.tostring(annex_html[0], encoding='utf-8')  # 规整html，输出二进制
            script_u_str = str(script_b_str, "utf-8")  # 转换成字符串
            self.rtnv.append(script_u_str)
        content = ''.join(self.rtnv)
        # print(content,'a_content')
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            if a.get('href'):
                a['href'] = 'http://www.ccgp-jiangxi.gov.cn' + a['href']
        return htmlpkg.unescape(str(soup))

    def ccgp_beijing(self):
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            url_split = self.page_url.split('/')
            url_split.pop()
            url_end = '/'.join(url_split)
            # print(a['href'],type(a['href']))
            a['href'] = a['href'].replace('.', url_end, 1)
            # print(a['href'],'xxxxx')
        # print(type(soup),'soup')
        # rtnv.append(htmlpkg.unescape(str(soup)))
        return htmlpkg.unescape(str(soup))

    def ccgp_liaoning(self):
        # 正确显示文章内容
        content = ''.join(self.rtnv)
        first_html = re.sub(r'style="display:none', 'style="display:block', content, re.S | re.M)
        second_html = re.sub(r'charset=gb2312', 'charset=utf-8', first_html, re.S | re.M)



        return second_html

    def yngp(self):
        try:
            # id_list = re.findall('bulletin_id=(.*)',self.page_url)
            # id = id_list[0] if id_list != [] else None
            #
            # file_url = 'http://www.yngp.com/filemanager.do?method=listnew&business_id=2000&pk_id='+str(id)+'&candel=0&flag=1'
            # # print(id,'id')
            # # print(file_url)
            #
            # headers = {
            #     # 'Cookie': 'xincaigou = 49737.2912.1072.0000;JSESSIONID = 6nPC_Xq29yaJn7eLW4jw7ExWf6lF5aJB0cz2HG_yN_BvbFusGEz3!-529845575',
            #     # 'Referer': 'http: // www.yngp.com / newbulletin_zz.do?method = preinsertgomodify & operator_state = 1 & flag = view & bulletin_id = -73be511b.174c007052c. - 7b28',
            #
            # }
            # user_agent_list = [
            #     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            #     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            #     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            #     "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            #     "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
            # ]
            # headers['User-Agent'] = random.choice(user_agent_list)
            #
            # data = {
            #     'current': '1',
            #     'rowCount': '50',
            #     'searchPhrase':'',
            # }
            # file_json = requests.post(url=file_url, data=data, headers=headers, verify=False).json()
            # # print(file_json['rows'],'file_json')
            # # print(1111111111)
            # if file_json['rows'] != []:
            #     # print('111111111')
            #     file_id = file_json['rows'][0]['file_id']
            #     data_file_name = file_json['rows'][0]['file_name']
            #     data_completeurl = file_json['rows'][0]['completeurl']
            #     url_en = urlencode({'file_id':file_id.encode('utf8'),'file_name':data_file_name.encode('gbk'),'completeurl':data_completeurl.encode('utf8')})
            #     # print(url_en)
            #     # print(file_id,data_file_name,data_completeurl,'xxxxx')
            #     download_file = 'http://www.yngp.com/filemanager.do?method=downloadFile&'+str(url_en)
            #     print(download_file)
            #     file_html = '<a href="{}">{}</a>'.format(download_file,str(data_file_name))
            #     self.rtnv.append(file_html)
                content = ''.join(self.rtnv)

                first_html = re.sub(r'display: none', 'display: block', content, re.S | re.M)
                return first_html
        except:
            print(sys.exc_info())
            return

    def ccgp_shandong(self):
        # 去除山东政府采购网的图片和
        content = ''.join(self.rtnv)
        p_html = re.sub(r'<img .*/>', '', content, re.S | re.M)
        clean_html = re.sub(r'<td .* class="Font16White".*>.*</td>', '', p_html, re.S | re.M)

        return clean_html

    def hngp_gov(self):
        headers = {}
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
        ]
        headers['User-Agent'] = random.choice(user_agent_list)
        det_html = requests.get(self.page_url, headers=headers, verify=False).content.decode('utf-8')
        det_html_out = html.unescape(det_html)

        annex_html = etree.HTML(det_html_out).xpath('//div[@class="List1 Top5"]')
        if annex_html:
            script_b_str = etree.tostring(annex_html[0], encoding='utf-8')  # 规整html，输出二进制
            script_u_str = str(script_b_str, "utf-8")  # 转换成字符串
            self.rtnv.append(script_u_str)
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            a['href'] = 'http://www.ccgp-jiangxi.gov.cn' + a['href']
        return htmlpkg.unescape(str(soup))

    def ccgp_hainan(self):
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):

            a['href'] = 'https://www.ccgp-hainan.gov.cn' + a['href']

        return htmlpkg.unescape(str(soup))


    def ccgp_hubei(self):
        annex_html = etree.HTML(self.det_html).xpath('//ul[@class="list-unstyled details-ul"]')
        if annex_html:
            script_b_str = etree.tostring(annex_html[0], encoding='utf-8')  # 规整html，输出二进制
            script_u_str = str(script_b_str, "utf-8")  # 转换成字符串
            self.rtnv.append(script_u_str)

        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            print(a['href'],'aaaaa')
            if a['href']:
                file_code = re.findall('encodeBase64\(\'(.+)\'\)',a['href'])[0]

                file = base64.b64encode(file_code.encode('utf-8')).decode()
                # print(file,'file')
                a['href'] = 'http://www.ccgp-hubei.gov.cn:8090/gpmispub/download?id=' + file

        return htmlpkg.unescape(str(soup))
        # return content

    def ccgp_sichuan(self):
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            if a['href'].startswith('/'):
                a['href'] = 'http://www.ccgp-sichuan.gov.cn' + a['href']

        return htmlpkg.unescape(str(soup))

    def ccgp_guizhou(self):
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            a['href'] = 'http://www.ccgp-guizhou.gov.cn' + a['href']

        return htmlpkg.unescape(str(soup))

    def ccgp_shaanxi(self):
        annex_html = etree.HTML(self.det_html).xpath('//div[@class="content-inner"]')
        if len(annex_html) >1 :
            script_b_str = etree.tostring(annex_html[1], encoding='utf-8')  # 规整html，输出二进制
            script_u_str = str(script_b_str, "utf-8")  # 转换成字符串
            self.rtnv.append(script_u_str)

        content = ''.join(self.rtnv)
        return content

    def txzb_miit_gov_cn(self):
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            a['href'] = 'http://txzb.miit.gov.cn' + a['href']

        return htmlpkg.unescape(str(soup))

    def bgpc_beijing_gov_cn(self):
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            if a.get('href') and a['href'].startswith('/'):
                print(a['href'])
            # print(a)
                a['href'] = 'http://bgpc.beijing.gov.cn' + a['href']

        return htmlpkg.unescape(str(soup))


    def bcactc(self):
        content = ''.join(self.rtnv)
        script_html = re.sub('<script language="javacript" src=".*type="text/javascript"/>','<script src="http://file.bcactc.com/FileInterface/Filelist.ashx?projectid=8a8083997491c8c70174b3ac920d721d&node=zbgg" ></script>',content)

        # print(script_html,'annex_html')

        return script_html

    def kfqgw_beijing(self):
        annex_html = etree.HTML(self.det_html).xpath('//div[@class="fujian"]')
        if len(annex_html) >=1 :
            script_b_str = etree.tostring(annex_html[0], encoding='utf-8')  # 规整html，输出二进制
            script_u_str = str(script_b_str, "utf-8")  # 转换成字符串
            # print(script_u_str)
            self.rtnv.append(script_u_str)
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            if a.get('href') and a['href'].startswith(r'./'):
                # print(a['href'])
                # print(a)
                page_list = self.page_url.split('/')
                page_list.pop()
                page_url_end = '/'.join(page_list)


                a['href'] = a['href'].replace('.',page_url_end,1)

        return htmlpkg.unescape(str(soup))


    def ccgp_tianjin(self):
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            if a.get('href') and a['href'].startswith('/'):
                print(a['href'])
                # print(a)
                a['href'] = 'http://tjgp.cz.tj.gov.cn' + a['href']

        return htmlpkg.unescape(str(soup))

    def gdgpo_gov(self):
        content = ''.join(self.rtnv)
        annex_html = etree.HTML(self.det_html).xpath('//a[contains(text(),".pdf")]|//a[contains(text(),".doc")]')[0]
        # print(annex_html,'annex_html')
        b_str = etree.tostring(annex_html, method="html", encoding='utf-8')  # 规整html，输出二进制
        u_str = str(b_str, "utf-8")  # 转换成字符串
        # print(u_str,'annex_html',type(u_str))



        return content + u_str

    def ccgp_shanxi(self):
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            a['href'] = 'http://www.ccgp-shanxi.gov.cn/' + a['href']

        return htmlpkg.unescape(str(soup))

    def ccgp_dalian(self):
        try:
            # print(111111111111111111111)
            content = ''.join(self.rtnv)
            soup = BeautifulSoup(content)
            for a in soup.findAll('a'):
                a['href'] = 'http://ccgp-dalian.gov.cn/' + a['href']
            # print(str(soup),'souppppppppppppppppp')
            return htmlpkg.unescape(str(soup))
        except:
            return ''.join(self.rtnv)

    def ccgp_chongqing(self):
        # print(self.det_html)
        try:
            try:
                with open(r'/bid/crawler/tools_monitor/cq_Intention.html','r',encoding='utf-8') as r:
                    cq_html = r.read()
                    # print(cq_html)
                    # print(111111111)
            except Exception as e:
                print(e)
                cq_html = ''
            title = self.det_html['title']
            # print(title,'ssssssssss')
            cq_html = re.sub('@title@',title,cq_html)
            # cq_html.replace('@title@',title)
            n = 0
            table_tr_model = '\n<tr><td align="center">xuhao</td><td align="center">mingcheng</td><td align="center">depict</td><td align="center">money</td><td align="center">expectTime</td><td align="center">remarks</td></tr>'
            for det_in in self.det_html['intentionDetaileList']:
                n += 1
                mingcheng = det_in['title']
                depict = det_in['depict']
                money = det_in['money']
                expectTime_stramp = str(det_in['expectTime']).replace('000','')
                dateArray = datetime.fromtimestamp(int(expectTime_stramp))
                otherStyleTime = dateArray.strftime("%Y-%m:")
                expectTime = otherStyleTime.replace('-','年').replace(':','月')
                remarks = det_in['remarks'] if det_in['remarks'] else '--'
                table_tr = table_tr_model.replace('xuhao',str(n)).replace('mingcheng',mingcheng).replace('depict',depict).replace('money',str(money)).replace('expectTime',expectTime).replace('remarks',remarks)
                cq_html += table_tr
                # print(det_in)

            a = '    </tbody></table>'
            cq_html += a
            return cq_html
        except Exception as e:
            # print(e)
            print(traceback.format_exc())


    def zfcg_qingdao(self):
        import logging
        import json
        from ast import literal_eval
        try:
            content = ''.join(self.rtnv)
            annex_html = etree.HTML(self.det_html).xpath('//script[1]/text()')[0]
            # print(annex_html,'999999999999',type(annex_html))
            annex_str = annex_html.replace('var ids = ','').replace(';','').replace('[','',1).replace(']','',1)
            # print(annex_str,type(annex_str))
            if annex_str != '':
                annex_json = literal_eval(annex_str)
                # print(annex_json,type(annex_json))
                annex_text = annex_json[1]
                annex_id = annex_json[0]
                annex_html = '<a href="http://zfcg.qingdao.gov.cn/sdgp2014/servlet/attach?type=site&id={annex_id}" target="_blank">{annex_text}</a>'.format(annex_id=annex_id,annex_text=annex_text)
                content = content+annex_html
                return content
            else:
                return ''.join(self.rtnv)
        except Exception as e:
            logging.exception(e)
            return


    def ccgp_gov(self):
        try:
            content = ''.join(self.rtnv)


            soup = BeautifulSoup(self.det_html)
            for a in soup.find_all('a',attrs={"class":re.compile('bizDownload')}):

                id = a.get('id')

                a['href'] = 'http://www.ccgp.gov.cn/oss/download?uuid=' + str(id)

                print(a,'aaaaaaaaaaaa')

                content = content+str(a)
            # print(content, '------------content-------------')

            return content
        except Exception as e:
            sys.exc_traceback(e)
            return

    def ccgp_intention(self):
        content = ''.join(self.rtnv)
        soup = BeautifulSoup(content)
        for a in soup.findAll('a'):
            a['href'] = 'http://cgyx.ccgp.gov.cn' + a['href']

        return htmlpkg.unescape(str(soup))



    # 主程序
    def main(self):
        # try:
            # 河北省政府采购网
            if self.tag_url == 'ccgp-hebei.gov.cn':
                return self.ccgp_hebei()

            # 河南省公共资源交易中心门户网
            elif self.tag_url == 'hnggzy':
                return self.hnggzy()

            # 江西公共资源交易网
            elif self.tag_url == 'jxsggzy.cn':
                return self.jxsggzy_cn()
            # 江西省政府采购网
            elif self.tag_url == 'ccgp-jiangxi.gov.cn':
                return self.ccgp_jiangxi()

            elif self.tag_url == 'hngp.gov.cn':
                return self.hngp_gov()

            # 北京市政府采购网
            elif self.tag_url == 'ccgp-beijing.gov.cn/':
                return self.ccgp_beijing()

            elif self.tag_url == 'ccgp-liaoning':
                return self.ccgp_liaoning()

            elif self.tag_url == 'yngp':
                return self.yngp()

            elif self.tag_url == 'ccgp-shandong':
                return self.ccgp_shandong()

            elif self.tag_url == 'ccgp-hainan.gov.cn':
                return self.ccgp_hainan()

            elif self.tag_url == 'ccgp-hubei':
                return self.ccgp_hubei()

            elif self.tag_url == 'ccgp-sichuan':
                return self.ccgp_sichuan()

            # elif self.tag_url == 'ccgp-guizhou':
            #     return self.ccgp_guizhou()

            elif self.tag_url == 'ccgp-shaanxi':
                return self.ccgp_shaanxi()

            elif self.tag_url == 'http://txzb.miit.gov.cn/':
                return self.txzb_miit_gov_cn()

            elif self.tag_url == 'bgpc.beijing.gov.cn':
                return self.bgpc_beijing_gov_cn()

            elif self.tag_url == 'www.bcactc.com':
                return self.bcactc()

            elif self.tag_url == 'kfqgw.beijing.gov.cn':
                return self.kfqgw_beijing()

            elif self.tag_url == 'ccgp-tianjin':
                return self.ccgp_tianjin()

            # elif self.tag_url == 'gdgpo.gov':
                # return self.gdgpo_gov()
            elif self.tag_url == 'ccgp-shanxi':
                return self.ccgp_shanxi()

            elif self.tag_url == 'ccgp-dalian':
                return self.ccgp_dalian()

            elif self.tag_url == 'ccgp-chongqing_intention':
                return self.ccgp_chongqing()
            elif self.tag_url == 'zfcg_qingdao':
                return self.zfcg_qingdao()
            elif self.tag_url == 'ccgp.gov.cn':
                return self.ccgp_gov()
            elif self.tag_url == 'ccgp-jiangsu':
                return self.ccgp_jiangsu()
            elif self.tag_url == 'ccgp_intention':
                return self.ccgp_intention()

            else:
                return ''.join(self.rtnv)
        # except:
        #     print(sys.exc_info())
        #     return