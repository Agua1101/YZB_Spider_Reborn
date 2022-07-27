# encoding:utf8
import json
import regex as re


Features = {}
Features["http://www.mof.gov.cn/"] = ['class="box_content"']
Features["ccgp.gov.cn"] = ['class="vF_detail_content"','class="vT_detail_main"','class="vT_detail_content w760c"','class="left_content"']
Features["zycg.gov.cn"] = ['id="printArea"','width="1000"','id="container"']
Features["http://txzb.miit.gov.cn"] = ['id="ef_region_inqu"','class="tableBorder"']
Features["ccgp_intention"] = ['class="pubtable"']
Features["http://www.ggzy.gov.cn/"] = ['class="detail_content"']
Features["http://www.mwr.gov.cn/"] = ['id="slywxl1"']
Features["bgpc.beijing.gov.cn"] = ['id="mainText"','class="content-right-content"','class="content-right-details-content"']
Features["ccgp-beijing.gov.cn/"] = ['']
Features["www.bcactc.com"] = ['class="ContextTable"']
Features["ggzyfw.beijing.gov.cn"] = ['class="newsCon"']
Features["ccgp-hebei.gov.cn"] = ['id="2020_VERSION"','width="930"','width="1200"']
Features["www.hebpr.cn"] = ['class="content_scroll"']
Features["ccgp-jiangxi.gov.cn"] = ['class="article-info"']
Features["ccgp-hainan.gov.cn"] = ['class="nei03_02"','class="content01"']
Features["ccgp-hubei"] = ['']
Features["jxsggzy.cn"] = ['class="article-info"']
Features["hngp.gov.cn"] = ['']
Features["hnggzy"] = ['id="TDContent"','id="divArtice"']
Features["zw.hainan.gov.cn"] = ['class="newsCon"']
Features["www.customs.gov.cn"] = ['align="left"']
Features["121.28.195.124"] = ['class="font_black"']
Features["hntba"] = ['class="news-xq"']
Features["zw.hainan.gov"] = ['class="zx-xxxqy-nr"','class="xly"','id="Zoom"']
Features["kfqgw.beijing.gov.cn"] = ['id="div_zhengwen"']
Features["ccgp-tianjin"] = ['class="pageInner"']
Features["prec_sxzwfw"] = ['class="body_main"']
Features["nmgp_gov"] = ['class="content-box-1"']
Features["ccgp-shanxi"] = ['//tr[@class="bk5"]']
Features["ccgp-shandong"] = ['bgcolor="#FFFFFF"','class="listConts"']
Features["gdgpo.gov"] = ['id="content"']
Features["ccgp-jiangsu"] = ['class="detail_con"']
Features["ccgp-jilin"] = ['id="xiangqingneiron"']
Features["hljcg.gov.cn"] = ['class="xxej"']
Features["ccgp-hunan"] = ['']
Features["ccgp-fujian"] = ['class="notice-con"']
Features["ccgp-chongqing"] = ['']
Features["ccgp-anhui"] = ['']
Features["ccgp-sichuan"] = ['class="package_lines layoutfix"']
Features["ccgp-liaoning"] = ['id="template"']
Features["ccgp-guangxi"] = ['']
Features["ccgp-guizhou"] = ['']
Features["yngp"] = ['class="vF_detail_content"','class="vT_detail_main"','class="vT_detail_content w760c"']
Features["ccgp-shaanxi"] = ['class="inner-Box','class="annBox"','class="content-inner"']
Features["ccgp-xinjiang"] = ['']
Features["ccgp-gansu"] = ['id="fontzoom"']
Features["ccgp-ningxia"] = ['class="vT_detail_content w100c','id="jjDiv"']
Features["ccgp-xizang"] = ['class="notice-con"']
Features["ccgp-qinghai"] = ['']
Features["cgw_xjbt"] = ['']
Features["zfcg_qingdao"] = ['class="cont"']
Features["nbzfcg"] = ['']
Features["szzfcg"] = ['id="contentDiv']
Features["ccgp-dalian"] = ['id="_Sheet1"']
Features["prec_sxzwfw"] = ['class="gycq-table"']
Features["zjzwfw"] = ['class="con"']
Features["hljggzyjyw"] = ['class="ewb-art-bd"']
Features["jszwfw"] = ['class="ewb-trade-right l"']
Features["lnggzy"] = ['id="zfcg_zbgs1_TDContent"','id="zfcg_zbgg1_TDContent"']
Features["ggzy_hebei"] = ['class="ewb-copy"']
Features["ggzyjy.nmg"] = ['class="detail_contect"','id="noticeArea"']
Features["ggzy_zwfwb"] = ['']
Features["jl_gov_cn"] = ['class="ewb-article-info"']
Features["shggzy"] = ['class="content"']
Features["ggzy_ah"] = ['id="content"']
Features["ggzyfw_fj"] = ['']
Features["ggzyjy_shandong"] = ['class="gycq-table"']
Features["hnsggzyfwpt"] = ['class="ewb-left-bd"']
Features["hbggzyfwpt"] = ['']
Features["hnsggzy"] = ['class="div-article2"','class="div-article"','class="content-article"']
Features["gxggzy"] = ['class="ewb-details-info"']
Features["cqggzy"] = ['id="mainContent"']
Features["ggzyjy_sc"] = ['class="clearfix"']
Features["ggzy_guizhou"] = ['']
Features["ggzy_yn"] = ['class="detail_contect"']
Features["ggzy_xizang"] = ['class="div-article2"']
Features["sxggzyjy"] = ['id="mainContent"','class="epoint-article-content jynr news_content"']
Features["ggzyjy_gansu"] = ['']
Features["qhggzyjy"] = ['class="xiangxiyekuang"']
Features["nxggzyjy"] = ['id="tab-1"']
Features["ggzy_xinjiang"] = ['class="ewb-info-bd"']
Features["ggzy_xjbt"] = ['class="infodetail"']
Features["ccgp-neimenggu-in"] = ['id="content-box-1"']
Features["ggzyjy_ordos"] = ['class="noticeArea"']



