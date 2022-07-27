import regex as re
from lxml import etree



class ProjectCodeEx():
    '''
    各个省份的项目编号独立的提取逻辑，过于通用的正则不要写在里面。
    '''

    def __init__(self,content=None,url_tag=None,det_html=None):
        self.content = content
        self.url_tag = url_tag
        self.det_html = det_html

    def special_ex(self):
        tag_dict = {'cgw_xjbt':self.btzf_ex,'ccgp-qinghai':self.ccgp_qinghai,'ccgp-xizang':self.ccgp_xizang,
                    'ccgp-ningxia':self.ccgp_ningxia,'zfcg_qingdao':self.ccgp_qingdao,'ccgp-gansu':self.ccgp_gansu,
                    'ccgp-shaanxi':self.ccgp_shaanxi,'ccgp-guizhou':self.ccgp_guizhou,'szzfcg':self.szzfcg,
                    'ccgp-guangxi':self.ccgp_guangxi,'ccgp-liaoning':self.ccgp_liaoning,'ccgp-dalian':self.ccgp_dalian,
                    'ccgp-sichuan':self.ccgp_sichuan,'ccgp-anhui':self.ccgp_anhui,'ccgp-chongqing':self.ccgp_chongqing,
                    'ccgp-fujian':self.ccgp_fujian,'ccgp-hunan':self.ccgp_hunan,'ccgp-jilin':self.ccgp_jilin,
                    'zfcg_czt_zj_gov':self.zfcg_czt_zj_gov,'ccgp-jiangsu':self.ccgp_jiangsu,'gdgpo.gov':self.gdgpo_gov,
                    'ccgp-shanxi':self.ccgp_shanxi,'ccgp-shandong':self.ccgp_shandong,'nmgp_gov':self.nmgp_gov,
                    'ccgp-hubei':self.ccgp_hubei,'ccgp-tianjin':self.ccgp_tianjin,'zw.hainan.gov':self.zw_hainan_gov,
                    'zw.hainan.gov.cn':self.zw_hainan_gov_cn,'hnggzy':self.hnggzy,'hngp.gov.cn':self.hngp_gov_cn,
                    'jxsggzy.cn':self.jxsggzy_cn,'ccgp-jiangxi.gov.cn':self.ccgp_jiangxi_gov_cn,'www.hebpr.cn':self.www_hebpr_cn,
                    'ccgp-hebei.gov.cn':self.ccgp_hebei_gov_cn,'kfqgw.beijing.gov.cn':self.kfqgw_beijing_gov_cn,
                    'www.bcactc.com':self.bcactc,'ggzyfw.beijing.gov.cn':self.ggzyfw_beijing_gov_cn,
                    'bgpc.beijing.gov.cn':self.bgpc_beijing_gov_cn,'http://www.ggzy.gov.cn/':self.ggzy_gov_cn,
                    'http://txzb.miit.gov.cn/':self.txzb_miit_gov_cn,'zycg.gov.cn':self.zycg_gov_cn,
                    'http://www.mof.gov.cn/':self.mof_gov_cn,'ccgp.gov.cn':self.ccgp_gov_cn,'ccgp-beijing.gov.cn/':self.ccgp_beijing_gov_cn,
                    'jszwfw':self.jszwfw,'shggzy':self.shggzy,'hnsggzy':self.hnsggzy,'ggzy_ah':self.ggzy_ah,
                    'ggzy_xjbt':self.ggzy_xjbt,'ggzy_xinjiang':self.ggzy_xinjiang,'nxggzyjy':self.nxggzyjy,
                    'ggzyjy_gansu':self.ggzyjy_gansu,'sxggzyjy':self.sxggzyjy,'ggzy_xizang':self.ggzy_xizang,
                    'ggzy_yn':self.ggzy_yn,'ggzy_guizhou':self.ggzy_guizhou,'ggzyjy_sc':self.ggzyjy_sc,
                    'gxggzy':self.gxggzy,'hbggzyfwpt':self.hbggzyfwpt,'hnsggzyfwpt':self.hnsggzyfwpt,
                    'ggzyjy_shandong':self.ggzyjy_shandong,'ggzyfw_fj':self.ggzyfw_fj,'jl_gov_cn':self.jl_gov_cn,
                    'ggzyjy.nmg':self.ggzyjy_nmg,'lnggzy':self.lnggzy,'ggzy_zwfwb':self.ggzy_zwfwb,
                    'ggzy_hebei':self.ggzy_hebei,'hljggzyjyw':self.hljggzyjyw,'zjzwfw':self.zjzwfw,

                    }
        return tag_dict[self.url_tag]()


    # 浙江公共资源交易平台
    def zjzwfw(self):
        regex_list = ['[A-Z]{4}\d{4}-[A-Z]{2}\d{5}-[A-Z]{4}\d{3}-[A-Z]{2}\d{2}','[A-Z]{4}\d{7}\([A-Z]\)','[A-Z]{4}\d{7}','[A-Z]{5}-\d{9}[A-Z]','[a-z]{2}-\d{4}-\d{2}','[A-Z]{6}-\d{4}-\d',
                      '[A-Z]{4}\d{4}[A-Z]-[A-Z]{2}-\d{3}','[A-Z]{4}\d{4}-[A-Z]{2}-[A-Z]{3}\d{3}','[A-Z]{2}-\d{7}-\d{2}',
                      '[A-Z]{5}\d{4}-[A-Z]{2}-\d{3}','\d{4}[A-Z]{6}\d{3}','\d{4}-\d{4}[A-Z]{4}\d{4}-\d','\d{4}-\d{4}[A-Z]{4}\d{4}',
                      '[A-Z]{4}\d{4}[A-Z]-\d{3}','[A-Z]{4}\(\d{4}\)-\d{3}','\d{4}-\d{4}[A-Z]{4}\d{4}-\d','\d{4}-\d{4}[A-Z]{4}\d{4}',
                      '[A-Z]{4}-[A-Z]{4}-\d{7}','\d{4}-\d{4}[A-Z]{4}\d{4}-\d','\d{4}-\d{4}[A-Z]{4}\d{4}','[\u4e00-\u9fa5]{4}\d{4}-\d{3}[\u4e00-\u9fa5]',
                      '[\u4e00-\u9fa5]{4}\d{4}-\d{2}-\d{2}','[A-Z]{4}-\d{9}','[A-Z]{6}-\d{4}-\d-\d{3}','[A-Z]-[A-Z]{2}\d{12}',
                      '[A-Z]{4}-[A-Z]\d{6}[A-Z]','[A-Z]{4}\d{9}','[A-Z]{4}\d{4}-\d{2}-\d','[A-Z]{4}\d{7}',
                      '[A-Z]{6}\[\d{4}\]\d{12}号','[A-Z]{2}-\d{7}','[A-Z]{2}\d{6}[A-Z]\d{2}',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['JSCG2022002(G)','NBITC-202210122G','ty-2021-38','LRZFCG-2021-6','ZZCG2021Q-GK-201','XZCG2021-GK-ZCY072',
               'ZJ-2230006-06','ZJPEC2021-SS-003','2021NBHSWT316','JHHX2021-FW11259-ZFCG102-CZ01','0762-2141CBNB1077-4',
               'JHCG2021C-053','XXCG(2021)-055','0762-2141CBNB1077-3','HJZX-GKZB-2021015','0762-2141CBNB1077-1','浙方咨招2021-128号',
               '浙江新顺2021-12-11','WZZR-202101066','ZJGYZX-2021-2-086','Z-GB202112210148','HZZR-F211118N',
               'ZJSX211217020','ZJWS2021-11-8','HXGK2021057','CXZFCG[2021]330282131376号','ZJ-2173157','CG202112A07',
               'ZJZZ2021007'
               ]


    # 黑龙江公共资源交易平台
    def hljggzyjyw(self):
        regex_list = ['[A-Z]{2,4}\[\d{4}\]\d{3,4}\.\d[A-Z]\d','[A-Z]{2,4}\[\d{4}\]\d{3,4}','[A-Z]{2}\d{4}-\d{3}-\d{2}','[A-Z]{4}\d{4}-\d{3}\.\d[A-Z]\d',
                      '[A-Z]{4}\d{4}-\d{3}-\d{4}','[A-Z]{4}\d{4}-\d{3}','\d{4}-\d{4}[A-Z]{7}\d{2}','[A-Z]{2}\d{8}',
                      '[A-Z]{4}-[A-Z]{2}-\d{5,6}\.\d[A-Z]\d','[A-Z]{4}-[A-Z]{2}-\d{5,6}','[A-Z]{4}\d{4}-[A-Z]{3}-\d{4}','[A-Z]{4}\d{2}[A-Z]\d{5}\.\d[A-Z]\d',
                      '[A-Z]{6}\d{8}\.\d[A-Z]\d','[A-Z]{2}-[A-Z]{3}-\d{7}\.\d[A-Z]\d','[A-Z]{4}-[A-Z]{3}-[A-Z]\d{5}',
                      '[A-Z]-\d{5}-[A-Z]{4}','[A-Z]{4}\d{4}[A-Z]{3}\d{3}-[A-Z]{3}\d{3}\.\d[A-Z]\d','[A-Z]{4}\d{4}[A-Z]{3}\d{3}-[A-Z]{3}\d{3}',
                      '[A-Z]{4}\d{2}[A-Z]{2}\d{3}\.\d[A-Z]\d','[A-Z]{4}\d{2}[A-Z]{2}\d{3}','[A-Z]{2}\d{8}\.\d[A-Z]\d',
                      '[A-Z]{3}\d{4}-\d{4}[A-Z]','[A-Z]{2}\d{4}[A-Z]\d{3}'
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['FD[2021]474','FA2021-032-14','GZCG2021-497.1B4','HQZB2021-178','0702-2140CITCHRB47','GZJT[2021]0097',
               'JA20211207','HTFW-JT-21087','DCZX2021-HLJ-0897','FWTH00G21013.1B3','BYNDFS20210043.1B1','WG[2021]083.1B3',
               'ZG-ZWG-2021137.1BD3','ZTSJ-HLJ-A21001','C-21788-BTZB','ZRZB-FW-21083.1B1','HTCL-JC-211010','TH-21146',
               'CYFW2021JCS125-HZY007.1B1','RKZJ21CG019.1B1','JA20211114.1B1','ZXDC2021X637','SC[2021]0829.1B1',
               'ZJX2021-2173H','DSZB-21047','ZS2021G9121',''
               ]




    # 河北公共资源交易平台
    def ggzy_hebei(self):
        regex_list = ['[A-Z]{2}\d{16}','[A-Z]{1,2}\d{22}','\d{4}[A-Z]{2}\s*-\s*\d{3}','[A-Z]{6}\d{7}'
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['HB2021113120020052','HB2021124670010033','2021CK - 193','I1301000075037347001004','ZC130800202102362001001',
               'TSXYZB2021036'
               ]

    # 天津市公共资源交易平台
    def ggzy_zwfwb(self):
        regex_list = ['[A-Z]{4}-\d{4}-[A-Z]{1,3}-\d{4}'
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['TGPC-2021-D-0881','TGPC-2021-D-0798','TGPC-2021-BHD-0105',''
               ]



    # 辽宁公共资源交易平台
    def lnggzy(self):
        regex_list = ['[A-Z]{4}-\d{7,8}','[A-Z]{4}\d{7}','[A-Z]{2}\d{2}-\d{6}-\d{5}','[A-Z]{3}\d{4}-\d{3}\(\d\)',
                      '[A-Z]{4}\d{7,9}','[A-Z]{2,4}\d{4}-\d{2,4}','[A-Z]{4}-\d{4}-\d{3}','[A-Z]{6}\d{4}-\d{2}',
                      ''
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['ZHCG-2021017','CAZB2021395','JH21-210800-03713','GZC2021-035(1)','DLBC2021110','FYCG2021-1010',
               'FYCG2021-1010','HL2021-1210','CJCG-2021-050','BPZC202111005','CAZB2021310','JH21-210700-06606',
               'JH21-210700-06522','JZHWTP2165','GZCYXG2021-05','DWZB-20211204','SJZB2021-0901-07',''

               ]


    # 内蒙古公共资源交易平台
    def ggzyjy_nmg(self):
        regex_list = ['[A-Z]{4,7}-[A-Z]-[A-Z]-\d{6}\.\d[A-Z]\d','\d{4}[A-Z]{2}\d{3}[A-Z]{2}\.\d[A-Z]\d',
                      '\d{4}[A-Z]{2}\d{3}[A-Z]{2}','[A-Z]{4,7}-[A-Z]-[A-Z]-\d{6}','[A-Z]{4,7}-[A-Z]-\d{6}\.\d[A-Z]\d',
                      '[A-Z]{4,7}-[A-Z]-\d{6}','[A-Z]{6}\d{4}-\d{3}'
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['HSZC-C-H-210025','WSZCQQS-C-F-210075','ESZCZQ-X-H-210030.1B1','2021CG115HW.1B1','2021CG024SG','CFJDCG2021-005',

               ]


    # 吉林公共资源交易平台
    def jl_gov_cn(self):
        regex_list = ['[A-Z]{8}-\d{7,10}','[A-Z]{4}-\d{4}-[A-Z]{2}-\d{3}','[A-Z]{4}-\d{4}-\d{3,4}','\d{4}-\d{4}[A-Z]{8}\d{4}',
                      '[A-Z]{4}-[A-Z]{2}-[A-Z]{4}\d{2}-\d{8}','[A-Z]{4}\d{4}-\d{3,4}','[A-Z]{8}-\d{7}','\[\d{8}\]-\d{4}',
                      '[A-Z]{2}-\d{4}-\d{2}-\d{8}','\d{8}[A-Z]\d{4}-\d','[A-Z]{4}-\d{8}','[A-Z]{6}-[A-Z]\d{4}[A-Z]{2}\d{3}',
                      '\d{8}[A-Z]\d{4}','[A-Z]{5}\d{9}','[A-Z]{4}-[A-Z]{4}-\d{5,7}',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['SYGGZYBM-2021686002','JLCD-2021-ZB-035','JLCD-2021-ZB-038','JLQS-2021-1210','THJT-2021-150',
                'SYGGZYBM-2021693','0773-2141GNJLHWJT3625','ZJGJ-CC-HWZB02-20211201','JLTC2021-033','QGGGZYBM-2021116',
                '[20210324]-0031','XQZC2021-0082','JM-2021-12-15441','20211216Z1329-1','WCZX-20211222','2021-0104',
                'JSZFCG—J2021ZX200','20211214Z1319','JLSZC202101834','JLZZ-ZFCG-2021029','ZYGJ-CZFW-21139',
                'JZCH2021-100',''
               ]


    # 福建公共资源交易平台
    def ggzyfw_fj(self):
        regex_list = ['\[\d{4,6}\][A-Z]{2,5}\[[A-Z]{2}\]\d{7}-\d','\[\d{4,6}\][A-Z]{2,5}\[[A-Z]{2}\]\d{7}-\d'
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['[350625]FJKT[TP]2021001-1','[350582]PC[GK]2021055','[350700]FJJX[XJ]2021015','[3500]FJSHR[GK]2021036',
               ''
               ]


    # 山东公共资源交易平台
    def ggzyjy_shandong(self):
        regex_list = ['[A-Z]{4}-[A-Z]{2}-\d{4}-\d{4}','[A-Z]{4}\d{18}'
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['SDGP370781202102000663','SDGP370181202102000718','ZFCG-GX-2021-5027','ZFCG-2021-0000631',''
               ]

    # 河南公共资源交易平台
    def hnsggzyfwpt(self):
        regex_list = ['[\u4e00-\u9fa5]{3,6}\(\d{4}\)\d{4}号','[\u4e00-\u9fa5]{3,6}-\d{4}-\d{2,3}-\d{2}',
                      '[\u4e00-\u9fa5]{3,6}-\d{4}-\d{2,3}','[A-Z]{2}-\d{4}-\d{3}','[A-Z]{2}\[\d{4}\]\d{3}-[A-Z]{2}\d{3}'
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['偃师政采磋商(2021)0446号','禹财竞谈-2021-156','新密磋商采购-2021-52','西工政采磋商(2021)0077号','安县公开采购-2021-36',
               '孟津政采磋商(2021)0234号','驻政采购-2021-07-15','殷磋商-2021-51','2021-11-39','驻政采购-2021-12-4',
               'CG-2021-226','MCGZ[2021]260-ZC188',''
               ]

    # 湖北公共资源交易平台
    def hbggzyfwpt(self):
        regex_list = ['[A-Z]{4}-\d{4}-\d{5}-[A-Z]{2}\d{5}','[A-Z]{4}-\d{4}-\d{3}','[A-Z]{6}-\d{8}-\d{2}','[A-Z]{3}-\d{4}-[A-Z]{2}\d{4}',
                      '[A-Z]{4}-\d{4}-\d{4}','[A-Z]{4}\[\d{4}\]\d{3}号','[A-Z]{3}\d{7}号',
                      '[A-Z]{4}-\d{4}-[A-Z]{2}-\d{2}','[A-Z]{4}-\d{6}[A-Z]{2}-\d{3}-\d','[A-Z]{5}-\d{4}-[A-Z]{2}\d{3}',
                      '[A-Z]{6}-\d{4}-\d{3}','[A-Z]{2}-[A-Z]{2}-\d{4}-\d{3}[A-Z]','[A-Z]{4}-\d{6}-[A-Z]{2}\d{3}',
                      '[A-Z]{3}-\d{8}-\d{6}-\d','[A-Z]{3}\d{4}-\d{6}-\d{2}[A-Z]\s\(\d\)','[a-z]{4}-\d{7}','[A-Z]{4}-[A-Z]{2}-\d{4}-\d{3}',
                      '[A-Z]{3}-\d{8}-\d{6}','[\u4e00-\u9fa5]\[\d{4}\][A-Z]{2}\d{4}号','[A-Z]{5}-[A-Z]{2}-\d{4}-\d{4}',
                      '[A-Z]{4}\d{6}[A-Z]\d{6}','[A-Z]{4}-\d{2}[A-Z]{3}-[A-Z]\d{3}','\d{8}-[A-Z]{6}-\d{3}',
                      '[A-Z]{8}-\d{4}[A-Z]-\d{3}','[A-Z]{5}-\d{4}[A-Z]{2}-\d{3}','[A-Z]{4}-[A-Z]{4}-\d{8}','[A-Z]{7}\d{6}',
                      '[A-Z]{4}\d{4}[A-Z]{2}\d{2}[A-Z]-\d{4}','[A-Z]{4}-[A-Z]{4}-\d{4}-\d{3}','[A-Z]{6}-\d{2}-\d{2}-\d{2}',
                      '[A-Z]{6}\[\d{4}\]\d{4}','[A-Z]{4}-[A-Z]{3}-[A-Z]{2}-\d{4}-\d{3}','[A-Z]{4}-\d{7}-[A-Z]{2}',
                      '[A-Z]{8}-[\u4e00-\u9fa5]{2}\d{4}-\d{4}','[A-Z]{5}-[A-Z]{2}-\d{6}-[A-Z]\d{3}','[A-Z]{2}-[A-Z]{4}-\d{4}-\d{3}',
                      '[\u4e00-\u9fa5]{4}\[\d{4}\]\d{3}号','[A-Z]{6}\d{4}-[A-Z]{3}-\([A-Z]\d-\d{2}\)-\d{3}',
                      '[A-Z]{3}-\d{6}-[A-Z]{2}\d{3}','[A-Z]{3}-\d{6}-[A-Z]{2}\d{3}','[A-Z]{6}-\d{4}-[A-Z]{4}\d{2}',
                      '[A-Z]{4}\d{4}-\d{3}-[A-Z]{3}','[A-Z]{4}-[A-Z]{3}-[A-Z]{2}-\d{4}-\d{3}',
                      '\d{12}', '[A-Z]{4}\d{7}', '[A-Z]{3}\d{3}',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['WHZC-2021-00168-CS00083','HSST-2021-022','ZHJLTF-20211124-70','EZC-2021-ZX0175','NHZB-2021-1205',
               'HBHR[2021]052号','TSG001','ZJSL2021037','202112170233','HAC2021292号','WHRP-2021-ZF-03',
               'ESLC-202112ZC-003-1','HBHCW-2021-FW046','DZZFCG-2021-160','BX-ZFCG-2021-014A','JZSJ-202112-FS012',
               'HBT-42210072-214736','ZJZ1422-202101-01F (2)','hbyc-2021173','HBJX-ZB-2021-342','HBT-17210439-214386-1',
               '茅采计备[2021]XM0114号','ZXHCS-GA-2021-0006','LTZB202112E188285','RMCG-21SZB-H008','HBT-16210347-215100',
               '20211229-XYGSXJ-031','HBYHZCCS-2021C-001','HBSXJ-2021CG-072','HBYC-ZFCG-20210114','HBHDZBS202123',
               'DZSH0710FW21YH-0215','DYZC-ZFCG-2021-034','ZKJWXY-21-12-08','QQZBZC[2021]1196','ZSHJ-HYQ-FW-2021-232',
               'HBZX-2021012-CG','HBTXZFCG-竞磋2021-1216','HBYHX-ZC-202111-H199','HP-ZFCG-2021-802','正天采字[2021]164号',
               'JMHAZB2021-QJL-(J4-04)-015','SSQ-202112-FS004','ZCZBTM-2021-ZFCG34','HBAY2021-111-CSS','ZSHJ-DHQ-FW-2021-875',
               ''
               ]



    # 广西公共资源交易平台
    def gxggzy(self):
        regex_list = ['[A-Z]{4}\d{4}-[A-Z]\d-\d{5,6}-[A-Z]{2,4}[(（]重\d?[）]','[A-Z]{4}\d{4}-[A-Z]\d-\d{6}-[A-Z]{4}',
                      '\d{4}-\d{3}[A-Z]{6}\d{3}','[A-Z]{5}\d{8}（重）','[A-Z]{5}\d{8}',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['GXZC2021-G3-004777-JDZB','0817-214GXYLZB005','GXKLG20211028（重）','GXZC2021-G3-004369-HXXM','GXZC2021-G1-004120-GXJT(重2）',
               'GXZC2021-G1-004120-GXJT(重）','NNZC2021-G3-00130-RY（重）',''
               ]


    # 四川省公共资源交易平台
    def ggzyjy_sc(self):
        regex_list = ['\d{15}','[\u4e00-\u9fa5]{4,5}[〔【]\d{4}[〕】]\d{2,3}号?'
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['510201202110710','小政采询价【2021】013号','松政采竞磋〔2021〕038号','南政采磋〔2021〕14号','宜政采公委〔2021〕13号',
               '宜政采磋﹝2021﹞29号',''
               ]




    # 贵州省公共资源交易平台
    def ggzy_guizhou(self):
        regex_list = ['[A-Z]{4}-[A-Z]{4}-[A-Z]{4}-\d{5}-\([A-Z]\)','[A-Z]{7}\d{4}-\d{3}[A-Z]','[A-Z]{4}\[\d{4}\]-\d{3}[A-Z]',
                      '[A-Z]{4}\[\d{4}\]-[A-Z]\d{3}','[A-Z]{4}\d{4}[A-Z]{2}\d{4}','[A-Z]{4}-\d{4}-[A-Z]\d{2}','\d{4}-\d{12}',
                      '[A-Z]{4}-\d[4}-[A-Z]{2}\d{3}号','[A-Z]{5}-\d{4}-[A-Z]{3}\d{3}','[A-Z]{5}\d{4}-\d{2}号',
                      '[\u4e00-\u9fa5]{4}【\d{6}】\d{4}-\d','\d{2}[A-Z]{2}\d{4}[A-Z]\d{3}号?','[\u4e00-\u9fa5]{4}【\d{6}】\d{4}',
                      '[A-Z]{4}-\d{4}-\d{3,4}','[A-Z]{4}-[A-Z]{5}-\d[4}-\d{3}','[A-Z]{5}-[A-Z]{2}-\d{8}','[A-Z]{4}\d{4}-\d{3}'
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['JLZX-JSHT-ZBCG-21084-(V)','BCXZFCG2021-049G','DJZB[2021]-170K','DJZB[2021]-Y011','ZJJD2021ZB9046',
               'GZGC-2021-C42','0637-218102011059','ASZY-2021-YC006号','GZLDN-2021-ZCB011','KJDZB2021-29号',
               '州公易采【202111】0032','93ZC2021F933','93ZC2021C907号','州公易采【202111】0003-2','ZDGX-2021-213',
               'GZZC-2021-0923','YGZC-JZXCS-2021-042','XGXZB-ZC-20210021','ZJZB2021-227',''
               ]



    # 云南公共资源交易平台
    def ggzy_yn(self):
        regex_list = ['[A-Z]{2}\d{7}[A-Z]\d{6}','[A-Z]{4}-[A-Z]{2}-\d{4}-[A-Z]-\d{3}','[A-Z]{4}\d{7}','[A-Z]{2}\d{10}[A-Z]\d',
                      '[A-Z]\d{2}[A-Z]{3}-[A-Z]{4}-\d{3}/\d','[A-Z]\d{2}[A-Z]\d[11][A-Z]\d','\d{4}-\d{4}[A-Z]{2}\d{6}/\d',
                      '[A-Z]\d{2}[A-Z]\d[11]','[A-Z]\d{2}[A-Z]\d{2}[A-Z]\d{8}','[A-Z]{6}\d{8}',
                      '[A-Z]{4}\[\d{4}\]-\d{3}','[A-Z]{2}-\d{4}-\d{2}','[A-Z]{4}-[A-Z]{2}-\d{4}-\d{2}','[A-Z]{2,5}\d{8,18}',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['ZZ2100688B030115','TAHP-YN-2021-ZB-101','YNJH2021210','YC2021310192','G21BYN-SJCG-006/1','C53A00621001612',
               '0848-2141ZC205159/4','Q53A00721001143C1','YNJH2021058','YC2021360193C6','Q53A00W21001377','S53A00721001198',
               'YNTTCG20211081','YNGH[2021]-326','TH-2021-36','P53A00121001115C1','ZC530000202100884001','DFZ20211111',
               'YDCSH20211212','YNQY-ZB-2021-61','YNLB20211028','P53A01021001219']



    # 西藏公共资源交易中心
    def ggzy_xizang(self):
        regex_list = ['[A-Z]{5}\d{4}-\d{4}','[\u4e00-\u9fa5]\[\d{20}\]','[A-Z]{4}-\d{6}[A-Z]{2}','[A-Z]{4}-[A-Z]{4}-\d{9}-\d',
                      '[\u4e00-\u9fa5]{3}（\d{4}）\d{20}','\d{20}','[A-Z]{6}-[a-zA-Z]{2}-\d{7}','[\u4e00-\u9fa5]{3}-\d{7}',
                      '[A-Z]{4}-[A-Z]{4}-\d{9}','[\u4e00-\u9fa5]{3}〔 ?2021〕\d{2}-[A-Z]{4}-[A-Z]{2}-\d{5}','[A-Z]{4}-[A-Z]-\d{7}',

                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['GZFCG2021-6408','拉财采[54010021210200003229]','LSZC-202114RJ','AXXM-LSCG-202108005','54010021210200003246',
               'GZJYXZ-ls-2021005','柳财采-2021018','XZHX-CG-2021003','拉财采（2021）54010021210200000226','SDGJ-XZZB-2021010-3',
               '柳财采〔 2021〕94—XZZB-YY-21030','XZCA-G-2021039','AXXM-LSCG-202108005']


    # 陕西公共资源交易中心
    def sxggzyjy(self):
        regex_list = ['[A-Z]{4}-[A-Z]{2}-\d{4}-\d{4}','[A-Z]{4}\d{4}-\d{2,4}','[A-Z]{4}-[A-Z]{2}-\d{7}-\d','[A-Z]{4}-[A-Z]{2}-\d{7}',
                      '[A-Z]{2}-\d{4}-\d{6}-\d','[A-Z]{4}\d{4}-[\u4e00-\u9fa5]{2}\d{3}','\d{4}-[A-Z]{4}-\d{3}',
                      '[A-Z]{4}-\d{4}-\d{3}','[\u4e00-\u9fa5]{2}-[\u4e00-\u9fa5]{3}-\d{4}-\d{5}','[A-Z]{5}-[A-Z]{2}-\d{6}-[A-Z]{2}',
                      '[A-Z]{2}-\d{4}-\d{3}',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['2021-JQ68-F3011(SCZJ2021-JT-2536/001R）','YWGL-ZC-2021-0051','SQZB2021-145','SNCG-FM-2021171','YL-2021-000052-4',
               'SNCG-FM-2021171','YL-2021-000052-4','SXXSJ2021-80','JYSH2021-政采033','2021-JCZC-084','SQZB2021-117',
               'SXJJ-2021-116','政采-扶风县-2021-00051','SZTCS-BJ-211132-GC','SQZB2021-119','XY-2021-102','SXJS-AK-2021-75',
               'ZXCG-AK-2021-0032','ZFCG-2021-JZ-224','LZBG2021-2502','']


    # 甘肃公共资源交易平台
    def ggzyjy_gansu(self):
        regex_list = ['[A-Z]{4}-[A-Z]{2}-\d{4}-\d{3}','\d{4}[a-z]{4}\d{5}','\d{4}-[A-Z]{8}-[A-Z]\d{4}',
                      '[A-Z]{2}\d{7}-[A-Z]{4}\d{2}\([A-Z]\)','[A-Z]{2}\d{5}[A-Z]{2}','[A-Z]{2}-\d{4}-\d{4}-[A-Z]\d{3}',
                      '[\u4e00-\u9fa5]{3}[A-Z]{3}\d{4}-\d{3}','[A-Z]{4}-\d{4}-采\d{3}','[\u4e00-\u9fa5]{3}\d{4}-\d{2}\s[A-Z]',
                      '\d{6}[A-Z]{2}\d{9}','[A-Z]{4}-\d{4}-\d{4}','\d{6}[A-Z]{2}\d{3}附\d','[A-Z]{3}\d{4}-\d{2}-[A-Z]{2}\d{2}号?',
                      '[\u4e00-\u9fa5]{3}（\d{4}）[A-Z]{2,4}-\d{3}','[\u4e00-\u9fa5]{3}\d{4}[A-Z]-\d{2}[\u4e00-\u9fa5]附1',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['ZFCG-XH-2021-050','2021zfcg03904','2021-JWGSLZXT-G1001','GZ2110013-LDYY40(Z)','TC21930BX','WJ-2021-2337-D012',
               '城交易ZGK2021-078','BJFH-2021-采160','安交政2021-45 C','207108JH620102001','XHZC-2021-1115','128001JH007附1',
               'YZC2021-09-JC18号','西政采（2021）BMGK-063号','七交易2021Z-19号附1','西政采（2021）CS-025号']



    # 宁夏公共资源交易平台
    def nxggzyjy(self):
        regex_list = ['[A-Z]{2,5}-[A-Z]{2,5}-\d{4}-\d{2,4}','[A-Z]{4}-\d{4}[A-Z]\d{3}','[A-Z]{4}-\d{4}-\d{2,3}',
                      '[A-Z]{4}【[\u4e00-\u9fa5]】-\d{7}','[A-Z]{4}-[A-Z]{3}-[A-Z]\d{5}','[A-Z]{4}-[A-Z]{3}/[A-Z]-\d{5}',
                      '[\u4e00-\u9fa5]{4}\[\d{4}\]-\d{3}号?','[A-Z]{4}-\d{4}-（采）-\d{3}','[\u4e00-\u9fa5]【[\u4e00-\u9fa5]】[\u4e00-\u9fa5]\d{4}[\u4e00-\u9fa5]\d{3}[\u4e00-\u9fa5]',
                      '[A-Z]{4}\d{8}','[A-Z]{3}/[A-Z]\d{6}','[A-Z]{6}-[A-Z]{2}-\d{6}','[\u4e00-\u9fa5][A-Z]-\d{4}-\d{5}',
                      '[A-Z]\[\d{2}\][A-Z]\d{3}','[\u4e00-\u9fa5]{5}（[\u4e00-\u9fa5]）【\d{4}】第\d{1,3}号',
                      '[A-Z]{4}-\d{4}[A-Z]{2}\d{3}','[A-Z]{4}【\d{4}】[A-Z]{2}\d{3}','[A-Z]{4}-\d{4}-（[A-Z]{2}）-\d{3}号?',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['NXZC-2021-95','NXDRD-CG-2021-17','ZXWY-NX-2021-0093','NXCX-2021ZC123','NX-HYXCC-2021-015',
               'SXHR【采】-2021019',' ZJZB-2021-071','ZTSJ-NZC-S21084','ZTSJ-NZC-S21084','ZJXD-ZZQ/A-21191',
               'ZTSJ-NZC-A21308','宁博政采[2021]-012号','NXJS-2021-（采）-038','正【招】字2021第039号','ZCJY20211205',
               'NZC/A210394','NXHRDL-ZC-210969','鼎夏ZC-2021-00148','NXZM[2021]ZC015','宁鹏程飞招（采）【2021】第59号',
               'HSZB-2021ZC199','NXCJ【2021】ZC005','ZJXD-ZZQ/A-21200','NXJM-2021（ZC）-036号','']

    # 新疆政府采购网公共资源交易平台
    def ggzy_xinjiang(self):
        regex_list = ['[A-Z]{2}\d{4}-\d{3}-\d','[A-Z]{2}\d{4}-\d{3}','[A-Z]{2}\d{4}-\d{2}号','[A-Z]{4,6}\d{7}',
                      '[A-Z]{8,9}\(\d{4}[A-Z]{2}\)\d{3}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['GK2021-083', 'GK2021-072','CS2021-023-2','CS2021-17号','BZFSCG2021309','BZFSCG2021308','HTBJFSCG(2021GK)035',
               'HTHTSFSCG(2021GK)014','BZBLGK2021018','BZCS2021016']

    # 新疆生产建设兵团公共资源交易平台
    def ggzy_xjbt(self):
        regex_list = ['[A-Z]\d[A-Z]\[\d{4}\]\d{2,4}号-\d{3}-\d{3}-\d{2}','[A-Z]\d[A-Z]\[\d{4}\]\d{2,4}号-\d{3}',
                      '[A-Z]{4,7}-\d{4}-\d{2,3}号?','[A-Z]{4,7}-\d{4}','[A-Z]\d[A-Z]{1,4}\[\d{4}\]\d{2,4}号','[A-Z]{4}-\d{2}',
                      '[A-Z]{2}\d{2}[A-Z]{5}\d{10}','[A-Z]{4}-\[\d{4}\]\d{3}-\d{3}','[A-Z]{4}-\[\d{4}\]\d{3}',
                      '[A-Z]\d[A-Z]\d{3}[A-Z]\[\d{4}\]\d{3}号','[A-Z]{4}\d{8}','[A-Z]{4}-\[\d{4}\]政采云\d{3}',
                      '[A-Z]{6}\d{4}-\d{3}','[A-Z]{4}\d{4}-\d{2}','[A-Z]{4}-\d{2}[A-Z]{4}\d{4}-\d{2}',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['B8S[2021]1674号-026','SCZB-2021-060','B8SKFQ[2021]45号','BT12SZCCS2021120301','HJZX-[2021]289','BZFW-[2021]140-002',
               'B8S133T[2021]342号','B8S[2021]9255号','B6S[2021]689号-003','BZHW-[2021]30','JXFS-2021-03','LTZB20210520',
               'XJJY-[2021]政采云003','BZZLCS2021-004','B6S[2021]388号-001-002-01','XCZC2021-57','HYZB-12','XJKH-04CGGK2021-02',
               'DESMLJY2021-009号',]


    # 安徽公共资源交易中心
    def ggzy_ah(self):
        regex_list = ['[A-Z]{4,6}-\d{7,8}','[A-Z]{3,4}\d{5,8}-\d','[A-Z]{2}-[A-Z]{4}\d{7,8}','[A-Z]{4}\d{4}\s\d{3}号','[A-Z]{2}\d{4}[A-Z]{2}\d{4}-\d',
                      '[A-Z]{4}\d{7}号','[A-Z]{5}-\d-[A-Z]-[A-Z]-\d{4}-\d{4}','[A-Z]-\d{4}-\d{3}','[A-Z]{3}-[A-Z]{2}-[A-Z]{2}-\d{7}',
                      '[a-z]{4}\d{6}-\d{3}-\d{2}','[a-z]{4}\d{6}-\d{3}','[A-Z]{2}-[A-Z]{2}-\d{4}-\d{3}[\u4e00-\u9fa5]\d{4}[\u4e00-\u9fa5]{2}\d{3}[\u4e00-\u9fa5]',
                      '[A-Z]{2}\d{2}[A-Z]{2}\d{4}[A-Z]{2}\d{4}','[A-Z]{6}\d{4}-\d{3}','[A-Z]{6}\d{4}-\d{3}（[\u4e00-\u9fa5]）',
                      '[A-Z]{2}-[A-Z]{4}\d{7}','\d{4}[A-Z]{2}\d{4}','[A-Z]{3}-[A-Z]{2}-[A-Z]{2}-\d{7}','[A-Z]{3,4}\d{5,8}',
                      '[A-Z]{2}\d{4}[A-Z]{2}\d{4}','[A-Z]{6}\d{4}―\d{3}','[A-Z]{4}-\d{4}-\d{3}','[A-Z]{2}\d{2}[A-Z]{2}\d{4}[A-Z]{2}\d{4}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['HQZFCG-2021168','SXGC2021475','EP-SXCG2021072','BZCG2021 297号','LQ2021JC1346','BZCG2021292号','MASCG-0-J-F-2021-1540',
               'H-2021-091','XCS-CG-XJ-2021056','YS2021JC1345','SZCGS2021-0091','AHKS-20211007','czcg202111-241','AHKS-20211113',
               'CG-HN-2021-172财2021年第475号','czcg202111-233-01','WH01CG2021FW2073','QSZBCG2021―165（第二次）','EP-XXCG2021139',
               'CZG42021428','2021CG7097','JXX-CG-CS-2021045','CZG42021419-2','GDS-CG-CS-2021295','THCG21076','TH2021JC1336-1',
               'QSZBCG2021―177','ZFCG-2021-098','EP-LBCG2021083','']


    def hnsggzy(self):
        regex_list = ['[A-Z]{8}\[\d{4}\]\d{3}','[\u4e00-\u9fa5]{4}\[\d{4}\]\d{6}号?','[A-Z]{4,6}-\d{4}-\d{3}','[A-Z]{4}-\d{4}[A-Z]{2}-\d{2}',
                      '[\u4e00-\u9fa5]{4,5}【\d{4}】\d{6}号?','[\u4e00-\u9fa5]{4,5}-?\d{4}-\d{4}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0]

        exm = ['HNZLLDCG[2021]050','澧财采计[2021]000201','HNMYCG-2021-020','湘财采计[2021]002389','YSZB-2021-011',
               'HHCD-2021CG-12','HNXGGZ-2021-014','株财采计[2021]000224号','桃财采计[2021]000242','湘财采计[2021]001448号',
               '岳财市采计【2021】000230号','中财采计-2021-1023','双峰财采计2021-0228','']


    # 兵团政府采购网
    def btzf_ex(self):
        # print(1111111111)
        regex_list = ['BTJY\d{2}[A-Z]{4}\d{7}','[A-Z]{4}（\d{4}）[A-Z]?-\d{3}','[A-Z]{4}-\[\d{4}\]\d{2,3}']
        for i in regex_list:
            result = re.search(i,self.content)
            if result:
                return re.findall(i,self.content)[0]

        exm = ['BTJY08CGGK2020288','BTJY04CGCS2020024','BTJY00CGCS2020065','BTJY00CGCS2020065','BTJY02CGCS2020117','BTJY06CGCS2020025',
               'BTJY09CGGK2020200','BTJY00CGCS2020139','BTJY12CGGK2020085','BTJY14CGGK2020028','BTJY08CGTP2020240','JTZB（2017）-088',
               'JWZB（2016）Z-322','BZHW-[2016]89','BZHW-[2016]223','']

        # return re.findall('[A-Z]{4}-\[\d{4}\]\d{2,3}',self.content)[0]

    # 青海省政府采购网
    def ccgp_qinghai(self):
        regex_list = ['([\u4e00-\u9fa5]{3,10}（[\u4e00-\u9fa5]{2}）(\d{4}-\d{3,4}|\d{4}-\d{3,4}-\d|\d{4}-\d{3,4}号))']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                return re.findall(i, self.content)[0][0]

        exm = ['江苏汇诚公招（服务）2020-0905','诺浩公招（货物）2020-042','兰州众信公招（服务）2020-040号','青海格建公招（货物）2020-087',
               '青海铭驰公招（货物）2020-049','弘之翼竞谈（货物）2020-015','青海诚德竞磋（服务）2020-132','北京建智达竞磋（货物）2020-002',
               '青海万事通竞磋（服务）2020-029-1','青海柯林公招（工程）2020-010-4','上海容基公招（货物）2020-080','青海机电公招（货物）2017-070',
               '华新询价（服务）2019-086号']

    # 西藏政府采购网
    def ccgp_xizang(self):
        result_list = etree.HTML(self.det_html).xpath('//div[@class="neirong"]//div[1]//text()')
        result_str = ''.join(result_list)
        # print(result_str)
        result = re.findall('项目编号：(.*)采购方式：',result_str, re.S | re.M)
        if result:
            return re.sub('\s*','',result[0])
        # print(result,'result')

        exm = ['XZZB-ALZT-ZD200070','Z210220000168-2','藏财采【2020】0674','SCFY-XZ-20200801','ALZT-XZZB-GJ200061',
               '林财采-W-[2020]67','XZYY-CG-RKZ2020006','ZXDCG-2020114','藏财采[2020]0002','ALCG-ZHJ-0730-206122050044/01',
               '2020-WJXZSN-W1008','XZTZ2020107','']

    # 宁夏政府采购网
    def ccgp_ningxia(self):
        regex_list = ['([A-Z]{8}\d{4}[A-Z]\d{3})','([A-Z]{4}-[A-Z]{2}\d{4}-\d{3})','([A-Z]{2}-[A-Z]{2}-\d{8})',
                      '[A-Z]{4}-[A-Z]{4}-\d{4}-\d{2}','([A-Z]{4}-\d{4}-\d{2})',]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i,self.content))
                return re.findall(i, self.content)[0]

        exm = ['NXDZH-2020（YC）015号','NXHXY【2020】023号','GZ2-20-09-245/-ZC-G','ZTSJ-NZC-Z20026',
               '银万博招(公)[2020]第1041号','ZSYX-(政采)-20201001','NXYMZFCG2004H036','宁博政采比[2020]-041号',
               'NXZM[2020]ZC032','ZTSJ-NZC-W20080','NXZH-2020-11','NXBZ-2020-(采)005号','ZKX(LW)20200915-058',
               'GCZB-(WJC）2020-102','NXRC采招字2020-017','SHXDZ[2020]第L004号','SZT2020-NX-XC-FW-0859','BJHL-CG2020-010',
               'NXSX-2020-33','XH-HN-20200828','TYZX-ZFCG-2020-25']

    # 青岛市政府采购网
    def ccgp_qingdao(self):
        regex_list = ['[A-Z]{4}\d{10}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i,self.content))
                return re.findall(i, self.content)[0]

        exm = ['ZFCG2020000867','ZFCG2020000713','ZFCG2020000913','ZFCG2020000841','ZFCG2020000681','JMCG2020000466',
               'HDCG2020000603','']

    # 甘肃政府采购网
    def ccgp_gansu(self):

        a = re.findall('采购项目编号：(.*?)采购项目名称：',self.content)
        print(a,'aaaa')

        exm = ['RHSAGK-20-0112JY', 'XTZBCG-2020019-2', 'BW20D059', 'TGZC2020-522', '0876-2004394', 'JCZC2020GK-220']
        if a :
            return a[0]

    # 新疆政府采购网
    def ccgp_xinjiang(self):


        exm = ['ZFCGA-ZYHXZB2020-113','TC209H09V','HLXJ2020-017','XHYJ-2020-13','ZFCGHY-20200127','2041xzj122',
               'WKZB2011XJCB61029','ctzb-2020-046','WTYZSZC20-084-2','XJXCT2020-ZB-104-02','']

    # 陕西政府采购网
    def ccgp_shaanxi(self):

        print('123456yeyeye')
        exm = ['SXZX2020-097','SZT2020-SN-SC-HW-0947','SXZBHX2020-13','SXXDDL-【2020】074','0617-2021HZ2026',
               'THXZB2020-1067','SCZD2020-ZB-1718/001','HXGJXM2020-ZC-CS1158','0617-2023FZ1892','ZDZI20-019ZSA',
               'HZGH-2020-215','SJ-2020-000097-4']

    # 贵州政府采购网
    def ccgp_guizhou(self):
        regex_list = ['[A-Z]{4,6}-\d{4}-\d{2,4}', '[A-Z]{4}-[A-Z]{2}\d{8}','[A-Z]{4}\d{4}-\d{3}[A-Z]{2}','[M]\d{16}',
                      '\d{4}-\d{12}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['GZWH-2020-1241','GZZC-2020-90',' JXZB-2020-007','GZTM-2020-183','HRCGY-QG-2020026','GZMC-ZC20201065',
               'GZMC-ZG20201046','GZFTCG-2020-141','0637-201102040555','THZB2020-326CG','CDQD-ZB2020-062','M4400000707007137',
               'THZB2020-225CG']

    # 深圳市政府采购网
    def szzfcg(self):
        regex_list = ['\d{4}-\d{4}[A-Z]{4}\d{4}','[A-Z]{4}\d{10}[A-Z]\d{2}','\d{4}-\d{8}','[A-Z]{4}-\d{5}[A-Z]{4}','[A-Z]{4}\d{8,10}',
                      '[A-Z]{4}-[A-Z]{2,4}-\d{4}-\d{3}','\d{4}[A-Z]{2}\d{4}[A-Z]{4}','[A-Z]{4}\d{4}-\d{3}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['1371-2041GHSZ1242','LHCG2020219278','SZDL2020335524','FTDL2020179916','SZDL2020335591','0733-20202448',
               'GXZX-20058SZGK','COBO2008282723F01','Tczb-20szb019','OITC-G200291433','COBO2010102746F01','SZHY-ZB-2020-081',
               'SZCTP20201013','2020XY1381LGYJ','SSZB-CGFW-2020-044','JX2020CG-H002','COBO2008172713H01','SSZX2020-401',
               ]

    # 广西政府采购网
    def ccgp_guangxi(self):
        regex_list = ['[A-Z]{4}\d{4}-[A-Z]\d-\d{5,6}-[a-zA-Z]{2,4}（重）','[A-Z]{4}\d{4}-[A-Z]\d-\d{5,6}-[a-zA-Z]{2,4}','[A-Z]{3}\(\d\)\d{7}[A-Z]{3}','[A-Z]{4}-\d{5}[A-Z]'
                      ,'[A-Z]{3}\d{2}-\d{3}','[A-Z]{4}-\d{4}-[A-Z]{2}\d{2}','[A-Z]{4}\d{4}-[A-Z]\d-\d{5,6}-\d{3}-[A-Z]{4}',
                      '\d{4}-\d{3}[A-Z]{6}\d{3}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]


        exm = ['NNZC2020-C3-260089-GXRT','YLZC2020-G3-30594-YZLZ','NNZC2020-G1-090029-GXXY','BSZC2020-G1-000524-YZLZ',
               'CZZC2020-G3-20520-GXJH','HCA(3)2020480GNN','NNZC2020-10135A','LCG20-019','NNZC2020-30219A','BSZC2020-J2-250523-gxrw',
               'BGGC-2020-GK14','YLZC2020-G2-30531-001-GXXQ','HCZC2020-G1-01244-KL','0817-204GXYLZB006','GGZC2020-G1-40053-SZQL（重）']

    # 辽宁省政府采购网
    def ccgp_liaoning(self):
        regex_list = ['[A-Z]{2}\d{2}-\d{6}-\d{5}','[A-Z]{6}\d{7,11}','[A-Z]{2}\d{8}','[A-Z]{4}\d{4}-\d{3,4}-\d','[A-Z]{4}\d{4}\s?\d{2}',
                      '[A-Z]{4}-\d{7}','[A-Z]{6}\d{7}','[A-Z]{5}\d{4}-\d{2}','[A-Z]{4}\d{17}','[A-Z]{8}\d{8}','[A-Z]{4}\d{4}[A-Z]{2}-\d{3}',
                      '[A-Z]{6}-[A-Z]{7}-\d{4}-\d{3}','[A-Z]{5}\s?\d{11}','[A-Z]{4}\d{4}-\d{3,4}','[A-Z]{5}\d{4}[A-Z]{2}\d{2}[A-Z]',
                      '[A-Z]{2}\d{4}\s?[A-Z]\d{3}','[A-Z]{4}-[A-Z]{2}\d{2}-\d{4}-\d{3}-\d']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['JH20-210000-65704','JH20-210000-42575','LNZCCG2020045','JH20-210124-00238','XY20201004','YKSGZC2020124',
               'BXZFCG20201016002','LNYD2020-1017','YDLN2000 40','STCG-2020024','LNZCCG2020043','FXCG2020-046',
               'FMXCG2020-50','LNZC21100020200800116','LNTYZFCG20201005','TLHX2020GK-021','JPZFCG-JZXCSCG-2020-175',
               'HLDZC 20200900415','LNYC2020-1015-1','AGJGC2020GF36A','DDCGJC2020045','CT2020 A036','LNTY-ZB01-2020-053-1']

    # 大连市政府采购网
    def ccgp_dalian(self):
        regex_list = ['[A-Z]{2}-\d{4}-\d{4}','[A-Z]{4}-\d{6,8}','[A-Z]{2}\d{4}-\d{4}','[A-Z]{2}\d{5}[A-Z]{2}\d{8}',
                      '[A-Z]{3}\d{9}-\d','[A-Z]{3}\d{7,9}-\d','[A-Z]{4,6}\d{4}-\d{3,4}','[A-Z]{3}\d{7,9}','[A-Z]{4}-\d{4}-\d{4}',
                      '[A-Z]-\d{4}-\d{2}-\d-\d']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['DR-2020-0924','ZQZC-2020125','ZQ2020-2107','ZZ02702HW04110054','DCZ202009077','DCZ202008039-1','LNHMCG2020-040',
               'LNHMCG2020-039','LNHMCG2020-045','HJZB2020-0923','BXZC2009052','ZQZC-2020113','XRCG2020-004','HKCG-200708',
               'JHCG-20200916','DLZY-2020-1005','FYCG2020-0717','DLZY-2020-09-3-1','TXCG-200805','']

    # 四川政府采购网
    def ccgp_sichuan(self):
        regex_list = ['\d{16}',]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['5101012020002504','5101222020001549','5109042020000555','5109042020000552','']

    # 安徽省政府采购网
    def ccgp_anhui(self):
        regex_list = ['[A-Z]{2,4}\d{20}','[A-Z]{2}\d{12}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['HFJJ20201023141056358001','HF20201023131801020001','SS202010210144','']

    # 重庆市政府采购网
    def ccgp_chongqing(self):
        regex_list = ['\d{2}[A-Z]\d{4,5}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['20A00366','20A02191','20C00029','20C00021']

    # 福建省政府采购网
    def ccgp_fujian(self):
        regex_list = ['\[\d{4,6}\][A-Z]{2,4}\[[A-Z]{2}\]\d{7}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['[3500]MZZJ[GK]2020022','[350100]SQ[GK]2020006','[350100]SQ[GK]2020006','[350100]SQ[GK]2020006',
               '[350121]WZ[GK]2020003','[3500]BYZB[GK]2020016','[3500]YFCG[TP]2020005','[350800]LYCG[GK]2020228',
               'MJGC[CS]2017001','CCZB[GK]2017004','']

    # 湖南政府采购网
    def ccgp_hunan(self):
        regex_list = ['\d{4,7}-\d{8}-\d{1,4}','[A-Z]{8}-\d{4}-\d{1,4}','[\u4e00-\u9fa5]{4}\[\d{4}\]\d{6}[\u4e00-\u9fa5]',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['1068805-20201026-54','3022-20201022-855','1022725-20201022-30','2921-20201022-260','HNSZZFCG-2020-0311',
               '1036908-20201020-3','3005-20200925-239','湘财采计[2019]015379号']

    # 吉林政府采购网
    def ccgp_jilin(self):
        regex_list = ['[A-Z]{4}-[A-Z]{2}-[A-Z]{4}-\d{8}','[A-Z]{8}-\d{7}','[A-Z]{5}\d{9}','\d{8}[A-Z]\d{4}','[A-Z]{2}-\d{4}-\d{2}-\d{5}',
                      '[A-Z]{2}-[A-Z]{4}-\d{4}-\d{3}','[A-Z]{4}\d{4}-\d{3,4}','[A-Z]{4}-\d{4}-[A-Z]{4}\d{4}',
                      '\d{4}-\d{4}[A-Z]{4}\d{4}','[A-Z]{5,6}-[A-Z]{4}-\d{7,8}','[A-Z]{4}-\d{4}-\d{3}','[A-Z]{4}-\d{4}-[A-Z]{2}\d{3}',
                      '[A-Z]{4}-\d{5}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['ZJGJ-DH-HWZB-20200802','SYGGZYBM-2020538','JLSZC202002112','20200915Z0932','JM-2020-07-13274',
               'HY-JLZB-2020-121','ZWHY2020-1028','ZKGL-2020-LYCG1027','0773-2041JLHW0200','JLSZC202002359',
               'SYGGZYBM-2020370','JLSZC202001865','HJZFCG-DYLY-2020010','0773-2041JLHW0211','THJT-2020-121',
               'LYZC2020-031','JLSXH-GCZB-20201005','EDZC-2020-WT070','JLZC-20107']

    # 浙江政府采购网
    def zfcg_czt_zj_gov(self):
        regex_list = ['[A-Z]{7}-\d{4}-\d{3}','[A-Z]{2}-[A-Z]{2}\d{4}-\d{3}','[A-Z]{4}\d{4}[A-Z]-\d{3}[A-Z]\d',
                      '\d{4}[A-Z]{6}\d{3}','[A-Z]{4}-\d{10}','[A-Z]{3}-[A-Z]{2}\d{4}-[A-Z]{2}\d{3}','[A-Z]{4}\d{4}-\d{2}-\d{2}',
                      '[A-Z]{6}\d{4}[A-Z]{2}-[A-Z]{2}-\d{3}','[A-Z]{4}-\d{8}','[\u4e00-\u9fa5]{4}【\d{4}】\d{3}',
                      '[\u4e00-\u9fa5]{3}\[\d{4}\]\d{4}[\u4e00-\u9fa5]-\d','[A-Z]{4}-[A-Z]{2}-[A-Z]\d-\d{7}',
                      '[A-Z]{4}-\d{7}[A-Z]','[A-Z]{4}-\d{4}-\d{3}','[A-Z]{4}\d{8}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['JSZFCGC-2020-001','YY-WJ2020-020','JHCG2020F-029C2','2020NBHSWT212','CTZB-2020100236','RSJ-GY2020-GK002',
               'DLLH2020-10-15','CYZFCG2020TL-GK-069','WZKH-20201023','浙诚律采【2020】027','绍柯采[2020]3543号-1',
               'GXTC-CZ-A1-2036066','ZJTZ-2020901Z','ZJDL-2020-080','JJWL20042070']

    # 江苏省政府采购网
    def ccgp_jiangsu(self):
        regex_list = ['[A-Z]{4}\d{4}-[A-Z]-[A-Z]-\d{3}-\d{3}','[\u4e00-\u9fa5]{6}\[\d{4}\]\d{2}[\u4e00-\u9fa5]',
                      '[A-Z]{6}-\d{4}[A-Z]\d{3}','[A-Z]{4}\([A-Z]\)-\d{7}','\d{6}[A-Z]\d{5}','[A-Z]\d{19}-\d',
                      '[A-Z]{4}-\d{4}[A-Z]{2}\d{4}','[A-Z]{2}-\d{9}[A-Z]','[A-Z]{4}-\d{7,12}',
                      '[A-Z]{4}\d{4}-[A-Z]-[A-Z]-\d{3}[\u4e00-\u9fa5]','[A-Z]{5}\d{4}-[A-Z]{2}-[A-Z]-\d{3}',
                      '[A-Z]{4}\d{4}[A-Z]\d{3}','[A-Z]{4}\d{4}-[A-Z]-\d{3}','[\u4e00-\u9fa5]{4}-\d{7}[\u4e00-\u9fa5]',
                      '\d{4}-\d{4}[A-Z]{6}\d{2}','[\u4e00-\u9fa5]{4}-\d{7}','[A-Z]{2}-[A-Z]\d{4}-\d{3}',
                      '\d{4}-\d{4}[A-Z]{5}\d{3}[A-Z]','[A-Z]{4}\d{2}[A-Z]\d{4}','[A-Z]{4}-[A-Z]\d{4}[A-Z]\d{3}',
                      '[A-Z]{2}\d{11}[A-Z]{2}','[A-Z]{3}\d{8}','[A-Z]{6}-（\d{4}）[\u4e00-\u9fa5]{3}\d{4}[\u4e00-\u9fa5]',
                      '[\u4e00-\u9fa5]{3}（\d{4}）[A-Z]{4}\d{3}','[\u4e00-\u9fa5]{3}【[\u4e00-\u9fa5]】\d{8}[\u4e00-\u9fa5]',
                      '[A-Z]{6}-\(\d{4}\)[\u4e00-\u9fa5]{3}\d{4}[\u4e00-\u9fa5]','[A-Z]{5}\d{4}-\d{4}']

        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]


        exm = ['SZCH2020-Y-G-030-005','智汇溧采标公[2020]12号','TCGGZY-2020G140','SYCG(D)-2020260','066020H24344',
               'E3213010313202010031-1','TCGGZY-2020G138','2020080309349','066020M84194','NJZC-2020GK0254',
               'SZCH2020-Y-G-030-003','QC-202091834D','JSZC-2020010','SZWK2020-W-G-015号','SZZCZ2020-XC-G-012',
               'HXZC-2020231042','JYZF2020G184','SZHT2020-G-021','恒泰采公-2020008号','1009-2041HOLLYF92',
               '1009-2041HOLLYF92','城投采公-2020077','YT-SG2020-027','0664-2060SUMEC746D','JSGC20G2127','JSCX-Z2020G001',
               'YT09202001663ZB','WSW10412020','ZJXQZC-（2020）公字第0016号','徐采公（2020）XZGX018','常建采【公】20201002号',
               'JYZF2020G181','徐采公（2020）XZXTD007','ZJZCFS-(2020)公字第0486号','NJJF-202010264498','XCGZX2020-0411',
               'SNZX-20201022',]

    # 广东政府采购网
    def gdgpo_gov(self):
        result_list = etree.HTML(self.det_html).xpath('//div[@class="zw_c_c_qx"]//span[4]/text()')
        result_str = ''.join(result_list)
        regex_str = '采购编号：'
        if re.search(regex_str, result_str):
            result = re.sub(regex_str, '', result_str)
            return result
        regex_list = ['\d{6}-\d{6}-\d{6}-\d{4}','[A-Z]{4}\d{2}-[A-Z]{2}\d{2}-[A-Z]{2}\d{3}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['440000-202010-199092-0007','GZGP20-PZ08-HG067',]

    # 山西政府采购网
    def ccgp_shanxi(self):
        result_list = etree.HTML(self.det_html).xpath('//font[@color="#F00000"]//text()')
        result_str = ''.join(result_list)
        if result_str:
            # print(result_str,'result_str')
            result = result_str.replace('招标编号：','')
            # print(result,'result')
            return result

        exm = ['Z14080001592024622203','Z14080001592024582201','Z14080001592027892203','2020壶财采办备案（555）号',
               '易能-CS-2020-004','2020JHC045','长分采（2020）JZTP/C4/2.','']

    # 山东政府采购网
    def ccgp_shandong(self):
        regex_list = ['[A-Z]{4}\d{10,21}','[A-Z]{4}-[A-Z]{2}-\d{4}-\d{4}','[A-Z]{4}\([A-Z]{2,4}\)-[A-Z]{2}-\d{4}-\d{4}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['SDGP370000202002005613','SDGP370000202002003558','SDGP370000202002004695','HDCG2020000655',
               'JNCZ-JC-2020-0942','JNCZ(SX)-JC-2020-0102','LSCG2020000312','LXCG2020000368','JNCZ-JC-2020-0930',
               'HDCG2020000663','CYCG2020000390','JNCZ(HYHA)-JC-2020-0102',]

    # 内蒙古政府采购网
    def nmgp_gov(self):
        regex_list = ['[A-Z]{8}-\d{4}-[A-Z]{2}\d{3}','[A-Z]{5,7}-[A-Z]-[A-Z]-\d{6}','[A-Z]{6}-[A-Z]{2}-[A-Z]{5}\d{1,4}',
                      '[A-Z]{6}-\d{4}-\d{3}','[A-Z]{17}','\d{4}[A-Z]{2,4}\d{3}[A-Z]{2}','[A-Z]{2}-\d{4}-[A-Z]{2}-\d{3}',
                      '[A-Z]{10}\d{4}-\d{3}','[A-Z]{5}-\d{4}-[A-Z]{2}\d{3}','[A-Z]{6,7}\d{4}-[A-Z]{2,4}-[A-Z]{2,4}\d{4}',
                      '[A-Z]{2}\d{4}[A-Z]\d{4}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['HSMYZYYY-2020-CG001','WSZCS-C-H-200047','BQGGCG2020-ZH-JZXCS0','NMGXJQ-2020-089','D03150727100048601',
               '2020CG211GC','AM-2020-ZC-158','2020CG195HW','2020KQCG046HW','2020CG211GC','KQGGZYXZTP2020-006',
               'XSGGCG2020-ZH-JZXCS0030-1','KEFGW-2020-CG001','WLGGGGC2020-GKZB-QT0004','XMGGCG2020-ZH-JZXCS0037',
               'ZG2020A0034','HRDXG-2020-ZB009','2020AHCG232HW','ESZCZQS-C-G-200227','ESZCDS-X-H-200110','']

    # 山西公共资源交易网
    def prec_sxzwfw(self):
        regex_list = ['[A-Z]{6}\d{4}-\d{3}','[A-Z]{3}-\d{4}-\d{3}','[A-Z]{19}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['GDZBJC2020-018','JXD-2020-209','E1407000827000808001','E1407000827001591001','']

    # 中国政府采购网湖北
    def ccgp_hubei(self):
        regex_list = ['[A-Z]{3,4}-\d{4,8}-\d{2,6}-\d{4}','[A-Z]{4}\d{11}','[A-Z]{6}-\d{4}-[A-Z]{2}\d{3}','[A-Z]{4}\d{4}-\d{4}',
                      '[A-Z]{3}\d{4}-\d{6}-\d{2}[A-Z]','[A-Z]{4}-\d{4}-\d{3}[\u4e00-\u9fa5]','[A-Z]{3}\d{4}-[A-Z]{3}-[A-Z]{3}-\d{2}',
                      '[A-Z]{2,4}-[A-Z]{3,4}-\d{3,4}-\d{2}','[A-Z]{2,4}-[A-Z]{3,4}-\d{3,4}','[A-Z]{3,4}-\d{4,8}-\d{2,6}',
                      '\d{4}[A-Z]{4}-[A-Z]\d{3}-[A-Z]','[A-Z]{8}-\d{6}','[A-Z]{2}\[\d{4}\][A-Z]{3}\d{3}[\u4e00-\u9fa5]',
                      '[A-Z]{7,8}\d{7}','[A-Z]&[A-Z]\d{4}-\d{3}','[A-Z]{4}-[A-Z]{2}-\d{8}[A-Z]{2}','[A-Z]{4}-\d{6}[A-Z]{2}-\d{6}',
                      '[A-Z]{6}\d{4}-[A-Z]{2}\d{4}','[A-Z]{4}-\d{7}-[A-Z]\d{5}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]


        exm = ['HBT-17200251-202690','XSCG20201102001','ZDLC-2020-171','HBHSCG-2020-SY082','XSCG20201102002',
               'HBHSCG-2020-SY073','HBDZ-2020-88','HZTD2020-0812','ZGZ1299-202001-01G','HBSF-ZC-2020-129',
               'JZY2020-QJL-JC4-34','HP-ZFCG-005','SXKQ-GQP-2020-01','ZDLC-2020-166号','HBXXYCG2020010#',
               'ZDLC-2020-174号','2020WHXD-C124-H','HBZHXEZB-202034','HG[2020]JZD024号','HZZBCGSY2020136',
               'Y&Z2020-125','DTR-2020-31','ZQLY-DL-20201017GC','TCZX-202011ZC-004001','SXKQ-DCPJ-2020-01',
               'HBFQTP2020-XM1106','SXKQ-GQP-2020-01','HBZZ-2020150-H20150']

    # 天津政府采购网
    def ccgp_tianjin(self):
        regex_list = ['[A-Z]{12}-[A-Z]{2}-\d{4}-\d{2}','[A-Z]{4,15}-\d{4}-\d{2,3}','\d{4}-\d{12}','[A-Z]{6}-[A-Z]{2}-\d{7}',
                      '[A-Z]{4}\d-\d{7}','[A-Z]{4,5}\d{4}-[A-Z]-\d{3,4}','[A-Z]{4}\d{4}[A-Z]{2}\d{3}','[A-Z]{4}-[A-Z]{2}-\d{4}-\d{2}',
                      '[A-Z]{4}\d{4}-[A-Z]-\d{4}','[A-Z]{4}-\d{4}-[A-Z]{4}-[A-Z]{2}\d{3}','[A-Z]{4}-\d{7}',
                      '[A-Z]{2}-[A-Z]{4,5}\d{7}','[A-Z]{4}\d{7}','\d{4}-\d{4}[A-Z]{3}\d{6}','[A-Z]{6}-[A-Z]{2}-\d{8}',
                      '[A-Z]-\d{4}[A-Z]-\d{3}','[A-Z]{4}\d{4}-\d{3}','[A-Z]{4}-[A-Z]{2}-[A-Z]{2}-\d{4}-\d{4}',
                      '[A-Z]{4}-[A-Z]-\d{2}-\d{3}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['STBCYGJGSSFA-RZ-2020-20','TJYH-2020-038','0615-204120050296','HCLHZB-CS-2020076','RWZB1-2020143',
               'HJGP-2020-F-034','YTZB2020ZC237','JGDGP-2020-A-038','TGPC-2020-A-0351','HYZB-NW-2020-08','ZRZX2020-A-0106',
               'XFZB-2020-TJHX-ZH128','JSZX-2020100','BH-ERMYY2020805','DQHZDXGXDZLGC-2020-01','KQZX-2020-93',
               'BH-ZLYY2020798','XYGK2020274','0760-2061ZFN101404','ZCZBZC-GK-20200121','J-1016B-508','WQCG2020-880',
               'JYZX-ZB-TJ-2020-0200','HFZX-F-20-001','WQCG2020-877',]

    # 政府采购-海南省人民政府政务服务中心
    def zw_hainan_gov(self):
        regex_list = ['[A-Z]{2,6}\d{4}-\d{1,4}[A-Z]','[A-Z]{2,6}\d{4}-\d{1,4}-\d{3}','[A-Z]{2,6}\d{4}-\d{1,4}','[A-Z]{4}-[A-Z]{2}-\d{4}-\d{3}',
                      '[A-Z]{4}\d{4}－\d{2}','[A-Z]{4,6}\d{8,9}-\d','[A-Z]{3,5}-\d{4}-\d{3,4}','[A-Z]{4,6}\d{8,9}',
                      '[A-Z]{4}[\u4e00-\u9fa5]{2}\d{2}【\d{2}】','[A-Z]{2,4}-[A-Z]{2,5}\d{7}','[A-Z]{3,5}-\d{4}-\d{3,4}[A-Z]',
                      '[A-Z]{4}-[A-Z]{2}--[A-Z]\d{7}','[A-Z]{4}-\d{4}-[A-Z]{6}\d{2}','[\u4e00-\u9fa5]{2}[A-Z]{4}-\d{4}-\d{3}',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['HNQL2020-043','HNQL2020-043','HXY2020-161R','HNZC2020-037-003','DGJY-CG-2020-017','HNTXGP2020-052',
               'HRCC2020－22','HFCC20201808','HNZX-2020-1001','ZZYDG-2020-1018','SJC2020-28','ZB2020-0710','HNFYYC2020-60',
               'HNDWZB202009106.','HFGC20201753-2','HNJY2020-1-106','SXXY琼招2020【44】','HNYZ-GK2020083','LZJB-2020-059R',
               'ZK-CGZCS2020086','YZF-2020-005','HNZN-HK--C2020009','HNRH-2020-HNSNCT01','中建ZBDL-2020-053']

    # 公共资源交易平台(海南省)
    def zw_hainan_gov_cn(self):
        regex_list = ['[A-Z]{2,6}\d{4}-\d{1,4}[A-Z]', '[A-Z]{2,6}\d{4}-\d{1,4}-\d{3}', '[A-Z]{2,6}\d{4}-\d{1,4}',
                      '[A-Z]{4}-[A-Z]{2}-\d{4}-\d{3}',
                      '[A-Z]{4}\d{4}－\d{2}', '[A-Z]{4,6}\d{8,9}-\d', '[A-Z]{3,5}-\d{4}-\d{3,4}', '[A-Z]{4,6}\d{8,9}',
                      '[A-Z]{4}[\u4e00-\u9fa5]{2}\d{2}【\d{2}】', '[A-Z]{2,4}-[A-Z]{2,5}\d{7}',
                      '[A-Z]{3,5}-\d{4}-\d{3,4}[A-Z]',
                      '[A-Z]{4}-[A-Z]{2}--[A-Z]\d{7}', '[A-Z]{4}-\d{4}-[A-Z]{6}\d{2}',
                      '[\u4e00-\u9fa5]{2}[A-Z]{4}-\d{4}-\d{3}','[A-Z]{4}-[A-Z]{3}-\d{4}-\d{4}'
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['HNGP-FJC-2020-4740','2020-JWHJHNG-1006','HNZY2020-38','YSKF003R','HNGP-FJC-2020-4737','HNGP-FJC-2020-4732',
               'SXFY2020-030','HNZZ2020056','HNZT2020-242','ZK-CGZDY2020132','HNYH2020-19-0310','HRCC2020－22','HFGC20201825H',
               'HNTXGP2020-052','ZB2020-0911','HNZC2020-037-003']

    # 中国海南政府采购网
    def ccgp_hainan_gov_cn(self):
        regex_list = ['[A-Z]{2,6}\d{4}-\d{1,4}[A-Z]', '[A-Z]{2,6}\d{4}-\d{1,4}-\d{3}', '[A-Z]{2,6}\d{4}-\d{1,4}',
                      '[A-Z]{4}-[A-Z]{2}-\d{4}-\d{3}',
                      '[A-Z]{4}\d{4}－\d{2}', '[A-Z]{4,6}\d{8,9}-\d', '[A-Z]{3,5}-\d{4}-\d{3,4}', '[A-Z]{4,6}\d{8,9}',
                      '[A-Z]{4}[\u4e00-\u9fa5]{2}\d{2}【\d{2}】', '[A-Z]{2,4}-[A-Z]{2,5}\d{7}',
                      '[A-Z]{3,5}-\d{4}-\d{3,4}[A-Z]',
                      '[A-Z]{4}-[A-Z]{2}--[A-Z]\d{7}', '[A-Z]{4}-\d{4}-[A-Z]{6}\d{2}',
                      '[\u4e00-\u9fa5]{2}[A-Z]{4}-\d{4}-\d{3}', '[A-Z]{4}-[A-Z]{3}-\d{4}-\d{4}','[A-Z]{5}\([A-Z]{2}\)-[A-Z]{2}-\d{8}',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['HNHXT-2020-035','GXJTHN-ZCGK2020039/02','HNJS2020-G010','SYZFCG-2020-20-1','HNJYG20200803-CC24',
               'HNGP2020-014','GXTC-D1-2052099','HNYH2020-20-0108','HZ2020-435-1','HNZT2020-241','HNQJX-2020-699',
               'HXY2020-161R','HFGC20201825H','ZK-CGZDY2020132','HNYH-CZ2020-010','ZKGSF(ZB)-HT-20204406',
               'HN-ZB-202000821-03','HXSJ-CG-2020087']

    # 河南省公共资源交易中心门户网
    def hnggzy(self):
        regex_list = ['[\u4e00-\u9fa5]{5,6}-\d{4}-\d{1,4}','[A-Z]{2}\d{12}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['豫财招标采购-2020-1289','豫财磋商采购-2020-531','豫财询价采购-2020-48','FW140801200002']

    # 河南省政府采购网
    def hngp_gov_cn(self):
        regex_list = ['([\u4e00-\u9fa5]{2,6}-\d{4}-\d{1,4})\d[、.]','[\u4e00-\u9fa5]{2,6}-\d{4}-\d{1,4}','[\u4e00-\u9fa5]{2,6}[A-Z]{2}-\d{4}-\d{1,4}',
                      '[\u4e00-\u9fa5]{2,6}【\d{4}】\d{2,4}[\u4e00-\u9fa5]','[A-Z]{4}\d{4}-\d{3}',
                      '[\u4e00-\u9fa5]{2,6}\d{4}-\d{1,4}','[\u4e00-\u9fa5]{2,6}\d{4}【\d{2,4}】',
                      '[\u4e00-\u9fa5]{2,6}\(\d{4}\)\d{2,4}[\u4e00-\u9fa5]','[A-Z]{4}-\d{4}-[A-Z]{2}-\d{3}',
                      '[A-Z]{4}-\d{4}-[A-Z]{2}\d{4}','\([\u4e00-\u9fa5]{2}\)[\u4e00-\u9fa5]{2}[A-Z]{4}-\d{4}-\d{4}',
                      '[\u4e00-\u9fa5]{2}\d[\u4e00-\u9fa5]\d{4}-\d{2}-\d{2}']
        for i in regex_list:
            # print(i)
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['镇财采购GK-2020-81','信财磋商采购-2020-122','信财公开招标-2020-176','XXZC2020-174','获财招标采购【2020】51号',
               'MCCGZB[2020]11号-B','中原公开-2020-192','泌政采【2020】237号','邓采2020-243','伊政分采【2020】088号',
               '2020-09-75','管竞争性磋商(2020)046号','HNRQ-2020-CG-017','偃政采2020【295】','202001630','ZLZB-2020-HW0002',
               '汝财招标采购-2019-109','宜阳工施招标(2020)0246号','(县区)新交GCZB-2020-0720','政府9月2021-09-49']

    # 江西公共资源交易网
    def jxsggzy_cn(self):
        regex_list = ['\d{4}-\d{3}[A-Z]{2}\d{7}-\d{2}','[A-Z]{4}\d{4}-[A-Z]{2}-[A-Z]{1,2}\d{3}','[A-Z]{4}\d{4}-[A-Z]\d{3}',
                      '[A-Z]{4}-\([A-Z]{2}\)\d{4}-[A-Z]{2}\d{3}','[A-Z]{7}\d{11}','[A-Z]{4}-[A-Z]{2}-\d{4}-\d{3}-\d{2}',
                      '[A-Z]{4}\d{4}-\d{2}-\d{4}','[A-Z]{4}\d{4}-[A-Z]{2}-\d{8}','[A-Z]{4}-\d{4}-[A-Z]{2}\d{3}',
                      '[A-Z]{4}\d{7}-\d','[A-Z]{4}-[A-Z]{4}\d{4}-[A-Z]\d{3}[\u4e00-\u9fa5]',
                      '[A-Z]{4}\d{4}-[A-Z]\d{4}-\d{2}[\u4e00-\u9fa5]','[\u4e00-\u9fa5]{2}-[A-Z]{2}\d{4}-\d{3}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['1313-204GZ2015101-03','JXHC2020-NC-DY031','JXZY2020-G003','JXRC-(NC)2020-GK010','JXAL2020-NC-Z10',
               'JXABXZC29202008060','JXRC-HK-2020-007-02','JXGZ2020-11-1601','ZXZB2020-JK-J001','GZKC2020-JX-J001',
               'JXTH2020-TP-20201026','JXZX-2020-ZC133','JXZT2020113-1','CJGC-JDZ2020-J001号','JXGZ2020-09-1102-1',
               'JXDY2020-J0115-04包','三连-YC2020-004']

    # 江西省政府采购网
    def ccgp_jiangxi_gov_cn(self):
        regex_list = ['\d{4}-\d{3}[A-Z]{2}\d{7}-\d{2}', '[A-Z]{4}\d{4}-[A-Z]{2}-[A-Z]{1,2}\d{3}',
                      '[A-Z]{4}\d{4}-[A-Z]\d{3}',
                      '[A-Z]{4}-\([A-Z]{2}\)\d{4}-[A-Z]{2}\d{3}', '[A-Z]{7}\d{11}',
                      '[A-Z]{4}-[A-Z]{2}-\d{4}-\d{3}-\d{2}',
                      '[A-Z]{4}\d{4}-\d{2}-\d{4}', '[A-Z]{4}\d{4}-[A-Z]{2}-\d{8}', '[A-Z]{4}-\d{4}-[A-Z]{2}\d{3}',
                      '[A-Z]{4}\d{7}-\d', '[A-Z]{4}-[A-Z]{4}\d{4}-[A-Z]\d{3}[\u4e00-\u9fa5]',
                      '[A-Z]{4}\d{4}-[A-Z]\d{4}-\d{2}[\u4e00-\u9fa5]', '[\u4e00-\u9fa5]{2}-[A-Z]{2}\d{4}-\d{3}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['1313-204GZ2015101-03', 'JXHC2020-NC-DY031', 'JXZY2020-G003', 'JXRC-(NC)2020-GK010', 'JXAL2020-NC-Z10',
               'JXABXZC29202008060', 'JXRC-HK-2020-007-02', 'JXGZ2020-11-1601', 'ZXZB2020-JK-J001', 'GZKC2020-JX-J001',
               'JXTH2020-TP-20201026', 'JXZX-2020-ZC133', 'JXZT2020113-1', 'CJGC-JDZ2020-J001号', 'JXGZ2020-09-1102-1',
               'JXDY2020-J0115-04包', '三连-YC2020-004']

    # 河北省公共资源交易中心
    def www_hebpr_cn(self):
        regex_list = ['[A-Z]{1,2}\d{16}','[A-Z]\d{12}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['HB2020113606010001','Z130000202124','HB2020103500020003','HB2020103610040067',]

    # 河北省政府采购网
    def ccgp_hebei_gov_cn(self):
        regex_list = ['[A-Z]{4}\([A-Z]{2}\)\d{7}','[A-Z]{7}-\d{7}','[A-Z]{4}-[A-Z]{3}-\d{3}','[A-Z]{4}\d{6}[A-Z]{4}\d{3}',
                      '[A-Z]{3}-[A-Z]\d{12}-\d','[A-Z]{4}-\d{4}[A-Z]\d{3}','[A-Z]{4,6}\d{8}-\d{2}',
                      '[A-Z]{4}-\d{2}[A-Z]\d{3}','[A-Z]{4}-\d{4}[A-Z]{3}\d{3}','[A-Z]{3,4}-\d{4,6}-\d{3,4}-\d{3}~\d{3}',
                      '[A-Z]{3,4}-\d{4,6}-\d{3,4}-\d{3}','[A-Z]{3,4}-\d{4,6}-\d{2,4}','[A-Z]{4,6}\d{8}','[A-Z]{4}\d{4}-[A-Z]{2}-\d{2}',
                      '[A-Z]{4}\d{4}-[A-Z]\d{3}','[A-Z]{4}\(\d{4}\)-\d{2}-\d{2}','[A-Z]\d{12,16}','[A-Z]{2}\d{16}',
                      '[A-Z]{4}\d{4}-\d{3}','\d{6}[A-Z]\d{2}[A-Z]\d{8}']
        for i in regex_list:
            ## print(i)
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['Z130000202235','Z130000202189','RHP-C232002783319-1','HBZJ-2020N878','BAZB20309101','MZZB-20Z015',
               'HBZJ-2020ZJK165','HBCT-201059-001','YTZB-2020-135','HXZB-2020-0171','HXZB-2020-0270-002',
               'JZD-2020-086','HBZJ-2020N723','BAZB20301901-03','HBXR2020-XT-47','BOAOZB20322201','Z1300002022702001',
               'HBCT-201005-001~004','HBCJ2020-A066','HBHY(2020)-02-65','HBSG(ZC)2020011','ZJZB-HXX-031',
               'HRCZBHS-2020026','ZDZB2020-015','130301Z02A20200432']

    # 北京经济技术开发区——政府采购中心
    def kfqgw_beijing_gov_cn(self):
        regex_list = ['\d{4}-\d{4}[A-Z]{2}\d{6}','[A-Z]{4}-\d{4}-[A-Z]\d{5}','[A-Z]{3}-\d{4}-[A-Z]{2}\d{3}-\d',
                      '\d{4}[A-Z]{3}\d{5}','[A-Z]{3,4}-\d{4,6}-\d{3,5}','[A-Z]{2}\d{2}-[A-Z]{8}-\d{4}',
                      '\d{4}[A-Z]{3}\d{5}','[A-Z]{4}〔\d{4}〕\d{5}','[\u4e00-\u9fa5]{2}\[\d{4}\]\d{3}[\u4e00-\u9fa5]（[\u4e00-\u9fa5]{2}）-\d',
                      '[A-Z]{2}\d{4}-\d{3}-\d{3}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['0610-2041NH081083','ZTXY-2020-F45625','HJP-2020-ZB071-1','2041STC71603','HJP-2020-ZB071-1',
               'ZLZB-2020-045','YQ03-KFQKJCXJ-2010','2041STC71944/01','BJZX〔2020〕21013','建招[2020]023政（框架）-5',
               'YQ03-KFQDQFWZX-2005','ZZHW-BJYZ-20005','DL2020-036-002','0610-2041NH080957','ZLZB-2020-034',
               'HJP-2020-ZB071-1']

    # 北京市工程建设交易网
    def bcactc(self):
        regex_list = ['\d{3}[A-Z]\d[A-Z]{2}\d{9}','[A-Z]\d{2}[A-Z]{1,4}\d[A-Z]{2,3}\d{8,10}','[A-Z]{1,4}\d[A-Z]{2,3}\d{8,10}',
                      '\d{4}[A-Z]{1,2}\d{7,8}','[A-Z]{4,5}\d{8}[A-Z]?',
                      '[A-Z]{4}\d[A-Z]{2}\d','\d{4}[A-Z]{2}\d{7}']
        for i in regex_list:
            ## print(i)
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['111F0SG202000022','105F0SG202000063','F0SG202000403','2020J00000333','FZZFA02000442','2020ZS0000114',
               'CRDT0WZ202000800','371T0JL202000100','YGKL20200298A','M0SJX02000024','J0SGX0520200003','2020JQ0000443',
               ]

    # 北京市公共资源交易服务平台
    def ggzyfw_beijing_gov_cn(self):
        regex_list = ['[A-Z]{4}\d{4}-\d{3}-\d{2}','\d{4}[A-Z]{2}\d{7}','[A-Z]\d[A-Z]{2}\d{9}','[A-Z]{2,4}\d{6,7}[A-Z]?','[\u4e00-\u9fa5]{2}[A-Z]\[\d{8}\]-\d{4}[\u4e00-\u9fa5]',
                      '[A-Z]{4,5}-\d{12}','[A-Z]{4,5}-\d{4}-[A-Z]?\d{4}','\d{4}-[a-z]{4}-[A-Z]{2}\d{3}-[A-Z]{3}',
                      '[A-Z]{3}\d{4}_\d{6}_\d{6}-[A-Z]{2}\d{3}','[A-Z]{3}\d{4}_\d{6}_\d{6}_\d{8}_[A-Z]{4}-[A-Z]{2}\d{3},[A-Z]{2}\d{3}',
                      '[A-Z]{4}\d{4}_\d{6}_\d{3}-[A-Z]{2}\d{4}-[A-Z]{2}\d{3}','[A-Z]{4}\d{2}[A-Z]{2}\d{4}',
                      '[A-Z]{4}\d{5}-\d{3}','[A-Z]{3}\d{4}_\d{6}_\d{3}-[A-Z]{2}\d{3}-[A-Z]{2}\d{3}','[A-Z]\d{6}[A-Z]\d{9,12}',
                      ]
        for i in regex_list:
            # print(i)
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]


        exm = ['S110000C005027081','2021JQ0000424','S110000C005027046','PXM2020_115208_000187-JH001-XM001','RGSZB-2020-152','WYCZ30120-085',
               'WYCZ30120-096','GFTC20EE0359','HTZX-2020-152','ZC203196Z','TZXM-202009289850','JBZC2020_014204_310-JH0025-XM001',
               'PXM2020_193311_000014_00412236_XMCG-JH003-XM001','PXM2020_020102_000139-JH001-XM001','2020-frmz-JH001-XM001',
               'MYZC-2020-C0367','SJSXM-202010101086','CPCG-202009254222','采计X[20200923]-4635号','HYHZ2020431',
               'HCYX2020077','SRCZ2020-005-03','F0SG202000297']

    # 北京市政府采购网
    def ccgp_beijing_gov_cn(self):
        regex_list = ['[A-Z]{4}\d{4}-\d{3}-\d{2}', '[A-Z]{2,4}\d{6,7}[A-Z]?',
                      '[\u4e00-\u9fa5]{2}[A-Z]\[\d{8}\]-\d{4}[\u4e00-\u9fa5]',
                      '[A-Z]{4,5}-\d{12}', '[A-Z]{4,5}-\d{4}-[A-Z]?\d{4}', '\d{4}-[a-z]{4}-[A-Z]{2}\d{3}-[A-Z]{3}',
                      '[A-Z]{3}\d{4}_\d{6}_\d{6}-[A-Z]{2}\d{3}',
                      '[A-Z]{3}\d{4}_\d{6}_\d{6}_\d{8}_[A-Z]{4}-[A-Z]{2}\d{3},[A-Z]{2}\d{3}',
                      '[A-Z]{4}\d{4}_\d{6}_\d{3}-[A-Z]{2}\d{4}-[A-Z]{2}\d{3}', '[A-Z]{4}\d{2}[A-Z]{2}\d{4}',
                      '[A-Z]{4}\d{5}-\d{3}', '[A-Z]{3}\d{4}_\d{6}_\d{3}-[A-Z]{2}\d{3}-[A-Z]{2}\d{3}',
                      '[A-Z]{2}\d{2}[A-Z]{2}-\d{3}[A-Z]{3}-\d{2}','\d{4}-\d{4}[A-Z]\d{7}[A-Z]','[A-Z]{4}-\d{12}',
                      '[A-Z]{2}\d{2}[A-Z]{2}-\d{3}[A-Z]{3}/\d{2}','[A-Z]{2}\d{4}[A-Z]{2}-[A-Z]{2}-[A-Z]{2}\d{4}',
                      '\d{4}-\d{2}-\d{6}-\d{6}-\d[A-Z]','\d{4}-\d{6}-\d{6}-\d','[A-Z]{4}_\d{2}_\d{4}',
                      ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]


        exm = ['PXM2020_115208_000186-JH001-XM001','PXM2020_193311_000014_00412236_XMCG-JH003-XM001',
               'JBZC2020_014204_310-JH0025-XM001','2020-frmz-JH001-XM001','PXM2020_056204_000005-JH00NaN-XM001',
               'JBZC2020_014223_302-JH0013-XM001','采计X【20201104】-4741号','SJSXM-202011021294','SYCG_20_1135',
               '2020-202001-000018-1','2020-19-105001-100041-1A','ZB2020BJ-TZ-SG0260','CPCG-202009073951',
               'FE20ZX-001LZY/51','0686-2041Q4791479Z','FE20ZX-002LZY-12',]

    # 北京市政府采购中心
    def bgpc_beijing_gov_cn(self):
        regex_list = ['[A-Z]{4}-[A-Z]\d{5}[A-Z]?']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]


        exm = ['BGPC-G20049','BGPC-A20011','BGPC-G19074B','']

    # 全国公共资源交易平台
    def ggzy_gov_cn(self):
        regex_list = ['[\u4e00-\u9fa5]{3}（\d{4}）[A-Z]{4}\d{2}-\d{4}','\[\d{6}\][A-Z]{2,6}\[[A-Z]{2}\]\d{7}','[A-Z]{4}\d{18}','[A-Z]{4}\([A-Z]\)-\d{4}-\d{3}',
                      '[A-Z]{4}\d{4}-[A-Z]{2}-\d{4}/\d{3}','[A-Z]{2,3}-[A-Z]{4,6}-\d{6,8}[A-Z]?-\d{3}','[A-Z]{2,6}-[A-Z]{4,6}-\d{6,8}[A-Z]?',
                      '[A-Z]{4,7}-\d{6,8}[A-Z]{2}-\d{3,6}','[A-Z]{4,7}-\d{6,8}[A-Z]?-\d{3,6}','[A-Z]{4}-\d{12}','[A-Z]{4,7}-\d{6,8}[A-Z]?',
                      '[A-Z]{3}-\d{2}-\d{7}','[A-Z]{4}\d{4}-\d{5}[A-Z]','[A-Z]{4}-\d{11}','[A-Z]{4}\d{4}-[A-Z]{2}\d{2}[A-Z]{2}-\d{2}',
                      '[A-Z]{4}-[A-Z]{4}（\d{4}）\d{3}[\u4e00-\u9fa5]','[A-Z]{5}-[A-Z]{2}-[A-Z]{2}\d{10}','[A-Z]{2,7}\d{7,16}','[A-Z]\d{20}',
                      '[A-Z]{4}\d{10}','[A-Z]{2}\d{5}[A-Z]{2}\d{3}','[A-Z]\d{3}[A-Z]{2}-[A-Z]{4}-[A-Z]{2}\d','[A-Z]{4}\d{4}-[A-Z]\d-\d{6}-[A-Z]{4}',
                      '[A-Z]{4}\d{4}-[A-Z]{2}-[A-Z]{2}-\d{3}','[A-Z]{4,8}\d{4}-\d{3,4}','[A-Z]{4}-\d{6}[A-Z]{2}-\d{3}','[A-Z]{4}\d{4}-[A-Z]{2}-[A-Z]\d{3}',
                      '[A-Z]{5}-[A-Z]{2}-\d{6}-[A-Z]\d{3}','[A-Z]{4}-\d{4}[\u4e00-\u9fa5]\d{2}[\u4e00-\u9fa5]','[\u4e00-\u9fa5]{2,4}-[A-Z]{2}\d{4}-\d{3}[A-Z]?',
                      '[\u4e00-\u9fa5]{2,5}[A-Z]{2}-\d{7}[\u4e00-\u9fa5]?','[A-Z]{4}\d{4}-[A-Z]{2}\d{3}',
                      '[A-Z]{4}-[A-Z]{2}-\d{4}-\d{3,4}','[A-Z]{4}\d{2}-\d{2}-\d{2}','\d{3}-\d{4}[A-Z]{2}-\d{3}','[A-Z]{4}-[A-Z]{3}-\d{4}-\d{3}',
                      '[A-Z]{4}\d{2}-\d{3}','[A-Z]{8}-\d{4}-\d{3}','[A-Z]{3}\d{4}-\d{2}-\d{3,4}','[A-Z]{4}\d{4}-[A-Z]\d{3}','[A-Z]{6}-\d{4}-\d{2}',
                      '[A-Z]{4}\d{2}[A-Z]{2}\d{4}','[A-Z]{6}-[A-Z]{2}\d{4}-\d{3}','\d{6}-\d{6}-\d{6}-\d{4}',
                      '\d{8}[A-Z]\d{4}','[\u4e00-\u9fa5]{4}\d{4}-\d{3}']
        for i in regex_list:
            # print(i)
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]


        exm = ['SCZD2020-CS-2475/001','HDZXCG-202009','DDZX-20201106077','ZB2020057','SCBCZR-CS-2020007','NNZC2020-30235F',
               'DDZX-20201106077','DDZX-20201106077','JXHD2020-CG11CG-02','XSGSCG-2020106','GSDW-2020064','ZB2020057',
               'NBGD-20201082S','20A02082','GSHC-ZFCG（2020）001号','HB2020103610360001','Z14080001592029172503',
               'HB2020103610360001','JXTC2020070527','浙安采字2020-029','S126JN-SZPT-SJ3','JXYJ2020-FZ-LA-009',
               'SHJS2020-034','CBZX-202011ZC-029','[2020]1697号','HBYHX-ZC-202011-F153','GSYX-2020第15号','XYCG20201101',
               'HBJX-ZB-2020-252','HBXY20-11-05','XSCG20201110001','131-2020CG-233','HHZX20-116','YGCXZFCG-2020-153',
               'ZFCG(F)-2020-014']

    # 工信部通信工程建设项目招标投标管理信息平台
    def txzb_miit_gov_cn(self):
        regex_list = ['[\u4e00-\u9fa5]{4}【\d{4}】\d{4}[\u4e00-\u9fa5]','[A-Z]{2,4}\d{11,14}','[A-Z]{6}\d{7,8}',
                      '[A-Z]{2}\d{5}[A-Z]','[A-Z]{4}-[A-Z]{4}-\d{4}-\d{3}','[A-Z]{4}-[A-Z]{4}-\d{5}','[A-Z]{4}\d{4}-\d{3}',
                      '[A-Z]{4}-\d{4}-\d{4}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]


        exm = ['咪文采音【2020】0221号','BJYD20200000749','SNYD20200001432','CMCC20200000301','NB37182020000079',
               'ZZDXZB2020004','TC209603H','JSZBZB20201433','TTGZ-GZCG-2020-026','HBTZ-BJLT-20072','GKCG2020-126',
               'NB37102020000756','FJZT-2020-0733',]

    # 中央政府采购网
    def zycg_gov_cn(self):
        regex_list = ['[A-Z]{2}-[A-Z]{3}\d{6}','[A-Z]{4}\d{14}','[A-Z]{2}\d{14}']
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]


        exm = ['GC-HGX200881','GC-HGX201135','GC-FGX201217','DZJJ20111110545620','FP20110910065720']

    # 中华人民共和国财政部
    def mof_gov_cn(self):
        regex_list = ['[A-Z]{4}\d{4}-[A-Z]-[A-Z]-\d{3}[\u4e00-\u9fa5]','[A-Z]{2}\d{7}[A-Z]{2}\d[A-Z]\d{2}','[A-Z]\d{4}-[A-Z]{3}\d{2}[A-Z]\d[A-Z]\d{2}',
                      '[A-Z]\d{4}-[A-Z]{3}\d{2}[A-Z]\d{4}','[A-Z]{2}\d{3}[A-Z]\d[A-Z]{2}','[A-Z]{4}-[A-Z]\d-\d{8}',
                      '[A-Z]{2}\d{2}[A-Z]{2}-[A-Z]\d{4}-[A-Z]{3}','[A-Z]{3}\d{4}[A-Z]{2}\d{2}[A-Z]{2}\d{2}[A-Z]',
                      '[A-Z]{6}-\d{4}-[A-Z]-\d{3}','[A-Z]{4}\d{18}','[A-Z]\d{16}','\d{2}[A-Z]{4}-\d{3}-\d{3}',
                      '[A-Z]{5}-[A-Z]{2}\d{4}','\d{4}-\d{4}[A-Z]{4}\d{4}','\d{4}-\d{12}/\d{2}','[A-Z]{4}\d{4}[A-Z]{3}\d{6}',
                      '\d{5}[A-Z]{2}\d{3}','[A-Z]{2}-[A-Z]{4}-\d{7}','[A-Z]{3}-\d{8}-\d{6}','[A-Z]{4}-\d{4}-[A-Z]\d{5}',
                      '[A-Z]{6}\d{8}',]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]


        exm = ['0733-20112270','ZZ0200674NA0A99','B0708-CMC20N7W42','B0708-CMC20N7317','TC209D0WH','GXTC-A1-20630794',
               'HG20GK-C0000-D138','CLF0120GZ10ZC18A','TJYNSJ-2020-F-041','M4400000707007750','20CNIC-031692-047',
               '0625-20102611','BIECC-ZB8923','0771-2040CIGJ0095','1639-204122190424/02','WKZB2011GDG300805',
               '20130ZB061','BD-JSJT-2020001','HBT-15200144-202297','ZTXY-2020-F26537','SDGP371323202102000263']

    # 中国政府采购网
    def ccgp_gov_cn(self):
        regex_list = ['[A-Z]{4}\([A-Z]{4}\)-[A-Z]{2}-\d{4}-\d{4}','[A-Z]{6}\(\d{4}\)\d{3}[A-Z]-\d', '[A-Z]{2}\d{7}[A-Z]{2}\d[A-Z]\d{2}', '[A-Z]\d{4}-[A-Z]{3}\d{2}[A-Z]\d[A-Z]\d{2}',
                      '[A-Z]\d{4}-[A-Z]{3}\d{2}[A-Z]\d{4}', '[A-Z]{2}\d{3}[A-Z]\d[A-Z]{2}', '[A-Z]{4}-[A-Z]\d-\d{8}',
                      '[A-Z]{2}\d{2}[A-Z]{2}-[A-Z]\d{4}-[A-Z]{3}', '[A-Z]{3}\d{4}[A-Z]{2}\d{2}[A-Z]{2}\d{2}[A-Z]',
                      '[A-Z]{6}-\d{4}-[A-Z]-\d{3}', '[A-Z]\d{16,20}', '\d{2}[A-Z]{4}-\d{3}-\d{3}',
                      '[A-Z]{5}-[A-Z]{2}\d{4}', '\d{4}-\d{4}[A-Z]{4}\d{4}', '\d{4}-\d{12}/\d{2}',
                      '[A-Z]{4}\d{4}[A-Z]{3}\d{6}','[A-Z]{4}\([A-Z]{4}\)-[A-Z]{2}-\d{4}-\d{4}',
                      '\d{5}[A-Z]{2}\d{3}','\d{2}[A-Z]\d{5}','[A-Z]{2}-[A-Z]{4}-\d{7}', '[A-Z]{3}-\d{8}-\d{6}',
                      '[A-Z]{4}-\d{4}-[A-Z]\d{5}','[A-Z]{2}-[A-Z]{4}-\d{5}','\d{4}-[A-Z]{2}\d{2}-[A-Z]\d{4}',
                      '[A-Z]{4}\d{18}']
        for i in regex_list:
            # print(i)
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]


        exm = ['']


    def nbzfcg(self):

        exm = []


    def yngp(self):

        exm = ['PLCGZX-2020-043']


    def jszwfw(self):
        regex_list = [
            '[A-Z]{4}\d{4}-[A-Z]{2}-[A-Z]-\d{3}-[A-Z]','[A-Z]{4}\d{4}-[A-Z]{2}-[A-Z]-\d{3}号?','[A-Z]{4}\d{4}-[A-Z]-\d{3}','[A-Z]{4}\d{9}-[A-Z]\d{2}','[A-Z]{4}-\d{10}-\d{3}-[A-Z]{2}',
            '\d{6}-[A-Z]-\d{13}-\d','[A-Z]{4}-\d{10}-[A-Z]{2}','[A-Z]{6}-\(\d{4}\)[\u4e00-\u9fa5]{3}\d{4}[\u4e00-\u9fa5]',
            '[A-Z]{4}\d{4}-[A-Z]-[A-Z]-\d{3}-\d{3}','[A-Z]{4}-\d{10}','[A-Z]\d{19}-\d','[A-Z]\d{19}','[A-Z]\d{12}\([A-Z]{2}\d{3}\)',
            ]
        for i in regex_list:
            result = re.search(i, self.content)
            if result:
                print(re.findall(i, self.content))
                return re.findall(i, self.content)[0]

        exm = ['WJZJ2021-WJ-G-005','Z320612210298(CS085)','E3213010313202112088-1','KSZC2021-G-155','WXXS202112009-X01',
               'HAZC-2021120458-001-HY','SZWK2021-WJ-G-029-A','320701-J-2021041401132-2','HAZC-2021110448-HY',
               'HAGC-2021120141-LS','ZJZCFS-(2021)商字第0720号','SZYJ2021-WJ-C-050号','YQJC2021-Y-G-029-001',
               'HAZC-2021120565','']

    def shggzy(self):
        p_num = etree.HTML(self.det_html).xpath('//div[@class="content-box"]//h4/text()')
        # print(p_num)
        if p_num:
            return p_num[0].replace('交易项目编号：','')


    # def ggzy_ah(self):
    #     regex_list = ['[A-Z]{3}-[A-Z]{2}-[A-Z]{2}-\d{7}','[\u4e00-\u9fa5]{2}[A-Z]\d{4}[A-Z]\d{3}-\d',
    #                   '[a-z]{4}\d{6}-\d{3}','[A-Z]{2}-[A-Z]{4}\d{7}[A-Z]?','[A-Z]{4}-\d{5}-[A-Z]{4}',
    #                   '[A-Z]{2}\d{4}[A-Z]{5}\d{3}','[A-Z]{5}\d{4}[A-Z]\d{3}','\d{4}[A-Z]{3}\d{3}']
    #     for i in regex_list:
    #         # print(i)
    #         result = re.search(i, self.content)
    #         if result:
    #             print(re.findall(i, self.content))
    #             return re.findall(i, self.content)[0]
    #
    #     exm = ['GDS-CG-TP-2021267','裕采G2021H715-3','czcg202109-126','EP-YQCG2021037','EP-SXCG2021030A','HBCG-21061-SHDL',
    #            'BB2021ZFCGJ328','2021CGF036','HJACG2021G140','GDS-CG-TP-2021267']


    def hbggzyfwpt(self):
        project_code = etree.HTML(self.det_html).xpath('//input[@id="purchaseProjectCode"]/@value')
        # print(project_code)
        if project_code:
            return project_code[0]



if __name__ == '__main__':
    url = '2021CG115HW.1B1'
    a = re.findall('\d{4}[A-Z]{2}\d{3}[A-Z]{2}\.\d[A-Z]\d',url)
    print(a)