#coding=UTF-8
from lxml import etree
import regex as re
import html as htmlpkg
import datetime
import time
# from items_table import *
import decimal
from yzb_conf import config as conf
from functools import reduce
from yzb_local_dict import local_dict
from pyhanlp import *
from yzb_db_connect import *
from yzb_get_dict_id import Dictionary
from yzb_tag_address import tag_address
from bs4 import BeautifulSoup
from html import unescape
import yzb_annex_fix
import yzb_project_code_ex
import yzb_win_bidder_ex
import yzb_project_id_ex
import yzb_url_list_ex
# from tools_monitor import content_special_ex as cse
from functools import reduce
import yzb_TextPreprocessing
import yzb_EX_Text

local_dic = local_dict()
gzcq, fblb, zhongbgg, cjgg, xqgg, tpgg, csgg, yqzbgg, xjgg, dylygs, zgys, zhaobgg, qtgs, qtgg, dyly, xj, jzxtp, jzxcs, yqzb, gkzb, qtcg, cgyx,htgg,ggfuxmys= Dictionary.dictionary()
# gzcq, fblb, zhongbgg, cjgg, xqgg, tpgg, csgg, yqzbgg, xjgg, dylygs, zgys, zhaobgg, qtgs, qtgg, dyly, xj, jzxtp, jzxcs, yqzb, gkzb, qtcg, cgyx = 1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,6,7,8,9,0,1,2

'''
(公共服务项目验收|补遗|更正通知|变更通知|更正公告|变更公告|补充公告|延期公告|澄清通知|澄清公告|废标公告|流标公告|废标|流标|未成交公告|异常公告|终止公告|中标公告|中标结果公示|中标结果|合同|成交公告|采购结果公告|成交结果公告|结果公告|需求公告|采购意向|意向公示|意向公开|竞争性谈判|竞争性磋商|邀请招标|询价|单一来源公示|资格预审|公开招标|采购公告|招标公告)
'''

wei = {}
wei["公共服务项目验收"] = (ggfuxmys, 1)
wei["补遗"] = (gzcq, 1)
wei["更正通知"] = (gzcq, 1)
wei["变更通知"] = (gzcq, 1)
wei["更正公告"] = (gzcq, 1)
wei["变更公告"] = (gzcq, 1)
wei["补充公告"] = (gzcq, 1)
wei["延期公告"] = (gzcq, 1)
wei["澄清通知"] = (gzcq, 1)
wei["澄清公告"] = (gzcq, 1)
wei["废标公告"] = (fblb, 1)
wei["流标公告"] = (fblb, 1)
wei["废标"] = (fblb, 1)
wei["流标"] = (fblb, 1)
wei["未成交公告"] = (fblb, 1)
wei["异常公告"] = (fblb, 1)
wei["终止公告"] = (fblb, 1)
wei["中标公告(?!截图|地址|标题|\s)"] = (zhongbgg, 1)
wei["中标结果公示"] = (zhongbgg, 1)
wei["中标结果"] = (zhongbgg, 1)
wei["合同(?!履行期限)"] = (htgg, 1)
wei["成交公告"] = (cjgg, 1)
wei["采购结果公告"] = (cjgg, 1)
wei["成交结果公告"] = (cjgg, 1)
wei["结果公告"] = (cjgg, 1)
wei["需求公告"] = (xqgg, 1)
wei["采购意向"] = (cgyx, 1)
wei["意向公示"] = (cgyx, 1)
wei["意向公开"] = (cgyx, 1)
wei["竞争性谈判"] = (tpgg, 2)
wei["竞争性磋商"] = (csgg, 2)
wei["邀请招标"] = (yqzbgg, 2)
wei["询价"] = (xjgg, 2)
wei["单一来源公示"] = (dylygs, 2)
wei["资格预审"] = (zgys, 2)
wei["公开招标"] = (zhaobgg, 3)
wei["采购公告"] = (zhaobgg, 3)
wei["招标公告"] = (zhaobgg, 3)
wei["公示"] = (qtgs, 4)
wei["公告|质疑答复函"] = (qtgg, 4)


meth = {}
meth["单一来源采购"] = dyly
meth["询价"] = xj
meth["竞争性谈判"] = jzxtp
meth["竞争性磋商"] = jzxcs
meth["磋商"] = jzxcs
meth["邀请招标"] = yqzb
meth["公开招标"] = gkzb
meth["招标公告"] = gkzb
meth["其他采购方式"] = qtcg
meth["废标公告"] = qtcg
meth["终止公告"] = qtcg
meth["流标公告"] = qtcg
meth["征求意见公告"] = qtcg







words = ["招标代理人：","经办人：","予以公示","评审部经办人","发布时间","采购预算：","组织机构代码","数量","排名","项目名称：","投标人","合同包\d","采购项目","采购数量","项目简介：","联系","序号","变更内容：","电子信箱","招标项目概况","二、","附件：","地\s*址","开户行","邮\s*编","联\s*系\s*人", "受理质疑电话","入围项目", "电话", "邮箱","邮\s*政\s*编\s*码","代理机构", "代理机构联系电话","发布人", "联系方式","项目名称", "项目联系人", "采购联系人", "项目编号", "采购编号", "采购人地址", "单位地址", "地址", "编号", "联系人",  "中标", "成交", "中选", "投标单位", "报价单位", "供应商", "采购人", "中标人", "招标人", "采购单位", "招标单位", "采购机构", "招标失败","操作指南", "宣告失败", "结果","登录", "中标候选人", "报价单位", "中标金额", "成交金额", "中标价格", "中标价", "成交价", "供应商名单", "中标供应商", "成交价格", "入围金额", "入围价格", "合同总金额", "合同金额", "最终报价", "投标报价", "报价", "费率", "投标人报价", "节支率", "浮动率", "投标单价", "废标",'情况', "公告","评审专家：","详细","^最终$","^信息$","传\s*真"]

name_words = ["详细","经办人：","评审部经办人","发布时间","采购预算：","采购项目","项目简介：","联系","变更内容：","电子信箱","招标项目概况","二、","附件：","地\s*址","开户行","邮\s*编","联\s*系\s*人", "受理质疑电话", "电话", "邮箱","邮\s*政\s*编\s*码","代理机构", "代理机构联系电话","发布人", "联系方式", "项目联系人", "采购联系人", "项目编号","项目名称", "采购编号", "采购人地址", "单位地址", "地址", "编号", "联系人",  "中标", "成交", "中选", "投标单位", "报价单位", "供应商", "采购人", "中标人", "招标人", "采购单位", "招标单位", "采购机构", "招标失败", "宣告失败", "结果", "中标候选人", "报价单位", "中标金额", "成交金额", "中标价格", "中标价", "成交价", "供应商名单", "中标供应商", "成交价格", "入围金额", "入围价格", "合同总金额", "合同金额", "最终报价", "投标报价", "报价", "费率", "投标人报价", "节支率", "浮动率", "投标单价", "废标", "公告","传真","^项目$",'地点','名称','情况']

title_words = ['变更内容：','[一二三四五六七八九十]、','[12345678]、']

package_class = ['第[一二三四五六七八九十]包','第[123456789]包','[A-Z一二三四五六七八九十]标段','已分包','标段[一二三四五六七八九十]','第[一二三四五六七八九十]标包','标段编号','合同包（[123456789]）','包[123456789]']