Xpaths = {}
Xpaths["http://www.mof.gov.cn/"] = ['//div[@class="box_content"]']
Xpaths["ccgp.gov.cn"] = ['//div[@class="vF_detail_content"]','//div[@class="vT_detail_main"]','//div[@class="vT_detail_content w760c"]','//div[@class="left_content"]']
Xpaths["zycg.gov.cn"] = ['//div[@id="printArea"]','//table[@width="1000"]','//script[@id="container"]']
Xpaths["http://txzb.miit.gov.cn/"] = ['//*[@id="ef_region_inqu"]','//table[@class="tableBorder"]']
Xpaths["ccgp_intention"] = ['//div[@class="pubtable"]']
Xpaths["http://www.ggzy.gov.cn/"] = ['/html/body/div[1]']
Xpaths["http://www.mwr.gov.cn/"] = ['//*[@id="slywxl1"]']
Xpaths["bgpc.beijing.gov.cn"] = ['//div[@id="mainText"]','//div[@class="content-right-content"]','//div[@class="content-right-details-content"]']
Xpaths["ccgp-beijing.gov.cn/"] = ['//div[@id="mainText"]','/html/body/div[1]/div[3]','/html/body/div[2]/div[3]']
Xpaths["www.bcactc.com"] = ['//table[@class="ContextTable"]']
Xpaths["ggzyfw.beijing.gov.cn"] = ['//div[@class="newsCon"]']
Xpaths["ccgp-hebei.gov.cn"] = ['table[@id="OLD_VERSION"]','//table[1]','//table[@id="2020_VERSION"]','//table[@width="930"]','//table[@width="1200"]']
Xpaths["www.hebpr.cn"] = ['//div[@class="content_scroll"]']
Xpaths["ccgp-jiangxi.gov.cn"] = ['//div[@class="article-info"]']
Xpaths["ccgp-hainan.gov.cn"] = ['//div[@class="nei03_02"]','//div[@class="content01"]']
Xpaths["ccgp-hubei"] = ['//div[@class="art_con"]//div[2]']
Xpaths["jxsggzy.cn"] = ['//div[@class="article-info"]']
Xpaths["hngp.gov.cn"] = ['//body']
Xpaths["hnggzy"] = ['//td[@id="TDContent"]','//div[@id="divArtice"]','//div[@class="row"]/div[2]']
Xpaths["zw.hainan.gov.cn"] = ['//div[@class="newsCon"]']
Xpaths["www.customs.gov.cn"] = ['//div[@align="left"]']
Xpaths["121.28.195.124"] = ['//td[@class="font_black"]','//div']
Xpaths["hntba"] = ['//div[@class="news-xq"]']
Xpaths["zw.hainan.gov"] = ['//div[@class="zx-xxxqy-nr"]','//div[@class="xly"]','//div[@id="Zoom"]']
Xpaths["kfqgw.beijing.gov.cn"] = ['//div[@id="div_zhengwen"]']
Xpaths["ccgp-tianjin"] = ['//div[@class="pageInner"]//table']
Xpaths["prec_sxzwfw"] = ['//div[@class="body_main"]']
Xpaths["nmgp_gov"] = ['//div[@class="content-box-1"]']
Xpaths["ccgp-shanxi"] = ['//tr[@class="bk5"]','.']
Xpaths["ccgp-shandong"] = ['//td[@bgcolor="#FFFFFF"]','//div[@class="listConts"]']
Xpaths["gdgpo.gov"] = ['//div[@id="content"]']
Xpaths["ccgp-jiangsu"] = ['//div[@class="detail_con"]','.']
Xpaths["ccgp-jilin"] = ['//div[@id="xiangqingneiron"]']
Xpaths["hljcg.gov.cn"] = ['//div[@class="xxej"]']
Xpaths["ccgp-hunan"] = ['//html']
Xpaths["ccgp-fujian"] = ['//div[@class="notice-con"]']
Xpaths["ccgp-chongqing"] = ['.']
Xpaths["ccgp-anhui"] = ['.']
Xpaths["ccgp-sichuan"] = ['//div[@id="myPrintArea"]//table','//div[@class="package_lines layoutfix"]','//div[@class="divcss5"]']
Xpaths["ccgp-liaoning"] = ['//div[@id="template"]']
Xpaths["ccgp-guangxi"] = ['.']
Xpaths["ccgp-guizhou"] = ['.']
Xpaths["yngp"] = ['//div[@class="vF_detail_content"]','//div[@class="vF_detail_content_container"]','//div[@class="vT_detail_main"]','//div[@class="vT_detail_content w760c"]']
Xpaths["ccgp-shaanxi"] = ['//div[@class="inner-Box"]','//div[@class="annBox"]','//div[@class="content-inner"]']
Xpaths["ccgp-xinjiang"] = ['.']
Xpaths["ccgp-gansu"] = ['//div[@id="fontzoom"]']
Xpaths["ccgp-ningxia"] = ['//div[@class="vT_detail_content w100c"]','//div[@id="jjDiv"]']
Xpaths["ccgp-xizang"] = ['//div[@class="notice-con"]']
Xpaths["ccgp-qinghai"] = ['.']
Xpaths["cgw_xjbt"] = ['.']
Xpaths["zfcg_qingdao"] = ['//div[@class="cont"]']
Xpaths["nbzfcg"] = ['//div[@class="frame_list01"]/table']
Xpaths["szzfcg"] = ['//div[@id="contentDiv"]','//body//table']
Xpaths["ccgp-dalian"] = ['//table[@id="_Sheet1"]','//table[@id="tblInfo"]']
Xpaths["prec_sxzwfw"] = ['//table[@class="gycq-table"]']
Xpaths["zjzwfw"] = ['//div[@class="con"]','//div[@class="content"]']
Xpaths["hljggzyjyw"] = ['//div[@class="ewb-art-bd"]']
Xpaths["jszwfw"] = ['//div[@class="ewb-trade-right l"]']
Xpaths["lnggzy"] = ['//td[@id="zfcg_zbgs1_TDContent"]','//td[@id="zfcg_zbgg1_TDContent"]']
Xpaths["ggzy_hebei"] = ['//div[@class="ewb-copy"]']
Xpaths["ggzyjy.nmg"] = ['//div[@class="detail_contect"]','//div[@id="noticeArea"]']
Xpaths["ggzy_zwfwb"] = ['//div[@class="content"]//div[@id="content"]']
Xpaths["jl_gov_cn"] = ['//div[@class="ewb-article-info"]']
Xpaths["shggzy"] = ['//div[@class="content"]']
Xpaths["ggzy_ah"] = ['//div[@id="content"]','.']
Xpaths["ggzyfw_fj"] = ['.']
Xpaths["ggzyjy_shandong"] = ['//table[@class="gycq-table"]']
Xpaths["hnsggzyfwpt"] = ['//div[@class="ewb-left-bd"]']
Xpaths["hbggzyfwpt"] = ['.']
Xpaths["hnsggzy"] = ['//div[@class="div-article2"]','//div[@class="div-article"]','//div[@class="content-article"]']
Xpaths["gxggzy"] = ['//div[@class="ewb-details-info"]']
Xpaths["cqggzy"] = ['//div[@id="mainContent"]']
Xpaths["ggzyjy_sc"] = ['//div[@class="clearfix"]']
Xpaths["ggzy_guizhou"] = ['.']
Xpaths["ggzy_yn"] = ['//div[@class="detail_contect"]']
Xpaths["ggzy_xizang"] = ['//div[@class="div-article2"]']
Xpaths["sxggzyjy"] = ['//div[@id="mainContent"]','//div[@class="epoint-article-content jynr news_content"]']
Xpaths["ggzyjy_gansu"] = ['.']
Xpaths["qhggzyjy"] = ['//div[@class="xiangxiyekuang"]']
Xpaths["nxggzyjy"] = ['//div[@id="tab-1"]']
Xpaths["ggzy_xinjiang"] = ['//div[@class="ewb-info-bd"]']
Xpaths["ggzy_xjbt"] = ['//div[@class="infodetail"]']
Xpaths["ccgp-neimenggu-in"] = ['//div[@id="content-box-1"]']
Xpaths["ggzyjy_ordos"] = ['//div[@class="noticeArea"]']




htmltcs = {}


def inithtmltcs():
    htmltcs["&ensp;"] = " "
    htmltcs["&emsp;"] = " "
    htmltcs["&nbsp;"] = " "
    htmltcs["&lt;"] = "<"
    htmltcs["&gt;"] = ">"
    htmltcs["&amp;"] = "&"
    htmltcs["&quot;"] = "\""
    htmltcs["&copy;"] = "©"
    htmltcs["&reg;"] = "®"
    htmltcs["&times;"] = "×"
    htmltcs["&divide;"] = "÷"
    htmltcs["&nbsp;"] = " "
    htmltcs["&iexcl;"] = "¡"
    htmltcs["&cent;"] = "¢"
    htmltcs["&pound;"] = "£"
    htmltcs["&curren;"] = "¤"
    htmltcs["&yen;"] = "¥"
    htmltcs["&brvbar;"] = "¦"
    htmltcs["&sect;"] = "§"
    htmltcs["&uml;"] = "¨"
    htmltcs["&copy;"] = "©"
    htmltcs["&ordf;"] = "ª"
    htmltcs["&laquo;"] = "«"
    htmltcs["&not;"] = "¬"
    htmltcs["&shy;"] = ""
    htmltcs["&reg;"] = "®"
    htmltcs["&macr;"] = "¯"
    htmltcs["&deg;"] = "°"
    htmltcs["&plusmn;"] = "±"
    htmltcs["&sup2;"] = "²"
    htmltcs["&sup3;"] = "³"
    htmltcs["&acute;"] = "´"
    htmltcs["&micro;"] = "µ"
    htmltcs["&para;"] = "¶"
    htmltcs["&middot;"] = "·"
    htmltcs["&cedil;"] = "¸"
    htmltcs["&sup1;"] = "¹"
    htmltcs["&ordm;"] = "º"
    htmltcs["&raquo;"] = "»"
    htmltcs["&frac14;"] = "¼"
    htmltcs["&frac12;"] = "½"
    htmltcs["&frac34;"] = "¾"
    htmltcs["&iquest;"] = "¿"
    htmltcs["&Agrave;"] = "À"
    htmltcs["&Aacute;"] = "Á"
    htmltcs["&Acirc;"] = "Â"
    htmltcs["&Atilde;"] = "Ã"
    htmltcs["&Auml;"] = "Ä"
    htmltcs["&Aring;"] = "Å"
    htmltcs["&AElig;"] = "Æ"
    htmltcs["&Ccedil;"] = "Ç"
    htmltcs["&Egrave;"] = "È"
    htmltcs["&Eacute;"] = "É"
    htmltcs["&Ecirc;"] = "Ê"
    htmltcs["&Euml;"] = "Ë"
    htmltcs["&Igrave;"] = "Ì"
    htmltcs["&Iacute;"] = "Í"
    htmltcs["&Icirc;"] = "Î"
    htmltcs["&Iuml;"] = "Ï"
    htmltcs["&ETH;"] = "Ð"
    htmltcs["&Ntilde;"] = "Ñ"
    htmltcs["&Ograve;"] = "Ò"
    htmltcs["&Oacute;"] = "Ó"
    htmltcs["&Ocirc;"] = "Ô"
    htmltcs["&Otilde;"] = "Õ"
    htmltcs["&Ouml;"] = "Ö"
    htmltcs["&times;"] = "×"
    htmltcs["&Oslash;"] = "Ø"
    htmltcs["&Ugrave;"] = "Ù"
    htmltcs["&Uacute;"] = "Ú"
    htmltcs["&Ucirc;"] = "Û"
    htmltcs["&Uuml;"] = "Ü"
    htmltcs["&Yacute;"] = "Ý"
    htmltcs["&THORN;"] = "Þ"
    htmltcs["&szlig;"] = "ß"
    htmltcs["&agrave;"] = "à"
    htmltcs["&aacute;"] = "á"
    htmltcs["&acirc;"] = "â"
    htmltcs["&atilde;"] = "ã"
    htmltcs["&auml;"] = "ä"
    htmltcs["&aring;"] = "å"
    htmltcs["&aelig;"] = "æ"
    htmltcs["&ccedil;"] = "ç"
    htmltcs["&egrave;"] = "è"
    htmltcs["&eacute;"] = "é"
    htmltcs["&ecirc;"] = "ê"
    htmltcs["&euml;"] = "ë"
    htmltcs["&igrave;"] = "ì"
    htmltcs["&iacute;"] = "í"
    htmltcs["&icirc;"] = "î"
    htmltcs["&iuml;"] = "ï"
    htmltcs["&eth;"] = "ð"
    htmltcs["&ntilde;"] = "ñ"
    htmltcs["&ograve;"] = "ò"
    htmltcs["&oacute;"] = "ó"
    htmltcs["&ocirc;"] = "ô"
    htmltcs["&otilde;"] = "õ"
    htmltcs["&ouml;"] = "ö"
    htmltcs["&divide;"] = "÷"
    htmltcs["&oslash;"] = "ø"
    htmltcs["&ugrave;"] = "ù"
    htmltcs["&uacute;"] = "ú"
    htmltcs["&ucirc;"] = "û"
    htmltcs["&uuml;"] = "ü"
    htmltcs["&yacute;"] = "ý"
    htmltcs["&thorn;"] = "þ"
    htmltcs["&yuml;"] = "ÿ"
    htmltcs["&fnof;"] = "ƒ"
    htmltcs["&Alpha;"] = "Α"
    htmltcs["&Beta;"] = "Β"
    htmltcs["&Gamma;"] = "Γ"
    htmltcs["&Delta;"] = "Δ"
    htmltcs["&Epsilon;"] = "Ε"
    htmltcs["&Zeta;"] = "Ζ"
    htmltcs["&Eta;"] = "Η"
    htmltcs["&Theta;"] = "Θ"
    htmltcs["&Iota;"] = "Ι"
    htmltcs["&Kappa;"] = "Κ"
    htmltcs["&Lambda;"] = "Λ"
    htmltcs["&Mu;"] = "Μ"
    htmltcs["&Nu;"] = "Ν"
    htmltcs["&Xi;"] = "Ξ"
    htmltcs["&Omicron;"] = "Ο"
    htmltcs["&Pi;"] = "Π"
    htmltcs["&Rho;"] = "Ρ"
    htmltcs["&Sigma;"] = "Σ"
    htmltcs["&Tau;"] = "Τ"
    htmltcs["&Upsilon;"] = "Υ"
    htmltcs["&Phi;"] = "Φ"
    htmltcs["&Chi;"] = "Χ"
    htmltcs["&Psi;"] = "Ψ"
    htmltcs["&Omega;"] = "Ω"
    htmltcs["&alpha;"] = "α"
    htmltcs["&beta;"] = "β"
    htmltcs["&gamma;"] = "γ"
    htmltcs["&delta;"] = "δ"
    htmltcs["&epsilon;"] = "ε"
    htmltcs["&zeta;"] = "ζ"
    htmltcs["&eta;"] = "η"
    htmltcs["&theta;"] = "θ"
    htmltcs["&iota;"] = "ι"
    htmltcs["&kappa;"] = "κ"
    htmltcs["&lambda;"] = "λ"
    htmltcs["&mu;"] = "μ"
    htmltcs["&nu;"] = "ν"
    htmltcs["&xi;"] = "ξ"
    htmltcs["&omicron;"] = "ο"
    htmltcs["&pi;"] = "π"
    htmltcs["&rho;"] = "ρ"
    htmltcs["&sigmaf;"] = "ς"
    htmltcs["&sigma;"] = "σ"
    htmltcs["&tau;"] = "τ"
    htmltcs["&upsilon;"] = "υ"
    htmltcs["&phi;"] = "φ"
    htmltcs["&chi;"] = "χ"
    htmltcs["&psi;"] = "ψ"
    htmltcs["&omega;"] = "ω"
    htmltcs["&thetasym;"] = "?"
    htmltcs["&upsih;"] = "?"
    htmltcs["&piv;"] = "?"
    htmltcs["&bull;"] = "•"
    htmltcs["&hellip;"] = "…"
    htmltcs["&prime;"] = "′"
    htmltcs["&Prime;"] = "″"
    htmltcs["&oline;"] = "‾"
    htmltcs["&frasl;"] = "⁄"
    htmltcs["&weierp;"] = "℘"
    htmltcs["&image;"] = "ℑ"
    htmltcs["&real;"] = "ℜ"
    htmltcs["&trade;"] = "™"
    htmltcs["&alefsym;"] = "ℵ"
    htmltcs["&larr;"] = "←"
    htmltcs["&uarr;"] = "↑"
    htmltcs["&rarr;"] = "→"
    htmltcs["&darr;"] = "↓"
    htmltcs["&harr;"] = "↔"
    htmltcs["&crarr;"] = "↵"
    htmltcs["&lArr;"] = "⇐"
    htmltcs["&uArr;"] = "⇑"
    htmltcs["&rArr;"] = "⇒"
    htmltcs["&dArr;"] = "⇓"
    htmltcs["&hArr;"] = "⇔"
    htmltcs["&forall;"] = "∀"
    htmltcs["&part;"] = "∂"
    htmltcs["&exist;"] = "∃"
    htmltcs["&empty;"] = "∅"
    htmltcs["&nabla;"] = "∇"
    htmltcs["&isin;"] = "∈"
    htmltcs["&notin;"] = "∉"
    htmltcs["&ni;"] = "∋"
    htmltcs["&prod;"] = "∏"
    htmltcs["&sum;"] = "∑"
    htmltcs["&minus;"] = "−"
    htmltcs["&lowast;"] = "∗"
    htmltcs["&radic;"] = "√"
    htmltcs["&prop;"] = "∝"
    htmltcs["&infin;"] = "∞"
    htmltcs["&ang;"] = "∠"
    htmltcs["&and;"] = "∧"
    htmltcs["&or;"] = "∨"
    htmltcs["&cap;"] = "∩"
    htmltcs["&cup;"] = "∪"
    htmltcs["&int;"] = "∫"
    htmltcs["&there4;"] = "∴"
    htmltcs["&sim;"] = "∼"
    htmltcs["&cong;"] = "∝"
    htmltcs["&asymp;"] = "≈"
    htmltcs["&ne;"] = "≠"
    htmltcs["&equiv;"] = "≡"
    htmltcs["&le;"] = "≤"
    htmltcs["&ge;"] = "≥"
    htmltcs["&sub;"] = "⊂"
    htmltcs["&sup;"] = "⊃"
    htmltcs["&nsub;"] = "⊄"
    htmltcs["&sube;"] = "⊆"
    htmltcs["&supe;"] = "⊇"
    htmltcs["&oplus;"] = "⊕"
    htmltcs["&otimes;"] = "⊗"
    htmltcs["&perp;"] = "⊥"
    htmltcs["&sdot;"] = "⋅"
    htmltcs["&lceil;"] = "?"
    htmltcs["&rceil;"] = "?"
    htmltcs["&lfloor;"] = "?"
    htmltcs["&rfloor;"] = "?"
    htmltcs["&lang;"] = "?"
    htmltcs["&rang;"] = "?"
    htmltcs["&loz;"] = "◊"
    htmltcs["&spades;"] = "♠"
    htmltcs["&clubs;"] = "♣"
    htmltcs["&hearts;"] = "♥"
    htmltcs["&diams;"] = "♦"
    htmltcs["&quot;"] = "\""
    htmltcs["&amp;"] = "&"
    htmltcs["&lt;"] = "<"
    htmltcs["&gt;"] = ">"
    htmltcs["&OElig;"] = "Œ"
    htmltcs["&oelig;"] = "œ"
    htmltcs["&Scaron;"] = "Š"
    htmltcs["&scaron;"] = "š"
    htmltcs["&Yuml;"] = "Ÿ"
    htmltcs["&circ;"] = "ˆ"
    htmltcs["&tilde;"] = "˜"
    htmltcs["&ensp;"] = " "
    htmltcs["&emsp;"] = " "
    htmltcs["&thinsp;"] = " "
    htmltcs["&zwnj;"] = "‌"
    htmltcs["&zwj;"] = "‍"
    htmltcs["&lrm;"] = "‎"
    htmltcs["&rlm;"] = "‏"
    htmltcs["&ndash;"] = "–"
    htmltcs["&mdash;"] = "—"
    htmltcs["&lsquo;"] = "‘"
    htmltcs["&rsquo;"] = "’"
    htmltcs["&sbquo;"] = "‚"
    htmltcs["&ldquo;"] = "“"
    htmltcs["&rdquo;"] = "”"
    htmltcs["&bdquo;"] = "„"
    htmltcs["&dagger;"] = "†"
    htmltcs["&Dagger;"] = "‡"
    htmltcs["&permil;"] = "‰"
    htmltcs["&lsaquo;"] = "‹"
    htmltcs["&rsaquo;"] = "›"
    htmltcs["&euro;"] = "€"
    htmltcs["&#8194;"] = " "
    htmltcs["&#8195;"] = " "
    htmltcs["&#160;"] = " "
    htmltcs["&#60;"] = "<"
    htmltcs["&#62;"] = ">"
    htmltcs["&#38;"] = "&"
    htmltcs["&#34;"] = "\""
    htmltcs["&#169;"] = "©"
    htmltcs["&#174;"] = "®"
    htmltcs["&#8482;"] = "™"
    htmltcs["&#215;"] = "×"
    htmltcs["&#247;"] = "÷"
    htmltcs["&#160;"] = " "
    htmltcs["&#161;"] = "¡"
    htmltcs["&#162;"] = "¢"
    htmltcs["&#163;"] = "£"
    htmltcs["&#164;"] = "¤"
    htmltcs["&#165;"] = "¥"
    htmltcs["&#166;"] = "¦"
    htmltcs["&#167;"] = "§"
    htmltcs["&#168;"] = "¨"
    htmltcs["&#169;"] = "©"
    htmltcs["&#170;"] = "ª"
    htmltcs["&#171;"] = "«"
    htmltcs["&#172;"] = "¬"
    htmltcs["&#173;"] = ""
    htmltcs["&#174;"] = "®"
    htmltcs["&#175;"] = "¯"
    htmltcs["&#176;"] = "°"
    htmltcs["&#177;"] = "±"
    htmltcs["&#178;"] = "²"
    htmltcs["&#179;"] = "³"
    htmltcs["&#180;"] = "´"
    htmltcs["&#181;"] = "µ"
    htmltcs["&#182;"] = "¶"
    htmltcs["&#183;"] = "·"
    htmltcs["&#184;"] = "¸"
    htmltcs["&#185;"] = "¹"
    htmltcs["&#186;"] = "º"
    htmltcs["&#187;"] = "»"
    htmltcs["&#188;"] = "¼"
    htmltcs["&#189;"] = "½"
    htmltcs["&#190;"] = "¾"
    htmltcs["&#191;"] = "¿"
    htmltcs["&#192;"] = "À"
    htmltcs["&#193;"] = "Á"
    htmltcs["&#194;"] = "Â"
    htmltcs["&#195;"] = "Ã"
    htmltcs["&#196;"] = "Ä"
    htmltcs["&#197;"] = "Å"
    htmltcs["&#198;"] = "Æ"
    htmltcs["&#199;"] = "Ç"
    htmltcs["&#200;"] = "È"
    htmltcs["&#201;"] = "É"
    htmltcs["&#202;"] = "Ê"
    htmltcs["&#203;"] = "Ë"
    htmltcs["&#204;"] = "Ì"
    htmltcs["&#205;"] = "Í"
    htmltcs["&#206;"] = "Î"
    htmltcs["&#207;"] = "Ï"
    htmltcs["&#208;"] = "Ð"
    htmltcs["&#209;"] = "Ñ"
    htmltcs["&#210;"] = "Ò"
    htmltcs["&#211;"] = "Ó"
    htmltcs["&#212;"] = "Ô"
    htmltcs["&#213;"] = "Õ"
    htmltcs["&#214;"] = "Ö"
    htmltcs["&#215;"] = "×"
    htmltcs["&#216;"] = "Ø"
    htmltcs["&#217;"] = "Ù"
    htmltcs["&#218;"] = "Ú"
    htmltcs["&#219;"] = "Û"
    htmltcs["&#220;"] = "Ü"
    htmltcs["&#221;"] = "Ý"
    htmltcs["&#222;"] = "Þ"
    htmltcs["&#223;"] = "ß"
    htmltcs["&#224;"] = "à"
    htmltcs["&#225;"] = "á"
    htmltcs["&#226;"] = "â"
    htmltcs["&#227;"] = "ã"
    htmltcs["&#228;"] = "ä"
    htmltcs["&#229;"] = "å"
    htmltcs["&#230;"] = "æ"
    htmltcs["&#231;"] = "ç"
    htmltcs["&#232;"] = "è"
    htmltcs["&#233;"] = "é"
    htmltcs["&#234;"] = "ê"
    htmltcs["&#235;"] = "ë"
    htmltcs["&#236;"] = "ì"
    htmltcs["&#237;"] = "í"
    htmltcs["&#238;"] = "î"
    htmltcs["&#239;"] = "ï"
    htmltcs["&#240;"] = "ð"
    htmltcs["&#241;"] = "ñ"
    htmltcs["&#242;"] = "ò"
    htmltcs["&#243;"] = "ó"
    htmltcs["&#244;"] = "ô"
    htmltcs["&#245;"] = "õ"
    htmltcs["&#246;"] = "ö"
    htmltcs["&#247;"] = "÷"
    htmltcs["&#248;"] = "ø"
    htmltcs["&#249;"] = "ù"
    htmltcs["&#250;"] = "ú"
    htmltcs["&#251;"] = "û"
    htmltcs["&#252;"] = "ü"
    htmltcs["&#253;"] = "ý"
    htmltcs["&#254;"] = "þ"
    htmltcs["&#255;"] = "ÿ"
    htmltcs["&#402;"] = "ƒ"
    htmltcs["&#913;"] = "Α"
    htmltcs["&#914;"] = "Β"
    htmltcs["&#915;"] = "Γ"
    htmltcs["&#916;"] = "Δ"
    htmltcs["&#917;"] = "Ε"
    htmltcs["&#918;"] = "Ζ"
    htmltcs["&#919;"] = "Η"
    htmltcs["&#920;"] = "Θ"
    htmltcs["&#921;"] = "Ι"
    htmltcs["&#922;"] = "Κ"
    htmltcs["&#923;"] = "Λ"
    htmltcs["&#924;"] = "Μ"
    htmltcs["&#925;"] = "Ν"
    htmltcs["&#926;"] = "Ξ"
    htmltcs["&#927;"] = "Ο"
    htmltcs["&#928;"] = "Π"
    htmltcs["&#929;"] = "Ρ"
    htmltcs["&#931;"] = "Σ"
    htmltcs["&#932;"] = "Τ"
    htmltcs["&#933;"] = "Υ"
    htmltcs["&#934;"] = "Φ"
    htmltcs["&#935;"] = "Χ"
    htmltcs["&#936;"] = "Ψ"
    htmltcs["&#937;"] = "Ω"
    htmltcs["&#945;"] = "α"
    htmltcs["&#946;"] = "β"
    htmltcs["&#947;"] = "γ"
    htmltcs["&#948;"] = "δ"
    htmltcs["&#949;"] = "ε"
    htmltcs["&#950;"] = "ζ"
    htmltcs["&#951;"] = "η"
    htmltcs["&#952;"] = "θ"
    htmltcs["&#953;"] = "ι"
    htmltcs["&#954;"] = "κ"
    htmltcs["&#955;"] = "λ"
    htmltcs["&#956;"] = "μ"
    htmltcs["&#957;"] = "ν"
    htmltcs["&#958;"] = "ξ"
    htmltcs["&#959;"] = "ο"
    htmltcs["&#960;"] = "π"
    htmltcs["&#961;"] = "ρ"
    htmltcs["&#962;"] = "ς"
    htmltcs["&#963;"] = "σ"
    htmltcs["&#964;"] = "τ"
    htmltcs["&#965;"] = "υ"
    htmltcs["&#966;"] = "φ"
    htmltcs["&#967;"] = "χ"
    htmltcs["&#968;"] = "ψ"
    htmltcs["&#969;"] = "ω"
    htmltcs["&#977;"] = "?"
    htmltcs["&#978;"] = "?"
    htmltcs["&#982;"] = "?"
    htmltcs["&#8226;"] = "•"
    htmltcs["&#8230;"] = "…"
    htmltcs["&#8242;"] = "′"
    htmltcs["&#8243;"] = "″"
    htmltcs["&#8254;"] = "‾"
    htmltcs["&#8260;"] = "⁄"
    htmltcs["&#8472;"] = "℘"
    htmltcs["&#8465;"] = "ℑ"
    htmltcs["&#8476;"] = "ℜ"
    htmltcs["&#8482;"] = "™"
    htmltcs["&#8501;"] = "ℵ"
    htmltcs["&#8592;"] = "←"
    htmltcs["&#8593;"] = "↑"
    htmltcs["&#8594;"] = "→"
    htmltcs["&#8595;"] = "↓"
    htmltcs["&#8596;"] = "↔"
    htmltcs["&#8629;"] = "↵"
    htmltcs["&#8656;"] = "⇐"
    htmltcs["&#8657;"] = "⇑"
    htmltcs["&#8658;"] = "⇒"
    htmltcs["&#8659;"] = "⇓"
    htmltcs["&#8660;"] = "⇔"
    htmltcs["&#8704;"] = "∀"
    htmltcs["&#8706;"] = "∂"
    htmltcs["&#8707;"] = "∃"
    htmltcs["&#8709;"] = "∅"
    htmltcs["&#8711;"] = "∇"
    htmltcs["&#8712;"] = "∈"
    htmltcs["&#8713;"] = "∉"
    htmltcs["&#8715;"] = "∋"
    htmltcs["&#8719;"] = "∏"
    htmltcs["&#8721;"] = "∑"
    htmltcs["&#8722;"] = "−"
    htmltcs["&#8727;"] = "∗"
    htmltcs["&#8730;"] = "√"
    htmltcs["&#8733;"] = "∝"
    htmltcs["&#8734;"] = "∞"
    htmltcs["&#8736;"] = "∠"
    htmltcs["&#8743;"] = "∧"
    htmltcs["&#8744;"] = "∨"
    htmltcs["&#8745;"] = "∩"
    htmltcs["&#8746;"] = "∪"
    htmltcs["&#8747;"] = "∫"
    htmltcs["&#8756;"] = "∴"
    htmltcs["&#8764;"] = "∼"
    htmltcs["&#8773;"] = "∝"
    htmltcs["&#8776;"] = "≈"
    htmltcs["&#8800;"] = "≠"
    htmltcs["&#8801;"] = "≡"
    htmltcs["&#8804;"] = "≤"
    htmltcs["&#8805;"] = "≥"
    htmltcs["&#8834;"] = "⊂"
    htmltcs["&#8835;"] = "⊃"
    htmltcs["&#8836;"] = "⊄"
    htmltcs["&#8838;"] = "⊆"
    htmltcs["&#8839;"] = "⊇"
    htmltcs["&#8853;"] = "⊕"
    htmltcs["&#8855;"] = "⊗"
    htmltcs["&#8869;"] = "⊥"
    htmltcs["&#8901;"] = "⋅"
    htmltcs["&#8968;"] = "?"
    htmltcs["&#8969;"] = "?"
    htmltcs["&#8970;"] = "?"
    htmltcs["&#8971;"] = "?"
    htmltcs["&#9001;"] = "?"
    htmltcs["&#9002;"] = "?"
    htmltcs["&#9674;"] = "◊"
    htmltcs["&#9824;"] = "♠"
    htmltcs["&#9827;"] = "♣"
    htmltcs["&#9829;"] = "♥"
    htmltcs["&#9830;"] = "♦"
    htmltcs["&#34;"] = "\""
    htmltcs["&#38;"] = "&"
    htmltcs["&#60;"] = "<"
    htmltcs["&#62;"] = ">"
    htmltcs["&#338;"] = "Œ"
    htmltcs["&#339;"] = "œ"
    htmltcs["&#352;"] = "Š"
    htmltcs["&#353;"] = "š"
    htmltcs["&#376;"] = "Ÿ"
    htmltcs["&#710;"] = "ˆ"
    htmltcs["&#732;"] = "˜"
    htmltcs["&#8194;"] = " "
    htmltcs["&#8195;"] = " "
    htmltcs["&#8201;"] = " "
    htmltcs["&#8204;"] = "‌"
    htmltcs["&#8205;"] = "‍"
    htmltcs["&#8206;"] = "‎"
    htmltcs["&#8207;"] = "‏"
    htmltcs["&#8211;"] = "–"
    htmltcs["&#8212;"] = "—"
    htmltcs["&#8216;"] = "‘"
    htmltcs["&#8217;"] = "’"
    htmltcs["&#8218;"] = "‚"
    htmltcs["&#8220;"] = "“"
    htmltcs["&#8221;"] = "”"
    htmltcs["&#8222;"] = "„"
    htmltcs["&#8224;"] = "†"
    htmltcs["&#8225;"] = "‡"
    htmltcs["&#8240;"] = "‰"
    htmltcs["&#8249;"] = "‹"
    htmltcs["&#8250;"] = "›"
    htmltcs["&#8364;"] = "€"