company = ''
ex_rule = {}
ex_rule['p_name_html'] = ['//p[@class="abc"]/text()']
ex_rule['p_name'] = ['项目名称(?:\s|{_})*(?:[：:]|{_}|[ ])+(?:\s|{_})*((?:[0-9-]{1,9}年|[一-龥])(?:(?!为)[一-龥#、.A-Z0-9—-]){2,40}(?:[“（(](?:(?!为)[一-龥#、.A-Z0-9—-]){2,40}[)）”](?:(?!为)[一-龥#、.A-Z0-9—-]){2,40})*(?<!项目名称.*?项目.*?)(?:项目|工程|工程类))']
ex_rule['p_name'].append('.*原公告项目名称：(.*?)2、原公告项目编号.*')
ex_rule['p_name'].append('.*项目名称：(.*?)2.\s* 采购编号：.*')
ex_rule['p_name'].append('.*项目名称：(.*?)项目联系人：.*联系方式:.*')
ex_rule['p_name'].append('.*项目名称：(.*?)采购联系人：.*联系方式:.*')
ex_rule['p_name'].append('.*项目名称：(.*?)2.项目编号：.*')
ex_rule['p_name'].append('.*项目名称：(.*?)采购项目编号.*')
ex_rule['p_name'].append('.*项目名称：(.*?)项目编号：.*')
ex_rule['p_name'].append('.*项目名称：(.*?)项目联系人：.*')
ex_rule['p_name'].append('.*项目名称：(.*?)项目登记号：.*')
ex_rule['p_name'].append('.*项目名称：(.*?)采购方式：.*')
ex_rule['p_name'].append('.*项目名称：(.*?)2、项目登记号：.*')
ex_rule['p_name'].append('.*项目名称：(.*?)2、项目编号：.*')
ex_rule['p_name'].append('.*项目名称：(.*?)4、采购结果如下.*')
ex_rule['p_name'].append('.*项目名称：(.*?)；\s*采购人（甲方）.*')
ex_rule['p_name'].append('.*项目名称：(.*?)二、采购方式：.*')
ex_rule['p_name'].append('.*项目名称：(.*?)[一二三四五六七八九]、.*')
ex_rule['p_name'].append('.*项目名称：(.*?)（[一二三四五六七八九]）.*')
ex_rule['p_name'].append('.*项目名称：(.*?)[123456789]、.*')
ex_rule['p_name'].append('.*项目名称:(.*?)标的名称:.*')
ex_rule['p_name'].append('.*采购项目名称(.*?)采购项目编号.*')
ex_rule['p_name'].append('.*项目名称(.*?)采购项目编号.*')
ex_rule['p_name'].append('.*项目名称(.*?)项目编号.*')
ex_rule['p_name'].append('.*项目名称(.*?)二、采购方式：.*')
ex_rule['p_name'].append('.*项目名称(.*?)采购人(甲方).*')
ex_rule['p_name'].append('.*招标项目名称(.*?)集中开标地点.*')
ex_rule['p_name'].append('.*招标项目名称：(.*?)集中开标地点.*')
ex_rule['p_name'].append('.*标的名称(.*?)项目编号.*')
ex_rule['p_name'].append('.*一、采购项目概况：.*项目名称：(.*?)预算金额：.*标的内容：.*')
ex_rule['p_name'].append('.*工程名称;(.*?)建设规模;.*')
ex_rule['p_name'].append('.*工程名称(.*?)建设地点.*')
ex_rule['p_name'].append('.*工程名称(.*?)开标时间.*')
ex_rule['p_name'].append('.*本招标项目为(.*?)[（、]招标编号：.*')
ex_rule['p_name'].append('.*1．招标条件(.*?)[（、]已批准.*')
ex_rule['p_name'].append('.*项目概况：(.*?)1.2招标内容：.*')
ex_rule['p_name'].append('.*公告名称：(.*?)采购人名称：.*')
ex_rule['p_name'].append('.*本招标项目(.*?)已由.*')
ex_rule['p_name'].append('.*建设项目(.*?)已由.*')
ex_rule['p_name'].append('.*文件标题(.*?)采购项目编号/包号.*')
# ex_rule['p_name'].append('.*项目名称：(.*?)项目编号：.*')
ex_rule['p_num'] = ['']
ex_rule['p_num'].append('(?:项目编号|项目编码|项目号|采购编号|标段编号|招标编号|标包编号|招标公告编号|采购代理编号|（采购计划编号）|采购任务编号|招标文件编号|采购项目文件编号|竞价编号)(?::|：|包号|为|\/|\s)*(.{0,64}?)(?:（第二次）|\s)*(?:（?(?:招标文件编号|采购人名称|采购执行编号|采购项目名称|项目联系方式|采购计划编号|项目联系人|预算金额|标段名称|采购形式|采购方式|中标单位|招标人|招标编号|项目名称|首次公告日期)|[一二三四五六七八九][、．]|\d[、.]|\s)')
ex_rule['p_num'].append('(?:工程编号)(?::|：|包号|为|\/|\s)*(.{0,64}?)(?:（第二次）|\s)*(?:（?(?:建设单位名称|建设单位名称|招标登记日期)|[一二三四五六七八九]、|\d、)')
ex_rule['p_num'].append('(?:项目编号（或招标编号、政府采购计划编号、采购计划备案文号等，如有）)(?::|：|包号|为|\/|\s)*(.{0,64}?)(?:（第二次）|\s)*(?:（?(?:招标文件编号|采购执行编号|采购项目名称|项目联系人)|[一二三四五六七八九]、|\d、)')
ex_rule['p_num'].append('(?:原公告的采购项目编号)(?::|：|包号|为|\/|\s)*(.{0,64}?)(?:（第二次）|\s)*(?:（?(?:原公告的采购项目名称|招标文件编号|采购执行编号|采购项目名称|项目联系人|预算金额)|[一二三四五六七八九]、|\d、)')
ex_rule['p_num'].append('(?:\(|（)(?:项目编号|项目编码|项目号|采购编号|招标编号|标包编号|招标公告编号|采购代理编号|（采购计划编号）|采购任务编号|招标文件编号|竞价编号)(?::|：|包号|为|\/|\s)*([^()（）]{0,64})(?:\)|）)')
# ex_rule['p_num'].append('.*原公告的采购项目编号：(.*?)原公告的采购项目：.*')
# ex_rule['p_num'].append('.*原公告的采购项目编号(.*?)原公告的采购项目名称.*')
# ex_rule['p_num'].append('.*采购项目编号（建议书编号）：(.*?)采购项目名称：.*')
# ex_rule['p_num'].append('.*采购项目标书编号：(.*?)采购人名称：.*')
# ex_rule['p_num'].append('.*采购项目编号：(.*?)三、项目预算金额.*')
# ex_rule['p_num'].append('.*采购项目编号：(.*?)采购项目名称：.*')
# ex_rule['p_num'].append('.*采购项目编号：(.*?)三、首次公告日期及发布媒介：.*')
# ex_rule['p_num'].append('.*采购项目编号：(.*?)三、采购项目用途.*')
# ex_rule['p_num'].append('.*采购项目编号：(.*?)三、采购公告发布日期.*')
# ex_rule['p_num'].append('.*采购项目编号（采购计划编号）：(.*?)三、首次公告日期：.*')
# ex_rule['p_num'].append('.*采购项目编号（采购计划编号）：(.*?)采购项目分包情况：.*')
# ex_rule['p_num'].append('.*采购项目编号（采购计划编号）：(.*?)[一二三四五六七八九]、.*')
# ex_rule['p_num'].append('.*采购项目编号/包号(.*?)采购人名称.*')
# ex_rule['p_num'].append('.*采购任务编号：(.*?)2、采购文件编号：.*')
# ex_rule['p_num'].append('.*项目序列号:(.*?)5、项目联系人:.*')
# ex_rule['p_num'].append('.*原公告项目编号：(.*?)3、首次公告日期：.*')
# ex_rule['p_num'].append('.*招标公告编号：(.*?)招标内容：.*')
# ex_rule['p_num'].append('.*招标公告编号：(.*?)）.*')
# ex_rule['p_num'].append('.*招标文件编号:(.*?)[123456789]、.*')
# ex_rule['p_num'].append('.*招标文件编号:(.*?)[123456789]、.*')
# ex_rule['p_num'].append('.*招标文件编号：(.*?)）.*')
# ex_rule['p_num'].append('.*招标文件编号：(.*?)[一二三四五六七八九]、.*')
# ex_rule['p_num'].append('.*1.2项目编号：(.*?)1.3项目预算：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)）.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)[123456789]、.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)[123456789]\..*')
# ex_rule['p_num'].append('.*项目编号：(.*?)[一二三四五六七八九]、.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)（[一二三四五六七八九]）.*')
# ex_rule['p_num'].append('.*项目编号：）(.*?)。因三家供应商.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)一、项目联系方式：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)项目联系方式：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)4、资金来源：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)2.3本项目标段划分及采购内容：.*')
# ex_rule['p_num'].append('.*项目编号：(\w{2}-\w{0,10}).*')
# ex_rule['p_num'].append('.*项目编号：(.*?)二、项目名称：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)二、包段划分.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)四、开标日期：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)项目名称：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)项目名称：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)采购人联系方式：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)招标编号：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)采购计划编号：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)中央国家机关政府采购中心对下列货物或服务进行公开招标.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)中央国家机关政府.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)查看需求公告.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)采购方式：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)本次变更涉及标包.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)信息来源：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)所属地区：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)采购人名称：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)招标条件.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)原公告日期：.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)单位地址:.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)二、.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)三、.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)四、.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)五、.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)六、.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)七、.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)八、.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)九、.*')
# ex_rule['p_num'].append('项目编号：(.*?)一、')
# ex_rule['p_num'].append('项目编号：(.*?)二、')
# ex_rule['p_num'].append('项目编号：(.*?)三、')
# ex_rule['p_num'].append('.*项目编号:(.*?)项目名称:.*')
# ex_rule['p_num'].append('.*项目编号:(.*?)项目联系人:.*')
# ex_rule['p_num'].append('.*项目编号:(.*?)一、.*')
# ex_rule['p_num'].append('.*项目编号:(.*?)二、.*')
# ex_rule['p_num'].append('.*项目编号:(.*?)[一二三四五六七八九]、.*')
# ex_rule['p_num'].append('.*项目编号:(.*?)[）,)].*')
# ex_rule['p_num'].append('.*项目编号(.*?)[一二三四五六七八九]、.*')
# ex_rule['p_num'].append('.*项目编号(.*?)挂牌起始.*')
# ex_rule['p_num'].append('.*项目编号(.*?)项目名称.*')
# ex_rule['p_num'].append('.*项目编号(.*?)谈判时间.*')
# ex_rule['p_num'].append('.*项目编号(.*?)采购方式.*')
# ex_rule['p_num'].append('.*项目编码：(.*?)项目名称：.*合同签订日期：.*')
# ex_rule['p_num'].append('.*采购编号：(.*?)文件号：.*')
# ex_rule['p_num'].append('.*采购编号：(.*?)评审日期：.*')
# ex_rule['p_num'].append('.*采购编号：(.*?)三、采购项目内容.*')
# ex_rule['p_num'].append('.*采购编号：(.*?)[）,\)].*')
# ex_rule['p_num'].append('.*采购编号：(.*?)一、.*')
# ex_rule['p_num'].append('.*采购编号：(.*?)二、.*')
# ex_rule['p_num'].append('.*采购编号：(.*?)三、.*')
# ex_rule['p_num'].append('.*采购编号：(.*?)项目名称：.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)2.2项目名称：.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)设备名称及数量.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)[（一）|（二）|（三）|（四）|（五）|（六）|（七）|（八）|（九）].*')
# ex_rule['p_num'].append('.*招标编号：(.*?)2.招标项目及范围.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)一、招标项目名称.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)二、项目名称：.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)2.招标项目内容：.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)1.招标条件.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)[）,\)].*')
# ex_rule['p_num'].append('.*招标编号：(.*?)2\.2.*')
# ex_rule['p_num'].append('.*招标编号（(.*?)[）,\)].*')
# ex_rule['p_num'].append('.*招标编号为(.*?)[）,\)].*')
# ex_rule['p_num'].append('.*招标编号：(.*?),招标人为.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)1\..*')
# ex_rule['p_num'].append('.*招标编号：(.*?)[一二三四五六七八九]、.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)[123456789]、.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)[123456789]\..*')
# ex_rule['p_num'].append('.*标包编号：(.*?)采购需求：.*')
# ex_rule['p_num'].append('.*项目登记号：(.*?)3、资金来源：.*')
# ex_rule['p_num'].append('.*项目编号(.*?)项目类型.*')
# ex_rule['p_num'].append('.*资格预审编号：(.*?)。2.2.*')
# ex_rule['p_num'].append('.*工程编号(.*?)招标登记日期.*')
# ex_rule['p_num'].append('.*工程编号(.*?)建设单位名称.*')
# ex_rule['p_num'].append('.*工程编号：(.*?)】.*')
# ex_rule['p_num'].append('.*招标编号：(.*?)\s.*')
# ex_rule['p_num'].append('.*招标公告(.*?)1.招标条件.*')
# ex_rule['p_num'].append('.*期数：(.*?)采购项目名称：.*')
# ex_rule['p_num'].append('.*采购文件编号：(.*?)2\.内容及分包情况.*')
# ex_rule['p_num'].append('.*采购文件编号：(.*?)2\..*')
# ex_rule['p_num'].append('.*采购文件编号：(.*?)\d、.*')
# ex_rule['p_num'].append('.*项目编号：(.*?)[）,\)].*')
# ex_rule['p_num'].append('.*编号：(.*?)[）,\)].*')
# ex_rule['p_num'].append('.*项目编[号码]：(.*?)项目联系人：.*')
# ex_rule['p_num'].append('[A-Z]{5}-\d{4}[A-Z]{2}\d{4}')
# ex_rule['p_num'].append('[a-zA-Z]{4}-\d{4}-\d{3}')
# ex_rule['p_num'].append('[a-zA-Z]{4}\d{18}')
# ex_rule['p_num'].append('[a-zA-Z]{4}\d{7}')
# ex_rule['p_num'].append('[a-zA-Z]{4}-[a-zA-Z]{2}-\d{4}-\d{4}')
# ex_rule['p_num'].append('[a-zA-Z]{4}-[a-zA-Z]{2}-\d{4}-\d{3}')
ex_rule['c_address'] = ['(?:招标人)(?::|：)(?:.*?)(?:招标代理机构)(?::|：)(?:.*?)(?:地址)(?::|：)(.*?)(?:地址)(?::|：)']
ex_rule['c_address'].append('(?:招标人)(?::|：)(?:.*?)(?:招标代理机构)(?::|：)(?:.*?)(?:地址)(?::|：)(.*?)(?:地址)(?::|：)')
ex_rule['c_address'].append('(?:采购单位|采购人信息名称)(?:.*?)(?:地\s*址)(?::|：)(.*?)(?:\d、|监管部门|联系方式|联系电话)(?:.*?)(?:集中采购机构|采购代理机构)')
ex_rule['c_address'].append('.*采购单位地址：(.*?)采购单位联系方式：.*')
ex_rule['c_address'].append('.*联系方式.*招标人：.*地址\(邮编\)(.*?)备注内容:.*否决投标单位及理由.*')
ex_rule['c_address'].append('.*采购单位地址：(.*?)三、采购项目名称：.*')
ex_rule['c_address'].append('.*采购单位地址：(.*?)评审专家：.*')
ex_rule['c_address'].append('.*单位地址:(.*?)开标时间：.*')
ex_rule['c_address'].append('.*采购中心地址：(.*?)邮政编码：.*')
ex_rule['c_address'].append('.*所属区域(.*?)所属行业.*')
ex_rule['c_address'].append('.*业主单位地址:(.*?)联系人：.*')
ex_rule['c_address'].append('.*招标（采购）人地址：(.*?)招标（采购）人联系方式：.*')
ex_rule['c_address'].append('.*采购人地址及联系方式：(.*?)；.*三、集中采购机构：.*')
ex_rule['c_address'].append('.*采购机构名称及联系方式：.*地址：(.*?)邮编：.*')
ex_rule['c_address'].append('.*采购人地址和联系方式.*地址：(.*?)联系电话：.*')
ex_rule['c_address'].append('.*采购人地址：(.*?)邮政编码：.*')
ex_rule['c_address'].append('.*采购人地址：(.*?)招标代理机构.*')
ex_rule['c_address'].append('.*采购人地址：(.*?)采购人联系方式：.*')
ex_rule['c_address'].append('.*采购人地址：(.*?)采购联系人：.*')
ex_rule['c_address'].append('.*采购人地址：(.*?)采购人邮编：.*采购人联系方式：.*')
ex_rule['c_address'].append('.*采购人地址：(.*?)采购人联系人：.*购人联系方式：.*')
ex_rule['c_address'].append('.*采购人地址：(.*?)联\s*系\s*人：.*采购代理机构.*')
ex_rule['c_address'].append('.*采购人地址：(.*?)4、联\s*系\s*电\s*话.*代理机构名称.*')
ex_rule['c_address'].append('.*采购人名称：.*采购人地址：(.*?)采购人联系方式：.*')
ex_rule['c_address'].append('.*采购人名称：.*详\s*细\s*地\s*址：(.*?)联\s*系\s*人：.*采购代理机构名称：.*')
ex_rule['c_address'].append('.*采购单位：.*地\s*址：(.*?)采购代理机构名称：.*')
ex_rule['c_address'].append('.*采购单位：.*地\s*址：(.*?)电\s*话：.*')
ex_rule['c_address'].append('.*投标报名地点(.*?)工程概况.*')
ex_rule['c_address'].append('.*招标人地址：(.*?)联\s*系\s*人：.*')
ex_rule['c_address'].append('.*招标人地址:(.*?)招标人联系方式:.*')
ex_rule['c_address'].append('.*招标人地址:(.*?)招标人联系：.*')
ex_rule['c_address'].append('.*采购单位联系方式：.*地\s*址：(.*?)联系方式：.*代理机构联系方式：.*')
ex_rule['c_address'].append('.*采购人名称：.*地\s*址：(.*?)项目联系人：.*采购代理机构名称：.*')
ex_rule['c_address'].append('.*采购人名称：.*地\s*址：(.*?)联\s*系\s*人.*采购代理机构名称：.*')
ex_rule['c_address'].append('.*采购人名称：.*地\s*址：(.*?)电\s*话.*采购代理机构.*')
ex_rule['c_address'].append('.*采购人名称:.*联系地址:(.*?)项目联系人:.*采购代理机构.*')
ex_rule['c_address'].append('.*采购人信息.*地\s*址:(.*?)联系方式:.*采购代理机构信息.*')
ex_rule['c_address'].append('.*采购人信息.*地\s*址:(.*?)项目联系人：.*采购代理机构信息.*')
ex_rule['c_address'].append('.*采购人信息.*地址：(.*?)传真：.*采购代理机构信息.*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址:(.*?)地\s*址[：:].*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)地\s*址[：:].*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)邮\s*编[：:].*招标代理机构[：:].*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)邮\s*编[：:].*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)电\s*话.*采购代理机构名称.*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)电\s*话.*代理机构名称.*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)电\s*话.*招标代理机构.*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)电\s*话.*招标代理.*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)电\s*话.*代理机构.*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*采购代理机构名称[：:].*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*采购代理机构.*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*招标代理机构.*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*招标代理.*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*代理机构.*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*招标代理机构.*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)采购代理机构名称[：:].*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)采购代理机构[：:].*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)招标代理机构[：:].*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)招标代理[：:].*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址[：:](.*?)代理机构[：:].*')
ex_rule['c_address'].append('.*招\s*标\s*人[：:].*地\s*址:(.*?)地\s*址:.*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)地\s*址[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*采购代理机构名称[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*采购代理机构[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*招标代理机构[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*招标代理[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*代理机构[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)联\s*系\s*人[：:].*供应商.*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)采购代理机构名称[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)采购代理机构[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)招标代理机构[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)招标代理[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)代理机构[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*地\s*址[：:](.*?)代理机构[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*联\s*系\s*地\s*址[：:](.*?)采购代理机构名称.*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*联\s*系\s*地\s*址[：:](.*?)采购代理机构.*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*联\s*系\s*地\s*址[：:](.*?)招标代理机构.*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*联\s*系\s*地\s*址[：:](.*?)招标代理.*')
ex_rule['c_address'].append('.*采\s*购\s*人[：:].*联\s*系\s*地\s*址[：:](.*?)代理机构.*')
ex_rule['c_address'].append('.*采\s*购\s*人.*地\s*址[：:](.*?)联\s*系\s*人[：:].*采购代理机构名称[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人.*地\s*址[：:](.*?)联\s*系\s*人[：:].*采购代理机构[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人.*地\s*址[：:](.*?)联\s*系\s*人[：:].*招标代理机构[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人.*地\s*址[：:](.*?)联\s*系\s*人[：:].*招标代理[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人.*地\s*址[：:](.*?)联\s*系\s*人[：:].*代理机构[：:].*')
ex_rule['c_address'].append('.*采\s*购\s*人.*地\s*址[：:](.*?)联\s*系\s*人[：:].*供应商.*')
ex_rule['c_address'].append('.*采购人信息.*地\s*址[：:](.*?)联系方式[：:].*采购代理机构信息.*')
ex_rule['c_address'].append('.*地\s*址[：:](.*?)邮\s*编[：:].*')
ex_rule['c_address'].append('.*单位地址;(.*?)单位性质;.*')
ex_rule['c_address'].append('.*单位地址(.*?)联系人.*')
ex_rule['c_address'].append('.*联系地址[：:](.*?)邮\s*箱.*')
ex_rule['c_address'].append('.*地\s*址[：:](.*?)邮\s*编[：:].*招标代理机构[：:].*')
ex_rule['c_address'].append('.*采购人名称:.*地\s*址:(.*?)联系电话:.*')
ex_rule['c_address'].append('.*送货地点[：:](.*?)联\s*系\s*电\s*话[：:].*')
ex_rule['c_address'].append('.*收货地点[：:](.*?)报价截止时间[：:].*')
# ex_rule['c_address'].append('.*地\s*址[：:](.*?)邮\s*编[：:].*')
# ex_rule['c_address'].append('.*地\s*址[：:](.*?)联系方式[：:].*')
# ex_rule['c_address'].append('.*地\s*址[：:](.*?)联系方法[：:].*')
# ex_rule['c_address'].append('.*地\s*址[：:](.*?)联\s*系\s*人[：:].*')
# ex_rule['c_address'].append('.*地\s*址[：:](.*?)地\s*址[：:].*')
# ex_rule['c_address'].append('.*地\s*址[：:](.*?)\s.*')
# ex_rule['c_address'].append('.*地\s*址[：:](.*?)地\s*址[：:].*')
ex_rule['c_address'].append('.*联系人及联系方式.*地址(.*?)地\s*址.*')
ex_rule['b_amount'] = {'thousand':['(?:本次招标项目计划投资|投资额及来源|采购预算控制价|预算总金额|项目总投资|本项目投资|采购控制价|合同估算价|项目规模|工程概算|项目概算|投资总额|招标规模|合计 预算|招标金额|项目预算|采购预算|预算金额|最高限价|预算资金|投资额|总预算|预算价)(?:：|:|标包【1_1】|\(招标控制价\)|人民币|金额|合计|为|约|￥|\s)*([\d,.]*?)(?:\s)*(?:[(（]?万元[)）]?|万)']}
ex_rule['b_amount']['thousand'].append('(?:本次招标项目计划投资|投资额及来源|采购预算控制价|预算总金额|项目总投资|本项目投资|采购控制价|合同估算价|项目规模|工程概算|项目概算|投资总额|招标规模|合计 预算|招标金额|项目预算|采购预算|预算金额|最高限价|预算资金|投资额|总预算|预算价)(?:：|:|标包【1_1】|\(招标控制价\)|人民币|金额|合计|为|约|￥|\s)*(万|万元|（万元）)(?:：|:|标包【1_1】|\(招标控制价\)|人民币|金额|合计|为|约|￥|\s)*([\d,.]*?)(?:[一二三四五六七八九十]、|\s)')
ex_rule['b_amount']['thousand'].append('.*本次招标预估采购金额约为\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算价及最高限价金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预估金额为\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*计划投资额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*资金自筹\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*自筹资金\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*自筹\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额（即最高投标限价）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：第[一二三四五六七八九]+标段：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额（元）：.{0,10}合计\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额（万元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*最高限价.*')
ex_rule['b_amount']['thousand'].append('.*预算金额（万元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*采用单一来源.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：最高\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：总预算\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额/?[：:]\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：\??\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*\(万元\).*')
ex_rule['b_amount']['thousand'].append('.*预算金额：\??\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元（人民币）.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[(（]万元[)）].*')
ex_rule['b_amount']['thousand'].append('.*预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*（万元\).*')
ex_rule['b_amount']['thousand'].append('.*预算金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：\?\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：约\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额（万元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[一二三四五六七八九]、.*')
ex_rule['b_amount']['thousand'].append('.*预算金额（万元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*采用单一来源.*')
ex_rule['b_amount']['thousand'].append('.*预算金额（人民币）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额\(招标控制价\)：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：本项目预算为\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额为\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算总金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算资金：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*投资额及来源(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)（万元）.*')
ex_rule['b_amount']['thousand'].append('.*小计(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)1.6 中标人数量：.*')
ex_rule['b_amount']['thousand'].append('.*本项目采购预算(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*本项目投资额：约(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*本项目投资(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*本项目投资约为(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*采购项目总预算\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*预算金额为：人民币(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万.*')
ex_rule['b_amount']['thousand'].append('.*项目规模：采购预算约为(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*项目预算：人民币(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*项目规模：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*项目预算：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*项目总投资：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*项目总投资\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*项目总投资为\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*项目预算及最高限价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*投资总额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*招标规模：约(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*招标规模：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*招标金额约\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*招标金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*招标金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*招标最高限价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*招标控制价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*评估价\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*招标总金额约\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*采购预算控制额度人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*采购预算控制额度\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*采购预算额度人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*采购预算额度\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*采购控制价为人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*采购项目预算：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*采购项目预算：人民币(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*采购预算（万元）(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)拟中标人.*')
ex_rule['b_amount']['thousand'].append('.*预算：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*采购预算：人民币(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*采购控制价：人民币(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*采购金额：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*采购预算：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*采购预算：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)（万元）.*')
ex_rule['b_amount']['thousand'].append('.*采购预算合计为(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*采购预算为(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*采购预算金额（人民币）：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
ex_rule['b_amount']['thousand'].append('.*工程概算：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*投资额\(万元\)( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)')
ex_rule['b_amount']['thousand'].append('.*总投资额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元')
ex_rule['b_amount']['thousand'].append('项目概算：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *|.*?)万元')
ex_rule['b_amount']['thousand'].append('项目估算投资：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *|.*?)万元')
ex_rule['b_amount']['thousand'].append('.*项目估算：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *|.*?)万元.*')
ex_rule['b_amount']['thousand'].append('.*合同估算价：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *|.*?)万元.*')
ex_rule['b_amount']['thousand'].append('.*合同估算价：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *|.*?)万.*')
ex_rule['b_amount']['thousand'].append('.*合同估算价( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *|.*?)（万元）')
ex_rule['b_amount']['thousand'].append('.*计划投资总额( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)（万元）')
ex_rule['b_amount']['thousand'].append('.*最高控制价为\s*(\d{1,5}.\d*)\s*万.*')
ex_rule['b_amount']['thousand'].append('.*最高投标限价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*最高限价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*最高限价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*\(万元\).*')
ex_rule['b_amount']['thousand'].append('.*总预算金额人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*[台约批]\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
# ex_rule['b_amount']['thousand'].append('.*万元.*[台约批]\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*.{1}.*')
ex_rule['b_amount']['thousand'].append('.*施工图审查费为\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount']['thousand'].append('.*项目预算\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*竞价要求.*')
ex_rule['b_amount']['thousand'].append('.*预算金额：\s*(.*)\s*万元.*')
# ex_rule['b_amount']['thousand'].append('.*\d\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
ex_rule['b_amount'].update({'normal':['(?:预算金额|预算总金额|项目预算|项目总预算|报价总金额|控制价合计|采购预算控制额度|招标控制价|控制价|招标规模|预算总价|采购预算金额|采购预算价|采购预算|采购项目预算|合同估算价|最高限价|总预算金额|上限价|投资总额)(?:（元）|\(元\)|[：:]|￥|约|总预算|[一二三四五六七八九]标段|（最高限价）|（元人民币）|（人民币）|人民币|第[一二三四五六七八九]包|（如有）|（小写）|[A-Z]分标)*(?:\s)*(\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d+[.,，]?\d+[.,，]?\d*)(?:\s)*(?:元|[一二三四五六七八九十]、)']})
ex_rule['b_amount']['normal'].append('.*项目预算：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)剩余时间：.*')
ex_rule['b_amount']['normal'].append('.*总预算金额\s*小写：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*投资总额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*项目总预算：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*项目预算\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额（最高限价）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额：一标段（进口）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*最高限价（元）.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*简要规格描述.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[\u4e00-\u9fa5].*')
ex_rule['b_amount']['normal'].append('.*项目预算（元）:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*参考品牌:.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*最高限价.*')
ex_rule['b_amount']['normal'].append('.*报价总金额：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)供应商报价详情.*')
ex_rule['b_amount']['normal'].append('.*控制价合计：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)元.*')
ex_rule['b_amount']['normal'].append('.*采购预算控制额度(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)元.*')
ex_rule['b_amount']['normal'].append('.*招标控制价(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)元.*')
ex_rule['b_amount']['normal'].append('.*控制价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*2.5招标范围：.*')
ex_rule['b_amount']['normal'].append('.*控制价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
# ex_rule['b_amount']['normal'].append('.*投标报价\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*招标规模：约\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*招标规模：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额：总预算\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*最高限价：.*')
ex_rule['b_amount']['normal'].append('.*预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*项目实施地点：.*')
ex_rule['b_amount']['normal'].append('.*预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*最高限价.*')
ex_rule['b_amount']['normal'].append('.*预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*（元）.*')
ex_rule['b_amount']['normal'].append('.*预算金额:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*（元）.*')
ex_rule['b_amount']['normal'].append('.*预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[\u4e00-\u9fa5].*')
ex_rule['b_amount']['normal'].append('.*预算金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[一二三四五六七八九十]、.*')
ex_rule['b_amount']['normal'].append('.*预算金额\(元\)：\s*(\d*|\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[\u4e00-\u9fa5].*')
ex_rule['b_amount']['normal'].append('.*预算总价\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算总金额（元）\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*（三）采购方式：.*')
ex_rule['b_amount']['normal'].append('.*预算总金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算总金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*（元）.*')
ex_rule['b_amount']['normal'].append('.*预算总金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[一二三四五六七八九十]、.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[一二三四五六七八九十]、.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*采购需求：.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*最高限价.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*最高限价.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*采购需求.*')
ex_rule['b_amount']['normal'].append('.*预算金额（人民币）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额：人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*项目预算（元）:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*是否允许提供进口产品:.*')
ex_rule['b_amount']['normal'].append('.*项目预算\(元\)\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*采购数量.*')
ex_rule['b_amount']['normal'].append('.*项目预算：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*项目预算为\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*项目预算第一包：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*采购预算控制额度：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*采购预算金额：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*采购预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*采购用途:.*')
ex_rule['b_amount']['normal'].append('.*采购预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*采购方式：.*')
ex_rule['b_amount']['normal'].append('.*采购预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*采购代理机构全称：.*')
ex_rule['b_amount']['normal'].append('.*采购预算价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*采购预算￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*\(元\).*')
ex_rule['b_amount']['normal'].append('.*采购预算：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*采购预算:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*采购预算.*人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*采购预算：人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*采购项目预算：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*合同估算价：人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*合同估算价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*最高限价（如有）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*最高限价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*本项目招标控制价为：.*总价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*本项目预算金额为\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('标段：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['b_amount']['normal'].append('.*[台约批]\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*人民币：元.*[台约批]\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*.{1}.*')
ex_rule['b_amount']['normal'].append('.*预算金额（元）.*招标文件\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*二、.*')
ex_rule['b_amount']['normal'].append('.*预算金额：A分标：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['b_amount']['normal'].append('.*预算金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*\d．.*')
ex_rule['b_amount']['normal'].append('.*预算金额：\s*(.*)\s*元.*')
ex_rule['b_amount'].update({'billion':['.*项目总投资(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)亿元.*']})
ex_rule['b_amount']['billion'].append('.*工程投资约\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*亿元.*')
ex_rule['b_amount']['billion'].append('.*工程投资\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*亿元.*')
ex_rule['b_amount']['billion'].append('.*约\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*亿元.*')
ex_rule['b_amount_h'] = {'thousand':['//p[@class="abc"]/text()']}
ex_rule['b_amount_h'].update({'normal':['//p[@class="16"]/span/text()']})
ex_rule['b_amount_h'].update({'billion':['//p[@class="def"]/text()']})
# ex_rule['b_amount_c'] = {'thousand':['.*合计人民币：(.*)万元.*']}
ex_rule['b_amount_c'] = {'normal':['.*项目预算：\s*(.*?)\s*元.*']}
ex_rule['b_amount_c'].update({'normal':['.*总预算价：(.*)元整.*']})
ex_rule['b_amount_c']['normal'].append('(?:预算金额)(?:[(（]大写[)）]|:|：|人民币)*(.*?)(?:圆整|元整|元)')
ex_rule['b_amount_c']['normal'].append('.*采购预算金额：.*大写：(.*?)元.*中标金额：.*')
ex_rule['b_amount_c']['normal'].append('.*采购预算：\s*(.*?)\s*圆整.*')
ex_rule['b_amount_c']['normal'].append('.*采购预算：\s*(.*?)\s*元整.*')
ex_rule['b_amount_c']['normal'].append('.*采购预算：\s*(.*?)\s*元.*')
ex_rule['b_amount_c']['normal'].append('.*合计人民币：(.*?)元.*')
ex_rule['b_amount_c']['normal'].append('.*采购控制总价：(.*?)圆整.*')
ex_rule['b_amount_c']['normal'].append('.*采购控制总价：(.*?)元整.*')
ex_rule['b_amount_c']['normal'].append('.*采购控制总价：(.*?)元.*')
ex_rule['b_amount_c']['normal'].append('.*项目预算：(.*?)元.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额：人民币(.*?)圆整.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额：人民币(.*?)元整.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额：人民币(.*?)元.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额：人民币\s*(.*?)\s*（.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额:人民币\s*(.*?)\s*圆整.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额:人民币\s*(.*?)\s*元整.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额:人民币\s*(.*?)\s*元.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额：人民币大写\s*(.*?)\s*圆整.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额：人民币大写\s*(.*?)\s*元整.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额：人民币大写\s*(.*?)\s*元.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额：(.*?)元.*')
ex_rule['b_amount_c']['normal'].append('.*预算金额人民币(.*分|.*角|.*元)￥.*')
ex_rule['b_amount_c']['normal'].append('.*预算总金额（元）：(.*?)元整.*')
ex_rule['b_amount_c']['normal'].append('.*公开招标预算金额：B分标：(.*?)元整.*')
ex_rule['b_amount_c']['normal'].append('.*竞争性谈判预算金额\(人民币\):大写：\s*(.*?)\s*元整.*')
ex_rule['b_amount_c']['normal'].append('.*大写：人民币(.*?)元整.*')
ex_rule['b_amount_c'].update({'billion':['.*合计人民币：(.*)亿.*']})
ex_rule['b_amount_s'] = {'thousand':['第[一二三四五六七八九]包：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元']}
ex_rule['b_amount_s']['thousand'].append('第[一二三四五六七八九]包\?\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*\(万元\)')
ex_rule['b_amount_s']['thousand'].append('[一二三四五六七八九]包[：:]\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元')
ex_rule['b_amount_s']['thousand'].append('(?:标项[一二三四五六七八九十])(?:人民币|\s)*([\d,.]*?)(?:万元)')
ex_rule['b_amount_s'].update({'normal':['第[一二三四五六七八九]包：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元']})
ex_rule['b_amount_s']['normal'].append('[一二三四五六七八九]包：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元?（大写')
ex_rule['b_amount_s'].update({'billion':['第[一二三四五六七八九]包：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*亿']})
ex_rule['b_amount_sp'] = ['.*预算金额：(.*?)最高限价：.*']
ex_rule['b_amount_sp'].append('.*预算金额：(.*?)采购内容：.*')
ex_rule['b_amount_sp'].append('.*预算金额：(.*?)采购内容：.*')
ex_rule['b_amount_sp'].append('(?:公开招标预算金额)(?:（万元）|:|：)*(.*?)(?:最高限价（万元）)')
ex_rule['c_name'] = ['.*采购人名称：(.*?)详\s*细\s*地\s*址：.*采购代理机构名称：.*']
ex_rule['c_name'].append('(?:采购代理机构信息（如有）|采购人信息|采购单位|采购人)(?:.*?)(?<!项目)(?<!成交供应商)(?:名\s*称)(?::|：)(.*?)(?:地\s*址|项目联系人|联系人|联系方式|联系地址|招标人地址|法人代表|办公地址|联系电话|采购人联系人|详细地址)(?::|：)')
ex_rule['c_name'].append('(?:采购人信息名称|采购人信息名称采购人信息名称|采购人名称（盖章）|采购人名称|采购单位名称|业主单位名称|招标人名称|采购单位|采购人|招标人)(?:：|:)(.*?)(?:(?:(?:采购单位地址|代理机构名称|采购人联系方式|采购人地址|采购经办人|联系方式|采购人联系人|招标代理机构|采购方式|联系电话|联\s*系\s*地\s*址|联\s*系\s*人|地\s*址)(?::|：))|[123456789]\.|[一二三四五六七八九][、.．])')
ex_rule['c_name'].append('(?:招标人)(?::|：)(.*?)(?:招标代理机构)(?::|：)')
ex_rule['c_name'].append('(?:釆购人信息名称|采购人名称（盖章）|采购人名称|招标人（采购人）|采购单位名称|业主单位名称|招标人名称|采购单位|采购人|招标人)(.*?)(?:(?:(?:采购单位地址|代理机构名称|采购人地址|采购经办人|招标人联系人|联系方式|采购人联系人|采购方式|联系电话|项目名称|联\s*系\s*地\s*址|联\s*系\s*人|地\s*址))|[123456789]\.|[一二三四五六七八九][、.．])')
ex_rule['c_name'].append('.*联系方式.*单位名称.*单位名称(.*?)项目负责人.*否决投标单位及理由.*')
ex_rule['c_name'].append('.*采购单位：(.*?)详细地址：.*')
ex_rule['c_name'].append('.*采购单位：(.*?)地\s*址：|公告时间：.*')
ex_rule['c_name'].append('.*采购单位：(.*?)[123456789]\..*')
ex_rule['c_name'].append('.*采购单位：(.*?)[一二三四五六七八九]、.*')
ex_rule['c_name'].append('.*一、采购单位名称：(.*?)二、采购单位地址：.*')
ex_rule['c_name'].append('.*采购人名称（盖章）：(.*?)地址：.*采购项目名称：.*')
ex_rule['c_name'].append('.*采购人名称：(.*?)采购人地址：.*')
ex_rule['c_name'].append('.*招标（采购）人全称：(.*?)招标（采购）人地址：.*')
ex_rule['c_name'].append('.*业主单位名称：(.*?)业主单位地址:.*')
ex_rule['c_name'].append('.*采购人名称、地址和联系方式(.*?)采购代理机构名称、地址和联系方式.*')
ex_rule['c_name'].append('.*招标方：(.*?)联\s*系\s*人：.*')
ex_rule['c_name'].append('.*采购机构名称及联系方式：.*名称：(.*?)地址：.*')
ex_rule['c_name'].append('.*采购人信息.*名称:(.*?)地址:.*采购代理机构信息.*')
ex_rule['c_name'].append('.*采购人（甲方）：(.*?)地\s*址：.*供应商.*')
ex_rule['c_name'].append('.*采\s*购\s*人:(.*?)二、采购项目名称.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联系方式：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)二、采购人地址及联系方式：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)采购人地址：.*')
ex_rule['c_name'].append('.*招标人联系：(.*?)招标人联系方式：.*')
ex_rule['c_name'].append('.*采\s*购\s*单\s*位：(.*?)公告时间：.*')
ex_rule['c_name'].append('.*采\s*购\s*单\s*位：(.*?)联\s*系\s*人：.*采购代理机构.*')
ex_rule['c_name'].append('.*采\s*购\s*单\s*位：(.*?)联\s*系\s*人：.*代理机构.*')
ex_rule['c_name'].append('.*采\s*购\s*单\s*位：(.*?)联\s*系\s*人：.*')
ex_rule['c_name'].append('.*采购单位名称：(.*?)采购单位地址：.*')
ex_rule['c_name'].append('.*采购单位名称：(.*?)地\s*址：.*')
ex_rule['c_name'].append('.*采购人\(甲方\)：(.*?)供应商\(乙方\)：.*')
ex_rule['c_name'].append('.*采购人名称：(.*?)采购人地址：.*')
ex_rule['c_name'].append('.*采购人名称：(.*?)2、采购项目联系人.*')
ex_rule['c_name'].append('.*采购人名称：(.*?)地\s*址：.*')
ex_rule['c_name'].append('.*采购人名称:(.*?)地\s*址:.*')
ex_rule['c_name'].append('.*采购人名称:(.*?)联系地址:.*')
ex_rule['c_name'].append('.*采购人名称:(.*?)地\s*址：.*')
ex_rule['c_name'].append('.*采购人名称：(.*?)联系人：.*')
ex_rule['c_name'].append('.*采购人名称(.*?)中标（成交）供应商名称.*')
ex_rule['c_name'].append('.*招标人名称：(.*?)招标人地址：.*')
ex_rule['c_name'].append('.*联系单位(.*?)单位地址.*')
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)二、招标代理机构：.*')
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)招标人地址：.*')
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)招标代理：.*')
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)地\s*址：.*招标代理机构：.*')
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)地\s*址：.*代理机构：.*')
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)地\s*址：.*招标代理.*')
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)地\s*址：.*代理机构名称.*')
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)地\s*址：.*')
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)联\s*系\s*人：.*')
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)\d、.*')
ex_rule['c_name'].append('.*建设单位(.*?)招标方式.*')
ex_rule['c_name'].append('.*联系方式 招\s*标\s*人：(.*?)招标代理机构：.*')
ex_rule['c_name'].append('.*招\s*标\s*人;(.*?)法人代表.*')
ex_rule['c_name'].append('.*采购单位：(.*?)成交供应商：|报价截止时间：.*')
ex_rule['c_name'].append('.*采购单位联系人：(.*?)成交供应商联系人：	.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)供应商名称：.*代理机构名称：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)代理机构：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人：.*集中采购机构：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人：.*采购代理机构名称：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人：.*采购代理机构：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人：.*招标代理机构：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人：.*代理机构：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人：.*招标代理：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人：.*采购代理机构名称：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人：.*采购代理机构：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人：.*招标代理机构：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人：.*代理机构：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人：.*招标代理：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*人.*采购代理机构：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)联\s*系\s*地\s*址：.*代理机构：.*')
ex_rule['c_name'].append('.*采购人信息.*名\s*称：(.*?)地\s*址：.*采购代理机构信息.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)办公地址：.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)地\s*址：.*')
ex_rule['c_name'].append('.*采\s*购\s*人(.*?)联系电话.*')
ex_rule['c_name'].append('.*采\s*购\s*人：(.*?)采购人联系人：.*')
ex_rule['c_name'].append('.*采购人信息.*名称：(.*?)地址 ：.*采购代理机构信息.*')
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)地\s*址：.*')
ex_rule['c_name'].append('.*联系人及联系方式.*招标人(.*?)招标机构.*')
ex_rule['c_name'].append('.*,招标人为(.*?)，招标代理机构为.*')  #http://txzb.miit.gov.cn/DispatchAction.do?_QUERY_STRING=ZWZGb3JtRW5hbWU9UE9JWDE4JnNlcnZpY2VOYW1lPVBNQlUwNiZwYWNrYWdlSWQ9MDAwMDAwMDAwMDAwMDAxODY1NzYmYnVsbGV0aW5JZD0wMDAwMDAwMDAwMDAwMDA4MzYxMyZKU0VTU0lPTklEPTQ1MTY5MTA5NEUwQkU1MzY2NkVCNUI2NDFFNjVCN0E0
ex_rule['c_name'].append('.*招\s*标\s*人：(.*?)招标代理机构：.*')
ex_rule['c_name'].append('.*建设单位：(.*?)代建单位：.*')
ex_rule['c_name'].append('.*建设单位：(.*?)联\s*系\s*人.*')
ex_rule['c_name'].append('.*招标单位名称(.*?)招标工程项目.*')
ex_rule['c_name'].append('.*1、：(.*?)地\s*址：.*')
# ex_rule['c_name'].append('.*联系方式(.*?)\s.*')
ex_rule['c_name'].append('.*采购单位：(.*?)[一二三四五六七八九]、.*')
ex_rule['c_man'] = ['.*项目招标文件负责人及电话：(.*?)项目评审 联 系 人.*']
ex_rule['c_man'].append('(?:采购人信息名称)(?:.*?)(?:联系人)(?::|：)*(.*?)(?:联系方式)(?:.*?)(?:江苏省政府采购中心信息|代理机构)')
ex_rule['c_man'].append('.*联系方式.*联\s*系\s*人(.*?)电\s*话.*否决投标单位及理由.*')
ex_rule['c_man'].append('.*采购人地址：.*采购人联系人：(.*?)采购人联系方式：.*代理机构全称：.*')
ex_rule['c_man'].append('.*采购单位联系方式：(.*?)三、采购代理机构信息.*')
ex_rule['c_man'].append('.*采购单位联系方式：(.*?)一、采购项目的名称、数量、简要规格描述或项目基本.*')
ex_rule['c_man'].append('.*采购单位联系方式：(.*?)一、拟采购的货物或者服务的说明:.*')
ex_rule['c_man'].append('.*采购单位联系方式：(.*?)三、采购项目的名称、数量、简要规格描述或项目基本概况介绍.*')
ex_rule['c_man'].append('.*采购人联系方式：(.*?)采购代理机构地址：.*')
ex_rule['c_man'].append('.*采购人联系人：(.*?)联系电话：.*九、说明.*')
ex_rule['c_man'].append('.*采购人联系人：(.*?)采购人联系电话：.*')
ex_rule['c_man'].append('.*招标联系人(.*?)对投标人资质要求.*')
ex_rule['c_man'].append('.*采购项目联系人姓名、电话(.*?)其他.*')
ex_rule['c_man'].append('.*采购项目联系人：(.*?)电话：.*')
ex_rule['c_man'].append('.*采购联系人：(.*?)联系电话：.*')
ex_rule['c_man'].append('.*项目联系人：(.*?)电话：.*')
ex_rule['c_man'].append('.*项目联系人：(.*?)（.*')
ex_rule['c_man'].append('.*招标（采购）人联系方式：(.*?)招标（采购）代理机构.*')
ex_rule['c_man'].append('.*采购人信息.*项目联系人（询问）：(.*?)项目联系方式（询问）：.*采购代理机构信息.*')
ex_rule['c_man'].append('.*采购人信息.*联系人：(.*?);联系电话：.*采购代理机构信息.*')
ex_rule['c_man'].append('.*采购人名称（盖章）：.*联\s*系\s*人：(.*?)电\s*话：.*采购项目名称：.*')
ex_rule['c_man'].append('.*采购人名称：.*联\s*系\s*人：(.*?)采购人联系电话：.*采购代理机构：.*')
ex_rule['c_man'].append('.*采购人名称：.*联\s*系\s*人：(.*?)电\s*话：.*采购代理机构名称：.*')
ex_rule['c_man'].append('.*联系方式：(.*?)代理机构联系方式：.*')
ex_rule['c_man'].append('.*联系方式：(.*?)一、.*')
ex_rule['c_man'].append('.*采购单位联系人：(.*?)成交供应商联系人：.*')
ex_rule['c_man'].append('.*采购项目联系人：(.*?)3、采购人地址.*')
ex_rule['c_man'].append('.*项目负责人：(.*?)中央国家机关政府采购中心.*')
ex_rule['c_man'].append('.*招标人地址：.*联\s*系\s*人:(.*?)联\s*系\s*电\s*话：.*')
ex_rule['c_man'].append('.*采购人信息.*项目联系人：(.*?)项目联系方式：.*采购代理机构信息.*')
ex_rule['c_man'].append('.*采购人名称：.*联\s*系\s*人：(.*?)联\s*系\s*方\s*式.*采购代理机构名称：.*')
ex_rule['c_man'].append('.*采购人名称：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话.*采购代理机构名称：.*')
ex_rule['c_man'].append('.*采购人名称：.*联\s*系\s*人：(.*?)电\s*话.*采购代理机构名称：.*')
ex_rule['c_man'].append('.*采购人名称：.*项目负责人：(.*?)联\s*系\s*电\s*话：.*采购代理机构名称：.*')
ex_rule['c_man'].append('.*采购人名称：.*项目负责人：(.*?)联\s*系\s*电\s*话：.*代理机构名称：.*')
ex_rule['c_man'].append('.*采购人名称:.*项目联系人:(.*?)联\s*系\s*电\s*话.*采购代理机构全称:.*')
ex_rule['c_man'].append('.*采购人名称.*联\s*系\s*人：(.*?)联\s*系\s*方\s*式.*采购代理机构.*')
ex_rule['c_man'].append('.*采购人名称.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话.*采购代理机构.*')
ex_rule['c_man'].append('.*采购人名称.*联\s*系\s*人：(.*?)电\s*话.*采购代理机构.*')
ex_rule['c_man'].append('.*采购人名称.*联\s*系\s*人：(.*?)地\s*址.*采购代理机构.*')
ex_rule['c_man'].append('.*采购人名称.*项目负责人：(.*?)联\s*系\s*电\s*话：.*采购代理机构.*')
ex_rule['c_man'].append('.*采购人名称.*项目负责人：(.*?)联\s*系\s*电\s*话：.*代理机构.*')
ex_rule['c_man'].append('.*采购人名称.*项目联系人:(.*?)联\s*系\s*电\s*话.*采购代理机构.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)联\s*系\s*方\s*式：.*采购代理机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)电\s*话：.*采购代理机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*采购代理机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)电\s*话：.*采购代理机构：.*')
ex_rule['c_man'].append('.*招\s*标\s*方：.*联\s*系\s*人：(.*?)联\s*系\s*方\s*式：.*招标代理人：.*')
ex_rule['c_man'].append('.*招\s*标\s*方：.*联\s*系\s*人：(.*?)电\s*话：.*招标代理人：.*')
ex_rule['c_man'].append('.*招\s*标\s*方：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*招标代理人：.*')
ex_rule['c_man'].append('.*采购单位及联系人电话.*联\s*系\s*人：(.*?)联\s*系\s*方\s*式：.*采购代理机构及联系人.*')
ex_rule['c_man'].append('.*采购单位及联系人电话.*联\s*系\s*人：(.*?)电\s*话：.*采购代理机构及联系人.*')
ex_rule['c_man'].append('.*采购单位及联系人电话.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*采购代理机构及联系人.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)联\s*系\s*方\s*式：.*集中采购机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)电\s*话：.*集中采购机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*集中采购机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)联\s*系\s*方\s*式：.*招标代理机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*招标代理机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)电\s*话：.*招标代理机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)电\s*话：.*代理机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*代理机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)联\s*系\s*方\s*式：.*代理机构：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)电\s*话：.*招标代理机构：.*')
ex_rule['c_man'].append('.*建设单位：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*代理机构.*')
ex_rule['c_man'].append('.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*采购代理机构名称：.*')
ex_rule['c_man'].append('.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*采购代理机构：.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)联\s*系\s*人：.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)联系方式：.*采购代理机构名称：.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)联系方式：.*采购代理机构：.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)联系方式：.*招标代理机构：.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)联系方式：.*代理机构：.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)联系方式：.*招标代理：.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*采购代理机构名称：.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*采购代理机构：.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*招标代理机构：.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*代理机构：.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*招标代理：.*')
ex_rule['c_man'].append('.*招\s*标\s*人：.*联\s*系\s*人：(.*?)电\s*话：.*采购代理机构名称：.*')
ex_rule['c_man'].append('.*招\s*标\s*人：.*联\s*系\s*人：(.*?)电\s*话：.*采购代理机构：.*')
ex_rule['c_man'].append('.*招\s*标\s*人：.*联\s*系\s*人：(.*?)电\s*话：.*招标代理机构：.*')
ex_rule['c_man'].append('.*招\s*标\s*人：.*联\s*系\s*人：(.*?)电\s*话：.*代理机构：.*')
ex_rule['c_man'].append('.*招\s*标\s*人：.*联\s*系\s*人：(.*?)电\s*话：.*招标代理：.*')
ex_rule['c_man'].append('.*招\s*标\s*人：.*联\s*系\s*人:(.*?)联\s*系\s*人:.*')
ex_rule['c_man'].append('.*招\s*标\s*人.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['c_man'].append('.*采\s*购\s*单\s*位：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*')
ex_rule['c_man'].append('.*采\s*购\s*单\s*位：.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['c_man'].append('.*采\s*购\s*单\s*位：.*联\s*系\s*人：(.*?)联\s*系\s*方\s*式：.*')
ex_rule['c_man'].append('.*采\s*购\s*单\s*位：.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['c_man'].append('.*采\s*购\s*单\s*位：.*联\s*系\s*人：(.*?)采购项目：.*')
ex_rule['c_man'].append('.*采\s*购\s*单\s*位：.*联\s*系\s*人：(.*?)采购单位地址：.*')
ex_rule['c_man'].append('.*采\s*购\s*单\s*位：.*联\s*系\s*人：(.*?){}.*'.format(company))
ex_rule['c_man'].append('.*采\s*购\s*单\s*位名称：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*')
# ex_rule['c_man'].append('.*联\s*系\s*人：(.*?)联系电话：.*')
# ex_rule['c_man'].append('.*联\s*系\s*人(.*?)联系电话.*')
# ex_rule['c_man'].append('.*联系电话:(.*?)采购中心地址:*')
# ex_rule['c_man'].append('.*联\s*系\s*人(.*?);联系电话.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)联\s*系\s*人：.*')
ex_rule['c_man'].append('.*采\s*购\s*人：.*联\s*系\s*人：(.*?)传\s*真：.*')
ex_rule['c_man'].append('.*采\s*购\s*人.*联\s*系\s*人：(.*?)联系方式：.*供应商.*')
ex_rule['c_man'].append('.*项目联系人:(.*?)联\s*系\s*电\s*话：.*')
ex_rule['c_man'].append('.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['c_man'].append('.*联\s*系\s*人：(.*?)送货地点：.*')
ex_rule['c_man'].append('.*联\s*系\s*人：(.*?)联\s*系\s*人：.*')
ex_rule['c_man'].append('.*联\s*系\s*人：(.*?)报价截止时间：.*') #http://www.zycg.gov.cn/article/wsjj_show/417375
ex_rule['c_man'].append('.*联\s*系\s*人：(.*?)联\s*系\s*人：.*')
ex_rule['c_man'].append('.*联\s*系\s*人(.*?)联系电话.*')
ex_rule['c_man'].append('.*八、采购项目联系人姓名和电话     姓\s*名：(.*?)电\s*话：.*') #http://www.mof.gov.cn/xinxi/difangbiaoxun/difangzhongbiaogonggao/201910/t20191013_3401383.html
ex_rule['c_man'].append('.*联系人及联系方式.*联系人(.*?)联系人.*')
ex_rule['c_num'] = ['(?:采购人信息|采\s*购\s*单\s*位|采\s*购\s*人|招\s*标\s*人)(?:.*?)(?:联\s*系\s*方\s*式|联\s*系\s*电\s*话|电\s*话)(?::|：)(.*?)(?:\d[、.]|[一二三四五六七八九]、)?(?:江苏省政府采购中心信息|采购代理机构信息|采购代理机构|招标代理机构|代理机构|招标代理)']
ex_rule['c_num'].append('(?:招标人)(?::|：)(?:.*?)(?:招标代理机构)(?::|：)(?:.*?)(?:电话)(?::|：)(.*?)(?:电话)(?::|：)')
ex_rule['c_num'].append('.*采购单位电话：(.*?)成交供应商电话：.*')
ex_rule['c_num'].append('.*联系方式.*电\s*话(.*?)电子邮件.*否决投标单位及理由.*')
ex_rule['c_num'].append('.*采购人联系人：.*采购人联系方式：(.*?)代理机构全称：.*')
ex_rule['c_num'].append('.*采购人信息.*联系方式：(.*?)2\.采购代理机构信息.*')
ex_rule['c_num'].append('.*采购机构名称及联系方式：.*电话：(.*?)\s.*')
ex_rule['c_num'].append('.*采购单位联系方式：(.*?)三、采购代理机构信息.*')
ex_rule['c_num'].append('.*采购单位联系方式：(.*?)三、项目用途、简要技术要求及合同履行日期：.*')
ex_rule['c_num'].append('.*采购单位联系方式：(.*?)一、采购项目的名称、数量、简要规格描述或项目基本.*')
ex_rule['c_num'].append('.*采购单位联系方式：(.*?)一、拟采购的货物或者服务的说明:.*')
ex_rule['c_num'].append('.*采购单位联系方式：(.*?)三、采购项目的名称、数量、简要规格描述或项目基本概况介绍.*')
ex_rule['c_num'].append('.*采购单位名称：.*电\s*话：(.*?)\s.*')
ex_rule['c_num'].append('.*采购单位名称：.*电\s*话：(.*?)$')
ex_rule['c_num'].append('.*采购单位联系人：.*联\s*系\s*电\s*话：(.*?)。.*')
ex_rule['c_num'].append('.*采购人联系方式：(.*?)采购代理机构地址：.*')
ex_rule['c_num'].append('.*采购人联系方式：(.*?)代理机构：.*')
ex_rule['c_num'].append('.*采购人信息.*联系电话：(.*?)\s*2.采购代理机构信息.*')
ex_rule['c_num'].append('.*采购人地址及联系方式：(.*?)三、集中采购机构：.*')
ex_rule['c_num'].append('.*采购项目联系人姓名、电话(.*?)其他.*')
ex_rule['c_num'].append('.*采购人联系方式.*联\s*系\s*电\s*话：(.*?)\s.*')
ex_rule['c_num'].append('.*采购人联系电话：(.*?)采购代理机构.*')
ex_rule['c_num'].append('.*采购人联系电话：(.*?)采购代理机构.*')
ex_rule['c_num'].append('.*采购人联系电话(.*?)监督电话及邮箱.*')
ex_rule['c_num'].append('.*招标联系电话(.*?)招标联系人.*')
ex_rule['c_num'].append('.*招标（采购）人联系方式：(.*?)招标（采购）代理机构.*')
ex_rule['c_num'].append('.*招标人联系方式:(.*?)招标代理机构：.*')
ex_rule['c_num'].append('.*;联系电话(.*?);文件联系人.*')#http://www.zycg.gov.cn/article/wsjj_show/417396
ex_rule['c_num'].append('.*采购人信息.*项目联系方式：(.*?)\s*\d\.采购代理机构信息.*')
ex_rule['c_num'].append('.*采购人名称：.*?联\s*系\s*电\s*话：(.*?)4、.*')
ex_rule['c_num'].append('.*采购人名称：.*联\s*系\s*方\s*式：(.*?)采购代理机构名称：.*')
ex_rule['c_num'].append('.*采购人名称：.*联\s*系\s*电\s*话：(.*?)采购代理机构名称：.*')
ex_rule['c_num'].append('.*采购人名称：.*联\s*系\s*电\s*话：(.*?)七、采购代理机构的名称、地址和联系方式.*')
ex_rule['c_num'].append('.*采购人名称：.*联\s*系\s*电\s*话：(.*?)采购中心地址：.*')
ex_rule['c_num'].append('.*采购人名称：.*电\s*话：(.*?)采购代理机构名称：.*')
ex_rule['c_num'].append('.*采购人名称：.*电\s*话：(.*?)\s.*')
ex_rule['c_num'].append('.*采购单位：.*联\s*系\s*电\s*话：(.*?)项目编号：.*成交供应商：.*')
ex_rule['c_num'].append('.*采购单位：.*联\s*系\s*电\s*话：(.*?) .*')
ex_rule['c_num'].append('.*采购单位名称：.*联\s*系\s*电\s*话：(.*?)。十一.*')
ex_rule['c_num'].append('.*一、采购单位名称：.*联\s*系\s*电\s*话：(.*?)）.*')
ex_rule['c_num'].append('.*采购单位及联系人电话.*电\s*话：(.*?)采购代理机构及联系人.*')
ex_rule['c_num'].append('.*采购联系人：.*联系电话：(.*?)采购代理机构：.*')
ex_rule['c_num'].append('.*采\s*购\s*人：.*联\s*系\s*方\s*式：(.*?)采购代理机构：.*')
ex_rule['c_num'].append('.*采\s*购\s*人：.*联\s*系\s*方\s*式：(.*?)代理机构.*')
ex_rule['c_num'].append('.*采\s*购\s*人：.*电\s*话：(.*?)采购代理机构：.*')
ex_rule['c_num'].append('.*采\s*购\s*人：.*电\s*话：(.*?)集中采购机构：.*')
ex_rule['c_num'].append('.*采\s*购\s*人：.*联\s*系\s*电\s*话：(.*?)采购代理机构：.*')
ex_rule['c_num'].append('.*采\s*购\s*人.*联\s*系\s*方\s*式：(.*?)\d\.供应商.*')
ex_rule['c_num'].append('.*采\s*购\s*人.*联\s*系\s*方\s*式：(.*?)\d、供应商.*')
ex_rule['c_num'].append('.*招\s*标\s*人：.*电\s*话：(.*?)传\s*真：.*采购代理机构名称：.*')
ex_rule['c_num'].append('.*招\s*标\s*人：.*电\s*话：(.*?)传\s*真：.*采购代理机构：.*')
ex_rule['c_num'].append('.*招\s*标\s*人：.*电\s*话：(.*?)传\s*真：.*招标代理机构：.*')
ex_rule['c_num'].append('.*招\s*标\s*人：.*电\s*话：(.*?)传\s*真：.*代理机构：.*')
ex_rule['c_num'].append('.*招\s*标\s*人：.*电\s*话：(.*?)传\s*真：.*招标代理：.*')
ex_rule['c_num'].append('.*招\s*标\s*人：.*电\s*话：(.*?)电子邮件：.*招标代理机构：.*')
ex_rule['c_num'].append('.*招\s*标\s*人：.*电\s*话：(.*?)电\s*话：.*')
ex_rule['c_num'].append('.*招\s*标\s*方：.*联\s*系\s*电\s*话：(.*?)招标代理人：.*')
ex_rule['c_num'].append('.*招\s*标\s*人：.*电\s*话:(.*?)电\s*话:.*')
ex_rule['c_num'].append('.*招标人地址：.*电\s*话：(.*?)E-Mail：.*')
ex_rule['c_num'].append('.*联\s*系\s*方\s*式：(.*?)传\s*真：.*采购代理机构名称：.*')
ex_rule['c_num'].append('.*联\s*系\s*方\s*式：(.*?)传\s*真：.*采购代理机构：.*')
ex_rule['c_num'].append('.*联\s*系\s*方\s*式：(.*?)传\s*真：.*招标代理机构：.*')
ex_rule['c_num'].append('.*联\s*系\s*方\s*式：(.*?)传\s*真：.*代理机构：.*')
ex_rule['c_num'].append('.*联\s*系\s*方\s*式：(.*?)传\s*真：.*招标代理：.*')
ex_rule['c_num'].append('.*项目联系人：.*电\s*话：(.*?)传\s*真：.*')
ex_rule['c_num'].append('.*电\s*话：(.*?)采购代理机构名称：.*')
ex_rule['c_num'].append('.*电\s*话：(.*?)采购代理机构：.*')
ex_rule['c_num'].append('.*电\s*话：(.*?)招标代理机构：.*')
ex_rule['c_num'].append('.*电\s*话：(.*?)代理机构：.*')
ex_rule['c_num'].append('.*电\s*话：(.*?)招标代理：.*')
ex_rule['c_num'].append('.*招\s*标\s*人：.*联\s*系\s*方\s*式：(.*?)传\s*真：.*.*')
ex_rule['c_num'].append('.*招\s*标\s*人：.*联系电话：(.*?)9.2招标机构名称：.*')
ex_rule['c_num'].append('.*招\s*标\s*人：.*联系电话：(.*?)\s.*')
ex_rule['c_num'].append('.*采购人联系人：.*联系电话：(.*?)九、说明：.*')
ex_rule['c_num'].append('.*联\s*系\s*人：.*电\s*话：(.*?)采购项目名称：.*')
ex_rule['c_num'].append('.*联\s*系\s*人：.*电\s*话：(.*?)招标代理机构：.*')
ex_rule['c_num'].append('.*联\s*系\s*电\s*话：(.*?)采购代理机构联系方式：.*')
ex_rule['c_num'].append('.*联\s*系\s*电\s*话：(.*?)开户银行：.*')
ex_rule['c_num'].append('.*联\s*系\s*电\s*话：(.*?)北京市政府采购中心.*')
ex_rule['c_num'].append('.*联系电话:(.*?)采购中心地址:.*')
ex_rule['c_num'].append('.*联\s*系\s*电\s*话：(.*?)到货时间：.*')
ex_rule['c_num'].append('.*联\s*系\s*电\s*话：(.*?)\d{2,4}年\d{1,2}月\d{1,2}日.*')
ex_rule['c_num'].append('.*采\s*购\s*单\s*位：.*联\s*系\s*人：(.*?)采购单位地址：.*')
ex_rule['c_num'].append('.*联系电话(.*?)电子邮箱.*')
ex_rule['c_num'].append('.*联系电话(.*?)联系地址.*')
ex_rule['c_num'].append('.*电\s*话：(.*?)九、代理费用.*')
ex_rule['c_num'].append('.*电\s*话：(.*?)招标代理机构：.*')
ex_rule['c_num'].append('.*电\s*话：(.*?)电\s*话：.*')
ex_rule['c_num'].append('.*电\s*话：(.*?)地\s*址：.*采购代理机构名称：.*')
ex_rule['c_num'].append('.*联系人及联系方式.*联系人.*电话(.*?)电话.*')
ex_rule['c_num'].append('.*联系方式：(.*?)代理机构联系方式：.*')
ex_rule['c_num'].append('.*联系方式：(.*?)一、.*')
ex_rule['c_num'].append('.*项目招标文件负责人及电话：(.*?)项目评审 联 系 人.*')
ex_rule['c_num'].append('.*项目负责人：(.*?)中央国家机关政府采购中心.*')
ex_rule['c_num'].append('.*联系方式：(.*?)招标代理机构：.*')
ex_rule['c_num'].append('.*联\s*系\s*人(.*?);联系电话.*')
ex_rule['c_num'].append('.*联系电话(.*?)招标代理机构.*')
ex_rule['c_num'].append('.*联系电话(.*?)采购代理机构.*')
ex_rule['c_num'].append('.*联系电话：(.*?)联系电话：.*')
ex_rule['a_name'] = ['.*代理机构：(.*?)代理机构联系人：.*']
# ex_rule['a_name'].append('(?:釆购人信息|采购人信息)(?:.*?)(?:江苏省政府采购中心信息|釆购代理机构信息|集中采购机构信息|采购代理机构信息（如有）|代理机构信息（如有）|代理机构信息)(?:.*?)(?:名称)(?:：|:)?(.*?)(?:地址)(?:.*?)(?:联系人|项目联系人|项目联系人（询问）|同级政府采购监督管理部门|联系方式)')
ex_rule['a_name'].append('(?:招标（采购）代理机构全称|采购代理机构全称|采购代理机构信息名称|采购代理机构信息|采购代理机构名称|代理机构名称|招标机构名称|代理机构全称|招标代理机构|招标代理机构全称|招标代理机构|采购代理机构|集中采购机构|采购代理单位|采购机构名称|招标代理|代理单位|代理机构)(?::|：)(.*?)(?:(?:(?:代理机构地址|联系地址|采购代理机构地址|联\s*系\s*地\s*址|联\s*系\s*人|详\s*细\s*地\s*址|采购代理机构地址|地\s*址|招标代理机构地址|采购代理机构联系方式|联系人（业务）|代理机构经办人|中标单位|项目经理|招标公司地址|详\s*细\s*电\s*话|联\s*系\s*电\s*话|地\s*点)(?::|：))|[一二三四五六七八九]、|[123456789]\.)')
ex_rule['a_name'].append('(?:招标（采购）代理机构全称|采购代理机构全称|采购代理机构信息名称|采购代理机构信息|采购代理机构名称|代理机构名称|招标机构名称|代理机构全称|招标代理机构|招标代理机构全称|采购代理机构|集中采购机构|采购代理单位|采购机构名称|招标代理|代理单位|代理机构)(.*?)(?:(?:(?:代理机构地址|联系地址|采购代理机构地址|联\s*系\s*地\s*址|联\s*系\s*人|详\s*细\s*地\s*址|采购代理机构地址|地\s*址|招标代理机构地址|采购代理机构联系方式|招标代理机构|联系人（业务）|代理机构经办人|中标单位|公告时间|项目经理|招标公司地址|详\s*细\s*电\s*话|联\s*系\s*电\s*话|地\s*点))|[一二三四五六七八九]、|[123456789]\.)')
ex_rule['a_name'].append('.*代理机构：(.*?)代理机构地址：.*')
ex_rule['a_name'].append('.*代理机构：(.*?)代理机构地址：.*')
ex_rule['a_name'].append('.*代理机构：(.*?)[一二三四五六七八九]、.*')
ex_rule['a_name'].append('.*代理机构：(.*?)[123456789]\..*')
ex_rule['a_name'].append('.*采购人信息.*集中采购机构信息.{0,10}名\s*称：(.*?)地\s*址：.*联系人：.*')
ex_rule['a_name'].append('.*采购人信息.*采购代理机构信息.{0,10}名\s*称：(.*?)地\s*址：.*项目联系人：.*')
ex_rule['a_name'].append('.*采购人信息.*采购代理机构信息.{0,10}名\s*称：(.*?)地\s*址：.*项目联系人（询问）：.*')
ex_rule['a_name'].append('.*采购人信息.*采购代理机构信息.{0,10}名\s*称：(.*?)地\s*址：.*同级政府采购监督管理部门.*')
ex_rule['a_name'].append('.*采购代理机构全称:(.*?)联系地址:.*')
ex_rule['a_name'].append('.*采购代理机构：(.*?)采购代理机构地址：.*')
ex_rule['a_name'].append('.*集中采购机构：(.*?)四、集中采购机构地址及联系方式：.*')
ex_rule['a_name'].append('.*采购代理机构信息.*名称:(.*?)地址:.*')
ex_rule['a_name'].append('.*采购代理机构：(.*?)地\s*址：.*')
ex_rule['a_name'].append('.*采购代理机构：(.*?)联\s*系\s*人.*')
ex_rule['a_name'].append('.*采购人名称：.*采购代理机构名称：(.*?)详\s*细\s*地\s*址：.*')
ex_rule['a_name'].append('.*采购代理机构名称：(.*?)详\s*细\s*地\s*址：.*')
ex_rule['a_name'].append('.*采购代理机构名称：(.*?)采购代理机构详\s*细\s*地\s*址：.*')
ex_rule['a_name'].append('.*采购代理机构名称：(.*?)采购代理机构地址：.*')
ex_rule['a_name'].append('.*采购代理机构名称：(.*?)地\s*址：.*采购单位名称：.*')
ex_rule['a_name'].append('.*采购代理机构名称：(.*?)地\s*址：.*')
ex_rule['a_name'].append('.*采购代理机构名称：(.*?)联\s*系\s*人：.*')
ex_rule['a_name'].append('.*集中采购机构：(.*?)地\s*址：.*')
ex_rule['a_name'].append('.*采购人名称：.*代理机构名称：(.*?)2、项目联系人.*')
ex_rule['a_name'].append('.*招标代理机构全称：(.*?)招标代理机构地址：.*')
ex_rule['a_name'].append('.*招标代理机构全称：(.*?)采购代理机构联系方式：.*')
ex_rule['a_name'].append('.*招标（采购）代理机构全称：(.*?)招标（采购）代理机构地址：.*')
ex_rule['a_name'].append('.*招标代理机构名称：(.*?)招标代理机构地址：.*')
ex_rule['a_name'].append('.*招标代理机构名称:(.*?)招标代理机构地址：.*')
ex_rule['a_name'].append('.*代理机构名称：(.*?)联\s*系\s*人：.*')
ex_rule['a_name'].append('.*代理机构名称：(.*?)联\s*系\s*地\s*址.*')
ex_rule['a_name'].append('.*代理机构名称：(.*?)地\s*址.*采购单位名称：.*')
ex_rule['a_name'].append('.*代理机构名称：(.*?)地\s*址.*')
ex_rule['a_name'].append('.*代理机构(.*?)中标、成交公告.*')
ex_rule['a_name'].append('.*招标代理机构：(.*?)安徽省分公司地址：.*')
ex_rule['a_name'].append('.*招标代理机构：(.*?)三、招标项目名称及编号：.*')
ex_rule['a_name'].append('.*招标代理机构：(.*?)地\s*址：.*')
ex_rule['a_name'].append('.*招标代理机构：(.*?)地\s*址:.*')
ex_rule['a_name'].append('.*招标代理机构：(.*?)联系人（业务）：.*')
ex_rule['a_name'].append('.*招标代理机构:(.*?)地\s*址:.*')
ex_rule['a_name'].append('.*招标代理机构：(.*?)招标代理机构地址:.*')
ex_rule['a_name'].append('.*招标代理机构：(.*?)联\s*系\s*人:.*')
ex_rule['a_name'].append('.*招标代理机构：(.*?)\s.*')
ex_rule['a_name'].append('.*招标代理人：(.*?)招标公司地址：.*')
ex_rule['a_name'].append('.*招\s*标\s*人：.*招标代理机构：(.*?)联\s*系\s*人：.*')
ex_rule['a_name'].append('.*招标代理：(.*?)联\s*系\s*人：.*')
ex_rule['a_name'].append('.*招标代理：(.*?)地\s*址：.*')
ex_rule['a_name'].append('.*招标代理：(.*?)详\s*细\s*地\s*址：.*')
ex_rule['a_name'].append('.*招标代理：(.*?)详\s*细\s*电\s*话：.*')
ex_rule['a_name'].append('.*采购代理机构信息.*名称：(.*?)地址：.*')
ex_rule['a_name'].append('.*代理机构全称：(.*?)代理机构地址：.*')
ex_rule['a_name'].append('.*公示期限.*代理机构：(.*?)地\s*址：.*联\s*系\s*人：.*')
ex_rule['a_name'].append('.*联系人及联系方式.*招标机构(.*?)地址.*地址.*')
ex_rule['a_name'].append('.*代理机构：(.*?)评标方法和标准：.*')
ex_rule['a_name'].append('.*代理机构:(.*?)地\s*址：.*')
ex_rule['a_name'].append('.*代理机构:(.*?)地\s*址:.*')
ex_rule['a_name'].append('.*代理机构:(.*?)地\s*址.*')
ex_rule['a_name'].append('.*代理机构：(.*?)地\s*址：.*')
ex_rule['a_name'].append('.*代理机构：(.*?)中标、成交公告：.*')
ex_rule['a_name'].append('.*代理机构：(.*?)联\s*系\s*地\s*址：.*')
ex_rule['a_name'].append('.*代理机构：(.*?)联\s*系\s*人：.*')
ex_rule['a_name'].append('.*集采机构：(.*?)联系电话：.*')
ex_rule['a_name'].append('.*招标机构名称：(.*?)详细地址：.*')
ex_rule['a_name'].append('.*采购代理机构(.*?)联\s*系\s*电\s*话.*')
ex_rule['a_name'].append('.*招标代理机构：(.*?)\d{2,4}年\d{1,2}月\d{1,2}日.*')
ex_rule['a_name'].append('.*招标人名称：(.*?)\d{2,4}年\d{1,2}月\d{1,2}日.*')
ex_rule['a_name'].append('.*联系方式.*招标代理机构：.*单位名称(.*?)单位名称.*否决投标单位及理由.*')
# ex_rule['a_name'].append('.*\s(.*?)联系人：.*')
ex_rule['a_man'] = ['.*代理机构联系人：(.*?)代理机构地址：.*']
ex_rule['a_man'].append('(?:采购人信息|采\s*购\s*单\s*位|采\s*购\s*人|招\s*标\s*人)(?:.*?)(?:江苏省政府采购中心信息|采购代理机构信息|集中采购机构信息|招标代理机构|代理机构)(?:.*?)(?:联系人|项目联系人|项目联系人（询问）|评审部经办人|经办人)(?::|：)(.*?)(?:\d[、.]|[一二三四五六七八九]、)?(?:联\s*系\s*方\s*式|联\s*系\s*电\s*话|电\s*话)')
ex_rule['a_man'].append('.*采购人信息.*集中采购机构信息.*联系人：(.*?)联系方式：.*')
ex_rule['a_man'].append('.*采购人信息.*采购代理机构信息.*项目联系人：(.*?)项目联系方式：.*')
ex_rule['a_man'].append('.*采购人信息.*采购代理机构信息.*项目联系人（询问）：(.*?)项目联系方式（询问）：.*')
ex_rule['a_man'].append('.*采购人信息.*采购代理机构信息.*项目联系人（询问）：(.*?)项目联系方式（询问）：.*同级政府采购监督管理部门.*')
ex_rule['a_man'].append('.*代理机构联系电话：.*代理机构联系人：(.*?)受理质疑电话：.*')
ex_rule['a_man'].append('.*采购代理机构联系人：(.*?)联系电话：.*采购人联系人：.*')
ex_rule['a_man'].append('.*招标（采购）代理机构联系方式：(.*?)招标内容.*')
ex_rule['a_man'].append('.*招标（采购）代理机构联系方式：(.*?)分包信息.*')
ex_rule['a_man'].append('.*招标（采购）代理机构联系方式：(.*?)中标候选人公示.*')
ex_rule['a_man'].append('.*招标（采购）代理机构联系方式：(.*?)中标内容.*')
ex_rule['a_man'].append('.*招标代理机构联系人：(.*?)招标代理机构联系方式：.*')
ex_rule['a_man'].append('.*采购代理机构联系方式：(.*?)五、中标信息招标公告日期：.*')
ex_rule['a_man'].append('.*采购代理机构联系方式：(.*?)五、中标信息.*')
ex_rule['a_man'].append('.*采购代理机构联系方式：(.*?)四、成交信息.*')
ex_rule['a_man'].append('.*采购代理机构联系方式：(.*?)四、废标、流标的原因.*')
ex_rule['a_man'].append('.*采购代理机构联系方式：(.*?)【.*')
ex_rule['a_man'].append('.*采购代理机构联系方式：(.*?)（最终版）.*')
ex_rule['a_man'].append('.*采购代理机构联系方式：(.*?)变更公告.*')
ex_rule['a_man'].append('.*采购代理机构联系方式：(.*?)更正公告.*')
ex_rule['a_man'].append('.*采购代理机构联系方式：(.*?)采购预算金额：.*')
ex_rule['a_man'].append('.*采购代理机构联系方式：(.*?)财政部门地址：.*')
ex_rule['a_man'].append('.*代理机构联系方式.*联\s*系\s*人：(.*?)电\s*话.*采购人联系方式.*')
ex_rule['a_man'].append('.*采购代理机构联系人及电话：(.*?)电\s*子\s*函\s*件：.*')
ex_rule['a_man'].append('.*招标代理机构人员姓名：(.*?)招标代理机构人员电话：.*')
ex_rule['a_man'].append('.*采购代理机构信息.*联系人：(.*?);联系电话：.*')
ex_rule['a_man'].append('.*招标代理机构：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*')
ex_rule['a_man'].append('.*招标代理机构：.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['a_man'].append('.*招标代理机构：.*联\s*系\s*人:(.*?)地\s*址:.*')
ex_rule['a_man'].append('.*招标代理机构:.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['a_man'].append('.*招标代理：.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['a_man'].append('.*集中采购机构：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*')
ex_rule['a_man'].append('.*集中采购机构：.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['a_man'].append('.*集中采购机构：.*联\s*系\s*人:(.*?)地\s*址:.*')
ex_rule['a_man'].append('.*招标代理人：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*')
ex_rule['a_man'].append('.*招标代理人：.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['a_man'].append('.*招标代理人：.*联\s*系\s*人:(.*?)地\s*址:.*')
ex_rule['a_man'].append('.*采购单位联系方式：(.*?)采购代理机构全称：.*')
ex_rule['a_man'].append('.*项目经办人：(.*?)联\s*系\s*电\s*话：.*')
ex_rule['a_man'].append('.*联系方法：(.*?)二、招标公告发布日期.*')
ex_rule['a_man'].append('.*采购代理机构全称:.*项目联系人:(.*?)联\s*系\s*电\s*话:.*')
ex_rule['a_man'].append('.*采购代理机构名称：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*采购单位名称：.*')
ex_rule['a_man'].append('.*采购代理机构名称：.*联\s*系\s*人：(.*?)电子邮件：.*采购单位名称：.*')
ex_rule['a_man'].append('.*采购代理机构名称：.*联\s*系\s*人：(.*?)电子函件：.*采购单位名称：.*')
ex_rule['a_man'].append('.*采购代理机构名称：.*联\s*系\s*人：(.*?)电\s*话：.*采购单位名称：.*')
ex_rule['a_man'].append('.*采购代理机构名称：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*电子邮件：')
ex_rule['a_man'].append('.*采购代理机构名称：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*电子函件：')
ex_rule['a_man'].append('.*采购代理机构名称：.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['a_man'].append('.*代理机构名称：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话.*采购单位名称：.*')
ex_rule['a_man'].append('.*代理机构名称：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话.*')
ex_rule['a_man'].append('.*代理机构名称：.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['a_man'].append('.*代理机构名称：.*项目联系人：(.*?)3、代理机构地点.*')
ex_rule['a_man'].append('.*代理机构名称：.*评审部经办人：(.*?)联\s*系\s*电\s*话：.*')
ex_rule['a_man'].append('.*代理机构名称：.*经办人：(.*?)联\s*系\s*电\s*话：.*')
ex_rule['a_man'].append('.*代理机构地址：.*联系人：(.*?)联\s*系\s*电\s*话：.*')
ex_rule['a_man'].append('.*项目联系方式.*项目联系人：(.*?)电\s*话：.*')
ex_rule['a_man'].append('.*采购代理机构：.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['a_man'].append('.*采购代理机构：.*联\s*系\s*人：(.*?)开\s*户\s*行：.*')
ex_rule['a_man'].append('.*采购代理机构：.*联\s*系\s*人：(.*?)联\s*系\s*方\s*式：.*')
ex_rule['a_man'].append('.*采购代理机构联系方式.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['a_man'].append('.*代理机构：.*联\s*系\s*人：(.*?)电\s*话：.*财政部门：.*')
ex_rule['a_man'].append('.*代理机构：.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['a_man'].append('.*代理机构：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*')
ex_rule['a_man'].append('.*代理机构：.*联\s*系\s*人：(.*?)联\s*系\s*方\s*式：.*')
ex_rule['a_man'].append('.*集采机构：.*联\s*系\s*人：(.*?) .*')
ex_rule['a_man'].append('.*联系人及联系方式.*联\s*系\s*人(.*?)电话.*电话.*')
ex_rule['a_man'].append('.*代理机构:.*项目联系人:(.*?)联\s*系\s*电\s*话:.*')
ex_rule['a_man'].append('.*招标机构名称：.*联\s*系\s*人：(.*?)联\s*系\s*电\s*话：.*')
ex_rule['a_man'].append('.*联系方式.*联\s*系\s*人(.*?)联\s*系\s*人.*否决投标单位及理由.*')
ex_rule['a_man'].append('.*联\s*系\s*人：(.*?)地\s*址：.*')
# ex_rule['a_man'].append('.*联\s*系\s*人：(.*?)电\s*话：.*')
# ex_rule['a_man'].append('.*联\s*系\s*人（业务）：(.*?)联系电话：.*')
# ex_rule['a_man'].append('.*联\s*系\s*人：(.*?)电\s*话：.*')
# ex_rule['a_man'].append('.*联\s*系\s*人：(.*?)电\s*话：.*')
ex_rule['a_tell'] = ['(?:采购人信息|采\s*购\s*单\s*位|采\s*购\s*人|招\s*标\s*人)(?:.*?)(?:江苏省政府采购中心信息|采购代理机构信息|集中采购机构信息|招标代理机构|代理机构)(?:.*?)(?:联\s*系\s*方\s*式|联\s*系\s*电\s*话|电\s*话)(?::|：)(.*?)(?:\d[、.]|[一二三四五六七八九]、)?(?:项目联系方式|电子邮箱|电子邮件|监管单位|传\s*真|网\s*址|招标内容|分包信息|中标候选人公示|中标内容|\d{4}年|$)']
ex_rule['a_tell'].append('.*代理机构联系人：(.*?)代理机构地址：.*')
ex_rule['a_tell'].append('.*采购人信息.*集中采购机构信息.*联系方式：(.*?)\d\..*')
ex_rule['a_tell'].append('.*采购人信息.*采购代理机构信息.*项目联系方式：(.*?)\s.*')
ex_rule['a_tell'].append('.*采购人信息.*采购代理机构信息.*项目联系方式（询问）：(.*?)\s.*')
ex_rule['a_tell'].append('.*采购人信息.*采购代理机构信息.*项目联系方式（询问）：(.*?)质疑联系人：.*同级政府采购监督管理部门.*')
ex_rule['a_tell'].append('.*联系方式.*电\s*话(.*?)电\s*话.*电子邮件.*否决投标单位及理由.*')
ex_rule['a_tell'].append('.*代理机构地址：.*代理机构联系电话：(.*?)代理机构联系人：.*受理质疑电话：.*')
ex_rule['a_tell'].append('.*招标（采购）代理机构联系方式：(.*?)招标内容.*')
ex_rule['a_tell'].append('.*招标（采购）代理机构联系方式：(.*?)分包信息.*')
ex_rule['a_tell'].append('.*招标（采购）代理机构联系方式：(.*?)中标候选人公示.*')
ex_rule['a_tell'].append('.*招标（采购）代理机构联系方式：(.*?)中标内容.*')
ex_rule['a_tell'].append('.*集中采购机构地址及联系方式：(.*?)五、采购项目名称：.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)五、中标信息招标公告日期：.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)五、中标信息.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)四、成交信息.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)四、废标、流标的原因.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)【.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)（最终版）.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)变更公告.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)更正公告.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)采购预算金额：.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)项目实施地点：.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)财政部门地址：.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式：(.*?)财政部门联系地址：.*')
ex_rule['a_tell'].append('.*招标代理机构联系方式:(.*?)中标结果公告发布日期：.*')
ex_rule['a_tell'].append('.*代理机构联系方式.*电\s*话：(.*?)7.采购人联系方式.*')
ex_rule['a_tell'].append('.*代理机构联系方式：(.*?)本项目招标公告日期：.*')
ex_rule['a_tell'].append('.*代理机构联系方式：(.*?)备注：.*')
ex_rule['a_tell'].append('.*招标代理机构联系方式：(.*?)原公告内容：.*')
ex_rule['a_tell'].append('.*招标代理机构人员电话：(.*?)招标代理机构人员邮箱：.*')
ex_rule['a_tell'].append('.*采购单位联系方式：(.*?)采购代理机构全称：.*')
ex_rule['a_tell'].append('.*采购代理机构联系人：.*联系电话：(.*?)采购人联系人：.*')
ex_rule['a_tell'].append('.*采购代理机构信息.*联系电话：(.*?)3.项目联系方式:.*')
ex_rule['a_tell'].append('.*招标代理机构名称.*联\s*系\s*方\s*式：(.*?)传\s*真：.*')
ex_rule['a_tell'].append('.*招标代理机构名称.*电\s*话：(.*?)$')
ex_rule['a_tell'].append('.*招标代理机构：.*电\s*话：(.*?)电子邮箱：.*')
ex_rule['a_tell'].append('.*招标代理机构：.*电\s*话：(.*?)电子邮件：.*')
ex_rule['a_tell'].append('.*招标代理机构：.*电\s*话：(.*?)传\s*真：.*')
ex_rule['a_tell'].append('.*招标代理机构：.*电\s*话：(.*?)网\s*址：.*')
ex_rule['a_tell'].append('.*招标代理机构：.*电\s*话：(.*?)监管单位：.*')
ex_rule['a_tell'].append('.*招标代理机构：.*电\s*话：(.*?)监督单位：.*')
ex_rule['a_tell'].append('.*招标代理机构：.*电\s*话：(.*?)本公告所含项目编号.*')
ex_rule['a_tell'].append('.*招标代理机构：.*电\s*话：(.*?)开户行：.*')
ex_rule['a_tell'].append('.*招标代理机构：.*联\s*系\s*电\s*话：(.*?)监\s*督\s*机\s*构：.*')
ex_rule['a_tell'].append('.*招标代理机构：.*联\s*系\s*人：(.*?)监 督 电 话：.*')
ex_rule['a_tell'].append('.*招标代理机构：.*电\s*话：(.*?)\s.*')
ex_rule['a_tell'].append('.*招标代理机构：.*电\s*话:(.*?)电子邮箱:.*')
ex_rule['a_tell'].append('.*招标代理机构:.*电\s*话：(.*?)\s.*')
ex_rule['a_tell'].append('.*招标代理：.*电\s*话：(.*?)邮\s*箱：.*')
ex_rule['a_tell'].append('.*招标代理：.*电\s*话：(.*?)电子邮件：.*')
ex_rule['a_tell'].append('.*招标代理：.*电\s*话：(.*?)网\s*址：.*')
ex_rule['a_tell'].append('.*招标代理：.*电\s*话：(.*?)传\s*真：.*')
ex_rule['a_tell'].append('.*招标代理：.*电\s*话：(.*?)电子邮箱：.*')
ex_rule['a_tell'].append('.*招标代理：.*电\s*话：(.*?).buttomlink.*')
ex_rule['a_tell'].append('.*招标代理：.*电\s*话：(.*?)\s.*')
ex_rule['a_tell'].append('.*集中采购机构：.*电\s*话：(.*?)邮\s*箱：.*')
ex_rule['a_tell'].append('.*集中采购机构：.*电\s*话：(.*?)电子邮件：.*')
ex_rule['a_tell'].append('.*集中采购机构：.*电\s*话：(.*?)网\s*址：.*')
ex_rule['a_tell'].append('.*集中采购机构：.*电\s*话：(.*?)传\s*真：.*')
ex_rule['a_tell'].append('.*集中采购机构：.*电\s*话：(.*?)电子邮箱：.*')
ex_rule['a_tell'].append('.*招标代理人：.*电\s*话：(.*?)邮\s*箱：.*')
ex_rule['a_tell'].append('.*招标代理人：.*电\s*话：(.*?)电子邮件：.*')
ex_rule['a_tell'].append('.*招标代理人：.*电\s*话：(.*?)网\s*址：.*')
ex_rule['a_tell'].append('.*招标代理人：.*电\s*话：(.*?)传\s*真：.*')
ex_rule['a_tell'].append('.*招标代理人：.*电\s*话：(.*?)电子邮箱：.*')
ex_rule['a_tell'].append('.*招\s*标\s*人：.*招标代理机构：.*电\s*话：(.*?)监督单位：.*')
ex_rule['a_tell'].append('.*采购代理机构：.*电\s*话：(.*?)传\s*真：.*')
ex_rule['a_tell'].append('.*采购代理机构：.*电\s*话：(.*?)邮\s*箱：.*')
ex_rule['a_tell'].append('.*采购代理机构：.*电\s*话：(.*?)电\s*话：.*采\s*购\s*单\s*位：.*')
ex_rule['a_tell'].append('.*采购代理机构：.*联\s*系\s*电\s*话：(.*?) .*')
ex_rule['a_tell'].append('.*采购代理机构：.*联\s*系\s*方\s*式：(.*?)发\s*布\s*人.*')
ex_rule['a_tell'].append('.*采购代理机构联系方式.*电\s*话：(.*?)采购方式：.*')
ex_rule['a_tell'].append('.*联系方法：(.*?)二、招标公告发布日期.*')
ex_rule['a_tell'].append('.*采购代理机构全称:.*联\s*系\s*电\s*话:(.*?)18、代理机构收费内容.*')
ex_rule['a_tell'].append('.*采购代理机构名称：.*联\s*系\s*电\s*话：(.*?)传\s*真：.*')
ex_rule['a_tell'].append('.*采购代理机构名称：.*联\s*系\s*电\s*话：(.*?)邮\s*箱：.*')
ex_rule['a_tell'].append('.*采购代理机构名称：.*联\s*系\s*电\s*话：(.*?)采购单位名称：.*')
ex_rule['a_tell'].append('.*采购代理机构名称：.*联\s*系\s*电\s*话：(.*?)电\s*子\s*函\s*件：.*')
ex_rule['a_tell'].append('.*采购代理机构名称：.*联\s*系\s*电\s*话：(.*?)电\s*子\s*邮\s*件：.*')
ex_rule['a_tell'].append('.*采购代理机构名称：.*电\s*话：(.*?)电\s*子\s*函\s*件：.*')
ex_rule['a_tell'].append('.*采购代理机构名称：.*电\s*话：(.*?)电子信箱：.*')
ex_rule['a_tell'].append('.*代理机构名称：.*联\s*系\s*电\s*话：(.*?)电子邮箱.*')
ex_rule['a_tell'].append('.*代理机构名称：.*联\s*系\s*电\s*话：(.*?)投标保证金账户.*采购单位名称：.*')
ex_rule['a_tell'].append('.*代理机构名称：.*电\s*话：(.*?)地\s*址：.*')
ex_rule['a_tell'].append('.*代理机构名称：.*电\s*话：(.*?)\s.*')
ex_rule['a_tell'].append('.*采购代理机构信息.*联系方式：(.*?)3\.项目联系方式.*')
ex_rule['a_tell'].append('.*代理机构地址：.*联\s*系\s*电\s*话：(.*?)E-Mail：.*')
ex_rule['a_tell'].append('.*代理机构：.*电\s*话：(.*?)邮\s*箱：.*')
ex_rule['a_tell'].append('.*代理机构：.*联\s*系\s*电\s*话：(.*?)邮\s*箱：.*')
ex_rule['a_tell'].append('.*代理机构：.*联\s*系\s*方\s*式：(.*?)邮\s*箱：.*')
ex_rule['a_tell'].append('.*代理机构：.*联\s*系\s*方\s*式：(.*?)联系地址：.*')
ex_rule['a_tell'].append('.*代理机构：.*联\s*系\s*电\s*话：(.*?)邮政编码：.*')
ex_rule['a_tell'].append('.*代理机构：.*电\s*话：(.*?)电子邮件：.*')
ex_rule['a_tell'].append('.*代理机构：.*电\s*话：(.*?)水行政监督部门：.*')
ex_rule['a_tell'].append('.*代理机构：.*联\s*系\s*电\s*话：(.*?)电子邮件：.*')
ex_rule['a_tell'].append('.*代理机构：.*联\s*系\s*方\s*式：(.*?)电子邮件：.*')
ex_rule['a_tell'].append('.*代理机构：.*电\s*话：(.*?)2019.*')
ex_rule['a_tell'].append('.*代理机构：.*电\s*话：(.*?)\s.*')
ex_rule['a_tell'].append('.*代理机构：.*电\s*话：(.*?)$')
ex_rule['a_tell'].append('.*集采机构：.*联\s*系\s*电\s*话：(.*?)单位地址：.*')
ex_rule['a_tell'].append('.*代理机构.*联\s*系\s*电\s*话:(.*?)\s.*')
ex_rule['a_tell'].append('.*招标机构名称：.*联\s*系\s*电\s*话：(.*?)\s.*')
ex_rule['a_tell'].append('.*联\s*系\s*电\s*话：(.*?)本项目其余相关信息均在.*')
ex_rule['a_tell'].append('.*联\s*系\s*电\s*话：(.*?)电子邮箱：.*')
ex_rule['a_tell'].append('.*联\s*系\s*电\s*话(.*?)采购项目名称.*')
ex_rule['a_tell'].append('.*招标人：.*招标代理：.*联\s*系\s*电\s*话：(.*?)\s.*')
ex_rule['a_tell'].append('.*联系人：.*电话：(.*?)财政部门：.*')
ex_rule['a_tell'].append('.*招\s*标\s*人：.*招标代理机构：.*电话：(.*?)\s.*')
ex_rule['a_tell'].append('.*联系人及联系方式.*电话.*电话(.*?)电子邮件.*')
ex_rule['a_tell'].append('.*联\s*系\s*电\s*话：(.*?)传\s*真：.*')
# ex_rule['a_tell'].append('.*电\s*话：(.*?)本项目招标师：.*')
# ex_rule['a_tell'].append('.*联\s*话：(.*?)开户名称：.*')
# ex_rule['a_tell'].append('.*电\s*话：(.*?)邮\s*箱：.*')
ex_rule['a_address'] = ['.*采购代理机构地址：(.*?)采购代理机构邮编：.*采购代理机构联系方式：.*']
ex_rule['a_address'].append('(?:采购人信息|采\s*购\s*单\s*位|采\s*购\s*人|招\s*标\s*人)(?:.*?)(?:江苏省政府采购中心信息|采购代理机构信息|集中采购机构信息|招标代理机构|代理机构)(?:.*?)(?:地址|代理机构地址)(?::|：)(.*?)(?:\d[、.]|[一二三四五六七八九]、)?(?:联系人|项目联系人|项目联系人（询问）|评审部经办人|经办人)')
ex_rule['a_address'].append('.*采购人信息.*集中采购机构信息.*地址：(.*?)联系人：.*')
ex_rule['a_address'].append('.*采购人信息.*采购代理机构信息.*地\s*址：(.*?)传\s*真：.*项目联系方式（询问）：.*')
ex_rule['a_address'].append('.*采购人信息.*采购代理机构信息.*地\s*址：(.*?)传\s*真：.*同级政府采购监督管理部门.*')
ex_rule['a_address'].append('.*采购代理机构地址：(.*?)采购代理机构联系方式：.*')
ex_rule['a_address'].append('.*采购代理机构地址：(.*?)采购代理机构联系人：.*')
ex_rule['a_address'].append('.*采购代理机构地址：(.*?)代理机构电话：.*')
ex_rule['a_address'].append('.*采购代理机构地址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*采购代理机构详\s*细\s*地\s*址：(.*?)采购代理机构联系人及电话：.*')
ex_rule['a_address'].append('.*招标（采购）代理机构地址：(.*?)招标（采购）代理机构联系方式：.*')
ex_rule['a_address'].append('.*招标代理机构地址：(.*?)邮政编码：.*')
ex_rule['a_address'].append('.*招标代理机构地址:(.*?)招标代理机构联系方式:.*')
ex_rule['a_address'].append('.*招标代理机构地址:(.*?)招标代理机构联系人：.*')
ex_rule['a_address'].append('.*招标公司地址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*集中采购机构地址及联系方式：(.*?)；.*五、采购项目名称：.*')
ex_rule['a_address'].append('.*采购代理机构全称:.*联系地址:(.*?)项目联系人:.*')
ex_rule['a_address'].append('.*采购代理机构信息.*地址:(.*?)联系方式:.*')
ex_rule['a_address'].append('.*采购代理机构名称：.*详\s*细\s*地\s*址：(.*?)邮\s*编：.*联\s*系\s*人：.*')
ex_rule['a_address'].append('.*采购代理机构名称：.*详\s*细\s*地\s*址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*采购代理机构名称：.*地\s*址：(.*?)邮\s*政\s*编\s*码：.*采购单位名称：.*')
ex_rule['a_address'].append('.*采购代理机构名称：.*地\s*址：(.*?)邮\s*政\s*编\s*码：.*')
ex_rule['a_address'].append('.*采购代理机构名称：.*地\s*址：(.*?)联\s*系\s*人：.*二、采购项目信息.*')
ex_rule['a_address'].append('.*采购代理机构名称：.*地\s*址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*采购代理机构名称：.*地\s*址：(.*?)采购文件咨询、质疑联系方式：.*')
ex_rule['a_address'].append('.*采购代理机构名称：.*地\s*点：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*代理机构名称：.*地\s*址：(.*?)评审部经办人：.*')
ex_rule['a_address'].append('.*代理机构名称：.*地\s*址：(.*?)经办人：.*')
ex_rule['a_address'].append('.*代理机构地址：(.*?)五、中标信息.*')
ex_rule['a_address'].append('.*代理机构地址：(.*?)代理机构联系方式：.*')
ex_rule['a_address'].append('.*代理机构地址：(.*?)代理机构联系电话：.*代理机构联系人：.*')
ex_rule['a_address'].append('.*代理机构地址：(.*?)一.*')
ex_rule['a_address'].append('.*代理机构地址：(.*?)联系人：.*')
ex_rule['a_address'].append('.*代理机构地址：(.*?)邮\s*编：.*')
ex_rule['a_address'].append('.*代理机构联系方式.*地\s*址：(.*?)联\s*系\s*人.*采购人联系方式.*')
ex_rule['a_address'].append('.*代理机构地点：(.*?)4、联系电话.*')
ex_rule['a_address'].append('.*采购代理机构：.*地\s*址：(.*?)电\s*话：.*采购单位：.*')
ex_rule['a_address'].append('.*采购代理机构：.*地\s*址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*采购代理机构：.*地\s*址：(.*?)邮\s*编.*')
ex_rule['a_address'].append('.*采购代理机构：.*地\s*址：(.*?)邮\s*政\s*编\s*码：.*')
ex_rule['a_address'].append('.*招标代理机构：.*地\s*址：(.*?)邮\s*编：.*')
# ex_rule['a_address'].append('.*招标代理机构：.*地\s*址：(.*?)邮\s*编：.*')
ex_rule['a_address'].append('.*招标代理机构：.*地\s*址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*招标代理机构：.*地\s*址：(.*?)电\s*子\s*邮\s*箱：.*')
ex_rule['a_address'].append('.*招标代理机构：.*地\s*址:(.*?)电\s*话:.*')
ex_rule['a_address'].append('.*采购代理机构名称：.*地\s*址：(.*?)\s.*')
ex_rule['a_address'].append('.*采购代理机构.*地\s*址：(.*?)\s.*')
ex_rule['a_address'].append('.*招标代理机构：.*地\s*址：(.*?)\s.*')
ex_rule['a_address'].append('.*招标代理机构:.*地\s*址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*招标代理：.*地\s*址：(.*?)\s.*')
ex_rule['a_address'].append('.*招标代理：.*地\s*址：(.*?)电\s*话：.*')
ex_rule['a_address'].append('.*招标代理：.*地\s*址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*招标代理：.*地\s*址：(.*?)电\s*子\s*邮\s*箱：.*')
ex_rule['a_address'].append('.*集中采购机构：.*地\s*址：(.*?)\s.*')
ex_rule['a_address'].append('.*集中采购机构：.*地\s*址：(.*?)电\s*话：.*')
ex_rule['a_address'].append('.*集中采购机构：.*地\s*址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*集中采购机构：.*地\s*址：(.*?)电\s*子\s*邮\s*箱：.*')
ex_rule['a_address'].append('.*招标代理机构：.*安徽省分公司地址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*代理机构名称：.*地\s*址：(.*?)招\s*标\s*人：.*')
ex_rule['a_address'].append('.*代理机构名称：.*地\s*址：(.*?)电\s*话.*')
ex_rule['a_address'].append('.*代理机构名称：.*地\s*址：(.*?)联\s*系\s*人.*')
ex_rule['a_address'].append('.*代理机构名称：.*地\s*址：(.*?)邮\s*政\s*编\s*码：.*采购单位名称：.*')
ex_rule['a_address'].append('.*采购代理机构信息.*地\s*址：(.*?)联系方式：.*项目联系方式.*')
ex_rule['a_address'].append('.*代理机构:.*地\s*址：(.*?)联系方法：.*')
ex_rule['a_address'].append('.*代理机构：.*地\s*址：(.*?)地\s*址：.*')
ex_rule['a_address'].append('.*代理机构：.*联\s*系\s*地\s*址：(.*?)如对上述中标结果有异议.*')
ex_rule['a_address'].append('.*代理机构：.*地\s*址：(.*?)电\s*话：.*')
ex_rule['a_address'].append('.*代理机构：.*地\s*址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*代理机构：.*地\s*址：(.*?)\s.*')
ex_rule['a_address'].append('.*集采机构：.*单位地址：(.*?)联系人：.*')
ex_rule['a_address'].append('.*公示期限.*地\s*址：(.*?)联\s*系\s*人：.*财政部门：.*')
ex_rule['a_address'].append('.*招标机构名称：.*详\s*细\s*地\s*址：(.*?)邮\s*编：.*')
ex_rule['a_address'].append('.*招标代理：.*地\s*址：(.*?)联\s*系\s*人：.*')
ex_rule['a_address'].append('.*联系方式.*地址\(邮编\)(.*?)地址\(邮编\).*否决投标单位及理由.*')
ex_rule['a_address'].append('.*联系人及联系方式.*地址.*地址(.*?)联系人.*联系人.*')
ex_rule['a_address'].append('.*地\s*址：(.*?)联系电话：.*')
# ex_rule['a_address'].append('.*地\s*址：(.*?)邮\s*编：.*')
# ex_rule['a_address'].append('.*地\s*址：(.*?)邮\s*编：.*邮\s*编：.*')
# ex_rule['a_address'].append('.*联系地址：(.*?)邮\s*编：.*')
# ex_rule['a_address'].append('.*地\s*址：(.*?)联\s*系\s*人：.*')
ex_rule['a_all'] = ['.*采购代理机构名称、地址和联系方式(.*?)项目名称.*']
ex_rule['w_money'] = {'thousand':['.*总中标金额：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)万元.*']}
ex_rule['w_money']['thousand'].append('(?:合同金额|成交金额|中标金额|中标（成交）金额|中标（成交）价格|合同总金额|投标价格|中标价|成交价)(?:（可填写下浮率、折扣率或费率）|（费率、单价等）|￥|¥|:|：|标包【1】|中标|小写|人民币|为|\s)*([\d.,]*?)(?:(?:[(（]?万元[)）]?)(?!以下|以上|至|以内))')
ex_rule['w_money']['thousand'].append('(?:合同金额|成交金额|中标金额|中标（成交）金额|中标（成交）价格|合同总金额|交易价格|投标价格|中标价)(?:[(（]?万元[)）]?)(?:|￥|¥|:|：|中标|小写|人民币|为|\s)*(\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d+[.,，]?\d+[.,，]?\d*)(?!以下|以上|至)(?:\s|[一二三四五六七八九]|明细|(?:(?:\d\.)?[\u4e00-\u9fa5]))')
# ex_rule['w_money']['thousand'].append('.*投标报价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*中标（成交）金额：（可填写下浮率、折扣率或费率）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*总成交金额：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
# ex_rule['w_money']['thousand'].append('.*总中标金额为：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*中标（成交）金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*\(万元\).*')
# ex_rule['w_money']['thousand'].append('.*中标（成交）金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*（万元）.*')
# ex_rule['w_money']['thousand'].append('.*中标（成交）金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*（单位：万元）.*')
# ex_rule['w_money']['thousand'].append('.*中标（成交）价格：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*中标（成交）价格：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*（万元）.*')
# ex_rule['w_money']['thousand'].append('.*中标（成交）价格：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*\(万元\).*')
# ex_rule['w_money']['thousand'].append('.*中标金额：人民币(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
# ex_rule['w_money']['thousand'].append('.*中标金额：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
# ex_rule['w_money']['thousand'].append('.*中标金额：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\(万元\).*')
# ex_rule['w_money']['thousand'].append('.*中标金额：￥(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
# ex_rule['w_money']['thousand'].append('.*中标金额：\s*人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
# ex_rule['w_money']['thousand'].append('.*中标金额(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
# # ex_rule['w_money']['thousand'].append('.*金额：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
# ex_rule['w_money']['thousand'].append('.*中标价格：.*：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
# ex_rule['w_money']['thousand'].append('.*中标价格：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
# ex_rule['w_money']['thousand'].append('.*中标价格\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*合同金额(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)万元.*')
# ex_rule['w_money']['thousand'].append('.*合同金额：(.*?)万元.*')
# ex_rule['w_money']['thousand'].append('.*中标金额.*小写：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*中标金额（万元）人民币：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*公告期限.*')
# ex_rule['w_money']['thousand'].append('.*中标金额\(万元\)：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*标段名称：.*')
# ex_rule['w_money']['thousand'].append('.*中标金额\(万元\)：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[一二三四五六七八九]、.*')
# ex_rule['w_money']['thousand'].append('.*合同金额\(万元\)\s*( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*合同签订日期.*')
# ex_rule['w_money']['thousand'].append('.*合同金额\(万元\)：\s*( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*[123456789]\..*')
# ex_rule['w_money']['thousand'].append('.*中标价（万元）\s*( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*公示时间.*')
# ex_rule['w_money']['thousand'].append('.*中标价：\s*( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*中\s标\s价：\s*( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*中标总金额人民币\s*( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*中标、成交金额\(万元\)\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*合同履行日期.*')
# ex_rule['w_money']['thousand'].append('.*中标（成交）金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*中标（成交）金额:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*中标（成交）金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*最终报价：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*成交价格：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*成交金额（万元）：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*[一二三四五六七八九].*')
# ex_rule['w_money']['thousand'].append('.*成交金额：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*成交信息.*金额：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*成交价\(万元\)( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*明细.*')
# ex_rule['w_money']['thousand'].append('.*成交价：( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*万元.*')
# ex_rule['w_money']['thousand'].append('.*本项目PPP建设工程投资额为\s*( *\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d* *)\s*万元.*')
# ex_rule['w_money']['thousand'].append('中标金额:\s*(.*)\s*万元')
ex_rule['w_money'].update({'normal':['.*投标报价：含税：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*']})
ex_rule['w_money']['normal'].append('.*投标报价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
# 中标金额 通用匹配
ex_rule['w_money']['normal'].append('(?<!例如)(?:合同金额|中标金额|中标价格|中标供应商\(投标总价\)|中标[（(]成交[）)]金额|合同总金额|投标价格|成交报价|中标价|中标|中标总价|投标报价|投标总价|工程金额|总中标|总报价|投标价|成交金额|合同价款|总价|价格|(?:(?<=\s)(?:金额)))(?:\(单位：元\)|（元）|\(元\)|￥|¥|:|：|合计|中标|小写|报价|RMB|中标候选供应商|人民币|设计费|设计费|为|（费率、单价等）|（人民币：元）|响应报价|（元/人民币）|（人民币）|（含税）|\(元/年\)|总金额|（可填写下浮率、折扣率或费率）|合同包1|（总价（元）\)|包一|（成交金额）|（元/优惠率）|\s|\?)*([,，.\d]+)(?!号线)(?:(?:[一二三四五六七八九]|(?:\d\.)?[^\d万]|\(元\)|（元）|（总价）|（单价）|地址)(?!/m2)|\s|\d号线)')
# 供货明细 专用提取
ex_rule['w_money']['normal'].append('(?:供货明细)(?:.*?)(?:报价)(?:（元）|\(元\)|￥|¥|:|：|中标|小写|人民币|为|总金额|包一|（元/优惠率）)*(?:\s)*(\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d+[.,，]?\d+[.,，]?\d*)(?:\s)*(?:[一二三四五六七八九]|(?:\d\.)?[\u4e00-\u9fa5]|\(元\)|（元）|（总价）)')
# 品目号 专用提取
ex_rule['w_money']['normal'].append('(?:品目号)(?:.*)(?<!预算)(?:金额)(?:（元）|\(元\)|￥|¥|:|：|中标|小写|报价|人民币|为|总金额|包一|（元/优惠率）|\s|\?)*(\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d+[.,，]?\d+[.,，]?\d*)(?:\s)*(?:[一二三四五六七八九]|(?:\d\.)?[\u4e00-\u9fa5]|\(元\)|（元）|（总价）)')
ex_rule['w_money']['normal'].append('.*投标报价:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*投标总价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*投标价格:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*合同总金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*合同总金额：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[\u4e00-\u9fa5].*')
ex_rule['w_money']['normal'].append('.*合同金额（元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*\d\..*')
ex_rule['w_money']['normal'].append('.*合同金额:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*合同金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*合同金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*履约期限.*')
ex_rule['w_money']['normal'].append('.*合同金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标价格\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标\（成交\）金额\（元\）\\\（%\）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[一二三四五六七八九]、.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*。?[一二三四五六七八九]、.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[一二三四五六七八九]、.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额（元）:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*。[一二三四五六七八九]、.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*；.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额：（\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元）.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*；.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*（总价）.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额:投标总价\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额:投标报价\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额.*总价:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额总价:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[一二三四五六七八九]、.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标（成交）金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*;.*')
ex_rule['w_money']['normal'].append('.*成交供应商\(投标总价\)：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*终报价为：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*成交价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*投标总价.*为：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('中标金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*中标数量：')
ex_rule['w_money']['normal'].append('总中标价格为\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('采购成交价格：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*标的成交价格：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标金额：中标\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标金额：¥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标金额：¥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[\u4e00-\u9fa5].*')
ex_rule['w_money']['normal'].append('.*中标金额:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标金额:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*中标标的名称.*')
# ex_rule['w_money']['normal'].append('.*中标金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*\(?元\)?.*')
ex_rule['w_money']['normal'].append('.*中标金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*下浮率.*')
ex_rule['w_money']['normal'].append('.*中标金额：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标金额：小写：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标金额：人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('.*中标金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[一二三四五六七八九]、.*')
ex_rule['w_money']['normal'].append('.*中标金额（元）：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*。.*')
ex_rule['w_money']['normal'].append('.*中标价格[：:]\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('中标价小写：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('中标价（元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('中标价（元）：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[一二三四五六七八九]、')
ex_rule['w_money']['normal'].append('中标价（元）\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*公告期')
ex_rule['w_money']['normal'].append('中标价（元）\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*公示开始时间')
ex_rule['w_money']['normal'].append('中标价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('中标价：人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('中标价\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('中标价\s*(\d*|\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*[\u4e00-\u9fa5]')
ex_rule['w_money']['normal'].append('.*中标价投标总报价\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('中标总价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*采购预算价：')
ex_rule['w_money']['normal'].append('.*中标报价\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('标的成交总额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元；')
ex_rule['w_money']['normal'].append('成交金额：人民币\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('成交金额：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*（')
ex_rule['w_money']['normal'].append('成交金额：中标\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('成交金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('成交金额:\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('.*成交价格：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('成\s*交\s*金\s*额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('成交金额.*小写：￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*）')
ex_rule['w_money']['normal'].append('.*中标、成交金额.*元/年\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元/三年.*')
ex_rule['w_money']['normal'].append('成交金额（人民币/元）.*磋商文件\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*公司')
ex_rule['w_money']['normal'].append('.*成交单价金额：.\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元.*')
ex_rule['w_money']['normal'].append('中标金额（元）.*公司\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
# ex_rule['w_money']['normal'].append('.*主要标的信息.*单价：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('总金额：（元）\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*供应商报价情况')
ex_rule['w_money']['normal'].append('￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*）；')
ex_rule['w_money']['normal'].append('中标金额（元）：.*￥\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元）.*代理服务费')
# ex_rule['w_money']['normal'].append('层\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
# ex_rule['w_money']['normal'].append('楼\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
# ex_rule['w_money']['normal'].append('号\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('报价总金额：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*供应商报价详情')
ex_rule['w_money']['normal'].append('成交总金额\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元')
ex_rule['w_money']['normal'].append('.*第一中标候选人.*投标报价：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)元.*第二中标候选人.*')
ex_rule['w_money']['normal'].append('.*第一中标候选人.*中标价格：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)元.*第二中标候选人.*')
ex_rule['w_money']['normal'].append('中标金额:\s*(.*)\s*元')
ex_rule['w_money'].update({'billion':['.*投标报价：含税：(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)元.*']})
ex_rule['w_money']['billion'].append('.*工程投资：小写：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*亿元.*')
ex_rule['w_money_r'] = {'thousand':['.*中标价（万元）\s*(.*)\s*公告期.*']}
ex_rule['w_money_r'].update({'normal':['.*中标价（元）\s*(.*)\s*公告期.*']})
ex_rule['w_money_r']['normal'].append('.*成交金额（人民币/元）.*磋商文件\s*(.*)\s*4.磋商评审小组成员.*')
# ex_rule['w_money_r']['normal'].append('.*中标金额\s*(.*)\s*元.*')
ex_rule['w_money_r'].update({'billion':['.*中标价（亿）\s*(.*?)\s*公告期.*']})
ex_rule['w_money_c'] = {'thousand':['.*中标价（万元）\s*(.*?)\s*公告期.*']}
ex_rule['w_money_c'].update({'normal':['.*中标金额（美元）：\s*(.*?)\s*元整（.*']})
ex_rule['w_money_c']['normal'].append('(?:成交金额|中标金额|成交价格|中标供应商金额|中标（成交）金额|中标（成交）价格|金额（人民币）|投标价格|成交价款|中标价|成交金额（元）|监理费)(?:￥|¥|:|：|中标|小写|人民币|报价|为)*(?:\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d+[.,，]?\d*|\d+[.,，]?\d+[.,，]?\d+[.,，]?\d+[.,，]?\d*)?(?:人民币（大写）|人民币大写|人民币|大写：人民币|大写：|成交价为人民币)*(?:\(|（)?([一二三四五六七八九壹贰叁肆伍陆柒捌玖拾佰陌仟万亿兆弌弍弎零〇]+?)(?:圆整|元整|元)(?:\)|）)?')
ex_rule['w_money_c']['normal'].append('(?:成交价)(?:.*?)(?:大写)(?::|：)(.*?)(?:圆整|元整|元)')
ex_rule['w_money_c']['normal'].append('.*成交金额：人民币\(大写\)\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*成交金额：人民币\(大写\)\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*成交金额：人民币\(大写\)\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*成交金额：人民币（大写）\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*成交金额：人民币（大写）\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*成交金额：人民币（大写）\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('成交金额: 人民币\s*(.*?)\s*元整')
ex_rule['w_money_c']['normal'].append('成交金额：人民币\s*(.*?)\s*元整')
ex_rule['w_money_c']['normal'].append('.*成交金额：人民币\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*成交金额：￥\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*成交金额：￥\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*成交金额：￥\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*成\s*交\s*金\s*额：\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*成\s*交\s*金\s*额：\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*成\s*交\s*金\s*额：\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*成交金额:\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*成交金额（人民币）：\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标（成交）金额：大写：\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标（成交）金额：人民币\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标（成交）金额人民币\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标（成交）金额人民币\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标（成交）金额：成交价为人民币\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标（成交）金额：\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标（成交）金额：\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标\(成交\)金额：\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：人民币（大写）\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：人民币（大写）\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：人民币（大写）\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：人民币大写\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：人民币大写\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：人民币大写\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标金额[:：]人民币\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额[:：]人民币\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额[:：]人民币\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标金额\(元\)：人民币\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额\(元\)：人民币\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额\(元\)：人民币\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标金额\(元\)：\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额\(元\)：\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额\(元\)：\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标金额（元）：人民币\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额（元）：人民币\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额（元）：人民币\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：大写：人民币\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：大写：人民币\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：大写：人民币\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标金额:大写：\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标金额:大写：\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：.*大写：\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标金额:\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额:\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标金额:\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标价：人民币\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标价：人民币\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标价：\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标价：\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*金额（人民币）:\s*(.*?)\s*圆整.*')
ex_rule['w_money_c']['normal'].append('.*金额（人民币）:\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*金额（人民币）:\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标报价：人民币\s*(.*?)\s*元整.*')
# ex_rule['w_money_c']['normal'].append('.*中标金额：人民币\s*([〇一二三四五六七八九零壹贰叁肆伍陆柒捌玖貮两十拾百佰千仟万萬亿億兆]*)\s*元.*[一二三四五六七八九]、.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：人民币\s*(.*?)\s*元.*[一二三四五六七八九]、.*')
ex_rule['w_money_c']['normal'].append('.*人民币\s*(.*?)\s*（￥.*')
ex_rule['w_money_c']['normal'].append('.*中标金额：\s*(.*?)\s*元整人民币.*')
ex_rule['w_money_c']['normal'].append('.*成交金额大写：\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标价（万元）\s*(.*?)\s*公告期.*')
ex_rule['w_money_c']['normal'].append('.*中标价（元）人民币（大写）\s*(.*?)\s*元整.*')
ex_rule['w_money_c']['normal'].append('.*中标价\s*(.*?)\s*元.*')
ex_rule['w_money_c']['normal'].append('.*中标情况:.*（\s*(.*?)\s*元整）.*')
ex_rule['w_money_c'].update({'billion':['.*中标价（亿）\s*(.*?)\s*公告期.*']})
ex_rule['w_money_s'] = {'thousand':['第[一二三四五六七八九]包：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元']}
ex_rule['w_money_s']['thousand'].append('第[一二三四五六七八九]包\?\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*\(万元\)')
ex_rule['w_money_s']['thousand'].append('[一二三四五六七八九]包[：:]\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*万元')
ex_rule['w_money_s']['thousand'].append('(?:成交价)(?:（万元）|\(万元\)|（万元/优惠率）|（%）)*(?:\s)*([\d、.]*)(?:\s)*(?:\(万元\)|（万元）|受让单位)')
ex_rule['w_money_s']['thousand'].append('(?:合同金额|中标金额|中标（成交）金额|合同总金额|投标价格|中标价|中标总价|投标总价|总中标|成交金额)(?:（万元）|\(万元\)|￥|¥|:|：|中标|小写|人民币|为|总金额|包一|（元/优惠率）|（%）)*([\d、.]*)(?:\s)*(?:[（(]?万元[)）]?)(?!至|以下|以上|以内)')
ex_rule['w_money_s']['thousand'].append('(?:合同金额|中标金额|中标（成交）金额|合同总金额|投标价格|中标价|中标总价|投标总价|总中标|成交金额)(?:￥|¥|:|：|中标|小写|人民币|为|总金额|包一|（元/优惠率）|（%）|\s)*(?:万元|（万元）|\(万元\))(?:￥|¥|:|：|中标|小写|人民币|为|总金额|包一|（元/优惠率）|（%）|\s)*([\d、.]*)(?!\d|至|以下|以上|以内|-)')
ex_rule['w_money_s'].update({'normal':['第[一二三四五六七八九]包：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元']})
ex_rule['w_money_s']['normal'].append('[一二三四五六七八九]包：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*元?（大写')
ex_rule['w_money_s']['normal'].append('(?:标段\d)(?::|：|\s)*([,.\d]*?)(?:\s)*(?:元)')
ex_rule['w_money_s']['normal'].append('(?:中标（成交）金额)(?:\s)*(?:第包\d+)(?::|：|\s)*([,.\d]*?)(?:\s)*(?:元)')
ex_rule['w_money_s']['normal'].append('(?:包[\d一二三四五六七八九十]+)(?::|：|\s|￥)*(?:[^,.\d]{,20})?([,.\d]*?)(?:\s)*(?!万|年)(?:元|（总价）|(?:\d\.)[\u4e00-\u9fa5]|[\u4e00-\u9fa5])') # 多个金额，其中有干扰金额
ex_rule['w_money_s']['normal'].append(r'(?<!例如)(?:合同金额|中标金额|中标（成交）金额|合同总金额|投标价格|中标价|成交价|中标总价|投标总价|总中标|成交金额|总价|最终报价)(?:（元）|\(元\)|￥|¥|:|：|中标|小写|人民币|报价|为|总金额|包一|（元/优惠率）|\(单位：元\)|（人民币/元）|（%）|\s|\\)*([\d、，,.]*)(?:[一二三四五六七八九]|(?:\d\.)[\u4e00-\u9fa5]|\(元\)|（元）|（总价）|元|\s|下浮率|标段\d)')
ex_rule['w_money_s'].update({'billion':['第[一二三四五六七八九]包：\s*(\d*.\d*|\d*.\d*.\d*|\d*.\d*.\d*.\d*|\d*.\d*.\d*.\d*.\d*)\s*亿']})
ex_rule['w_bider'] = ['.*中标单位：\s*(.*?)\s*中标金额：.*']
ex_rule['w_bider'].append('(?:中标单位|供应商名称|中标供应商)(?::|：|\s)*(?:投标人名称|包一|单位名称)(?::|：|\s)*(.*?)(?:中标供应商|单位地址|报价|供应商地址)')
ex_rule['w_bider'].append('(?:中标单位投标人名称|第一中标\(成交\)候选人|中标成交供应商名称|第一成交候选供应商|第一成交候选人|中标供应商名称|供应商名称|成交供应商信息|中标人（供应商）|第一中标候选人|中标（成交）人|第一标段中标人|中标单位名称|成交供应商名称|中标人单位名称|成交供应商|中标候选人名称|中标供应商|中标人名称|成交人名称|成交单位|中标单位|中标人|成交人|中标商|供应商)(?:\s|：|:|企业名称|（乙方）|合同包1|名称|为)*(.+?)(?:;|；|\?)*(?:地址|供应商地址|中标单价总和|中标金额|地址|统一社会信用代码|中标人地址|标的名称|法人代表|中标供应商地址|中标供应商联系地址|中标成交供应商地址|投标报价|联系电话|联系地址|单位|总报价|中标价|中标（成交）金额|供应商组织机构代码|成交金额|联系方式|最终单价|供应商统一社会信用代码|第一中标候选人|第二中标候选人|招标类别|成交报价|主要中标内容|成交供应商|采购数量|组织机构代码证号|报价|成交价|序号一|\s)')
ex_rule['w_bider'].append('(?:中标单位投标人名称|第一中标\(成交\)候选人|中标成交供应商名称|第一成交候选供应商|第一成交候选人|中标供应商名称|供应商名称|成交供应商信息|中标人（供应商）|第一中标候选人|中标（成交）人|第一标段中标人|中标单位名称|成交供应商名称|中标人单位名称|成交供应商|中标候选人名称|中标供应商|中标人名称|成交人名称|成交单位|中标单位|中标人|成交人|中标商|供应商)(?:\s|：|:|企业名称|（乙方）|合同包1|名称|为)*(.+?公司)(?:;|；|\?)*')
ex_rule['w_bider'].append('(?:招标人确定)(.*?)(?:为该项目的中标人)')
ex_rule['w_bider'].append('.*中标供应商：\s*(.*?)\s*中标单价总和：.*')
ex_rule['w_bider'].append('.*中标供应商：\s*(.*?)\s*中标金额：.*')
ex_rule['w_bider'].append('.*中标供应商：\s*(.*?)\s*地址：.*')
ex_rule['w_bider'].append('.*中标供应商：\s*(.*?)\s*统一社会信用代码：.*')
ex_rule['w_bider'].append('.*中标供应商：\s*(.*?)\s*[123456789]\..*')
ex_rule['w_bider'].append('.*中标供应商：\s*(.*?)\s*[123456789]、.*')
ex_rule['w_bider'].append('.*中标人名称:\s*(.*?)\s*中标人地址:.*')
ex_rule['w_bider'].append('.*中标人名称：\s*(.*?)\s*中标人地址：.*')
ex_rule['w_bider'].append('.*中标人名称：\s*(.*?)\s*中标金额：.*')
ex_rule['w_bider'].append('.*中标人名称：\s*(.*?)\s*[一二三四五六七八九]、.*')
ex_rule['w_bider'].append('.*中标人名称\s*(.*?)\s*标的名称.*')
ex_rule['w_bider'].append('.*中标人名称\s*(.*?)\s*地\s*址.*')
ex_rule['w_bider'].append('.*中标供应商名称\s*(.*?)\s*法人代表.*')
ex_rule['w_bider'].append('.*中标供应商名称：\s*(.*?)\s*中标供应商地址：.*')
ex_rule['w_bider'].append('.*中标供应商名称：\s*(.*?)\s*中标供应商联系地址：.*')
ex_rule['w_bider'].append('.*中标成交供应商名称：\s*(.*?)\s*中标成交供应商地址：.*')
ex_rule['w_bider'].append('.*中标供应商名称：\s*(.*?)\s*联系地址：.*')
ex_rule['w_bider'].append('.*中标供应商名称：\s*(.*?)\s*中标金额：.*')
ex_rule['w_bider'].append('.*中标供应商名称：\s*(.*?)\s*中标价：.*')
ex_rule['w_bider'].append('.*中标供应商名称:\s*(.*?)\s*中标（成交）金额.*')
ex_rule['w_bider'].append('.*中标供应商名称:\s*(.*?)\s*中标金额.*')
ex_rule['w_bider'].append('.*中标供应商名称\s*(.*?)\s*中标供应商地址.*')
ex_rule['w_bider'].append('.*中标供应商\s*(.*?)\s*成交金额.*')
ex_rule['w_bider'].append('.*中标供应商\s*(.*?)\s*联系方式.*')
ex_rule['w_bider'].append('.*中标供应商\s*(.*?)\s*中标供应商地址.*')
ex_rule['w_bider'].append('.*中标商：\s*(.*?)\s*中标金额：.*')
ex_rule['w_bider'].append('.*磋商申请人名称：\s*(.*?)\s*磋商申请人地址：.*')
ex_rule['w_bider'].append('.*供应商名称：\s*(.*?)\s*;?供应商地址：.*')
ex_rule['w_bider'].append('.*供应商名称：\s*(.*?)\s*供应商地点：.*')
ex_rule['w_bider'].append('.*供应商名称：\s*(.*?)\s*;?供应商地址.*')
ex_rule['w_bider'].append('.*供应商名称：\s*(.*?)\s*;?供应商统一社会信用代码：.*')
ex_rule['w_bider'].append('.*供应商名称:\s*(.*?)\s*成交金额:.*')
ex_rule['w_bider'].append('.*供应商名称:\s*(.*?)\s*供应商地址：.*')
ex_rule['w_bider'].append('.*供应商名称：\s*(.*?)\s*供应商地：.*')
ex_rule['w_bider'].append('.*供应商名称:\s*(.*?)\s*供应商地址:.*')
ex_rule['w_bider'].append('.*供应商名称\s*(.*?)\s*；?供应商地址.*')
ex_rule['w_bider'].append('.*中标单位名称：\s*(.*?)\s*统一社会信用代码：.*')
ex_rule['w_bider'].append('.*中标单位：\s*(.*?)\s*投标报价：.*')
ex_rule['w_bider'].append('.*中标单位：\s*(.*?)\s*中标金额：.*')
ex_rule['w_bider'].append('.*中标单位：\s*(.*?)\s*中标价格：.*')
ex_rule['w_bider'].append('.*中标单位：\s*(.*?)\s*中标总价：.*')
ex_rule['w_bider'].append('.*中标单位：\s*(.*?)\s*中标价：.*')
ex_rule['w_bider'].append('.*中标单位：\s*(.*?)\s*企业注册地址：.*')
ex_rule['w_bider'].append('.*中标单位：\s*(.*?)\s*中标人地址：.*')
ex_rule['w_bider'].append('.*中标单位：\s*(.*?)\s*中标单位地址：.*')
ex_rule['w_bider'].append('.*中标单位：\s*(.*?)\s*中标范围：.*')
ex_rule['w_bider'].append('.*中标单位：\s*(.*?)\s*地\s*址：.*')
ex_rule['w_bider'].append('.*中标单位:\s*(.*?)\s*（?地\s*址：.*')
ex_rule['w_bider'].append('.*中标单位\s*(.*?)\s*投标报价（万元）.*')
ex_rule['w_bider'].append('.*中标单位\s*(.*?)\s*招标类别.*')
ex_rule['w_bider'].append('.*中标单位名称\s*(.*?)\s*中标单位地址.*')
ex_rule['w_bider'].append('.*中标单位名称\s*(.*?)\s*地\s*址.*')
ex_rule['w_bider'].append('.*评标结果.*中标候选人:\s*(.*?)\s*中标金额：.*')
ex_rule['w_bider'].append('.*中标供应商名称: \s*(.*?)\s*法人代表:.*')
ex_rule['w_bider'].append('.*推荐成交供应商\s*(.*?)\s*地址.*')
ex_rule['w_bider'].append('.*中标（成交）信息：.*供应商名称：\s*(.*?)\s*供应商联系人：.*')
ex_rule['w_bider'].append('.*中标（成交）信息：.*供应商名称：\s*(.*?)\s*供应商地址：.*')
ex_rule['w_bider'].append('.*中标（成交）信息.*供应商名称：\s*(.*?)\s*供应商地址：.*')
ex_rule['w_bider'].append('.*中标（成交）供应商：\s*(.*?)\s*中标（成交）金额：.*')
ex_rule['w_bider'].append('.*中标、成交供应商名称:\s*(.*?)\s*法人代表:.*')
ex_rule['w_bider'].append('.*中标供应商：.*供应商名称：\s*(.*?)\s*详细地址：.*')
ex_rule['w_bider'].append('.*中标/成交供应商名称：\s*(.*?)\s*地址：.*')
ex_rule['w_bider'].append('.*中标人（公司名称）：\s*(.*?)\s*中标金额.*')
ex_rule['w_bider'].append('.*中标人：\s*(.*?)\s*中标下浮率：.*')
ex_rule['w_bider'].append('.*中\s*标\s*人：\s*(.*?)\s*，?中标金额：.*')
ex_rule['w_bider'].append('.*中标人：\s*(.*?)\s*中标总价：.*')
ex_rule['w_bider'].append('.*中标人[：:]\s*(.*?)\s*中标价格[：:].*')
ex_rule['w_bider'].append('.*中标人：\s*(.*?)\s*中标价：.*')
ex_rule['w_bider'].append('.*中标人：\s*(.*?)\s*中标报价.*')
ex_rule['w_bider'].append('.*中标人：\s*(.*?)\s*资质等级：.*')
ex_rule['w_bider'].append('.*中标人：\s*(.*?)\s*中标人地址：.*')
ex_rule['w_bider'].append('.*中标人：\s*(.*?)\s*投标报价：.*')
ex_rule['w_bider'].append('.*中标人：\s*(.*?)\s*（?地址.*')
ex_rule['w_bider'].append('.*中标人：\s*(.*?)\s*；?统一社会信用代码：.*')
ex_rule['w_bider'].append('.*中标人：\s*(.*?)\s*[一二三四五六七八九]\．.*')
ex_rule['w_bider'].append('.*中标人：\s*(.*?)\s*[一二三四五六七八九]、.*')
ex_rule['w_bider'].append('.*中标人\s*(.*?)\s*中标价(元).*')
ex_rule['w_bider'].append('.*中标人\s*(.*?)\s*中标价.*')
ex_rule['w_bider'].append('.*成交人名称：\s*(.*?)\s*成交人地址：.*')
ex_rule['w_bider'].append('.*成交人名称\s*(.*?)\s*成交人地址.*')
ex_rule['w_bider'].append('.*成交人：\s*(.*?)\s*成交金额：.*')
ex_rule['w_bider'].append('.*成交人：\s*(.*?)\s*地\s址：.*')
ex_rule['w_bider'].append('.*成交人：\s*(.*?)\s*成交人地址：.*')
ex_rule['w_bider'].append('.*成交供应商名称：\s*(.*?)\s*成交供应商地址：.*')
ex_rule['w_bider'].append('.*成交供应商名称：\s*(.*?)\s*成交供应商联系人：.*')
ex_rule['w_bider'].append('.*成交供应商名称：\s*(.*?)\s*成交金额：.*')
ex_rule['w_bider'].append('.*成交供应商名称:\s*(.*?)\s*成交供应商地址:.*')
ex_rule['w_bider'].append('.*成交供应商名称\s*(.*?)\s*成交供应商联系人.*')
ex_rule['w_bider'].append('.*成交供应商名称\s*(.*?)\s*成交供应商电话.*')
ex_rule['w_bider'].append('.*成交供应商名称\s*(.*?)\s*企业代码.*')
ex_rule['w_bider'].append('.*成交供应商：\s*(.*?)\s*最终报价：.*')
ex_rule['w_bider'].append('.*成交供应商：\s*(.*?)\s*成交价：.*')
ex_rule['w_bider'].append('.*成交供应商：\s*(.*?)\s*地址：.*采购人、代理机构名称及联系方式.*')
ex_rule['w_bider'].append('.*成交供应商：\s*(.*?)\s*采购单位联系人：.*')
ex_rule['w_bider'].append('.*成交供应商：\s*(.*?)\s*地\s*址：.*')
ex_rule['w_bider'].append('.*成交供应商：\s*(.*?)\s*成交折扣：.*')
ex_rule['w_bider'].append('.*成交供应商：\s*(.*?)\s*，?成交供应商地址：.*')
ex_rule['w_bider'].append('.*成交供应商：\s*(.*?)\s*供应商地址：.*')
ex_rule['w_bider'].append('.*成交供应商：\s*(.*?)\s*\d、.*')
ex_rule['w_bider'].append('.*成交供应商:\s*(.*?)\s*成交价:.*')
ex_rule['w_bider'].append('.*成交供应商:\s*(.*?)\s*\d\.成交供应商地址：.*')
ex_rule['w_bider'].append('.*成交候选人：\s*(.*?)\s*成交金额:.*')
ex_rule['w_bider'].append('.*成交供应商\s*(.*?)\s*[一二三四五六七八九]、.*')
ex_rule['w_bider'].append('.*成交供应商信息：.*名称:\s*(.*?)\s*,?联系人:.*')
ex_rule['w_bider'].append('.*成交单位\s*(.*?)\s*成交单位地址.*')
ex_rule['w_bider'].append('.*成交单位：\s*(.*?)\s*地\s*址：.*')
ex_rule['w_bider'].append('.*成交结果：\s*(.*?)\s*为本项目预成交供应商.*')
ex_rule['w_bider'].append('.*服务商名称：\s*(.*?)\s*服务商地址：.*')
ex_rule['w_bider'].append('.*中标结果：1.\s*(.*?)\s*，中标下浮率.*')
ex_rule['w_bider'].append('.*中标结果：第一名：\s*(.*?)\s*第二名：.*')
ex_rule['w_bider'].append('.*中标信息.*1.名称：\s*(.*?)\s*2\.地址：.*')
ex_rule['w_bider'].append('.*中标信息.*1.名称：\s*(.*?)\s*\d\.*.*')
ex_rule['w_bider'].append('.*投标人名称：\s*(.*?)\s*投标人地址：.*')
ex_rule['w_bider'].append('.*供应商（乙方）：\s*(.*?)\s*地\s*址：.*')
ex_rule['w_bider'].append('.*供应商：\s*(.*?)\s*中标金额：.*')
ex_rule['w_bider'].append('.*供应商：\s*(.*?)\s*；?\s*成交金额：.*')
ex_rule['w_bider'].append('.*竞标单位名称：\s*(.*?)\s*竞标单位地址：.*')
ex_rule['w_bider'].append('.*中标候选人名称：\s*(.*?)\s*中标候选人地址：.*')
ex_rule['w_bider'].append('.*推荐的中标候选人：\s*(.*?)\s*中标价：.*')
ex_rule['w_bider'].append('.*第一中标候选人：\s*(.*?)\s*投标总报价：.*')
ex_rule['w_bider'].append('.*第一中标候选人：\s*(.*?)\s*投标报价：.*')
ex_rule['w_bider'].append('.*第一中标候选人：\s*(.*?)\s*，?报价：.*')
ex_rule['w_bider'].append('.*第一中标候选人：\s*(.*?)\s*中标金额：.*')
ex_rule['w_bider'].append('.*第一中标候选人：\s*(.*?)\s*（联合体成员：.*')
ex_rule['w_bider'].append('.*第一中标候选人:\s*(.*?)\s*（得分：.*')
ex_rule['w_bider'].append('.*中标候选人：\s*(.*?)\s*报价：.*')
ex_rule['w_bider'].append('.*第一成交候选人：\s*(.*?)\s*地\s*址：.*')
ex_rule['w_bider'].append('.*第一成交候选人:\s*(.*?)\s*成交金额：.*')
ex_rule['w_bider'].append('.*第一中标\(成交\)候选人:\s*(.*?)\s*中标\(成交\)金额：.*')
ex_rule['w_bider'].append('.*中标（成交）人：\s*(.*?)\s*中标（成交）价（投标总价）：.*')
ex_rule['w_bider'].append('.*第一标段中标人：\s*(.*?)\s*总价.*')
ex_rule['w_bider'].append('.*第一成交候选供应商：\s*(.*?)\s*；?成交报价：.*')
ex_rule['w_bider'].append('.*第一名：\s*(.*?)\s*报价：.*')
ex_rule['w_bider'].append('.*中标银行：\s*(.*?)\s*一年期定期存款年利率.*')
ex_rule['content'] = ['//div[@class="vT_detail_content w760c"]//text()']
ex_rule['content'].append('//div[@class="vF_detail_content_container"]//text()')
ex_rule['content'].append('//div[@class="vF_detail_content"]//text()')
ex_rule['content'].append('//div[@class="vT_detail_main"]//text()')
ex_rule['content'].append('//div[@class="vT_z w100"]//text()')
ex_rule['content'].append('//div[@class="ewb-details-info"]//text()')
ex_rule['content'].append('//div[@class="pubtable"]//text()')
ex_rule['content'].append('//div[@class="package_lines layoutfix"]//text()')
ex_rule['content'].append('//form[@name="Frm_Order"]/table/tr/td/text()')
ex_rule['content'].append('//tr[@class="bk5"]//text()')
ex_rule['content'].append('//script[@id="container"]//text()')
ex_rule['content'].append('//table[@width="85%"]/tr/td/text()')
ex_rule['content'].append('//table[@class="tableBorder"]/tr/td//text()')
ex_rule['content'].append('//table[@style="width: 260mm;"]//text()')
ex_rule['content'].append('//table[@id="tblInfo"]//text()')
ex_rule['content'].append('//div[@style="line-height:25px"]//text()')
ex_rule['content'].append('//div[@id="slywxl1"]//text()')
ex_rule['content'].append('//div[@id="fontzoom"]//text()')
ex_rule['content'].append('//div[@id="printArea"]//text()')
ex_rule['content'].append('//div[@id="template"]//text()')
ex_rule['content'].append('//div[@id="jjDiv"]//text()')
ex_rule['content'].append('//div[@class="box_content"]//text()')
ex_rule['content'].append('//div[@class="ewb-copy"]//text()')
ex_rule['content'].append('//div[@class="content-right-details-content"]//text()')
ex_rule['content'].append('//div[@class="detail"]//text()')
ex_rule['content'].append('//div[@class="detail_contect"]//text()')
ex_rule['content'].append('//div[@class="cont-info"]//text()')
ex_rule['content'].append('//div[@class="fully"]//text()')
ex_rule['content'].append('//table[@class="gycq-table"]//text()')
ex_rule['content'].append('//div[@class="cont"]//text()')
ex_rule['content'].append('//div[@class="infodetail"]//text()')
ex_rule['content'].append('//div[@class="content"]//text()')
ex_rule['content'].append('//div[@class="content-inner"]//text()')
ex_rule['content'].append('//div[@class="content-right-content"]//text()')
ex_rule['content'].append('//table[@class="hei_text"]//text()')
ex_rule['content'].append('//div[@class="zt-child"]//text()')
ex_rule['content'].append('//div[@class="clearfix"]//text()')
ex_rule['content'].append('//div[@class="WordSection1"]//text()')
ex_rule['content'].append('//div[@class="cont"]//text()')
ex_rule['content'].append('//div[@class="cs_two_box_fk"]//text()')
ex_rule['content'].append('//div[@class="vT_detail_content w100c"]//text()')
# ex_rule['content'].append('//div[@id="createForm"]//text()')
ex_rule['content'].append('//div[@style="text-align: center; font-size: 22pt;"]//text()')
ex_rule['content'].append('//div[@id="divArtice"]//text()')
ex_rule['content'].append('//div[@class="ewb-article-info"]//text()')
ex_rule['content'].append('//div[@class="zx-xxxqy-nr"]//text()')
ex_rule['content'].append('//div[@id="xiangqingneiron"]//text()')
ex_rule['content'].append('//div[@id="div_zhengwen"]//text()')
ex_rule['content'].append('//div[@id="y_detail_con"]//text()')
ex_rule['content'].append('//div[@class="content"]//div[@id="content"]//text()')
ex_rule['content'].append('//div[@class="you"]//text()')
ex_rule['content'].append('//div[@class="art_con"]//text()')
ex_rule['content'].append('//div[@class="div-article2"]//text()')
ex_rule['content'].append('//div[@class="ewb-left-bd"]//text()')
ex_rule['content'].append('//div[@class="body_main"]//text()')
ex_rule['content'].append('//div[@class="frameNews"]//text()')
ex_rule['content'].append('//div[@class="ewb-art-bd"]//text()')
ex_rule['content'].append('//div[@class="content-box-1"]//text()')
ex_rule['content'].append('//div[@class="view TRS_UEDITOR trs_paper_default trs_web"]//text()')
ex_rule['content'].append('//div[@class="epoint-article-content jynr news_content"]//text()')
ex_rule['content'].append('//table[@id="2020_VERSION"]//text()')
ex_rule['content'].append('//div[@id="myPrintArea"]//table//text()')
ex_rule['content'].append('//div[@class="content_scroll"]//text()')
ex_rule['content'].append('//div[@class="article-info"]//text()')
ex_rule['content'].append('//div[@class="xiangxiyekuang"]//text()')
ex_rule['content'].append('//td[@id="zfcg_zbgs1_TDContent"]//text()')
ex_rule['content'].append('//td[@id="zfcg_zbgg1_TDContent"]//text()')
ex_rule['content'].append('//div[@id="print-content"]//text()')
ex_rule['content'].append('//div[@id="mainContent"]//text()')
ex_rule['content'].append('//div[@id="contentDiv"]//text()')
ex_rule['content'].append('//div[@id="tab-1"]//text()')
ex_rule['content'].append('//div[@id="Zoom"]//*[name(.)!="style"]//text()')
ex_rule['content'].append('//table[@class="Content"]//text()')
ex_rule['content'].append('//table[@id="tab"]//text()')
ex_rule['content'].append('//div[@class="nei03_02"]//text()')
ex_rule['content'].append('//div[@class="ewb-info-bd"]//text()')
ex_rule['content'].append('//div[@class="article-list2"]//text()')
ex_rule['content'].append('//div[@class="frame_list01"]/table//text()')
# ex_rule['content'].append('//div[@class="content03"]//text()')
# ex_rule['content'].append('//div[@class="newsCon"]//td[@width="436"]//text()')
# ex_rule['content'].append('//input/value()')
ex_rule['content'].append('//div[@class="newsCon"]//text()')
ex_rule['content'].append('//div[@class="ewb-trade-right l"]//text()')
ex_rule['content'].append('//div[@class="xxej"]//text()')
ex_rule['content'].append('//div[@class="left_content"]//text()')
ex_rule['content'].append('//div[@class="neirong"]//text()')
ex_rule['content'].append('//div[@id="noticeArea"]//text()')
ex_rule['content'].append('//div[@id="detailNeirong"]//text()')
# ex_rule['content'].append('//div[@class="content"]//text()')
ex_rule['content'].append('//div[@class="notice-con"]//text()')
ex_rule['content'].append('//div[@class="easysite-news-text"]//text()')
ex_rule['content'].append('//div[@class="con_row"]//text()')
ex_rule['content'].append('//div[@class="detail_contect"]//text()')
ex_rule['content'].append('//div[@class="news-xq"]//text()')
ex_rule['content'].append('//div[@class="xly"]//text()')
ex_rule['content'].append('//div[@class="ewb-notice-bd"]//text()')
ex_rule['content'].append('//div[@class="detail_con"]//text()')
ex_rule['content'].append('//div[@align="left"]//text()')
ex_rule['content'].append('//div[@class="row"]//text()')
ex_rule['content'].append('//div[@class="zw_c_c_cont"]//text()')
ex_rule['content'].append('//body//table//text()')
ex_rule['content'].append('//td[@bgcolor="#FFFFFF" and @align="center"]//text()')
ex_rule['content'].append('//table[@width="1000"]/tr/td//text()')
ex_rule['content'].append('/html/body/table[4]/tr/td/table/tr/td[2]/table/tr[2]/td/table/tr[2]/td[2]/table//text()')
ex_rule['title'] = ['//div[@class="vF_detail_header"]/h2/text()']
ex_rule['title'].append('//div[@class="vT_detail_header"]/h2/text()')
ex_rule['title'].append('//div[@class="pages_title"]/text()')
ex_rule['title'].append('//h3[@class="article-title"]/text()')
ex_rule['title'].append('//div[@class="content-title"]/text()')
# ex_rule['title'].append('//table[@bgcolor="F2F7FB"]/tr/td/h3/text()')
ex_rule['title'].append('//table/tr/td[@class="font_biao1"]/text()')
ex_rule['title'].append('//td[@align="center"]/h3/text()')
ex_rule['title'].append('//div[@id="title-box"]//text()')
# ex_rule['title'].append('//td[@align="center",bgcolor="#d0e7f5"]//text()')
ex_rule['title'].append('//td[@class="STYLE1"]/text()')
ex_rule['title'].append('//td[@id="tdTitle"]//b/text()')
ex_rule['title'].append('//div[@class="fully"]/h4/text()')
ex_rule['title'].append('//div[@class="detail"]/h4/text()')
ex_rule['title'].append('//div[@id="mycontent"]//p/text()')
# ex_rule['title'].append('//table[@class="tableBorder"]/tr/td/text()')
ex_rule['title'].append('//div[@id="slywxl2"]/h1/text()')
ex_rule['title'].append('//div[@id="detailTitle1"]/text()')
ex_rule['title'].append('//div[@class="bodytop"]/h2/text()')
ex_rule['title'].append('//div[@class="title-box"]/p/text()')
ex_rule['title'].append('//div[@class="headline"]/p/text()')
ex_rule['title'].append('//span[@id="project_name"]/text()')
ex_rule['title'].append('//div[@class="content-right-details-top"]/span/text()')
ex_rule['title'].append('//div[@style="text-align: center;margin:28px 0 28px 0;"]/span/text()')
ex_rule['title'].append('//div[@class="content-right-details-title"]/text()')
ex_rule['title'].append('//div[@class="details_page"]/p/text()')
ex_rule['title'].append('//div[@class="xl-box-t"]/././text()')
ex_rule['title'].append('//div[@id="divArtice"]/h3/text()')
# ex_rule['title'].append('//table[@width="930"]//span[@class="txt2"]/text()')
ex_rule['title'].append('//span[@class="txt2"]/text()')
ex_rule['title'].append('//span[@id="lblNoticeTitle"]/text()')
ex_rule['title'].append('//div[@style="xnrx"]/div/h3/text()')
ex_rule['title'].append('//div[@class="art_con"]//div[1]//h2[1]/span/text()')
ex_rule['title'].append('//div[@class="zw_c_c_title"]/text()')
ex_rule['title'].append('//div[@class="content-box"]/h2/text()')
ex_rule['title'].append('//div[@class="listConts"]/h1/text()')
ex_rule['title'].append('//div[@class="div-title"][1]/text()')
ex_rule['title'].append('//div[@class="content-title"]/text()')
ex_rule['title'].append('//div[@class="xiangxiyebiaoti"]//text()')
ex_rule['title'].append('//h2[@class="ewb-con-h"]/text()')
ex_rule['title'].append('//h2[@class="ewb-trade-h"]/text()')
ex_rule['title'].append('//h2[@class="ewb-art-hd"]/text()')
ex_rule['title'].append('//h2[@class="title_con"]/text()')
ex_rule['title'].append('//h2[@class="detailed-title"]/text()')
ex_rule['title'].append('//h2[@class="title"]/text()')
ex_rule['title'].append('//h2[@class="ewb-info-tt"]/text()')
ex_rule['title'].append('//h2[@class="tc"]/text()')
ex_rule['title'].append('//h2[@class="sd"]/text()')
ex_rule['title'].append('//h2[@class="ewb-info-title"]/text()')
ex_rule['title'].append('//h2[@class="sd"]/font/text()')
ex_rule['title'].append('//h2[@id="titlecontent"]/text()')
ex_rule['title'].append('//h3[@class="ewb-article-tt"]/text()')
ex_rule['title'].append('//h3[@class="detail_t"]/text()')
ex_rule['title'].append('//h3[@id="title"]/text()')
ex_rule['title'].append('//h1[@class="content-tit"]/text()')
ex_rule['title'].append('//h1[@id="sign_title"]/text()')
ex_rule['title'].append('//h1[@class="ewb-left-tt"]/text()')
ex_rule['title'].append('//h1[@class="h-title"]/text()')
ex_rule['title'].append('//h6[@class="title"]/text()')
ex_rule['title'].append('//div[@class="article-info"]/h1//text()')
ex_rule['title'].append('//div[@class="flfg"]/h2/text()')
ex_rule['title'].append('//div[@id="jjDiv"]//strong/text()')
ex_rule['title'].append('//div[@id="print-content"]/h1/text()')
ex_rule['title'].append('//div[@id="onprint-title"]/h4/text()')
ex_rule['title'].append('//div[@class="row"]/div[2]/table/tr[1]/td//text()')
ex_rule['title'].append('//div[@class="newsTex"]/h1/text()')
ex_rule['title'].append('//div[@class="dtit"]/h1/text()')
ex_rule['title'].append('//div[@class="easysite-news-title"]/h2/text()')
ex_rule['title'].append('//div[@class="notice-hear"]/h2/text()')
ex_rule['title'].append('//span[@class="customize__projectName"]/text()')
ex_rule['title'].append('//table[@class="infro_table"]//h4/text()')
ex_rule['title'].append('//table[@class="infro_table"]/tr/th/h2/text()')
ex_rule['title'].append('//div[@style="line-height:25px"]/p[@align="center"]/text()')
ex_rule['title'].append('//h1/text()')
ex_rule['title'].append('//div[@style="line-height:35px; font-size:25px; font-weight:bold; text-align:center; min-height:40px; margin-bottom:10px;"]/text()')
ex_rule['title'].append('//div[@class=" editcon"]/p[@style="text-align: center;"]/span/span/text()')
ex_rule['title'].append('//div[@class="biaottt"]/text()')
ex_rule['title'].append('//div[@class="title"]/h3/text()')
ex_rule['title'].append('//td/p[1]//font[@size="+0"]/span/text()')
ex_rule['title'].append('//div[@class="zx-xxxqy"]/h2/text()')
ex_rule['title'].append('//div[@class="frameNews"]/h1/text()')
ex_rule['title'].append('//div[@class="reportTitle"]/h1/text()')
ex_rule['title'].append('//div[@class="cont-info"]//h1[1]/text()')
ex_rule['title'].append('//h2[@class="package_headline layoutfix"]/text()')
ex_rule['title'].append('//tr[@class="bk5"]//div[@align="center"]/h2/text()')
ex_rule['title'].append('//div[@class="title"]/text()')
ex_rule['title'].append('//h2[@class="title"]/text()')
ex_rule['title'].append('//div[@id="center"]/h2/text()')
ex_rule['title'].append('//p[@class="cs_title_P1"]//text()')
ex_rule['title'].append('//p[@class="info-title-especially"]//text()')
ex_rule['title'].append('//body[@class="view"]/header/h1/text()')
# ex_rule['title'].append('//p[@align="center"]//text()')
ex_rule['title'].append('//p[@class="mtt_01"]/text()')
# ex_rule['title'].append('//td[@colspan="2"]/div/text()')
ex_rule['title'].append('//h2/span/h2/text()')
# ex_rule['title'].append('parent\.document\.title=\'(.*?)\';\}')
ex_rule['title'].append('//table/tr/td/h1/text()')
ex_rule['title'].append('//table/tr/td/span/text()')
ex_rule['title'].append('//input[@name="UnitId"]/parent::div/text()')
ex_rule['title'].append('//tr[@class="tr1"]//td[@width="45%"]/span/text()')
# ex_rule['title'] = {'ccgp.gov.cn':['//div[@class="vF_detail_header"]/h2/text()']}
# ex_rule['title'].update({'zycg.gov.cn':['//div[@class="pages_title"]/text()']})
# ex_rule['title'].update({'http://txzb.miit.gov.cn/':['//div[@class="pages_title"]/text()']})
# ex_rule['title'].update({'http://txzb.miit.gov.cn/':['//div[@class="pages_title"]/text()']})
# ex_rule['title'].update({'http://txzb.miit.gov.cn/':['//div[@class="pages_title"]/text()']})
# ex_rule['title'].update({'http://txzb.miit.gov.cn/':['//div[@class="pages_title"]/text()']})
ex_rule['title_html'] = ['parent\.document\.title=\'(.*?)\';\}']
ex_rule['title_content'] = ['.*公示名称(.*?)发布时间.*']
ex_rule['title_content'].append('.*中标业绩详情(.*?)招标人.*')
ex_rule['title_content'].append('.*工程名称(.*?)建设单位.*')
ex_rule['title_content'].append('.*工程名称(.*?)建设地点.*')
ex_rule['title_content'].append('.*招标公告名称：(.*?)招标公告编号：.*')
ex_rule['title_content'].append('.*公示名称：(.*?)公示编号：.*')
ex_rule['title_content'].append('.*标段\(包\)(.*?)所属行业：.*')
ex_rule['title_content'].append('.*\s(.*?)1.招标条件.*')
ex_rule['title_content'].append('.*原公告内容：(.*?)1.招标条件.*')
ex_rule['title_content'].append('.*】(.*?)1．招标条件.*')
ex_rule['title_content'].append('.*[招标,中标,更正,公开招标,竞争性谈判]公告')
ex_rule['date'] = ['.*公告时间：(.*?)项目名称：.*']
# ex_rule['date'].append('\d{2,4}年\d{1,2}月\d{1,2}日')
ex_rule['date'].append('.*招标公告发布日期(.*?)三、开标日期.*')
ex_rule['date'].append('.*更正日期：(.*?)原公告项目名称：.*')
ex_rule['date'].append('.*更公告日期：(.*?)变更事项：.*')
ex_rule['date'].append('.*原公告日期：(.*?)变更公告日期：.*')
ex_rule['date'].append('.*发布日期：(.*?) .*')
ex_rule['date'].append('.*发布日期：(.+)')
ex_rule['date'].append('.*中标日期：(.*?) .*')
ex_rule['date'].append('.*公示开始时间(.*?) .*')
ex_rule['date'].append('.*挂牌起始日期(.*?)挂牌截止日期.*')
ex_rule['date'].append('.*时间：(.*?)至.*')
ex_rule['date'].append('.*请于(.*?)至.*')
ex_rule['date'].append('\d{4}年\d{2}月\d{2}日')
ex_rule['date'].append('\d{4}-\d{2}-\d{2}')
ex_rule['date_html'] = ['//div[@class="vF_detail_header"]/p/span[@id="pubTime"]/text()']
ex_rule['date_html'].append('//div[@class="ewb-bar-info"]/text()')
ex_rule['date_html'].append('//div[@id="detailTime"]/text()')
ex_rule['date_html'].append('//p[@class="infotime"]/text()')
ex_rule['date_html'].append('//p[@class="title_p"]/text()')
ex_rule['date_html'].append('//p[@class="easysite-news-describe"]/text()')
ex_rule['date_html'].append('//td[@class="txt7"]/span/text()')
ex_rule['date_html'].append('//p[@class="p_o"]/span/text()')
ex_rule['date_html'].append('//p[@class="detailed-desc"]/span/text()')
ex_rule['date_html'].append('//p[@class="cs_title_P3"]//text()')
ex_rule['date_html'].append('//p[@class="kdg"]/text()')
ex_rule['date_html'].append('//p[@class="info"]/span/text()')
ex_rule['date_html'].append('//td[@id="tdTitle"]//font[@class="webfont"]/text()')
ex_rule['date_html'].append('//span[@id="pubTime"]/text()')
ex_rule['date_html'].append('//span[@id="f_noticeTime"]/text()')
ex_rule['date_html'].append('//span[@id="scene_sign_start"]/text()')
ex_rule['date_html'].append('//span[@id="lblnoticePubDate"]/text()')
ex_rule['date_html'].append('//span[@style="padding-right:50px"]/text()')
ex_rule['date_html'].append('//span[@class="datetime"]/text()')
ex_rule['date_html'].append('//h3[@class="wzxq"]/span/text()')
ex_rule['date_html'].append('//h3[@class="wzxq"]/text()')
ex_rule['date_html'].append('//em[@class="red"]/text()')
ex_rule['date_html'].append('//time[@pubdate="pubdate"]//text()')
ex_rule['date_html'].append('//div[@class="bodytop"]/div[1]/text()')
ex_rule['date_html'].append('//div[@class="div-title2"]/text()')
ex_rule['date_html'].append('//div[@class="info-source"]/text()')
ex_rule['date_html'].append('//div[@class="feed-time"]/text()')
ex_rule['date_html'].append('//div[@class="ewb-details-sub"]/text()')
ex_rule['date_html'].append('//div[@class="content-title2"]/span/text()')
ex_rule['date_html'].append('//div[@class="ewb-left-info"]/text()')
ex_rule['date_html'].append('//div[@class="tip"]/span/text()')
ex_rule['date_html'].append('//div[@class="ewb-trade-info"]/text()')
ex_rule['date_html'].append('//div[@class="biaotq"]/text()')
ex_rule['date_html'].append('//div[@class="xiangxidate"]//text()')
ex_rule['date_html'].append('//div[@class="ewb-article-sources"]/text()')
ex_rule['date_html'].append('//div[@class="ewb-info-intro"]//text()')
ex_rule['date_html'].append('//div[@class="ewb-info-intro"]/span/text()')
ex_rule['date_html'].append('//div[@class="art-box l"]/text()')
ex_rule['date_html'].append('//div[@class="title-time"]/div/p/span/text()')
ex_rule['date_html'].append('//div[@class="ty-p1"]/span[3]/text()')
ex_rule['date_html'].append('//div[@class="ewb-title-info"]/span[1]/text()')
ex_rule['date_html'].append('//div[@class="TxtCenter BorderTopDot Gray "]//span[2]/text()')
ex_rule['date_html'].append('//div[@class="mtt"]/p[2]/text()')
ex_rule['date_html'].append('//div[@class="info-box"]/span/text()')
ex_rule['date_html'].append('//div[@class="ty-p1"]//span[1]/text()')
ex_rule['date_html'].append('//div[@class="property"]//span[2]/text()')
ex_rule['date_html'].append('//div[@class="zw_c_c_qx"]/p/span[3]/text()')
ex_rule['date_html'].append('//div[@class="zw_c_c_qx"]/p/span[2]/text()')
ex_rule['date_html'].append('//div[@class="source"]/span/text()')
ex_rule['date_html'].append('//div[@class="reportTitle"]//span/text()')
ex_rule['date_html'].append('//div[@class="cont-info"]//p[@class="time"]/text()')
ex_rule['date_html'].append('//div[@class="project-number"]//span/text()')
ex_rule['date_html'].append('//div[@class="notice-hear"]//span[3]/text()')
ex_rule['date_html'].append('//div[@class="art_info"]/span/text()')
ex_rule['date_html'].append('//div[@class="you"]/div/div/div[2]/text()')
ex_rule['date_html'].append('//div[@class="article-info"]/text()')
ex_rule['date_html'].append('//div[@class="ewb-main-bar"]/text()')
ex_rule['date_html'].append('//font[@class="webfont"]//text()')
ex_rule['date_html'].append('//div[@class="TxtCenter BorderTopDot Gray "]//span[3]/text()')
ex_rule['date_html'].append('//div[@class="content-right-details-info"]/text()')
ex_rule['date_html'].append('//div[@class="art_con"]/div[1]/div[1]/span[1]//text()')
ex_rule['date_html'].append('//span[@class="time"]/text()')
ex_rule['date_html'].append('//tr[@class="tr1"]/td[4]//text()')
ex_rule['date_html'].append('//td[@height="20" and @class="Font9" and contains(text(),"时间")]/text()')
ex_rule['date_html'].append('//*[@id="ef_region_inqu"]/div[1]/table/tr[3]/td')
ex_rule['date_html'].append('//td[@style="font-weight:bold;font-size:12px;padding-right:10px;"]/text()[2]')
ex_rule['date_html'].append('/html/body/div[3]/div/div[2]/div[2]/div/div/div[1]/p/text()[1]')
ex_rule['pro'] = ['.*评标专家：(.*?)四、中标结果：.*']
ex_rule['pro'].append('.*评审专家：(.*?)11、.*')
ex_rule['pro'].append('.*评审专家：(.*?)12、.*')
ex_rule['pro'].append('.*评审专家：(.*?)13、.*')
ex_rule['pro'].append('.*评审专家：(.*?)14、.*')
ex_rule['pro'].append('.*评审专家：(.*?)15、.*')
ex_rule['pro'].append('.*评审专家：(.*?)[123456789]、.*')
ex_rule['pro'].append('.*评审专家：(.*?)招标机构名称：.*')
ex_rule['pro'].append('.*评审委员会成员名单：(.*?)代理费用收费标准：.*')
ex_rule['pro'].append('.*评审小组(.*?)[一二三四五六七八九]、.*')
ex_rule['pro'].append('.*八、专家名单：(.*?)九、采购人、.*')
ex_rule['pro'].append('.*专家组名单：(.*?)马龙县公共资源交易中心.*')
ex_rule['pro'].append('.*谈判小组成员名单：(.*?)七、成交结果：.*')
ex_rule['pro'].append('.*评标小组成员名单：(.*?)[一二三四五六七八九]、.*')
ex_rule['pro'].append('.*评委姓名：(.*?)[a-zA-Z].*')
ex_rule['pro'].append('.*评审委员会成员名单:(.*?)\d{1,2}、.*')
ex_rule['pro'].append('.*评标委员会成员名单：(.*?)中标候选人.*')
ex_rule['pro'].append('.*评标委员会成员名单：(.*?)特此公告.*')
ex_rule['pro'].append('.*评审委员会成员名单：(.*?)供货商信息：.*')
ex_rule['pro'].append('.*评标委员会名单：(.*?)七、招标项目联系方式.*')
ex_rule['pro'].append('.*评标委员会：(.*?)衷心感谢各投标人的积极参与.*')
ex_rule['pro'].append('.*评审委员会.*负责人：(.*?)[一二三四五六七八九]、.*')
ex_rule['pro'].append('.*评标委员会成员（谈判小组、询价小组）成员名单(.*?)采购项目联系人姓名、电话.*')
ex_rule['pro'].append('.*询价小组成员名单：(.*?)[一二三四五六七八九]、.*')
ex_rule['url'] = ['//table[@class="news"]/tr/td[@class="news"]/a/@href']
ex_rule['url'].append('//div/table[@id="moredingannctable"]/tr/td/a/@href')
ex_rule['url'].append('//table[@id="moredingannctable"]//a/@href')
ex_rule['url'].append('//div[@class="lby-lbnr"]/ul/li/a/@href')
ex_rule['url'].append('//ul[@id="itemContainer"]//a/@href')
ex_rule['url'].append('//table[@class="news"]/tbody/tr/td[@class="news"]/a/@href')
ex_rule['url'].append('//div[@class="content-right-lby"]/div/ul/li/a/@href')
ex_rule['url'].append('//div[@class="newscontain"]//a/@href')
ex_rule['url'].append('//div[@class="list clear"]//a/@href')
ex_rule['url'].append('//div[@class="newListwenzi"]//a/@href')
ex_rule['url'].append('//div[@class="sTradingInformationSelectedBtoList"]//a/@onclick')
ex_rule['url'].append('//div[@class="gui-title-bottom"]//li/@onclick')
ex_rule['url'].append('//table[@width="740"]//a/@href')
ex_rule['url'].append('//ul[@class="xwbd_lianbolistfrcon"]//a/@href')
ex_rule['url'].append('//table[@id="MyGridView1"]//a/@href')
ex_rule['url'].append('//table[@width="98%"]/tr/td/a/@href')
ex_rule['url'].append('//table[@id="newsItem"]/tr/td/a/@href')
ex_rule['url'].append('//table[@width="668"]/tr/td/a/@href')
ex_rule['url'].append('//table[@class="table table-hover dataTables-example"]//a/@href')
ex_rule['url'].append('//td[@width="665"]/a/@href')
ex_rule['url'].append('//td[@id="MoreInfoListjyxx1_tdcontent"]/a/@href')
ex_rule['url'].append('//div[@class="ewb-info-bd con"]//a/@href')
ex_rule['url'].append('//table[@id="ctl00_ContentPlaceHolder3_gdvNotice3"]//a/@href')
ex_rule['url'].append('//table[@id="gdvNotice3"]//a/@href')
ex_rule['url'].append('//table[@id="ctl00_ContentPlaceHolder3_gdvDemandNotice"]//a/@href')
ex_rule['url'].append('//table[@id="ctl00_ContentPlaceHolder3_gdvDeal"]//a/@href')
ex_rule['url'].append('//table[@id="data_tab"]//a/@href')
ex_rule['url'].append('//div[@class="content-right-content-center"]//a/@href')
ex_rule['url'].append('//div[@class="cs_two_content"]//a/@href')
ex_rule['url'].append('//*[@class="xinxi_ul"]//a/@href')
ex_rule['url'].append('//ul[@class="serach-page-results list-unstyled"]//a/@href')
ex_rule['url'].append('//ul[@class="news_list2"]//a/@href')
ex_rule['url'].append('//ul[@class="article-list-a"]//a/@href')
ex_rule['url'].append('//ul[@class="wb-data-item"]//a/@href')
ex_rule['url'].append('//ul[@class="article-list2"]//a/@href')
ex_rule['url'].append('//ul[@class="article-list2"]//a/@url')
ex_rule['url'].append('//ul[@class="article-listjy2"]//a/@href')
ex_rule['url'].append('//ul[@class="ewb-list"]//a/@href')
ex_rule['url'].append('//ul[@class="inner-ul"]//a/@href')
ex_rule['url'].append('//ul[@class="detail_content_right_box_content_ul"]//p/@onclick')
ex_rule['url'].append('//div[@class="public_list_team"]//a/@href')
ex_rule['url'].append('//div[@class="content_right fr"]//div[4]//a/@href')
ex_rule['url'].append('//ul[@class="vT-srch-result-list-bid"]/li/a/@href')
ex_rule['url'].append('//ul[@id="div_ul_1"]//li/a/@href')
ex_rule['url'].append('//ul[@class="article-list2"]//a/@href')
ex_rule['url'].append('//ul[@id="showList"]/ul[@class="ewb-info-items"]//a/@href')
ex_rule['url'].append('//div[@id="newsList"]//li/a/@href')
ex_rule['url'].append('//div[@id="news_div"]//a/@href')
ex_rule['url'].append('//div[@class="info"]//a/@href')
ex_rule['url'].append('//div[@class="zc_contract_top"]//table//tr/td[1]/a/@href')
ex_rule['url'].append('//div[@id="list_right"]//li/a/@href')
ex_rule['url'].append('//div[@class="xnrx"]//a/@href')
ex_rule['url'].append('//table[@class="table table-no tab-striped tab-hover"]//a/@href')
ex_rule['url'].append('//table[@class="newsTable listdt"]//a/@href')
ex_rule['url'].append('//ul[@class="dataList"]//li/a/@href')
ex_rule['url'].append('//ul[@class="Expand_SearchSLisi"]//li/a/@href')
ex_rule['url'].append('//ul[@id="content_001002001001"]//a/@href')
ex_rule['url'].append('//ul[@id="content_001002001002"]//a/@href')
ex_rule['url'].append('//ul[@id="content_001002001003"]//a/@href')
ex_rule['url'].append('//ul[@id="content_001002002004"]//a/@href')
ex_rule['url'].append('//ul[@id="content_001002002003"]//a/@href')
ex_rule['url'].append('//ul[@id="content_001002002002"]//a/@href')
ex_rule['url'].append('//ul[@id="content_001002002001"]//a/@href')
ex_rule['url'].append('//ul[@id="content_001002004001"]//a/@href')
ex_rule['url'].append('//ul[@id="content_001002004003"]//a/@href')
ex_rule['url'].append('//div[@class="ewb-infolist"]//a/@href')
ex_rule['url'].append('//div[@class="bid_information bid_information_as"]//a/@href')
ex_rule['url'].append('//div[@class="Top10 PaddingLR15"]/div[@class="List2"]//a/@href')
ex_rule['url'].append('//table[@class="divlxyz"]//a/@href')
ex_rule['url'].append('//tbody[@class="tableBody"]//a/@href')
ex_rule['url'].append('//tbody[@class="conn_list_items"]//tr/@href')
ex_rule['url'].append('//ul[@class="nei03_04_08_01"]//em//a/@href')
ex_rule['url'].append('//table[@class="nei03_04_08_01"]//em//a/@href')
ex_rule['url'].append('//ul[@class="news-list-content list-unstyled margin-top-20"]//li/a/@href')
ex_rule['url'].append('//ul[@class="news-list-content list-unstyled margin-top-20"]//li/a/@href')
ex_rule['url'].append('//table[@class="newtable"]//a/@href')
ex_rule['url'].append('//ul[@class="conList_ull"]//a/@href')
ex_rule['url'].append('//div[@class="publicont"]//a/@href')
ex_rule['url'].append('//div[@class="list-info"]//div[@class="info"]/ul//a/@href')
ex_rule['url'].append('//div[@class="yahoo"]//a/@onclick')
ex_rule['url'].append('//div[@class="table-box"]//a/@href')
ex_rule['url'].append('//div[@class="BeltBar BeltBar2"]/dl/dd//a/@href')
ex_rule['url'].append('//table//td[@class="Font9"]//a[@class="five"]/@href')
ex_rule['url'].append('//table[@id="node_list"]//a/@href')
ex_rule['url'].append('//ul[@class="m_m_c_list"]//li/a/@href')
ex_rule['pak'] = ['//span[@id="con"]//text()']
ex_rule['pak'].append('//div[@class="table-box"]//a/@href')
# ex_rule['c_html'] = {'http://www.mof.gov.cn/':['//div[@class="box_content"]']}
# ex_rule['c_html'].update({'ccgp.gov.cn':['//div[@class="vF_detail_content"]','//div[@class="vT_detail_main"]','//div[@class="vT_detail_content w760c"]','//div[@class="left_content"]']})
# ex_rule['c_html'].update({'zycg.gov.cn':['//div[@id="printArea"]','//table[@width="1000"]','//script[@id="container"]']})
# ex_rule['c_html'].update({'http://txzb.miit.gov.cn/':['//*[@id="ef_region_inqu"]','//table[@class="tableBorder"]']})
# ex_rule['c_html'].update({'ccgp_intention':['//div[@class="pubtable"]']})
# ex_rule['c_html'].update({'http://www.ggzy.gov.cn/':['/html/body/div[1]']})
# ex_rule['c_html'].update({'http://www.mwr.gov.cn/':['//*[@id="slywxl1"]']})
# ex_rule['c_html'].update({'bgpc.beijing.gov.cn':['//div[@id="mainText"]','//div[@class="content-right-content"]','//div[@class="content-right-details-content"]']})
# ex_rule['c_html'].update({'ccgp-beijing.gov.cn/':['/html/body/div[1]/div[3]','/html/body/div[2]/div[3]']})
# ex_rule['c_html'].update({'www.bcactc.com':['//table[@class="ContextTable"]']})
# ex_rule['c_html'].update({'ggzyfw.beijing.gov.cn':['//div[@class="newsCon"]']})
# ex_rule['c_html'].update({'ccgp-hebei.gov.cn':['//table[1]','//table[@id="2020_VERSION"]','//table[@width="930"]','//table[@width="1200"]']})
# ex_rule['c_html'].update({'www.hebpr.cn':['//div[@class="content_scroll"]']})
# ex_rule['c_html'].update({'ccgp-jiangxi.gov.cn':['//div[@class="article-info"]']})
# ex_rule['c_html'].update({'ccgp-hainan.gov.cn':['//div[@class="nei03_02"]','//div[@class="content01"]']})
# ex_rule['c_html'].update({'ccgp-hubei':['//div[@class="art_con"]//div[2]']})
# ex_rule['c_html'].update({'jxsggzy.cn':['//div[@class="article-info"]']})
# ex_rule['c_html'].update({'hngp.gov.cn':['//body']})
# ex_rule['c_html'].update({'hnggzy':['//td[@id="TDContent"]','//div[@id="divArtice"]','//div[@class="row"]/div[2]']})
# ex_rule['c_html'].update({'zw.hainan.gov.cn':['//div[@class="newsCon"]']})
# ex_rule['c_html'].update({'www.customs.gov.cn':['//div[@align="left"]']})
# ex_rule['c_html'].update({'121.28.195.124':['//td[@class="font_black"]','//div']})
# ex_rule['c_html'].update({'hntba':['//div[@class="news-xq"]']})
# ex_rule['c_html'].update({'zw.hainan.gov':['//div[@class="zx-xxxqy-nr"]','//div[@class="xly"]','//div[@id="Zoom"]']})
# ex_rule['c_html'].update({'kfqgw.beijing.gov.cn':['//div[@id="div_zhengwen"]']})
# ex_rule['c_html'].update({'ccgp-tianjin':['//div[@class="pageInner"]//table']})
# ex_rule['c_html'].update({'prec_sxzwfw':['//div[@class="body_main"]']})
# ex_rule['c_html'].update({'nmgp_gov':['//div[@class="content-box-1"]']})
# ex_rule['c_html'].update({'ccgp-shanxi':['//tr[@class="bk5"]','.']})
# ex_rule['c_html'].update({'ccgp-shandong':['//td[@bgcolor="#FFFFFF"]','//div[@class="listConts"]']})
# ex_rule['c_html'].update({'gdgpo.gov':['//div[@id="content"]']})
# ex_rule['c_html'].update({'ccgp-jiangsu':['//div[@class="detail_con"]','.']})
# ex_rule['c_html'].update({'ccgp-jilin':['//div[@id="xiangqingneiron"]']})
# ex_rule['c_html'].update({'hljcg.gov.cn':['//div[@class="xxej"]']})
# ex_rule['c_html'].update({'ccgp-hunan':['//html']})
# ex_rule['c_html'].update({'ccgp-fujian':['//div[@class="notice-con"]']})
# ex_rule['c_html'].update({'ccgp-chongqing':['//*','.']})
# ex_rule['c_html'].update({'ccgp-anhui':['//div[@class="frameNews"]//table[1]','//div[@class="frameNews"]//div[4]','//div[@class="frameNews"]']})
# ex_rule['c_html'].update({'ccgp-sichuan':['//div[@id="myPrintArea"]//table','//div[@class="package_lines layoutfix"]']})
# ex_rule['c_html'].update({'ccgp-liaoning':['//div[@id="template"]']})
# ex_rule['c_html'].update({'ccgp-guangxi':['//*']})
# ex_rule['c_html'].update({'ccgp-guizhou':['.']})
# ex_rule['c_html'].update({'yngp':['//div[@class="vF_detail_content"]','//div[@class="vT_detail_main"]','//div[@class="vT_detail_content w760c"]']})
# ex_rule['c_html'].update({'ccgp-shaanxi':['//div[@class="inner-Box"]','//div[@class="annBox"]','//div[@class="content-inner"]']})
# ex_rule['c_html'].update({'ccgp-xinjiang':['//*']})
# ex_rule['c_html'].update({'ccgp-gansu':['//div[@id="fontzoom"]']})
# ex_rule['c_html'].update({'ccgp-ningxia':['//div[@class="vT_detail_content w100c"]','//div[@id="jjDiv"]']})
# ex_rule['c_html'].update({'ccgp-xizang':['//div[@class="notice-con"]']})
# ex_rule['c_html'].update({'ccgp-qinghai':['//*']})
# ex_rule['c_html'].update({'cgw_xjbt':['.']})
# ex_rule['c_html'].update({'zfcg_qingdao':['//div[@class="cont"]']})
# ex_rule['c_html'].update({'nbzfcg':['//div[@class="frame_list01"]/table']})
# ex_rule['c_html'].update({'szzfcg':['//div[@id="contentDiv"]','//body//table']})
# ex_rule['c_html'].update({'ccgp-dalian':['//table[@id="_Sheet1"]','//table[@id="tblInfo"]',]})
# ex_rule['c_html'].update({'prec_sxzwfw':['//table[@class="gycq-table"]']})
# ex_rule['c_html'].update({'zjzwfw':['//div[@class="con"]']})
# ex_rule['c_html'].update({'hljggzyjyw':['//div[@class="ewb-art-bd"]']})
# ex_rule['c_html'].update({'jszwfw':['//div[@class="ewb-trade-right l"]']})
# ex_rule['c_html'].update({'lnggzy':['//td[@id="zfcg_zbgs1_TDContent"]','//td[@id="zfcg_zbgg1_TDContent"]','//div[@class="ewb-notice-bd"]']})
# ex_rule['c_html'].update({'ggzy_hebei':['//div[@class="ewb-copy"]']})
# ex_rule['c_html'].update({'ggzyjy.nmg':['//div[@class="detail_contect"]','//div[@id="noticeArea"]']})
# ex_rule['c_html'].update({'ggzy_zwfwb':['//div[@class="content"]//div[@id="content"]']})
# ex_rule['c_html'].update({'jl_gov_cn':['//div[@class="ewb-article-info"]']})
# ex_rule['c_html'].update({'shggzy':['//div[@class="content"]']})
# ex_rule['c_html'].update({'ggzy_ah':['//div[@id="content"]','.']})
# ex_rule['c_html'].update({'ggzyfw_fj':['.']})
# ex_rule['c_html'].update({'ggzyjy_shandong':['//table[@class="gycq-table"]']})
# ex_rule['c_html'].update({'hnsggzyfwpt':['//div[@class="ewb-left-bd"]']})
# ex_rule['c_html'].update({'hbggzyfwpt':['.']})
# ex_rule['c_html'].update({'hnsggzy':['//div[@class="div-article2"]']})
# ex_rule['c_html'].update({'gxggzy':['//div[@class="ewb-details-info"]']})
# ex_rule['c_html'].update({'cqggzy':['//div[@id="mainContent"]']})
# ex_rule['c_html'].update({'ggzyjy_sc':['//div[@class="clearfix"]']})
# ex_rule['c_html'].update({'ggzy_guizhou':['.']})
# ex_rule['c_html'].update({'ggzy_yn':['//div[@class="detail_contect"]']})
# ex_rule['c_html'].update({'ggzy_xizang':['//div[@class="div-article2"]']})
# ex_rule['c_html'].update({'sxggzyjy':['//div[@id="mainContent"]','//div[@class="epoint-article-content jynr news_content"]']})
# ex_rule['c_html'].update({'ggzyjy_gansu':['.']})
# ex_rule['c_html'].update({'qhggzyjy':['//div[@class="xiangxiyekuang"]']})
# ex_rule['c_html'].update({'nxggzyjy':['//div[@id="tab-1"]']})
# ex_rule['c_html'].update({'ggzy_xinjiang':['//div[@class="ewb-info-bd"]']})
# ex_rule['c_html'].update({'ggzy_xjbt':['//div[@class="infodetail"]']})
ex_rule['page'] = {'ggzyfw.beijing.gov.cn':['//ul[@class="pages-list"]/li/a/text()']}
ex_rule['method'] = ['.*采购方式：(.*?)六、成交情况.*']
ex_rule['intro'] = ['.*1.招标条件(.*?)2.项目概况与招标范围.*']
ex_rule['intro'].append('.*二、采购项目信息(.*?)三、成交信息.*')
ex_rule['intro'].append('.*三、详细内容:(.*?)1.项目情况.*')
ex_rule['annex'] = {'zycg.gov.cn':['//div[@class="art_accessary"]//a/@href']}
ex_rule['annex'].update({'bgpc.beijing.gov.cn':['//div[@class="content-right-content"]//p/a/@href']})
ex_rule['annex'].update({'ccgp-beijing.gov.cn/':['/html/body/div[1]/div[3]//p/a/@href','/html/body/div[2]/div[3]//p/a/@href']})
ex_rule['w_bider_html'] = {'hngp.gov.cn':['//td[@class="suojin"]//table/tr[2]/td[3]/text()']}



# 运行时间
def count_time(func):
    def int_time(*args, **kwargs):
        start_time = datetime.datetime.now()  # 程序开始时间
        func(*args, **kwargs)
        over_time = datetime.datetime.now()   # 程序结束时间
        total_time = (over_time-start_time).total_seconds()
        print('程序共计%s秒' % total_time)
    return int_time


# 提取表格内容
def table_ex(html):
    table = etree.HTML(html).xpath('//div[@class="table"]/table/tbody/tr//td[@class="title"]/text()')
    return table


# 提取列表URL
def url_ex(html=None,url_tag=None):
    try:
        u_ex = yzb_url_list_ex.UrlListEX(text=html, url_tag=url_tag)
        url_list = u_ex.url_ex()
        print(url_list,'uuuuuuuuuuu')
        if not url_list:
            # print('1111111111111')
            for i in ex_rule['url']:
                # print('2222222222222222222')
                if etree.HTML(html).xpath(i):
                    # print(i)
                    return etree.HTML(html).xpath(i) # 指定数据行
            return '空'
        # print(3333333333333333)
        return url_list
    except:
        return '空'


# 提取正文HTML
def content_html_ex(det_html,url,page_url=None,extra=None):
    #提取标签和内容

    # try:
        Xp = yzb_EX_Text.Xpaths
        rtnv = []
        # print(ex_rule['c_html'][url])
        for i in Xp[url]:
            # print(i)
            # print(etree.HTML(det_html).xpath(i))
            c_html = etree.HTML(det_html).xpath(i)[:1]
            # print(c_html,'===========c_html===============')
            for j in c_html:
                b_str = etree.tostring(j,method="html",encoding='utf-8', pretty_print=False)   #规整html，输出二进制
                u_str = str(b_str, "utf-8")  #转换成字符串
                u_str = u_str.replace('%5C','\\')
                ## 去除a标签
                # soup = BeautifulSoup(u_str)
                # for a in soup.findAll('a'):
                #     del a['href']
                # # print(type(soup),'soup')
                # rtnv.append(htmlpkg.unescape(str(soup)))
                rtnv.append(htmlpkg.unescape(str(u_str)))
                # print(rtnv)
            if rtnv != []:
                content_fix = yzb_annex_fix.AnnexFix(det_html=det_html, tag_url=url, page_url=page_url, rtnv=rtnv, extra=extra)
                content = content_fix.main()
                # print(content,'ccccccc')
                content = re.sub('<style.*?>[\s\S]*?</style>','',content)
                content = re.sub('<!--[\s\S]*?-->','',content)
                content = re.sub('<samp','<span',content)
                content = re.sub('</samp>','</span>',content)
                content = re.sub('(?<=<)form|(?<=</)form','div',content)
                # print(content,'content')
                if not content:
                    return ''.join(rtnv)
                # print(content,'---------------content-----------------')
                return content


        return '空'
    # except Exception as e:
    #     print(sys.exc_info())


def unit_price_ex(table_str):
    normal_restr = '(?:单价)(?:\(元\)|（元）)?(?:{_})*([\d.,]*?)(?:{_}|{\^\^\^})'
    million_restr = '(?:单价)(?:\(万元\)|（万元）)?(?:{_})*([\d.,]*?)(?:{_}|{\^\^\^})'

    return price_ex(normal_restr,million_restr,table_str)


def total_price_ex(table_str):
    normal_restr = '(?:成交金额|中标金额|总金额|中标价|金额|总价)(?:\(元\)|（元）|:|：|{_})*([\d.,]*?)(?:{_}|{\^\^\^}|[\u4e00-\u9fa5])'
    million_restr = '(?:成交金额|中标金额|总金额|中标价|金额|总价)(?:\(万元\)|（万元）|:|：|{_})*([\d.,]*?)(?:{_}|{\^\^\^}|[\u4e00-\u9fa5])'

    return price_ex(normal_restr,million_restr,table_str)


def price_ex(normal_restr,million_restr,table_str):
    # 单位是元
    normal_price = normal_price_ex(normal_restr, table_str)
    # 单位是万元
    million_price = million_price_ex(million_restr, table_str)

    return normal_price if normal_price else million_price


def normal_price_ex(normal_restr,table_str):
    price_list = re.findall(normal_restr, table_str)
    if set(price_list) != {''} and price_list != []:
        print(price_list,'price_list')

        return decimal.Decimal(price_list[0].strip().replace(',', '')) * 100


def million_price_ex(million_restr,table_str):
    price_list = re.findall(million_restr, table_str)
    if set(price_list) != {''} and price_list != []:
        print(price_list, 'price_list')
        return decimal.Decimal(price_list[0].strip().replace(',', '')) * 1000000





def brand_model_ex(table_str):
    bm_restr = '(?:品牌、型号（规格）)(?:{_})(.*?)(?:{_})'
    b_restr = '(?:货物品牌|品牌)(?:（如有）)?(?:{_})*(.*?)(?:{_}|{\^\^\^})'
    m_restr = '(?:规格型号|货物型号|型号)(?:{_})*(.*?)(?:{_}|{\^\^\^})'

    bm = re.findall(bm_restr,table_str)
    if bm != []:
        bm = bm[0]
        brand_list = re.findall('(?:品牌)(?:：)(?:\s)*(.*?)(?:\s)*(?:型号)',bm)
        model_list = re.findall('(?:型号)(?:：)(?:\s)*(.*?)(?:\s)*(?:{_})*$',bm)
    else:
        brand_list = re.findall(b_restr, table_str)
        model_list = re.findall(m_restr, table_str)
    brand = ''.join(brand_list).replace('{^^^}','').replace('{_}','')
    model = ''.join(model_list).replace('{^^^}','').replace('{_}','')

    return table_word_filter(brand),table_word_filter(model)


def quantity_ex(table_str):
    # print(table_str)
    quantity_list = re.findall('(?:数量)(?:（单位）)?(?:{_})*(.*?)(?:{_})', table_str)
    print(quantity_list)
    quantity = ''.join(re.findall('[0-9一二三四五六七八九十]+',''.join(quantity_list)))
    if re.search('[一二三四五六七八九十]',quantity):
        print(quantity,'qqqqqqqqqqqqqqqqqqqq')
        quantity = chinese_to_num(quantity)
    if not quantity:
        return
    return quantity


def purchase_details_ex(table_str):
    purchase_details_list = re.findall('(?:(?<!供应商)名称|采购内容|主要中标内容)(?:(?:{_})+|(?:：))(.*?)(?:{_}|供应商名称)',table_str)
    # print(purchase_details_list,'purchase_details_list')
    for i in range(len(purchase_details_list)-1,-1,-1):
        if re.search('采购',purchase_details_list[i]):
            purchase_details_list.pop(i)

    purchase_details_list = de_duplication(purchase_details_list)

    return table_word_filter(''.join(purchase_details_list))


def winbider_table_ex(table_str):
    win_bider_list = re.findall('(?:供应商名称|中标候选人|中标单位)(?:{_}|：|:)*(.*?)(?:{_}|供应商地址)', table_str)
    for i in range(len(win_bider_list)-1,-1,-1):
        win_bider_list[i] = re.sub('{\^\^\^}|{_}', '', win_bider_list[i])
        if re.search('品牌（如有）|规格型号|货物品牌|签订合同|货物名称|单价|数量|序号|详见|工期',win_bider_list[i]):
            win_bider_list.pop(i)

    win_bider_list = de_duplication(win_bider_list)


    print(win_bider_list,'win_bider_list')
    return ''.join(win_bider_list)



def pkg_details_by_regex(table_str,bid_id,d_save=None):
    print(table_str,'table_str')
    # 采购内容
    purchase_details = purchase_details_ex(table_str)
    # 品牌,型号
    brand,model = brand_model_ex(table_str)
    # 数量
    quantity = quantity_ex(table_str)
    # 单价
    unit_price = unit_price_ex(table_str)
    # 总价
    total_price = total_price_ex(table_str)
    # 中标供应商
    win_bider  = winbider_table_ex(table_str)

    print('purchase_details: ',purchase_details)
    print('brand: ',brand)
    print('model: ',model)
    print('quantity: ',quantity)
    print('unit_price: ',unit_price)
    print('total_price: ',total_price)
    print('win_bider: ',win_bider)
    # d_save = '12132213'
    if d_save:
        if (brand != None or model != None) and (unit_price != None or total_price != None) and purchase_details:
            save_pkg_details(purchase_details, brand, model, quantity, unit_price, total_price, win_bider, bid_id,d_save=d_save)
        elif purchase_details and total_price and win_bider:
            save_pkg_details(purchase_details, brand, model, quantity, unit_price, total_price, win_bider, bid_id,
                             d_save=d_save)






def table_word_filter(word):
    word = re.sub('{_}|{\^\^\^}','',word)
    filter_word = '详见标书|详见投标文件|标的|采购'
    if not re.search(filter_word,word):
        return word



# def pkg_details_by_sign(table_str):
#     row_list = table_str.split('{^^^}')
#     # print(row_list,'row')
#     for row in row_list:
#         # print(re.search('tbl_start_tag|tbl_end_tag','{_}{_}'),'ssssssssssss')
#         if (not re.search('[\u4e00-\u9fa5]|[A-Za-z0-9]',row)) or re.search('tbl_start_tag|tbl_end_tag',row):
#             continue
#         else:
#             unit_list = row.split('{_}{_}{_}')
#             num = unit_list[0]
#             units = unit_list[1]
#             # units = unit_list[1].split('{_}{_}')
#             # print(num,'num')
#             # print(units,'units')
#             pkg_details_by_regex(units)

def de_duplication(data_list):
    num_list = []
    for num in data_list:
        if num not in num_list:
            num_list.append(num)
    return num_list



def get_subproject_by_num(num_list_rough,content,bid_id,d_save=None):
    num_list = de_duplication(num_list_rough)

    for i in range(len(num_list)):
        if i == len(num_list)-1:
            subproject = re.findall(f'(?:{num_list[i]})(.*?)(?:tbl_end_tag)', content)
        else:
            subproject = re.findall('(?:'+str(num_list[i])+')(?:{_})((?:(?!'+str(num_list[i])+').)*?)(?:'+str(num_list[i+1])+')',content)
        # print(subproject,'subproject')
        if len(subproject) >= 1:
            pkg_details_by_regex(''.join(subproject),bid_id,d_save=d_save)


def get_subproject_by_tblnum(content,bid_id,d_save=None):
    restr = '(?:中标（成交）信息|主要标的信息)(?:tbl_start_tag)(?:.*?)(?:tbl_end_tag)'
    subproject_list = re.findall(restr,content)
    # print(subproject_list,'subproject')
    pkg_details_by_regex(''.join(subproject_list),bid_id,d_save=d_save)


def get_subproject(pkg_num_list,subproject_num_list,content,bid_id,d_save=None):
    if pkg_num_list != [] and subproject_num_list != []:
        # 如果既有分包又有子项目，特殊处理
        pkg_num_set = set([re.sub('[a-zA-Z0-9-]','',i) for i in pkg_num_list])
        if len(pkg_num_set) > 1:
            # 如果拆出来 有的叫包 有的叫标 视为提取错误，按子项目提取
            get_subproject_by_num(subproject_num_list, content,bid_id,d_save=d_save)
        elif len(pkg_num_list) == 1 and len(subproject_num_list) > 1:
            get_subproject_by_num(subproject_num_list, content,bid_id,d_save=d_save)
        else:
            get_subproject_by_num(pkg_num_list, content,bid_id,d_save=d_save)
    elif pkg_num_list != [] and subproject_num_list == []:
        # 有分包，没有子项目
        get_subproject_by_num(pkg_num_list, content,bid_id,d_save=d_save)
    elif pkg_num_list == [] and subproject_num_list != []:
        # 没分包有子项目
        get_subproject_by_num(subproject_num_list, content,bid_id,d_save=d_save)
    else:
        # 没分包没子项目,大概率有一个内容
        get_subproject_by_tblnum(content,bid_id,d_save=d_save)


def save_pkg_details(purchase_details,brand,model,quantity,unit_price,total_price,win_bider,bid_id,d_save=None):
    d = {}

    notnull_dict(str(bid_id), d, 'bid_id')
    notnull_dict(purchase_details, d, 'purchase_details')
    notnull_dict(brand, d, 'brand')
    notnull_dict(model, d, 'model')
    notnull_dict(str(quantity), d, 'quantity')
    notnull_dict(str(unit_price), d, 'unit_price')
    notnull_dict(str(total_price), d, 'total_price')
    notnull_dict(win_bider, d, 'winning_bidder')

    d_save.insert('t_bid_pkg', d)
    # return purchase_details,brand,model,quantity,unit_price,total_price,win_bider


def pkg_ex(content,bid_id,d_save=None):
    try:
        print(content,'pre_content')
        pkg_num_list = yzb_TextPreprocessing.GetPkgs(content)
        pkg_num_list.sort()
        print(pkg_num_list,'pkg_num_list')
        subproject_num_list = yzb_TextPreprocessing.GetSubproject(content)
        print(subproject_num_list,'subproject_num_list')

        get_subproject(pkg_num_list, subproject_num_list, content,bid_id,d_save=d_save)
    except Exception as e:
        print(e)







def delete_css(content):
    rule = [
        # '(.*?)[\u4e00-\u9fa5].*',
        '.*/>',
        '{.*?}',
        # '.*;}',
        '.*-->',

    ]

    for j in rule:
        for n in range(2):
            half_content = content[:int(len(content)/2)]
            if re.search(j,half_content, re.I | re.S):
                wrong_data = re.findall(j,half_content, re.I | re.S)
                if wrong_data != []:
                    # print(wrong_data)
                    wrong_data = wrong_data[0]
                    content_clean = half_content.replace(wrong_data,'')
                    content = content_clean + content[int(len(content) / 2):]
                    # print(wrong_data,'hahahaha')
                    # print('匹配到',j)
                else:
                # print(content_clean)
                    content = half_content+content[int(len(content)/2):]
    return content

# 提取正文
def content_ex(html,url_tag=None,extra=None,key=0):
    '''
    如果key等于1提取整个html作为content，如果key等于0提取特定位置html

    过滤文章规则：简介取前150个字，如果前150个字内有乱码去掉，如果乱码长度大于150个字？如果乱码在后面 如何处理？
    '''

    # try:

    html = yzb_TextPreprocessing.SPL_Preprocessing(content=html, website=url_tag)
    # print('11111111111111')
    # print(html,'html')

    # if key == 1:
    result1 = etree.HTML(html).xpath('//text()')
    # print(result1)
    # else:
    #     # contentspex = cse.ContentSpecialEx(det_html=html,url_tag=url_tag,extra=extra)
    #     # result1 = contentspex.special_ex()
    #     # if not result1:
    #         for i in ex_rule['content']:
    #
    #             result1 = etree.HTML(html).xpath(i)
    #             # print(result1)
    #             # print(i)
    #             # print(result1)
    #
    #             if result1 and len(''.join(''.join(result1).split())) > 50:
    #                 # print(''.join(''.join(result1).split()),'tttttttttttttt')
    #                 print(i,'dddddddddddd')
    #                 break
    #             # elif result1 and len(''.join(''.join(result1).split())) < 100:
    #             #     print(''.join(''.join(result1).split()),'tttttttttttt')
    if result1:
        if len(result1) == 1:
            # print(i, 'content')
            content1 = ''.join(result1).replace('\n', '').replace('\r', '').replace(' ', '').replace('	', '')
            content = etree.HTML(content1).xpath('//*/text()')
            return ''.join(content).replace('\n', '').replace('\r', '').replace(' ', '').replace('	', '')

        content = ''.join(result1).replace('\n','').replace('\r','').replace(' ', '').replace('	', '')

        pre_content = content
        # pkg_ex(content)
        content = re.sub('tbl_end_tag|tbl_start_tag|{\^\^\^}|{_}',' ',content)
        # 删除CSS样式，避免简介全是CSS
        # content = delete_css(content)
        if '招标人或其招标代理机构主要负责人（项目负责人）：（盖章）招标人或其招标代理机构：（盖章）' in content:
            return content.replace('招标人或其招标代理机构主要负责人（项目负责人）：（盖章）招标人或其招标代理机构：（盖章）',''),pre_content
        return content,pre_content

    return '空','空'
    # except Exception as e:
    #     print(sys.exc_info())
    #     return '空'


def title_clean(title):
    # 添加过滤词
    clean_word = '^\[政采云\]|^\[交易公告\]|^\[.{1,2}[区]\]|\[20\d{2}\]'

    title = re.sub(clean_word,'',title)

    return title

# 提取标题
def title_ex(html):
    try:
        for i in ex_rule['title']:
            # print(i)
            if not etree.HTML(html).xpath(i) == []:
                print(i,'tttttttttt')
                if etree.HTML(html).xpath(i) == []:
                    continue
                # title = etree.HTML(html).xpath(i)[0]

                title_list = [i.strip() for i in etree.HTML(html).xpath(i)]
                title = re.sub('\s','',''.join(list(dict.fromkeys(title_list))))
                # print(title,'tititititi')
                if 4 < len(title) < 128:
                    return title_clean(title)
                else:
                    return title_clean(title)[:127]
        for i in ex_rule['title_html']:
            if re.search(i,html, re.I | re.S):
                print(i)
                title = ''.join(re.findall(i, html)).strip()
                if 5 < len(title) < 128:
                    return title_clean(title)
                else:
                    return title_clean(title)[:127]
        return '空'
    except:
        return '空'


def title_ex_content(content):
    # 从文章中提取标题
    try:
        for i in ex_rule['title_content']:
            # print(i)
            if re.search(i,content, re.I | re.S):
                # print(re.findall(i, content),'title')
                print(i)
                title = ''.join(re.findall(i, content)).strip()
                if 5 < len(title) < 128:
                    return title_clean(title)
                else:
                    return title_clean(title)[:127]
        return '空'
    except:
        return '空'


# 提取标题整合
def title_ex_total(content,html):
    title = title_ex(html)
    if title == '空':
        print('content')
        return title_ex_content(content)
    print('html')
    return title

#从html中提取项目名称
def project_name_html_ex(html):
    try:
        for i in ex_rule['p_name_html']:
            if not etree.HTML(html).xpath(i) == []:
                print(i)
                project_name = ''.join(etree.HTML(html).xpath(i)).strip()
                # print(title,'tititititi')
                return project_name
        return '空'
    except:
        return '空'


# 提取项目名称
def project_name_ex(content,title=''):
    stopword = ['补遗', '更正通知', '变更通知', '更正公告', '变更公告', '补充公告', '延期公告', '废标公告', '流标公告', '工程项目', '废标', '流标', '未成交公告',
                '异常公告', '终止公告', '中标公告', '中标公示', '中标结果公示', '成交公告', '采购结果公告', '成交结果公告', '结果公告', '需求公告', '竞争性谈判', '竞争性磋商',
                '邀请招标', '询价', '单一来源', '资格预审', '公开招标', '采购公告', '招标公告', '公示', '公告', '采购项目', '服务项目', '采购及服务项目', '采购', '竞价',
                '项目', '评标']
    try:
        for i in ex_rule['p_name']:
            if re.search(i,content, re.I | re.S) and re.findall(i, content) != []:
                # print(i)
                # print(re.findall(i, content),'xxxxxxxxxxxxxxxx')
                p_name = ''.join(re.findall(i, content)).strip().replace(',','')
                if 2 < len(p_name) < 128 and title_filter(p_name):
                    return p_name
        if re.search('.*项目|.*工程',title):
            return ''.join(re.findall('.*项目|.*工程',title)).strip().replace(',','')
        if title:
            project_name = title
            for j in stopword:
                if j in title:
                    project_name = project_name.replace(j, '')
            return project_name
        # if title:
        #     return title
        return '空'
    except :
        return '空'


# 项目编号过滤
def project_num_filter(result):
    res = result.replace(':', '').replace('：', '').replace(';', '')
    if res.endswith('、') or res.endswith('.'):
        return res[:-1]
    else:
        return res



# 提取项目编号
def project_num_ex(content,url_tag=None,det_html=None):
    try:
        # 通用提取方式
        for i in ex_rule['p_num']:
            if re.search(i, content, re.I | re.S):
                print(i,'aaaaaaaaaa')
                # print(re.findall(i, content),'xxxxxxxxxxxxxx')
                nums = re.findall(i, content)
                for num in nums:
                    # num = re.findall(i, content)[0]
                    # print(num,'num')
                    if re.search('（$', num):
                        num = re.sub('（$', '', num)[0]
                    if 2 < len(num) < 64 and word_filter(num) and num != '':
                        return project_num_filter(num)

        # 各个网站单独提取方式
        try:
            pce = yzb_project_code_ex.ProjectCodeEx(content, url_tag, det_html)
            result = pce.special_ex()
            print(result,'11')
            if 2 < len(result) < 64 and word_filter(result):

                return project_num_filter(result)
        except:
            pass

        return '空'
    except:
        print(sys.exc_info())
        return '空'


def latest_date(sql_date=None,web_date=''):
    try:
        # 老数据的日期
        # if s_time == '':

        s_time = sql_date.timestamp()
        # print(s_time)
        try:
            # 新数据的日期
            w_time = time.mktime(time.strptime(web_date, '%Y-%m-%d %H:%M'))
        except:
            w_time = time.mktime(time.strptime(web_date, '%Y-%m-%d'))

        diff = int(s_time) - int(w_time)
        # print(diff)
        if diff <= 0:
            # 新数据日期比较新，保留新数据

            return 0
        else:
            # 老数据日期比较新，保留老数据
            return 1

    except Exception as e:
        print(e)
        return 2





#比较日期
def valid_date(timestr):
    # print(timestr,'timestr----------------')
    #获取当前时间日期
    # nowTime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    # print(nowTime_str)
    #mktime参数为struc_time,将日期转化为秒，
    # e_time = time.mktime(time.strptime(nowTime_str,"%Y-%m-%d %H:%M"))
    # print(e_time)
    # print(timestr)
    try:
        try:
            s_time = time.mktime(time.strptime(timestr, '%Y-%m-%d %H:%M'))
            nowTime_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
            e_time = time.mktime(time.strptime(nowTime_str, "%Y-%m-%d %H:%M"))
        except:
            s_time = time.mktime(time.strptime(timestr, '%Y-%m-%d'))
            nowTime_str = datetime.datetime.now().strftime('%Y-%m-%d')
            e_time = time.mktime(time.strptime(nowTime_str, "%Y-%m-%d"))
        # print(s_time)
        #日期转化为int比较
        # print(s_time,'s_time')
        diff = int(s_time)-int(e_time)
        # print(diff)
        if diff <= 0:
            # print('1111111111111')
            return 1
        else:
            print('所查日期不能大于当前时间！！！')
            return 0
    except Exception as e:
        print(e,'xxxxxxxxxxxxx')
        return 2


# 提取公告日期
def date_ex_html(html):
    try:
        for i in ex_rule['date_html']:
            # print(i)
            date_rough = etree.HTML(html).xpath(i)
            if not date_rough == []:
                # print(date_rough)
                # print(etree.HTML(html).xpath(i),'11111111111111')
                date_int = re.findall('\d{8,14}',date_rough[0])
                # print(date_int,'date_int')
                if date_int:
                    year = date_int[0][:4]
                    month = date_int[0][4:6]
                    day = date_int[0][6:8]
                    hour = date_int[0][8:10]
                    minute = date_int[0][10:12]
                    second = date_int[0][12:14]
                    date_rough = [f'{year}-{month}-{day} {hour}:{minute}:{second}']
                    # print(year,month,day,hour,minute,second)
                date_s = re.findall('(((1[6-9]|[2-9]\d)\d{2})-([1-9]|0[1-9]|1[012])-(0[1-9]|[12]\d|3[01]|[1-9])[ ]+(([01]\d|2[0-3]):[0-5]\d))',date_rough[0].strip().replace('年','-').replace('月','-').replace('日','').replace('/','-').replace('.','-'), re.I | re.S)
                # print(date_s, '**************')
                if date_s and date_s != []:
                    date_s = date_s[0][0]
                    if valid_date(date_s):
                        return date_s
                date_s = re.findall('(((1[6-9]|[2-9]\d)\d{2})-([1-9]|0[1-9]|1[012])-(0[1-9]|[12]\d|3[01]|[1-9]))',date_rough[0].strip().replace('年','-').replace('月','-').replace('日','').replace('/','-').replace('.','-'), re.I | re.S)
                # print(date_s,'##############')
                if date_s and date_s != []:
                    date_s = date_s[0][0]
                    if valid_date(date_s):
                        return date_s
                date_s = re.findall('((1[6-9]|[2-9]\d)-([1-9]|0[1-9]|1[012])-(0[1-9]|[12]\d|3[01]|[1-9]))',date_rough[0].strip().replace('年','-').replace('月','-').replace('日','').replace('.','-'), re.I | re.S)
                # print(date_s,'--------------')
                if date_s and date_s != []:
                    date_s = '20'+ date_s[0][0]
                    if valid_date(date_s):
                        return date_s

        return '空'
    except Exception as e:
        print(e)
        return '空'


# 提取公告日期
def date_ex_content(content):
    try:
        for i in ex_rule['date']:
            if re.search(i,content, re.I | re.S):
                # print(i,'date_re')
                date_rough = re.findall(i, content).pop().strip().replace('年','-').replace('月','-').replace('日','').replace('.','-')
                # print(date_rough,'date_rough')
                # print(re.findall(i, content, re.I | re.S),'date_rough')
                date_s = re.findall('^((?!0000)[0-9]{4}-((0[1-9]|1[0-2])-(0[1-9]|1[0-9]|2[0-8])|(0[13-9]|1[0-2])-(29|30)|(0[13578]|1[02])-31)|([0-9]{2}(0[48]|[2468][048]|[13579][26])|(0[48]|[2468][048]|[13579][26])00)-02-29)$',date_rough)
                if not date_s:
                    continue
                date_s = date_s[0]
                # print(date_s,'date_s')
                if type(date_s) != str and len(date_s) > 0:
                    date_s = date_s[0]
                if valid_date(date_s) == 1:
                    return date_s
                elif valid_date(date_s) == 0:
                    return datetime.datetime.now().strftime('%Y-%m-%d')
        if re.search('\d{2,4}年\d{1,2}月\d{1,2}日|\d{2,4}-\d{1,2}-\d{1,2}',content, re.I | re.S):
            date_ss = re.findall('(((1[6-9]|[2-9]\d)\d{2})-(0[1-9]|1[012])-(0[1-9]|[12]\d|3[01]|[1-9]))', content)[0][0].pop().strip().replace('年','-').replace('月','-').replace('日','').replace('.','-')
            if valid_date(date_ss) == 1:
                return date_ss
        return '空'
    except:
        return '空'



def date_ex(html,content):
    try:
        d_html = date_ex_html(html)
        if d_html != '空':
            print('html')
            return d_html
        print('content')
        return date_ex_content(content)
    except Exception as e:
        print(e)
        return '空'


# 提取评标专家
def pro_ex(content):
    try:
        for i in ex_rule['pro']:
            if re.search(i,content, re.I | re.S):
                pro = re.findall(i, content)[0].strip().replace('；','')
                if 1 < len(pro) < 32 and word_filter(pro) and pro != '':
                    return pro
        return '空'
    except:
        pass

def get_method_by_regex(content):
    regex_list = [
        '(?:本项目采购\s*方式)(?::|：)(.*?)(?:\d[.、])',
    ]
    for i in regex_list:
        if re.search(i, content, re.I | re.S):
            method = re.findall(i, content)[0].strip()
            return method


# 提取采购方式
def method_ex(title,content):
    try:
        # for i in ex_rule['method']:
        #     if re.search(i,content, re.I | re.S):
        #         print(re.findall(i, content)[0].strip())
        #         return meth[re.findall(i, content)[0].strip()]
        m = get_method_by_regex(content)
        for k, v in meth.items():
            if m:
                if re.search(k, m, re.I | re.S):
                    return v
        for k, v in meth.items():
            # print(k,'kkkkkkkkk')
            if re.search(k, title, re.I | re.S):
                return v
        for k, v in meth.items():
            if re.search(k, content, re.I | re.S):
                # 将从文本提出的单一来源采购方式，改为其他
                if v == dyly:
                    return 21
                return v
        return 21
    except:
        return 21


# 提取公告类型
def type_ex(title,content='',win_money=None):
    try:
        # print(title,'title_type')
        for k, v in wei.items():

            if re.search(k, title, re.I | re.S):
                # 遇到成交公告，判断正文有没有中标金额，如果没有废标字样，如果有并且没有金额，判断此公告为废标公告。
                end_words = ['成交公告','采购结果公告','成交结果公告','结果公告']
                if k in end_words:
                    v = get_type(content,win_money)
                    print(v,'vvvvvvvvvvvvv')
                    return v

                print(k)
                return v[0]
        # content_type_list = []
        for k, v in wei.items():
            if re.search(k, content, re.I | re.S):
                if v[0] == 44:
                    # 合同 这两个字在什么类型的公告中都出现的很多
                    t = re.search('合同公告|合同金额|合同编号|合同名称', content, re.I | re.S)
                    if not t:
                        continue

                print(k,'kkkkkkkkkkkk')
                # content_type_list.append(v)

        # print(content_type_list,'content_type_list')
                return v[0]
        return 14
    except:
        return 14


def get_type(content,win_money=None):
    for k, v in wei.items():
        type_content = re.search(k, content, re.I | re.S)
        # print(k,'k')
        # print(type_content,'type_content')
        # print(v[0],'v0')
        # print(fblb, 'fblb')
        # print(win_money,'win_money')


        if type_content and v[0] == fblb and (not win_money or win_money == '空'):
            # print(win_money, 'wwwwwwwww')
            # print(fblb, 'fblb')
            # print(type_content, 'type_content')
            print(k)
            return v[0]
        # elif type_content and v[0] != fblb:
        #     print(k)
        #     return v[0]
    return 4

# 提取采购人分类
def purchaser_class_ex(content):
    # 1.人工打标签
    # 2.机器学习分类算法自动打
    pass


# 提取项目简介
def project_intro_ex(content):
    try:
        for i in ex_rule['intro']:
            if re.search(i,content, re.I | re.S):
                return re.findall(i, content)[0].strip()[:150]
        project_intro = content
        # print(project_intro)
        return project_intro[:150]
    except:
        pass



def money_ex(str_money):
    try:
        print(str_money,'str_money')
        # print(re.search('kljkjk',str_money))
        if re.search('元整',str_money) or re.search('[〇壹贰叁肆伍陆柒捌玖拾佰仟万亿]',str_money):
            # for i in ['中标金额','成交金额','成交结果','中标结果','中标价格','报价','预算']:
                # c_money = re.findall('.*{}(.*?)元整.*'.format(i),str_money, re.I | re.S)
            c_money = re.findall('[〇一二三四五六七八九零壹贰叁肆伍陆柒捌玖拾佰仟万亿]*',str_money, re.I | re.S)
            # print(c_money,'ccccccccccccccccc')
            if c_money:
                for i in c_money:
                    if len(i) > 1:
                        try:
                            # print(i)
                            return str(decimal.Decimal(chinese_to_num(i) * 100))
                        except:
                            pass

        guess_money = re.search('万元|万',str_money)
        # print(guess_money)
        if not guess_money:
            # print(re.findall('\d+.\d+|\d+.\d+.\d+|\d+.\d+.\d+.\d+|\d+.\d+.\d+.\d+.\d+',str_money)[0].strip().replace(',',''),'guessmoney')
            return str(int(decimal.Decimal(re.findall('\d+.\d+.\d+.\d+.\d+|\d+.\d+.\d+.\d+|\d+.\d+.\d+|\d+.\d+|\d+',str_money)[0].strip().replace(',',''))*100))
        # print(decimal.Decimal(
        #     re.findall('\d+.\d+.\d+.\d+.\d+|\d+.\d+.\d+.\d+|\d+.\d+.\d+|\d+.\d+|\d+', str_money)[0].strip().replace(',',
        #                                                                                                         '')) * 1000000)
        return str(int(decimal.Decimal(re.findall('\d+.\d+.\d+.\d+.\d+|\d+.\d+.\d+.\d+|\d+.\d+.\d+|\d+.\d+|\d+',str_money)[0].strip().replace(',',''))*1000000))
    except:
        return


def match_th():
    n = 1
    th_list = []
    aa = []

    while n:
        aa = etree.HTML(html).xpath(
            '//div[@class="vF_detail_content"]//table[1]//th[1]//td[{}]//text()'.format(str(n)))
        # print(aa,'aaaaaaaaaaaaa')
        if aa == []:
            aa = etree.HTML(html).xpath('//table[1]//th[1]//td[{}]//text()'.format(str(n)))
        elif not aa:
            n = 1
            break
        n += 1

    th_list.append(''.join(aa).strip())

    return th_list


def table_money_ex(html,buy_type,url_tag='',table_name='id="zhongbiaoxinxi"'):
    try:
        flag = 0
        n = 1
        a_list = []
        b_list = []


        for i in range(1,3):
            while n:
                # if url_tag == 'ccgp-hebei.gov.cn':
                #     aa = etree.HTML(html).xpath('//table[@id="detail"]//tr[{}]//td[{}]//text()'.format(str(i),str(n))
                # else:
                aa = etree.HTML(html).xpath('//div[@class="vF_detail_content"]//table[1]//tr[1]//th[{}]//text() | //div[@class="vF_detail_content"]//table[1]//tr[{}]//td[{}]//text()'.format(str(n),str(i),str(n)))
                # print(aa,'aaaaaaaaaaaaa')
                if aa == []:
                    aa = etree.HTML(html).xpath(
                        '//table[@id="detail"]//tr[1]//th[{}]//text() | //table[@id="detail"]//tr[2]//td[{}]//text()'.format(str(n),str(n)))
                    if aa == []:
                        aa = etree.HTML(html).xpath(
                            '//table[@{table_name}]//tr[1]//th[{}]//text() | //table[@{table_name}]//tr[{}]//td[{}]//text()'.format(
                                str(n), str(i), str(n), table_name=table_name))
                        # print(aa, '====================================')
                        if aa == []:
                            aa = etree.HTML(html).xpath(
                                '//div[@id="textarea"]//table[1]//table//tr[1]//th[{}]//text() | //div[@id="textarea"]//table[1]//table//tr[{}]//td[{}]//text()'.format(
                                    str(n), str(i), str(n)))

                            if aa == []:
                                aa = etree.HTML(html).xpath(
                                    '//table[@class="template-bookmark uuid-1599570948000 code-AM014zbcj001 text-中标/成交结果信息"]//tr[1]//th[{}]//text() | //table[@class="template-bookmark uuid-1599570948000 code-AM014zbcj001 text-中标/成交结果信息"]//tr[1]//td[{}]//text()'.format(
                                        str(n), str(n)))
                                if aa == []:
                                    # print(aa)
                                    aa = etree.HTML(html).xpath(
                                        '//table[1]//tr[1]//th[{}]//text() | //table[1]//tr[{}]//td[{}]//text()'.format(str(n), str(i),str(n)))

                                else:
                                    flag = 1

                if not aa:
                    n = 1
                    break
                if i == 1:
                    a_list.append(''.join(aa).strip().replace('\n','').replace(' ','').replace('\t','').replace('\r',''))
                elif i == 2:
                    b_list.append(''.join(aa).strip().replace('\n','').replace(' ','').replace('\t','').replace('\r',''))
                if flag == 2:
                    # print(flag)
                    break
                n += 1


        # print(len(a_list),a_list,'a_list')
        # print(len(b_list),b_list,'b_list')


        # a = [i for i in etree.HTML(html).xpath('//div[@class="vF_detail_content"]//table//tr[1]//text()') if not ' ' in i ]
        # b = [i for i in etree.HTML(html).xpath('//div[@class="vF_detail_content"]//table//tr[2]//text()') if not ' ' in i ]
        # c = etree.HTML(html).xpath('//div[@class="vF_detail_content"]//table//tr[3]//text()')
        # print(a_list)
        # print(b_list)
        # print(c)

        if flag == 1 or flag == 2:
            table_list = a_list
        else:
            table_list = list(map(lambda x, y: x + y, a_list, b_list))
        print(table_list,'+++++++++++++++++++')
        if buy_type == 1:
            for i in table_list:
                if re.search('期限',i):
                    continue
                if re.search('预算|最高限价|采购金额|预算金额|预算金额（万元）|控制总价\(元\)|控制金额\(元\)',i):
                    money = money_ex(i)
                    # print(money)
                    if money and int(money) < 100000000000:
                        # print(money)
                        return money
        if buy_type == 2:
            for j in table_list:
                if re.search('期限',j):
                    continue
                if re.search('中标金额|成交金额|成交金额(万元)|成交结果|中标结果|中标价格|报价|中标价|中标（成交）金额（单位：元）|中标（成交）金额\(元\)投标报价:|中标（成交）金额\(元\)|中标总价|成交价|总价',j) and not re.search('以下|以上|至|以内',j):
                    money = money_ex(j)
                    # print(money,'bidmoney')
                    if money and 100 < int(money) < 100000000000:
                        return money
        return '空'
    except Exception as e:
        print(sys.exc_info())
        return '空'





# 提取中标金额
def winbid_money_ex(content):
    try:
        #单位是 万元 的
        for i in ex_rule['w_money']['thousand']:
            try:
                if re.search(i,content, re.I | re.S):

                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(re.findall(i, content)[0].strip().replace(',', '')) * 1000000 * conf.dollar)
                    # print(re.findall(i, content)[0],'ooooooooo')
                    print(i)

                    thousand = decimal.Decimal(re.findall(i, content)[0].strip().replace(',',''))*1000000
                    # print(int(thousand))
                    if len(str(int(thousand))) < 14 and not str(int(thousand)).startswith('-'):
                        return str(thousand)
            except:
                pass
        #单位是 元
        for i in ex_rule['w_money']['normal']:
            try:
                # print(i)
                if re.search(i,content, re.I | re.S):

                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(re.findall(i, content)[0].strip().replace(',', '')) * 100 * conf.dollar)
                    # print(re.findall(i, content)[0],'xxxxxxxxx')
                    print(i,'aaaaaaaaaaaaa')
                    print(re.findall(i, content),'bbbbbbbbbbbbbbbb')
                    for i in re.findall(i, content):
                        if i:
                            normal = decimal.Decimal(i.strip().replace(',',''))*100
                            print(normal)
                            if len(str(int(normal))) < 14:
                                return str(normal)
            except:
                print(1111111111)
                # continue
        #单位是 亿 的，转换为万元
        for i in ex_rule['w_money']['billion']:
            try:
                if re.search(i,content, re.I | re.S):
                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(re.findall(i, content)[0].strip().replace(',', '')) * 10000000000 * conf.dollar)
                    # print(re.findall(i, content)[0],'xxxxxxxxx')
                    return str(decimal.Decimal(re.findall(i, content)[0].strip().replace(',',''))*10000000000)
            except:
                pass
        return '空'
    except Exception as e:
        print('Exception:',e)
        return '空'


# 有多个中标价格求和
def win_money_split_ex(content):

    try:
        #单位是 万元 的
        for i in ex_rule['w_money_s']['thousand']:
            try:
                # print(i)
                if re.search(i,content, re.I | re.S):
                    moneys = re.findall(i, content)
                    # print(i,'dsaaaaaaaaaa')
                    if '美元' in i or '$' in i:
                        return str(sum([decimal.Decimal(x) * 1000000 for x in re.findall(i, content)])*conf.dollar)
                    # print(re.findall(i, content)[0],'ooooooooo')
                    if '、' in moneys[0]:
                        moneys = moneys[0].split('、')
                    # print(moneys,'moneys-------------')
                    thousand = total_amount(moneys,1000000)


                    # thousand = sum([decimal.Decimal(x.strip().replace(',', '')) * 1000000 for x in moneys])
                    if len(str(int(thousand))) < 14:
                        return str(thousand)
            except:
                pass
        #单位是 元 的，转换为万元
        for i in ex_rule['w_money_s']['normal']:
            try:
            #     print(i)
                if re.search(i,content, re.I | re.S):
                    # print(i)
                    moneys = re.findall(i, content)
                    print(moneys, 'moneys-------------')
                    if '美元' in i or '$' in i:
                        return str(sum([decimal.Decimal(x) * 100 for x in re.findall(i, content)])*conf.dollar)
                    # print(re.findall(i, content, re.I | re.S),'xxxxxxxxx')

                    normal = total_amount(moneys, 100)
                    # print(moneys,'moneys-------------')
                    # normal = sum([decimal.Decimal(x.strip().replace(',',''))*100 for x in moneys])
                    if len(str(int(normal))) < 14:
                        return str(normal)
            except:
                pass
        #单位是 亿 的，转换为万元
        for i in ex_rule['w_money_s']['billion']:
            try:
                if re.search(i,content, re.I | re.S):
                    # print(i)
                    if '美元' in i or '$' in i:
                        return str(sum([decimal.Decimal(x) * 10000000000 for x in re.findall(i, content)])*conf.dollar)
                    # print(re.findall(i, content)[0],'xxxxxxxxx')
                    return str(sum([decimal.Decimal(x.strip().replace(',',''))*10000000000 for x in re.findall(i, content)]))
            except:
                pass
        return '空'
    except Exception as e:
        print('Exception:',e)
        return '空'

# 粗提取
def win_money_rough_ex(content):
    try:
        #单位是 万元 的
        for i in ex_rule['w_money_r']['thousand']:
            try:
                if re.search(i,content, re.I | re.S):
                    rough = re.findall(i, content)[0]
                    if '美元' in i or '$' in i:
                        result = str(
                            decimal.Decimal(''.join(re.findall('[\d*.]', rough)).strip().replace(',', '')) * 1000000* conf.dollar)
                        return result
                    thousand = decimal.Decimal(''.join(re.findall('[\d*.]', rough)).strip().replace(',', '')) * 1000000
                    if len(str(int(thousand))) < 14:
                        return str(thousand)
            except:
                pass
        #单位是 元 的，转换为万元
        for i in ex_rule['w_money_r']['normal']:
            try:
                if re.search(i,content, re.I | re.S):
                    rough = re.findall(i, content)[0]
                    if '美元' in i or '$' in i:
                        result = str(
                            decimal.Decimal(''.join(re.findall('[\d*.]', rough)).strip().replace(',', '')) * 100* conf.dollar)
                        return result
                    # print(rough)
                    # print(re.findall('\d*\.\d*|\d*.\d*.\d*|\d*\.\d*.\d*\.\d*|\d*\.\d*\.\d*\.\d*\.\d*', rough))

                    normal = decimal.Decimal(''.join(re.findall('[\d*.]', rough)).strip().replace(',', ''))*100
                    if len(str(int(normal))) < 14:
                        return str(normal)
            except:
                pass
        #单位是 亿 的，转换为万元
        for i in ex_rule['w_money_r']['billion']:
            try:
                if re.search(i,content, re.I | re.S):
                    rough = re.findall(i, content)[0]
                    if '美元' in i or '$' in i:
                        result = str(
                            decimal.Decimal(''.join(re.findall('[\d*.]', rough)).strip().replace(',', '')) * 10000000000* conf.dollar)
                        return result
                    result = str(decimal.Decimal(''.join(re.findall('[\d*.]', rough)).strip().replace(',', '')) * 10000000000)
                    return result
            except:
                pass
        return '空'
    except Exception as e:
        print('Exception_r:',e)
        return '空'


# 中标金额是中文，提取并转换
def win_money_chinese(content):
    try:
        # 单位是 万元 的
        for i in ex_rule['w_money_c']['thousand']:
            try:
                if re.search(i,content, re.I | re.S):
                    # print(i)
                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(sum([chinese_to_num(i.strip().replace(',','')) for i in re.findall(i, content)])) * 1000000*conf.dollar)
                    # print(re.findall(i, content)[0],'ooooooooo')
                    return str(decimal.Decimal(sum([chinese_to_num(i.strip().replace(',','')) for i in re.findall(i, content)]))*1000000)
            except:
                pass
        # 单位是 元 的，转换为万元
        for i in ex_rule['w_money_c']['normal']:
            try:
                # print(i)
                if re.search(i,content, re.I | re.S):
                    print(i)
                    if '美元' in i or '$' in i:
                        # print(re.findall(i, content)[0],'xxxxxxxxx')
                        return str(decimal.Decimal(sum([chinese_to_num(i.strip().replace(',','')) for i in re.findall(i, content)])) * 100*conf.dollar)
                    # print(re.findall(i, content)[0],'xxxxxxxxx')
                    return str(decimal.Decimal(sum([chinese_to_num(i.strip().replace(',','')) for i in re.findall(i, content)]))*100)
            except:
                pass
        # 单位是 亿 的，转换为万元
        for i in ex_rule['w_money_c']['billion']:
            try:
                if re.search(i, content, re.I | re.S):
                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(chinese_to_num(re.findall(i, content)[0].strip().replace(',',''))) * 10000000000*conf.dollar)
                    # print(re.findall(i, content)[0],'xxxxxxxxx')
                    return str(decimal.Decimal(chinese_to_num(re.findall(i, content)[0].strip().replace(',',''))) * 10000000000)
            except:
                pass
        return '空'
    except Exception as e:
        print('Exception:',e)
        return '空'


def money_ex_special(det_html,url_tag,content):
    if url_tag=='ccgp-hebei.gov.cn':
        try:
            # 取id="con"的span标签(<span id="con">)下的全部内容（不含标签）
            table_str = etree.HTML(det_html).xpath('//span[@id="con"]/text()')[0]
            # 以#_@_@分割字符串，返回一个列表
            table_list = table_str.split('#_@_@')
            # 取列表中索引为10的内容，去除‘，’和空格，这个内容就是金额
            money = table_list[10].strip().replace(',','')
            if '#_#' in money:

                money = sum([int(i) for i in money.split('#_#')])

            win_money =  decimal.Decimal(money)*100

            return str(win_money)
        except Exception as e:
            print(e)
            return '空'
    elif url_tag=='ccgp-tianjin':
        table_name = 'id="projectBundleList"'
        return table_money_ex(html=det_html,buy_type=2,url_tag=url_tag,table_name=table_name)

    # else:
    #     is_win_money = re.search('(?<!例如)(?:中标成交结果公告|中标[(（]成交[）)]结果公告|中标结果公示|中标结果公告|中标公告|中标公示|成交公告)(?!发布之日)',content)
    #     print(re.findall('(?:中标成交结果公告|中标[(（]成交[）)]结果公告|中标结果公示|中标结果公告|中标公告|中标公示|成交公告)(?!发布之日)',content),'-------lililili-------')
    #     if is_win_money:
    #         win_money = re.findall('(?:[\u4e00-\u9fa5])(?::|：)?([\d.,]*?)(?:元人民币|元)',content)
    #         # print(win_money, 'win_money')
    #         for i in win_money:
    #             if i:
    #                 return str(decimal.Decimal(i.strip().replace(',', '')) * 100)



    return '空'

def table_yixiang_money(table_xpath='',table2_xpath='',det_html=''):

    table_header = etree.HTML(det_html).xpath(table_xpath)
    # print(table_header,len(table_header),'table_header')
    t = ''.join(table_header)
    t = re.sub('\s+', '@-@', t)
    table_header = t.strip('@-@').split('@-@')
    # a = [table_header[i-1]+table_header[i] for i in range(len(table_header)) if table_header[i].startswith('（')]
    table_center = etree.HTML(det_html).xpath(table2_xpath)
    # print(table_center,len(table_center),'table_center')
    t = ''.join(table_center)
    t = re.sub('\s+', '@-@', t)
    table_center = t.strip('@-@').split('@-@')
    # print(table_center)
    table_dict = dict(zip(table_header, table_center))
    # print(table_dict)
    title_list = ['预算金额（万元）', '预算（万元）']
    for i in title_list:
        try:
            budget_money = decimal.Decimal(table_dict[i].strip().replace(',', '')) * 1000000
            # print(budget_money)
            return str(budget_money)
        except:
            pass


def budget_money_special(det_html,url_tag):
    try:
        if url_tag=='ccgp-hebei.gov.cn':
            try:
                table_str = etree.HTML(det_html).xpath('//span[@id="intentionAnncInfos"]/text()')[0]
                table_list = table_str.split('#_@_@')
                # print(table_list)
                budget_money = decimal.Decimal(table_list[3].strip().replace(',', '')) * 100
                return str(budget_money)
            except Exception as e:
                print(e)
                return '空'
        elif url_tag == 'ccgp-shandong':
            title_xpath = '//div[@id="textarea"]//table[1]//table//tr[1]//text()'
            table_xpath = '//div[@id="textarea"]//table[1]//table//tr[2]//text()'
            if table_yixiang_money(title_xpath,table_xpath,det_html):
                return table_yixiang_money(title_xpath,table_xpath,det_html)
            else:
                return '空'

        elif url_tag == 'ccgp-tianjin':
            title_xpath = '//tr[@class="tableHeader"]//text()'
            table_xpath = '//tr[@class="tableHeader"]//following-sibling::tr[1]//text()'
            if table_yixiang_money(title_xpath,table_xpath,det_html):
                return table_yixiang_money(title_xpath,table_xpath,det_html)
            else:
                return '空'

        elif url_tag == 'ccgp-jiangsu':
            title_xpath = '//div[@class="IntentionDisclosurePreviewTable"]//table[1]//thead//text()'
            table_xpath = '//div[@class="IntentionDisclosurePreviewTable"]//table[1]//tr[1]//text()'

            table_header = etree.HTML(det_html).xpath(title_xpath)
            print(table_header, len(table_header), 'table_header')

            table_center = etree.HTML(det_html).xpath(table_xpath)
            print(table_center, len(table_center), 'table_center')

            table_dict = dict(zip(table_header, table_center))
            print(table_dict)
            title_list = ['预算金额（万元）', '预算（万元）','采购预算(万元)']
            for i in title_list:
                try:
                    budget_money = decimal.Decimal(table_dict[i].strip().replace(',', '').replace('万元','')) * 1000000
                    # print(budget_money)
                    return str(budget_money)
                except:
                    continue
            return '空'

        elif url_tag == 'ccgp-sichuan':
            title_xpath = '//div[@class="tableBox"]//table//tr[1]//text()'
            table_xpath = '//div[@class="tableBox"]//table//tr[3]//text()'
            if table_yixiang_money(title_xpath, table_xpath, det_html):
                return table_yixiang_money(title_xpath, table_xpath, det_html)
            else:
                return '空'






        else:
            return '空'

    except:
        return '空'





def win_money_all(content,html,url_tag=''):
    try:
        # w_rough = win_money_rough_ex(content)
        w_special = money_ex_special(html,url_tag,content)
        print(w_special,'w_special')
        w_sum = win_money_split_ex(content)
        print(w_sum,'w_sum')
        # w_sum = '空'
        w_chinese = win_money_chinese(content)
        print(w_chinese,'w_chinese')
        w_money = winbid_money_ex(content)
        print(w_money,'w_money')
        w_table = table_money_ex(html,2,url_tag)
        print(w_table,'w_table')


        if w_sum != '空':
            if float(w_sum) >= 0:
                print('1')
                return w_sum
        elif w_special != '空':
            if float(w_special) >= 0:
                print('5')
                return w_special
        elif w_chinese != '空' and w_chinese != '0':
            if float(w_chinese) > 0:
                print('2')
                return w_chinese
        elif w_money != '空':
            if float(w_money) >= 0:
                print('3')
                return w_money
        elif w_table != '空':
            if float(w_table) >= 0:
                print('4444')
                return w_table

        return '空'
    except Exception as e:
        print('Exception:',e)
        return '空'


def winning_bidder_all(content,html,url_tag):
    try:
        w_bidder = winning_bider(content)
        w_bidder_table = winning_bider_table(html,url_tag)

        if w_bidder_table != '空':
            print('win_bid:  1')
            return w_bidder_table
        elif w_bidder != '空':
            print('win_bid:  2')
            return w_bidder
        return '空'
    except Exception as e:
        print('Exception:', e)
        return '空'


def winning_bider(content):
    try:
        for i in ex_rule['w_bider']:
            # print(i)
            if re.search(i,content, re.I | re.S):
                # print(content,'wb_content')
                # print(i)
                result_list = re.findall(i, content)
                for result_1 in result_list:
                    if len(result_1) > 1:

                        if len(result_1) < 64 and word_filter(result_1):
                            return word_clear(result_1)
        return '空'
    except:
        return '空'

# 从表格提取中标单位
def winning_bider_table(html,url_tag=None):
    try:
        flag = 0
        n = 1
        a_list = []
        b_list = []

        for i in range(1,3):
            while n:
                # if url_tag == 'ccgp-hebei.gov.cn':
                #     aa = etree.HTML(html).xpath('//table[@id="detail"]//tr[{}]//td[{}]//text()'.format(str(i),str(n))
                # else:
                wb = yzb_win_bidder_ex.WinningBidderEx(html=html, url_tag=url_tag, i=i, n=n)
                aa,flag = wb.wb_ex()
                # print(aa,'111111111')
                # aa = etree.HTML(html).xpath('//div[@class="vF_detail_content"]//table[1]//tr[1]//th[{}]//text() | //div[@class="vF_detail_content"]//table[1]//tr[{}]//td[{}]//text()'.format(str(n),str(i),str(n)))
                # print(aa,'aaaaaaaaaaaaa')
                if aa == [] or aa == None:
                    aa = etree.HTML(html).xpath(
                        '//table[@id="detail"]//tr[1]//th[{}]//text() | //table[id="detail"]//tr[2]//td[{}]//text()'.format(str(n),str(n)))
                    if aa == []:
                        aa = etree.HTML(html).xpath('//table[@class="template-bookmark uuid-1599570948000 code-AM014zbcj001 text-中标/成交结果信息"]//tr[1]//th[{}]//text() | //table[@class="template-bookmark uuid-1599570948000 code-AM014zbcj001 text-中标/成交结果信息"]//tr[1]//td[{}]//text()'.format(str(n), str(n)))
                        if aa == []:
                            aa = etree.HTML(html).xpath(
                                '//table[1]//tr[1]//th[{}]//text() | //table[1]//tr[{}]//td[{}]//text()'.format(str(n), str(i),str(n)))
                        else:
                            flag = 1
                # print(aa,flag)
                if not aa:
                    n = 1
                    break
                if i == 1:
                    a_list.append(''.join(aa).strip())
                elif i == 2:
                    b_list.append(''.join(aa).strip())
                if flag == 2:
                    # print(flag)
                    break
                n += 1


        # print(len(a_list),a_list,'a_list')
        # print(len(b_list),b_list,'b_list')


        # a = [i for i in etree.HTML(html).xpath('//div[@class="vF_detail_content"]//table//tr[1]//text()') if not ' ' in i ]
        # b = [i for i in etree.HTML(html).xpath('//div[@class="vF_detail_content"]//table//tr[2]//text()') if not ' ' in i ]
        # c = etree.HTML(html).xpath('//div[@class="vF_detail_content"]//table//tr[3]//text()')
        # print(a_list)
        # print(b_list)
        # print(c)
        if flag == 1 or flag == 2:
            table_list = a_list
        else:
            table_list = list(map(lambda x, y: x + y, a_list, b_list))
        # print(table_list,'xxxxxxxxx')
        for j in table_list:
            regex_str = '中标供应商名称|供应商名称|中标供应商|供应商名称|成交供应商|成交单位|成交候选人|中标单位|中标人|供应商信息|供应商|投标商名称'
            if re.search(regex_str,j):
                bidder = re.sub(regex_str,'',j)
                # print(money)
                if len(bidder) < 64 and '':
                    return bidder
        return '空'
    except Exception as e:
        print(sys.exc_info(),'xxxxxxxx')
        return '空'

def bidder_ex(str_bidder):
    try:
        # print(str_money,'str_money')
        if re.search('元整',str_bidder):
            # for i in ['中标金额','成交金额','成交结果','中标结果','中标价格','报价','预算']:
                # c_money = re.findall('.*{}(.*?)元整.*'.format(i),str_money, re.I | re.S)
            c_money = re.findall('[〇一二三四五六七八九零壹贰叁肆伍陆柒捌玖拾佰仟万亿]*',str_bidder, re.I | re.S)
            # print(c_money)
            if c_money:
                for i in c_money:
                    if i:
                        try:
                            # print(i)
                            return str(decimal.Decimal(chinese_to_num(i) * 100))
                        except:
                            pass

        guess_money = re.search('万元|万',str_bidder)
        # print(guess_money)
        if not guess_money:
            # print(re.findall('\d+.\d+|\d+.\d+.\d+|\d+.\d+.\d+.\d+|\d+.\d+.\d+.\d+.\d+',str_money)[0].strip().replace(',',''))
            return str(int(decimal.Decimal(re.findall('\d+.\d+.\d+.\d+.\d+|\d+.\d+.\d+.\d+|\d+.\d+.\d+|\d+.\d+|\d+',str_bidder)[0].strip().replace(',',''))*100))
        # print(decimal.Decimal(
        #     re.findall('\d+.\d+.\d+.\d+.\d+|\d+.\d+.\d+.\d+|\d+.\d+.\d+|\d+.\d+|\d+', str_money)[0].strip().replace(',',
        #                                                                                                         '')) * 1000000)
        return str(int(decimal.Decimal(re.findall('\d+.\d+.\d+.\d+.\d+|\d+.\d+.\d+.\d+|\d+.\d+.\d+|\d+.\d+|\d+',str_bidder)[0].strip().replace(',',''))*1000000))
    except:
        return


def winning_bider_html(html,url):
    try:
        for i in ex_rule['c_html'][url]:
            if not etree.HTML(html).xpath(i) == []:
                winbid = etree.HTML(html).xpath(i)
                return winbid
        return '空'
    except Exception as e:
        print('Exception:',e)

def subject_ex(title):
    try:
        stopword = ['更正通知','变更通知','更正公告','变更公告','补充公告','延期公告','废标公告','流标公告','工程项目','废标','流标','未成交公告','异常公告','终止公告','中标公告','中标公示','中标结果公示','成交公告','采购结果公告','成交结果公告','结果公告','需求公告','竞争性谈判','竞争性磋商','邀请招标','询价','单一来源','资格预审','公开招标','采购公告','招标公告','公示','公告','采购项目','服务项目','采购及服务项目','采购','竞价','项目','评标','招标','补遗',]
        word_n_list = []
        last = ''
        word_nz = ''
        word_n = ''
        for j in stopword:
            if j in title:
                title = title.replace(j,'')
        w_list_l = [i.toString() for i in HanLP.segment(title)]
        w_str_l = ','.join(w_list_l)
        w_list = w_str_l.split('/nis').pop().split('/ns').pop().split(',')
        w_str = ','.join(w_list)
        # print(w_list)

        # if '/cc' in w_str:
        #     for c in range(len(w_list)):
        #         if '/cc' in w_list[c]:
        #             return '{},{}'.format(re.sub('/[a-z]{1,3}','',''.join(w_list[c-1])),re.sub('/[a-z]{1,3}','',''.join(w_list[c+1])))
        for word in w_list:
            if word.endswith('/cc'):
                pass
            if word.endswith('/nz'):
                word_nz = word
                # print(word.replace('/nz',''))
                # break
            if word.endswith('/n'):
                word_n = word
                if last[-2:] == word[-2:]:
                    if last not in word_n_list:
                        word_n_list.append(last)
                    if word not in word_n_list:
                        word_n_list.append(word)
            last = word
        if word_nz != '':
            return word_nz.replace('/nz','')
        elif word_n_list != []:
            return ''.join(word_n_list).replace('/n','')
        elif word_n != '':
            return word_n.replace('/n','')
        return re.sub('/[a-z]{1,3}','',''.join(w_list))[:63]

    except Exception as e:
        print(e)


# 提取品目
# def items_ex(title):
#     try:
#         for item in item_list:
#             if re.search(item,title):
#                 return re.findall(item,title)[0]
#         return '空'
#     except Exception as e:
#         # print(e)
#         return '空'

# 提取省市区
def province_ex_second(address):
    # 提取标题中没有后缀的省市区
    try:
        for adds in address:
            # print(local_dic)
            # print(local_dic.values())
            for k, v in local_dic.items():

                for k_city, v_city in v.items():

                    for v_town in v_city:

                        clean_town = re.sub('旗|满族自治县|维吾尔自治区|壮族自治区|满族蒙古族自治县|回族自治县|哈萨克自治州|自治州|地区|自治区|区|县|市|省','',v_town)
                        if len(clean_town)>1 and clean_town in adds:
                            return [k, k_city, v_town]

                    clean_city = re.sub('旗|满族自治县|维吾尔自治区|壮族自治区|满族蒙古族自治县|回族自治县|哈萨克自治州|自治州|地区|自治区|区|县|市|省', '', k_city)
                    if len(clean_city)>1 and clean_city in adds:
                        return [k, k_city, '空']
                # print(k)
                clean_province = re.sub('旗|满族自治县|维吾尔自治区|壮族自治区|满族蒙古族自治县|回族自治县|哈萨克自治州|自治州|地区|自治区|区|县|市|省', '', k)
                # print(clean_province)
                if len(clean_province)>1 and clean_province in adds:
                    return [k, '空' , '空']
        return ['空', '空', '空']
    except Exception as e:
        print(e)
        return ['空', '空', '空']


# 提取省市区
def province_ex(address_list,url_tag=None):
    """
    提取采购单位的省份

    :param address: 传入采购单位地址
    :return: 返回查询到的省，如果查询不到返回‘其他’
        例：address:广州市黄埔大道西601号    return 广东省
    """
    # import jieba

    # print(local_dic)
    # address_list.remove(None)
    address_list_split = re.findall('.*旗|.*矿区|.*满族自治县|.*满族蒙古族自治县|.*回族自治县|.*自治州|.*地区|.{1,4}自治区|.{1,4}镇|.{1,4}区|.{1,4}县|.{1,4}市|.{2,3}省|',''.join(address_list))
    # 由于采集的地址省在最前，区在最后所以翻转列表使地址更精确
    address_list_split = [i for i in address_list_split if i != '']
    address_list_split.reverse()
    print(address_list_split,'address_list_split')

    # town = re.findall('.*区|.*县|.*矿区|.*满族自治县|.*满族蒙古族自治县|.*回族自治县|.*自治州|.*地区|.*省|.*自治区|.*市',address)
    try:
        final_address = []
        for address in address_list_split:
            if address:
                for k, v in local_dic.items():
                    province = re.search(k, address, re.I | re.S)
                    for k_city, v_city in v.items():
                        city = re.search(k_city, address, re.I | re.S)
                        for v_town in v_city:
                            town = re.search(v_town, address, re.I | re.S)
                            # city = re.search(k_city, address, re.I | re.S)
                            # province = re.search(k, address, re.I | re.S)
                            if town:
                                if [k, k_city, v_town] not in final_address:
                                    final_address.append([k, k_city, v_town])
                                # return [k, k_city, v_town]
                            # elif city:
                            #     return [k, k_city, '空']
                            # elif province:
                            #     return [k, '空', '空']
                        if city:
                            if [k, k_city, '空'] not in final_address:
                                final_address.append([k, k_city, '空'])
                            # return [k, k_city, '空']
                    if province:
                        if [k, '空', '空'] not in final_address:
                            final_address.append([k, '空', '空'])
                        # return [k, '空', '空']
        print(final_address,'final_address')
        if len(final_address) == 1:
            return final_address[0]
        elif len(final_address) > 1:
            for i in range(len(final_address)):
                print(final_address[i][2],len(final_address[i][2]))
                if (final_address[i][2].endswith('县')) and (len(final_address[i][2]) > 2):
                    return final_address[i]
                elif (final_address[i][2] == '鼓楼区'):
                    if final_address[i][0]  in address_list or final_address[i][1] in address_list:
                        return final_address[i]
                    else:
                        return ['空', '空', '空']
                elif final_address[i][2] != '空':
                    if final_address[i][1] in address_list_split:
                        return final_address[i]
                    elif final_address[i][0] in address_list_split:
                        return final_address[i]
                # elif ('吉县' in final_address[i][2]) and (len(final_address[i][2]) > 2):
                #     return final_address[i]


            return final_address[0]
        else:

            return ['空', '空', '空']
    except Exception as e:
        print(e)
        return ['空', '空', '空']


def province_ex_all(address_list_list,url_tag):
    try:
        p = tag_address.get(url_tag)

        print(address_list_list,'---------------address_list_list')
        for address_list in address_list_list:
            print(address_list,'address_list')
            if None in address_list:
                address_list.remove(None)
            elif address_list == ['空']:
                continue
            first = province_ex(address_list, url_tag)
            # print(first,'----------------first')
            if first==['空', '空', '空']:
                second = province_ex_new(address_list)
                # print(second,'---------------second')
                if second==['空', '空', '空']:
                    print(1111111111111)
                    # for tag, add_province in tag_address.items():
                    #     # print(tag)
                    #     if tag == url_tag:
                    # return [p, '空', '空']
                    continue
                if second[0] == p:
                    return second
                elif p != None:
                    return [p, '空', '空']
                else:
                    return second
            if first[0] == p and p != None:
                return first
            elif p != None:
                return [p, '空', '空']
            else:
                return first
        # print(p,'22222222222222222222')
        if p == None:
            p = '空'
        return [p, '空', '空']
    except:
        return ['空', '空', '空']



#提取省开发版
def province_ex_new(address_list):
    """
    提取采购单位的省份

    :param address: 传入采购单位地址
    :return: 返回查询到的省，如果查询不到返回‘其他’
        例：address:广州市黄埔大道西601号    return 广东省
    """

    # print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')

    import jieba
    import jieba.posseg as pseg
    jieba.load_userdict(f'{conf.crawler_file}local_dict.py')
    address_str = ''.join(address_list)

    sentence_seged = pseg.cut(address_str)

    outstr = []
    for x in sentence_seged:
        # print(x)
        if x.flag == 'ns' or x.flag == 'nt' or x.flag == 'nz' and not x.word.endswith('国'):
            outstr.append(x.word)
    print(outstr,'outstr')
    return province_ex_second(outstr)




def rm_region(str):
    return re.findall('.*区|.*县|.*矿区|.*满族自治县|.*满族蒙古族自治县|.*回族自治县|.*自治州|.*地区|.*自治区|.*市|.*省|',str)


def province_s(list_address):
    try:
        return list_address[0]
    except:
        return '空'


def city_s(list_address):
    try:
        return list_address[1]
    except:
        return '空'


def town_s(list_address):
    try:
        return list_address[2]
    except:
        return '空'


# 提取分包情况
def subcontract_ex(content):
    # try:
    #     if re.search('未分包|不分包|不进行分包', content, re.I | re.S):
    #         return '不分包'
    #     return '分包'
    # except:
    #     pass
    try:
        package_list = '|'.join(package_class)
        if re.search(package_list, content, re.I | re.S):
            return '已分包'
        return '未分包'
    except:
        return '未分包'

# 合计金额
def total_amount(money_list,unit=100):
    # print(money_list)
    # 将字符串list，转换为数字list
    money_list_float = [decimal.Decimal(money_float.strip().replace(',',''))*unit for money_float in money_list if money_float != '']
    money_list_float = list({}.fromkeys(money_list_float).keys())
    # 给金额去重，去除重复金额影响，但也有可能去掉正确金额
    # print(money_list_float)

    # 取最大金额，判断最大金额是不是其他金额总和
    max_money = max(money_list_float)

    t_money = sum(money_list_float)
    # print(t_money,'金额总和')
    if t_money == 2*max_money:
        return max_money
    elif len(set(money_list_float)) == 1:
        return money_list_float[0]

    else:
        return t_money

# 从文中提取预算金额
def budget_amount_ex_content(content):
    try:
        # 单位是 万元 的，转换为元
        for i in ex_rule['b_amount']['thousand']:
            try:
                if re.search(i,content, re.I | re.S):
                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(re.findall(i, content)[0].strip()) * 1000000 * conf.dollar)
                    print(re.findall(i, content),'ooooooooo')
                    print(i,'wwwwwwwww')

                    for i in re.findall(i, content):
                        if i:
                            normal = decimal.Decimal(i.strip().replace(',',''))*1000000
                            print(normal)
                            if len(str(int(normal))) < 14:
                                return str(normal)
            except:
                print(sys.exc_info())

        # 单位是 元 的
        for i in ex_rule['b_amount']['normal']:
            try:
                if re.search(i,content, re.I | re.S):
                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(re.findall(i, content)[0].strip()) * 100 * conf.dollar)
                    # print(re.findall(i, content)[0],'xxxxxxxxx')
                    # print(i, 'rrrrrrrrr')
                    # print(re.findall(i, content),'test_money')
                    # money_list = re.findall(i, content)
                    # if len(money_list) > 1:
                        # 提取分包合计金额，因为写了分包内容提取，暂时不用
                        # normal = total_amount(re.findall(i, content))
                    # else:
                    for i in re.findall(i, content):
                        if i:
                            normal = decimal.Decimal(i.strip().replace(',',''))*100
                            print(normal)
                            if len(str(int(normal))) < 14:
                                return str(normal)
                    # print(normal)
            except:
                pass
        # 单位是 亿 的，转换为万元
        for i in ex_rule['b_amount']['billion']:
            try:
                if re.search(i, content, re.I | re.S):
                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(re.findall(i, content)[0].strip()) * 10000000000 * conf.dollar)
                    # print(re.findall(i, content)[0],'xxxxxxxxx')
                    # print(i, 'yyyyyyyyy')
                    return str(decimal.Decimal(re.findall(i, content)[0].strip().replace(',', '')) * 10000000000)
            except:
                pass
        return '空'
    except Exception as e:
        print('Exception:',e)
        return '空'


# 有多个预算金额时提取预算金额的和
def budget_amount_sum_ex(content):
    try:
        #单位是 万元 的
        for i in ex_rule['b_amount']['thousand']:
            try:
                if re.search(i,content, re.I | re.S):
                    if '美元' in i or '$' in i:
                        return str(sum([decimal.Decimal(x.strip().replace(',','')) * 1000000 for x in re.findall(i, content)]) * conf.dollar)
                    # print(re.findall(i, content)[0],'ooooooooo')
                    print(i)
                    thousand = sum([decimal.Decimal(x.strip().replace(',',''))*1000000 for x in re.findall(i, content)])
                    if len(str(int(thousand))) < 13:
                        return str(sum([decimal.Decimal(x.strip().replace(',',''))*1000000 for x in re.findall(i, content)]))
            except Exception as e:
                print(e)

        #单位是 元 的，转换为万元
        for i in ex_rule['b_amount']['normal']:
            try:
                if re.search(i,content, re.I | re.S):
                    if '美元' in i or '$' in i:
                        return str(sum([decimal.Decimal(x.strip().replace(',','')) * 100 for x in re.findall(i, content)]) * conf.dollar)
                    # print(re.findall(i, content, re.I | re.S),'xxxxxxxxx')
                    print(i)
                    normal = sum([decimal.Decimal(x.strip().replace(',',''))*100 for x in re.findall(i, content)])
                    if len(str(int(normal))) < 13:
                        return str(normal)
            except:
                pass
        #单位是 亿 的，转换为万元
        for i in ex_rule['b_amount']['billion']:
            try:
                if re.search(i,content, re.I | re.S):
                    if '美元' in i or '$' in i:
                        return str(sum([decimal.Decimal(x.strip().replace(',','')) * 10000000000 for x in re.findall(i, content)]) * conf.dollar)
                    # print(re.findall(i, content)[0],'xxxxxxxxx')
                    return str(sum([decimal.Decimal(x.strip().replace(',',''))* 10000000000 for x in re.findall(i, content)]))
            except:
                pass
        return '空'
    except Exception as e:
        print('Exception:',e)
        return '空'


# 从HTML提取预算金额
def budget_amount_ex_html(html):
    try:
        # 单位是 万元 的
        for i in ex_rule['b_amount_h']['thousand']:
            try:
                if etree.HTML(html).xpath(i) != []:
                    # print(i)
                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(etree.HTML(html).xpath(i)[0].strip().replace(',','')) * 1000000 * conf.dollar)
                    # print(re.findall(i, html)[0],'ooooooooo')
                    thousand = decimal.Decimal(etree.HTML(html).xpath(i)[0].strip().replace(',',''))* 1000000
                    # print(thousand,len(thousand))
                    if len(str(int(thousand))) < 12 and thousand >= 0:
                        return str(decimal.Decimal(etree.HTML(html).xpath(i)[0].strip().replace(',',''))* 1000000)
            except:
                pass
        # 单位是 元 的，转换为万元
        for i in ex_rule['b_amount_h']['normal']:
            try:
                if etree.HTML(html).xpath(i) != []:
                    # print(i)
                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(etree.HTML(html).xpath(i)[0].strip().replace(',','')) * 1000000 * conf.dollar)
                    # print(re.findall(i, html)[0],'xxxxxxxxx')
                    normal = decimal.Decimal(etree.HTML(html).xpath(i)[0].strip().replace(',',''))*100
                    if len(str(int(normal))) < 12 and normal >= 0:
                        return str(normal)
            except:
                pass
        # 单位是 亿 的，转换为万元
        for i in ex_rule['b_amount_h']['billion']:
            try:
                if etree.HTML(html).xpath(i) != []:
                    # print(i)
                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(etree.HTML(html).xpath(i)[0].strip().replace(',','')) * 1000000 * conf.dollar)
                    # print(re.findall(i, html)[0],'xxxxxxxxx')
                    return str(decimal.Decimal(etree.HTML(html).xpath(i)[0].strip().replace(',', '')) * 10000000000)
            except:
                pass
        return '空'
    except Exception as e:
        print('Exception:',e)
        return '空'


# 提取中文数字预算金额，并转为阿拉伯数字
def budget_chinese_ex(content):
    try:
        # 单位是 万元 的
        # for i in ex_rule['b_amount_c']['thousand']:
        #     try:
        #         print(i)
        #         if re.search(i,content, re.I | re.S):
        #             if '美元' in i or '$' in i:
        #                 return str(decimal.Decimal(chinese_to_num(re.findall(i, content)[0].strip().replace(',',''))) * 1000000 * conf.dollar)
        #             print(re.findall(i, content)[0],'ooooooooo')
        #             print(chinese_to_num(re.findall(i, content)[0].strip().replace(',','')))
        #             return str(decimal.Decimal(chinese_to_num(re.findall(i, content)[0].strip().replace(',','')))*1000000)
        #     except:
        #         pass
        # 单位是 元 的，转换为万元
        for i in ex_rule['b_amount_c']['normal']:
            try:
                # print(i)
                if re.search(i,content, re.I | re.S):
                    # print(i,'xxxxxxxxxxxxxxx')
                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(chinese_to_num(re.findall(i, content)[0].strip().replace(',',''))) * 100 * conf.dollar)
                    # print(re.findall(i, content)[0],'xxxxxxxxx')
                    # print(chinese_to_num(re.findall(i, content)[0].strip())*100)
                    return str(decimal.Decimal(chinese_to_num(re.findall(i, content)[0].strip().replace(',','')))*100)
            except:
                pass
        # 单位是 亿 的，转换为万元
        for i in ex_rule['b_amount_c']['billion']:
            try:
                # print(i)
                if re.search(i, content, re.I | re.S):
                    if '美元' in i or '$' in i:
                        return str(decimal.Decimal(chinese_to_num(re.findall(i, content)[0].strip().replace(',',''))) * 10000000000 * conf.dollar)
                    # print(re.findall(i, content)[0],'xxxxxxxxx')
                    return str(decimal.Decimal(chinese_to_num(re.findall(i, content)[0].strip().replace(',',''))) * 10000000000)
            except:
                pass
        return '空'
    except Exception as e:
        print('Exception:',e)
        return '空'


# 提取分包金额
def budget_amount_split_ex(content):
    try:
        for i in ex_rule['b_amount_sp']:
            if re.search(i, content, re.I | re.S):
                amount_space = ''.join(re.findall(i, content, re.I | re.S))
                # 单位是 万元 的
                for i in ex_rule['b_amount_s']['thousand']:
                    try:
                        if re.search(i, amount_space, re.I | re.S):
                            if '美元' in i or '$' in i:
                                return str(sum([decimal.Decimal(x.strip().replace(',', '')) * 1000000 for x in
                                                re.findall(i, amount_space)]) * conf.dollar)
                            # print(re.findall(i, content)[0],'ooooooooo')
                            print(i)
                            print(re.findall(i, amount_space))

                            thousand = sum(
                                [decimal.Decimal(x.strip().replace(',', '')) * 1000000 for x in list(set(re.findall(i, amount_space)))])

                            if len(str(int(thousand))) < 13:
                                return str(sum([decimal.Decimal(x.strip().replace(',', '')) * 1000000 for x in
                                                re.findall(i, amount_space)]))
                    except Exception as e:
                        print(e)

                # 单位是 元 的，转换为万元
                for i in ex_rule['b_amount_s']['normal']:
                    try:
                        if re.search(i, amount_space, re.I | re.S):
                            if '美元' in i or '$' in i:
                                return str(sum([decimal.Decimal(x.strip().replace(',', '')) * 100 for x in
                                                re.findall(i, amount_space)]) * conf.dollar)
                            # print(re.findall(i, content, re.I | re.S),'xxxxxxxxx')
                            print(i)
                            normal = sum([decimal.Decimal(x.strip().replace(',', '')) * 100 for x in re.findall(i, amount_space)])
                            if len(str(int(normal))) < 13:
                                return str(normal)
                    except:
                        pass
                # 单位是 亿 的，转换为万元
                for i in ex_rule['b_amount_s']['billion']:
                    try:
                        if re.search(i, content, re.I | re.S):
                            if '美元' in i or '$' in i:
                                return str(sum([decimal.Decimal(x.strip().replace(',', '')) * 10000000000 for x in
                                                re.findall(i, content)]) * conf.dollar)
                            # print(re.findall(i, content)[0],'xxxxxxxxx')
                            return str(sum([decimal.Decimal(x.strip().replace(',', '')) * 10000000000 for x in
                                            re.findall(i, content)]))
                    except:
                        pass
        return '空'
    except Exception as e:
        print('Exception:', e)
        return '空'



# 提取预算金额汇总
def budget_amount_ex(content,html,url_tag='',table_name='id="zhongbiaoxinxi"'):
    try:
        b_sp = budget_money_special(html,url_tag)
        # print(1)
        b_h = budget_amount_ex_html(html)
        # print(2)
        b_c = budget_chinese_ex(content)
        # print(3)
        # b_s = budget_amount_sum_ex(content)
        b_s = budget_amount_split_ex(content)
        # print(4)
        b_e = budget_amount_ex_content(content)
        # print(5)
        b_t = table_money_ex(html,1,url_tag,table_name)
        # print(6)


        if b_sp != '空':
            print('budget_special')
            if float(b_sp)>0:

                return b_sp
        if b_h != '空':
            print('html_budget')
            if float(b_h)>0:

                return b_h
        if b_s != '空':
            print('budget_split')
            if float(b_s) > 0:
                return b_s

        if b_c != '空':
            print('bc')
            if float(b_c) > 0:

                return b_c
        # elif b_s != '空':
        #     print('sum')
        #     if float(b_s)>=0:
        #
        #         return b_s
        if b_e != '空':
            print('content')
            if float(b_e) >0:

                return b_e
        if b_t != '空':
            print('table')
            if float(b_t) >0:

                return b_t
        return '空'
    except Exception as e:
        print('Exception:',e)
        return '空'


# 提取采购单位名称
def comp_name_ex(content):
    try:
        for i in ex_rule['c_name']:
            # print(i)
            if re.search(i,content, re.I | re.S) :
                for i in re.findall(i,content, re.I | re.S):
                    # result_2 = re.match('[\u4e00-\u9fa5]*',result_1).group()
                    if 1 < len(i) < 64 and word_filter(i):
                        return word_clear(i)
        return '空'
    except:
        return '空'


# 提取采购单位联系人
def comp_contact_ex(content):
    try:
        for i in ex_rule['c_man']:
            if re.search(i,content, re.I | re.S):
                # print(re.findall(i, content)[0],'xxxxxxxxxxxx')
                # print(i)
                result_list = re.findall(i, content)
                for i in result_list:

                    result_1 = i.strip().strip('，').strip('、') # 去除数字
                    # print(result_1,'@@@@@@@@@@@')
                    if len(result_1) > 20:
                        continue
                    result_2 = re.match('[\u4e00-\u9fa5]*',result_1).group() #取第一个匹配到的人名
                    # print(result_2,'result_2')
                    if result_2 and len(result_2) < 32 and name_filter(result_2):
                        return result_2
                    if len(''.join(re.findall('[\u4e00-\u9fa5]*',result_1))) < 32 and name_filter(''.join(re.findall('[\u4e00-\u9fa5]*',result_1))):
                        return ''.join(re.findall('[\u4e00-\u9fa5]*',result_1))
        return '空'
    except Exception as e:
        print(e)
        return '空'


# 提取采购单位地址
def comp_address_ex(content):
    try:
        for i in ex_rule['c_address']:
            if re.search(i,content, re.I | re.S):
                print(i)
                # print(re.findall(i,content),'xxxxxxxxxxxxx')
                c_address = re.findall(i, content)[0].strip()
                if len(c_address) < 128 and word_filter(c_address):
                    return word_clear(c_address)
        return '空'
    except:
        return '空'


# 提取采购单位联系电话
def comp_tell_ex(content):
    try:
        for i in ex_rule['c_num']:
            if re.search(i,content, re.I | re.S):
                print(i)
                print(re.findall(i, content)[0],'xxxxxxxxxxxx')
                aa = re.findall(i, content)[0].strip()
                c_num = ' '.join(set(re.findall('\d{3,4}[-－]*\d{6,8}|\d{7,12}|\d{3,4}[-－]*\d{4}\s*\d{4}|（\d{4}）\d{7}', aa)))
                if len(c_num) < 64 and word_filter(c_num):
                    return c_num
        return '空'
    except:
        return '空'


# 提取代理机构名称、地址、联系方式
def agency_all_ex(content):
    try:
        for i in ex_rule['a_all']:
            try:
                if re.search(i,content, re.I | re.S):
                    # print(i)
                    # print(re.findall(i, content)[0],'xxxxxxxxxxxx')
                    aa = re.findall(i, content)[0].strip()
                    aal = aa.split('、')
                    a_name = aal[0]
                    a_address = aal[1]
                    a_man = re.findall('.*联系人：(.*)、联系电话：.*',aa)[0]
                    a_tell = re.findall('.*联系电话：(.*)',aa)[0]

                    return a_name,a_address,a_man,a_tell
            except Exception as e:
                print(e)
        a_name = agency_name_ex(content)
        a_address = agency_address_ex(content)
        a_man = agency_contact_ex(content)
        a_tell = agency_tell_ex(content)
        return a_name,a_address,a_man,a_tell
    except Exception as e:
        print(e,'ssssss')
        return '空'



# 提取代理机构名称
def agency_name_ex(content):
    try:
        for i in ex_rule['a_name']:
            if re.search(i,content, re.I | re.S):
                print(i,'sssssssssssssssssssss')
                names = re.findall(i, content)
                for name in names:
                    if len(name) < 64 and name_filter(name):
                        return word_clear(name)
        return '空'
    except:
        return '空'


# 提取代理机构联系人
def agency_contact_ex(content):
    try:
        for i in ex_rule['a_man']:
            if re.search(i,content, re.I | re.S):
                # print(i)
                # print(re.findall(i,content),'xxxxxxxxxxx')
                result_1 = re.findall('\D*', re.findall(i, content)[0].strip())[0].strip('，').strip('：')
                result_2 = re.match('[\u4e00-\u9fa5]*', result_1).group()
                if len(result_2) < 32 and word_filter(result_2):
                    return word_clear(result_2)
        return '空'
    except:
        return '空'


# 提取代理机构地址
def agency_address_ex(content):
    try:
        for i in ex_rule['a_address']:
            if re.search(i,content, re.I | re.S):
                # print(i)
                address = re.findall(i, content)[0].strip()
                # print(address)
                if len(address) < 128 and word_filter(address):
                    return word_clear(address)
        return '空'
    except:
        return '空'


# 提取代理机构联系电话
def agency_tell_ex(content):
    try:
        for i in ex_rule['a_tell']:
            if re.search(i,content, re.I | re.S):
                print(i)
                # print(re.findall(i, content)[0])
                aa = re.findall(i, content)[0].strip()
                num_list = re.findall('\d{3,4}[-－]*\d{6,8}|\d{7,12}|\d{3,4}[-－]*\d{4}\s*\d{4}|（\d{4}）\d{7}', aa)
                a_num = ' '.join(reduce(lambda x,y:x if y in x else x + [y],[[],]+num_list))
                if len(a_num) < 64 and word_filter(a_num):
                    return a_num
        return '空'
    except:
        return '空'

# 提取附件
def ex_annex(html,url):
    try:
        # print(ex_rule['c_html'][url])
        for i in ex_rule['annex'][url]:
            annex = etree.HTML(html).xpath(i)
            if annex:
                return annex
        return '空'
    except Exception as e:
        print('Exception:',e)
        return '空'


def proj_id_ex(page_url,url_tag,type_id):
    try:
        pj = yzb_project_id_ex.ProjectIdEx(page_url, url_tag)
        project_id = pj.pj_id_ex()
        print(type_id,type(type_id))
        if type_id == 41:
            return project_id
        else:
            return '空'
    except:
        return '空'
    # print(project_id)


# 获取总页数
def get_page(html,url):
    try:
        for i in ex_rule['page'][url]:
            if etree.HTML(html).xpath(i):
                page_str = ''.join(etree.HTML(html).xpath(i))
                return int(''.join(re.findall('.*/(.*?)页.*',page_str)))
    except:
        pass

def word_clear(string):
    return re.sub('\d、$|（\d）|\d\.|[,，;；（ (]$|^[:：]','',string)


# 过滤提取的字段
def word_filter(string):
    """

    :param string: 提取的字段
    :return: 如果字段内含有words_list中的关键字返回False，
             如果没有返回True
    """

    words_list = '|'.join(words)
    if re.search(words_list,string,re.I | re.S):
        # print(re.findall(words_list,string,re.I | re.S))
        return False
    return True


def name_filter(string):
    words_list = '|'.join(name_words)
    if re.search(words_list, string, re.I | re.S):
        return False
    return True


def title_filter(string):
    """

        :param string: 提取的字段
        :return: 如果字段内含有words_list中的关键字返回False，
                 如果没有返回True
        """

    words_list = '|'.join(title_words)
    if re.search(words_list, string, re.I | re.S):
        return False
    return True


# 中文金额转数字金额
def chinese_to_num(cn):
    cn_num = {
        '〇': 0,
        '一': 1,
        '二': 2,
        '三': 3,
        '四': 4,
        '五': 5,
        '六': 6,
        '七': 7,
        '八': 8,
        '九': 9,
        '零': 0,

        '壹': 1,
        '贰': 2,
        '叁': 3,
        '肆': 4,
        '伍': 5,
        '陆': 6,
        '柒': 7,
        '捌': 8,
        '玖': 9,

        '貮': 2,
        '两': 2,
    }

    cn_unit = {
        '十': 10,
        '拾': 10,
        '百': 100,
        '佰': 100,
        '千': 1000,
        '仟': 1000,
        '万': 10000,
        '萬': 10000,
        '亿': 100000000,
        '億': 100000000,
        '兆': 1000000000000,
    }

    money_unit ={
        '元':0,
        '元整':0,
        '角':0.1,
        '分':0.01,

    }

    else_num = re.findall('元.角.分|元.角|元.分|元|元整',cn)
    if else_num:
        cn = cn.replace(else_num[0],'')
    lcn = list(cn)
    unit = 0
    ldig = []

    while lcn:
        cndig = lcn.pop()
        if cndig in cn_unit:
            unit = cn_unit.get(cndig)
            if unit == 10000:
                ldig.append('w')
                unit = 1
            elif unit == 100000000:
                ldig.append('y')
                unit = 1
            elif unit == 1000000000000:
                ldig.append('z')
                unit = 1
            continue
        else:
            dig = cn_num.get(cndig)

            if unit:
                dig = dig * unit
                unit = 0

            ldig.append(dig)
    if unit == 10:
        ldig.append(10)

    ret = 0
    tmp = 0

    while ldig:
        x = ldig.pop()

        if x == 'w':
            tmp *= 10000
            ret += tmp
            tmp = 0

        elif x == 'y':
            tmp *= 100000000
            ret += tmp
            tmp = 0

        elif x == 'z':
            tmp *= 1000000000000
            ret += tmp
            tmp = 0

        else:
            tmp += x

    ret += tmp
    if else_num:
        cent = deal_cent(else_num[0],cn_num)
        return ret + cent
    return ret


def deal_cent(cn=None,cn_num=None):
    # print(cn)
    if re.search('.角.分', cn):
        cent = re.findall('.角.分', cn)
        # print(cent)
        cent_list = []
        if cent:
            cent_str = cent[0].replace('角','').replace('分','')
            for i in cent_str:
                cent_list.append(str(cn_num.get(i)))

            # print(cent_list)
            cent_end = int(''.join(cent_list))/100
            # print(cent_end)
            return cent_end
    elif re.search('.角', cn):
        cent = re.findall('.角', cn)
        cent_list = []
        if cent:
            cent_str = cent[0].replace('角', '')
            for i in cent_str:
                cent_list.append(str(cn_num.get(i)))

            # print(cent_list)
            cent_end = int(''.join(cent_list)) / 10
            # print(cent_end)
            return cent_end
    elif re.search('.分', cn):
        cent = re.findall('.分', cn)
        cent_list = []
        if cent:
            cent_str = cent[0].replace('分', '')
            for i in cent_str:
                cent_list.append(str(cn_num.get(i)))

            # print(cent_list)
            cent_end = int(''.join(cent_list)) / 100
            # print(cent_end)
            return cent_end
    # print(cent)


def notnull_judge(str):
    if str == '空':
        return
    return str




if __name__ == '__main__':
    print(chinese_to_num('壹仟贰佰肆拾贰万'))
    # '壹佰捌拾玖万玖仟柒佰伍拾贰元伍角伍分'