inithtmltcs()


restr0 = "(?:采购|招标|项目|标书|文件|备案)[^\r\n]{0,6}?(?:代码|编码|编号|批准文号)|(?:采购|招标)[^\r\n]{0,6}?(?:联系人|负责人)|(?:采购|招标)[^\r\n]{0,6}?(?:联系方式|电话)|(?:采购机构|代理)[^\r\n]{0,6}?(?:联系人|负责人)|代理[^\r\n]{0,6}?(?:联系方式|电话)"
restr1 = "中标人班子配备|中标结果公告|行贿犯罪档案|招标文件获取|参加投标企业|项目经理获奖|企业综合实力|质量管理体系|未中标供应商|落标供应商|异议与投诉|中标供应商|质疑和投诉|投标人获奖|招标人公章|投标人信用|投标人惩罚|评标委员会|性能及技术|中标人公告|异议和投诉|招标人确认|负责人获奖|答疑及澄清|文件的递交|文件的获取|文件的异议|其他公示项|竞争性谈判|采购计划号|交付使用期|体外循环量|开户银行|中标企业|(?<![一-龥])采购项目|投标总价|项目经理|项目业主|中标单位|中标金额|中标人名称|标段划分|报价修正|评标办法|生产厂家|生产厂商|厂商|招标公告|项目审批|版权所有|联系处室|中标公示|电子邮件|文件正文|谈判小组|项目总工|中心简介|代理公司|辅助功能|小型工程|中标公告|行政区划|监理人员|营业执照|详细评审|资格审查|行业划分|采购合同|包别划分|工业用地|主营业务|投诉受理|工期要求|项目总监|投标报名|企业获奖|项目技术|采购商品|投标保证|标包划分|初步评审|评标入围|施工合同|招标方式|资料公示|售后服务|合同文本|评分办法|材料设备|比选办法|其他事宜|附件下载|其它工程|补充事宜|结果公示|综合信用|文件递交|中标候选|招标单位|联合主体|项目简介|中标公司|电子函件|供应商|转发率|交货期|成交价|采购人|第一名|安全员|第二名|第三名|第1名|第2名|第3名|第4名|第5名|第6名|第7名|第8名|第9名|经办人|施工员|条款号|品目号|公示期|材料员|质量员|供货期|控制价|质保期|成交人|起始价|建造师|服务期|绿化率|质检员|容积率|预算价|合同包|发包人|工本费|入围价|注册地|资料员|江西省|造价员|第一包|负责人|第二包|标段一|标段二|标段三|标段四|标段五|标段六|标段七|标段八|标段九|一标段|二标段|三标段|四标段|五标段|六标段|七标段|八标段|九标段|职称证|包件号|收款人|新工艺|标书费|开户行|监理员|编制人|第三包|品目[一二三四五六七八九十]+|有效期|申请人|商务分|技术分|工程名|保证金|总投资|代表人|履行期|注册号|下浮率|估算价|身份证|批复号|合格证|代理人|许可证|汇总表|投资额|预留金|服务费|标段数|保证期|成员表|委托书|委托人|监理费|工程师|评审费|监理师|排序人|联合体|管理员|发布人|百分比|招商人|操作员|感光度|供应期|中选价|打印量|单位人|加价率|维护期|折价率|负载量|受托人|予埋件|管护期|工程期|应答人|成活率|候选价|建设期|校准点|磁强计|培训期|分享期|序列号|签订期|管养期|实洋价|机构号|证件号|像素数|管理期|监督人|招标人|询价人|监控点|获奖人|失真度|宣传期|对比度|主持人|监管人|解析度|合同期|百分率|消耗量|纸张数|养护期|分辩率|职称号|起止期|服务点|机构人|谈判人|层站数|维修期|设计人|负荷量|分子量|签发人|合同号|采购包|发生量|截止期|投诉人|报建号|优惠率|代码号|经手人|租用期|公示人|版本号|基准价|供热期|收油率|线程数|调试期|工具包|平均价|均匀度|吞吐量|标志牌|试用期|合作人|注入量|合同段|初审人|准确度|雕立牌|价格|机构位|备案人|制热量|公告期|标本量|供货价|清晰度|供货量|报价率|结算率|授权人|耗电量|分割数|用户数|文件号|杂点率|探测点|确定度|独柱式|浮动率|电阻率|解像度|发包价|参与人|承诺期|时间期|光度计|确认号|样品数|载客数|技术期|端口数|预算额|接收人|灵敏度|金额格|田村段|概算价|完成期|制冷量|标识牌|码洋价|水位计|公示限|暂估额|采购量|佣金率|包组号|采购价|累积量|承储期|连接件|核心数|粗糙度|履约期|照明度|投放期|发热量|保修期|交付期|节资率|编制期|安装期|监测期|交验期|传输率|公证人|控制额|备远人|摔跤人|领取人|双人式|责任期|眼压计|蒸汽量|保质期|到货期|征集人|竞得人|批件号|合同额|竞价人|受理人|分辨率|代理位|核准号|电气件|处理量|刊例价|监理标|碎纸量|稳定度|车辆数|回报率|中标额|记录人|中标期|承载量|监理包|公牛号|储备期|制作人|公式期|责任人|折让率|服务包|牵头人|时间段|施工标|届满期|推荐人|协调人|传真号|电导率|精确度|项目包|执行期|指导价|合作期|实施期|利润率|承租人|维保期|附加分|登记号|撰写人|包干价|乘员数|谈判价|全能型|单位|投资人|租赁期|菌落数|进驻期|两个包|供餐期|收益率|审核人|设计标|专利号|分成率|验收期|波动度|项目名称|运维期|组织人|报价人|成交额|工程量|基本型|见证人|承包人|总价计|通道数|组建期|监理期|收据价|受理号|代建人|折扣率|计费额|折扣价|配置数|键盘数|节约率|合同价|平整度|设计期|法律|权重|分值|货物(?![一-龥])|剂量|序号|地址|标段|备注|工期|账号|户名|包号|电话|其他|附件|传真|项号|品目|评委|性别|年龄|身高|体重|数量|产地|名次|合计|专家|编号|排序|标项|职务|业绩|分标|排名|总分|名称|质量|姓名|日期|网址|面积|包名|邮编|小写|小计|地点|岗位|分包|法人|标号|得分|单价|组员|结构|大写|时间|总价|子包|包组|说明|品牌|售价|比例|组长|类型|证号|资质|证书|金额|等级|原因|意见|须知|区域|名单|条件|号码|成员|方式|个数|范围|规模|内容|规格|全称|理由|要求|位置|数额|编码|额度|措施|指标|情况|事项|代码|费用|方法|标准|资格|人员|媒体|限价|概述|明细|费率|信息(?!中心)|资料|机构|签字|附录|造价|媒介|对象|清单|计划|评分|来源|地域|类别|预算|行业|概况|总额|因素|年限|深度|周期|性质|学历|承诺|简称|代表|参数|部门|结果|单位|型号|证件|地区|邮箱|期限|跨度|高度|层数|信箱|收入|总数|描述|价格|材料|用途|时限|报价|系数|细则|账户|标题|提示|强度|标识|程度|家数|依据|声明|甲方|联系|优惠|乙方|是否|文件|下浮法定|发布|备案|中标|折扣|标书|代理|包段|盖章|签章|全价|份额|营期|外型|视点|定位|苗期|号数|节点|件数|位数|程式|国标|厂址|列数|剂型|速度|漏率|评标|定标|页数|共计|格式|形式|优点|分数|界限|状况|次数|能量|发牌|住址|模型|点数|键数|倍率|天数|开标|进度|时点|集数|制式|目标|合价|供期|产型|频段|位址|排数|针数|公期|产量|功率|样式|票价|硬度|民称|气量|牌位|大号|标人|背包|底价|审计|投标|造型|第包|匹数|餐标|指数|炉型|标包|角度|尺寸|特点|部位|厚度|年度|幅度|箱包|汇率|硬件|部件|船期|构件|盐度|来价|上量|折率|地段|精度|套数|期数|排量|路段|小号|册数|幅数|宽度|路数|保额|成分|行号|转数|照度|水量|文号|频率|总计|赔额|总量|估价|定价|空间|定点|摊点|限期|通量|黑度|期间|塔式|需求|化分|扩容|返点|配件|流量|书号|号牌|包件|尺度|商标|型式|称量|时段|时期|时量|风量|系人|速率|设计|部分|含量|站牌|路牌|级数|亮度|基数|支数|字号|税号|温度|移位|职称|卡号|位率|标价|阶段|限额|缸数|重量|稿件|份数|吨价|轴位|机型|统计|包数|如期|测量|标牌|工况|组件|元件|印数|饭量|帐号|报标|湿度|容量|组分|计价|信号|燃点|娄量|比率|倍数|门数|拨号|利率|灰度|运费|吊装费|项数|芯数|函号|效率|频点|粒度|竞价(?![一-龥])|相数|长度|核数|密度|批号|评价|浮点|浓度|车型|桩号|段号|人数|岁数|烈度|车位|盘式|模式|频度|器件|秤量|款式|选人|上限|线数|租期|种类|种族|民族|姓氏|体积|容积|面积|直径|半径|外径|内径|口径|颜色|分类|额定|级别|院校|工作经历|链接|用户名|密码|登录名|机器码|驻地|驻所|建议|职能|职位|职业|技能|热度|力矩|扭矩|转矩|压力|电压|电流|电阻|水压|品种|类目|品类|压强|压缩比|压缩率|变量|增量|中标价|中标商|标段名|负责人|包"
restr2 = "(?:" + restr0 + "|" + restr1 + ")(?![一-龥])"
restr = "[一-龥]{0,8}?(?:" + restr2 + "(?!$))+|^是否.*?$"
restr3 = "(?<![省市县].*)(?:" + restr2 + ")|^是否.*?$"
restr4 = "[一-龥]{0,4}?" + "(?:" + restr0 + "|" + restr1 + ")" + "+$|^是否.*?$"


CONTINUITYWORDS = ["编码", "代码", "编号", "项目名称", "采购", "招标", "项目", "招标公告", "中标公告", "废标公告", "竞争性谈判", "合同公告", "预算", "预算金额", "采购预算金额", "采购人名称", "采购单位", "采购单位名称", "单位名称", "招标单位", "成交人", "招标人名称", "招标人", "采购人", "甲方", "采购人(甲方)", "采购人联系方式", "采购单位", "采购人地址", "联系人", "负责人", "采购单位地址", "采购人单位地址", "招标人地址", "招标单位地址", "招标人单位地址", "代理机构", "采购机构", "招标代理", "代理机构地址", "代理单位地址", "采购机构地址", "代理机构单位地址", "联系方式", "电话"]
CONTINUITYWORDS.extend(["第五包", "第5包", "E包", "v包", "第四包", "第4包", "D包", "iv包", "第三包", "第3包", "C包", "iii包", "第二包", "第2包", "B包", "ii包", "第一包", "第1包", "A包", "i包"])
CONTINUITYWORDS.extend(["第五标段", "第5标段", "E标段", "v标段", "第四标段", "第4标段", "D标段", "iv标段", "第三标段", "第3标段", "C标段", "iii标段", "第二标段", "第2标段", "B标段", "ii标段", "第一标段", "第1标段", "A标段", "i标段"])
CONTINUITYWORDS.extend(["中标金额", "联系地址", "招商人", "地址", "代理人", "采购代理", "招标代理", "单价", "招标方", "比选人", "中标价", "投标价", "中标金额"])




re.DEFAULT_VERSION = re.V1





def findfirst(restr, txt, parm = re.I | re.S):
    fda = re.findall(restr, txt, parm)
    rtnv = (fda or [""])[0]
    return rtnv


def ForJson(jsonstr, website):
    content = jsonstr
    if website == "forbakup":
        try:
            jo = json.loads(content, strict = False)
            rtnv = str(jo)
            return rtnv
        except:
            content = findfirst('"Content"\s*:\s*"(.*?)(?:","|"\s*})', content, re.I | re.S)
            content = re.sub("\\\\([\"'])", "\\1", content)
            content = re.sub("\\\\[trnfv]", "", content)
            if content == "": return jsonstr
            return content
    elif website == "api.jszbtb.com":
        try:
            jo = json.loads(content, strict = False)
            rtnv = str(jo["data"]["bulletincontent"])
            return rtnv
        except:
            content = findfirst('"bulletincontent"\s*:\s*"(.*?)(?:","|"\s*})', content, re.I | re.S)
            content = re.sub("\\\\([\"'])", "\\1", content)
            content = re.sub("\\\\[trnfv]", "", content)
            if content == "": return jsonstr
            return content
    elif website == "ggzyjy.gansu.gov.cn":
        try:
            jo = json.loads(content, strict = False)
            rtnv = str(jo["custom"]["gonggaocontent"])
            return rtnv
        except:
            content = findfirst('"gonggaocontent"\s*:\s*"(.*?)(?:","|"\s*})', content, re.I | re.S)
            content = re.sub("\\\\([\"'])", "\\1", content)
            content = re.sub("\\\\[trnfv]", "", content)
            if content == "": return jsonstr
            return content
    elif website == "manager.zjzfcg.gov.cn":
        try:
            jo = json.loads(content, strict = False)
            rtnv = str(jo["noticeContent"])
            return rtnv
        except:
            content = findfirst('"noticeContent"\s*:\s*"(.*?)(?:","|"\s*})', content, re.I | re.S)
            content = re.sub("\\\\([\"'])", "\\1", content)
            content = re.sub("\\\\[trnfv]", "", content)
            if content == "": return jsonstr
            return content
    elif website == "www.ccgp-hunan.gov.cn":
        rtnv = re.sub('^{"msg":"[^a-z0-9一-龥]*?"}', "", content, 0, re.I | re.S)
        return rtnv
    elif website == "www.cqgp.gov.cn":
        try:
            jo = json.loads(content, strict = False)
            rtnv = str(jo["notice"]["html"])
            return rtnv
        except:
            content = findfirst('"html"\s*:\s*"(.*?)(?:","|"\s*})', content, re.I | re.S)
            content = re.sub("\\\\([\"'])", "\\1", content)
            content = re.sub("\\\\[trnfv]", "", content)
            if content == "": return jsonstr
            return content
    elif website == "www.fjggfw.gov.cn":
        try:
            jo = json.loads(content, strict = False)
            rtnv = str("".join(jo["data"]))
            return rtnv
        except:
            content = findfirst('"data"\s*:\s*\\[\s*"(.*?)(?:"\\],"|"\s*]\s*})', content, re.I | re.S)
            content = content.replace("\",\"", "")
            content = re.sub("\\\\([\"'])", "\\1", content)
            content = re.sub("\\\\[trnfv]", "", content)
            if content == "": return jsonstr
            return content
    elif website == "www.gzsztb.gov.cn":
        try:
            jo = json.loads(content, strict = False)
            rtnv = str(jo["Content"])
            return rtnv
        except:
            content = findfirst('"Content"\s*:\s*"(.*?)(?:","|"\s*})', content, re.I | re.S)
            content = re.sub("\\\\([\"'])", "\\1", content)
            content = re.sub("\\\\[trnfv]", "", content)
            if content == "": return jsonstr
            return content
    return jsonstr