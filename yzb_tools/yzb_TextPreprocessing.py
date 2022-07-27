# encoding:utf8
import sys
import regex as re
from yzb_EX_Text import *
from lxml.html.clean import Cleaner
from bs4 import BeautifulSoup
from lxml import etree
import html as htmlpkg
import traceback
from copy import copy, deepcopy

# Html预处理
def SPL_Preprocessing(DLSM_UUID='111', content='', website=''):
    # DLSM_UUID_G.set(DLSM_UUID)
    # 预处理开始
    content = content or ""

    # 所有内容都转换为小写
    # content = content.lower()

    # head标签中仅保留title
    content = CleanHead(content)
    # 去除样式

    content = re.sub("<style[\s\S]*?</style>", "", content, re.I | re.S)
    # print(content, 'content')
    # 为了保存用于显示的文本
    content = GetDisplayContent(content, website)
    # print(content,'content1')



    # print('222222222222222')
    # 修复html结构
    content = re.sub("[a-z0-9/+]{100,}=*", "", content, 0, re.I | re.S)
    content = re.sub("(<=^.{500,})<html [^>]*?>|</html>(?=.{500,}$)|<!doctype[^>]*?>|<img [^>]*?>|<image [^>]*?>", "", content, re.I | re.S)
    content = re.sub("""<([a-z0-9]+) [^>]*?style=['"\s]+display[:\s]+none[^>]*?>[^<>]+?</\\1>""", "", content, re.I | re.S)

    # print(content,'content')
    content = RepairHtml(content)

    # 剔除span标签,剔除注释,剔除脚本
    content = re.sub("<input [^>]*? value=\"([^>]*?)\"[^>]*?>", "\\1", content, 0, re.I | re.S)
    content = ConvertPreLable(content)
    content = re.sub("\s*<span[^<>]*?>\s*|\s*</span>\s*|\s*<!--.*?-->\s*|\s*<script .*?</script>\s*", "", content, 0, re.I | re.S)

    # 剔除带链接的锚
    content = DelTags_ByFeatures(content, ["a"], ["href"], [], [], [], ["公司", "设计院", "研究院"])
    # WORDCOUNT = len(re.sub("[^一-龥]", "", display_content))

    # 剔除可能影响提取结果的内容
    content = re.sub("各合同包报价情况.*?各合同包成交供应商如下", "", content, 0, re.I | re.S)  # www.ggzy.gov.cn 此站中所有数据都是大表格形式的.


    # tablein = False
    # =========================如果含有表格,表格作转置处理=======================[*****]
    if "<table " in content or "<table>" in content:
        # tablein = True
        tmp = content
        # print(tmp,'tmp')
        content = htc_old(tmp, 1, DLSM_UUID)
        if len(content) == len(tmp):  # 表格行数太多,程序放弃处理
            print("表格行数太多,程序放弃处理.")
            # DLSM_UUID_G.processexit("表格行数太多,程序放弃处理.")
    # 剔除无分隔或换行作用的标签(仅剔除标签本身,不删除内容) 该方法于20181007加入,标签暂定这些,具体情况再删减
    # print(content,'content')


    corexml = DelTags_self(content, ["abbr", "acronym", "address", "applet", "area", "article", "aside", "audio", "b", "base", "basefont", "bdi", "bdo", "big", "blockquote", "button", "canvas", "caption", "center", "cite", "code", "col", "colgroup", "command", "datalist", "dd", "del", "details", "dfn", "dialog", "dir", "dl", "dt", "em", "embed", "fieldset", "figcaption", "figure", "font", "footer", "frame", "frameset", "header", "i", "iframe", "img", "input", "ins", "kbd", "keygen", "label", "legend", "link", "main", "map", "mark", "menuitem", "meta", "meter", "nav", "noframes", "noscript", "object", "optgroup", "option", "output", "param", "progress", "q", "rp", "rt", "ruby", "s", "samp", "script", "section", "select", "small", "source", "span", "strike", "strong", "style", "sub", "summary", "sup", "textarea", "tfoot", "time", "track", "tt", "var", "video", "wbr"], True)
    corexml = re.sub("<u>(.*?)</u>", " \\1 ", corexml, 0, re.I | re.S)  # <u>标签内部一般是value数据,把u标签替换成空格,防止value与后面的key拼接在一起
    # 剔除多余的空格
    # print(corexml,'corexml')
    # corexml = KillUnusefulSpace(CONTINUITYWORDS, corexml)
    corexml = HtmlKillTrans(corexml)
    corexml = det(corexml)
    # print(content, 'content')

    # 包号范围识别和转换,例如:"包A到包C" -> "包A 包B 包C"  例如: "标段一至四" -> "标段一 标段二 标段三 标段四"
    corexml = FillPkgNumber_Area(corexml, True)

    # 识别描述性的包号(枚举) 例如:"第一、三、五包" -> "包一 包三 包五"
    corexml = FillPkgNumber_Enum(corexml, True)

    # 调整包号 "一包" -> "包一"  "2包" -> "包2"  "3{_}包" -> "包3"
    corexml = re.sub("[（(]?(?<!(?:[A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-][.、]?)(?=[A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-]))((?:[A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-]|(?:质量检测|造价管理|施工|监理|设计|采购)(?!项目)){1,5})[）)]? *(?:[{]_[}])? *(项目包|标段|(?<![0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ][）)]?)项目|标项|分包|分标|标包|包件|(?:合同)?(?<!承)包|标(?![一-龥])|(?<![招投中废流])(?<=(?:质量检测|造价管理|施工|监理|设计|采购|采购).{0,3})标(?![段包][A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]))", "\\2\\1", corexml, 0, re.I | re.S)
    corexml = re.sub("(项目包|标段号|标段|标项|项目|分包|分标|标包|包号|包件|序号|(?:合同)?(?<!承)包|(?<![招投中废流])(?<=(?:质量检测|造价管理|施工|监理|设计|采购).{0,3})标(?![段包][A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ])) *(?:[{]_[}])? *[（(]?((?:[A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-](?!次)|质量检测|造价管理|施工|监理|设计|采购){1,5}(?!(?:[A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-]|质量检测|造价管理|施工|监理|设计|采购)))[）)]?", "\\1\\2{_}", corexml, 0, re.I | re.S)
    # print(corexml, 'corexml')
    # 获取项目简介
    # Introduction = GetIntroduction(content)
    # print(display_content)
    # print(corexml)

    return corexml


# 把所有内容都切分成行
def SPL_SplitToLines(corexml, tablein):
    lines = hstl(corexml)
    lines = DelUnrelatedLines(lines)
    lines = [(re.sub("(?<=(?<![0-9])[0-9]{3})，(?=[0-9]{3}(?![0-9]))", ",", line) if SomeWordsIn(["元", "金额", "价", "万"], line) else line) for line in lines]
    lines = ConcatKonlyV(lines)  # 20180907加入 0919最后修改
    if not tablein:
        if len(lines) > 600:  # 如果总行数超过600行,则取前300行和后300行
            lines = [line for i, line in enumerate(lines) if i < 300 or i > len(lines) - 300]
    projnumb_lines = deepcopy(lines)
    for i, line in enumerate(lines):
        lines[i] = re.sub("({_}|[ ])+", "\\1", line)
        # 剔除无用空格
        lines[i] = KillUnusefulSpace(CONTINUITYWORDS, lines[i])
        # 剔除中文括号
        lines[i] = re.sub("【|】", "", lines[i])
    for i, line in enumerate(projnumb_lines):
        # 剔除数字附近的空格
        projnumb_lines[i] = re.sub("(?<=[0-9])\s|\s(?=[0-9])", "", projnumb_lines[i])
    return lines, projnumb_lines


def ConcatKonlyV(Lines):  # lines中,如果某一行为
    newLines = []
    LastType = ""
    for i, line in enumerate(Lines):
        if i == 0:
            newLines.append(line)
            continue
        ThisType = CheckKV(line)  # 待定
        if LastType == "Konly" and ThisType == "Vonly" and NoWordIn(["tbl_start_tag", "tbl_end_tag", "{^^^}"], line):
            newLines[-1] += " " + line
            LastType = "KandV"
        else:
            newLines.append(line)
            LastType = ThisType
    return newLines


def CheckKV(longstr):
    if SomeWordsIn(["{^^^}", "tbl_start_tag", "tbl_end_tag"], longstr): return ""
    lstr = re.sub("<[^>]*?>", "", longstr)  # 剔除标签
    lstr = re.sub("^\s+|\s+$", "", lstr)  # 剔除两端空格
    lstr_m = re.sub("[(（].*?[）)]", "", lstr, 0, re.I | re.S)  # 剔除括号内容
    # tmp = re.sub("{^^^}", "保留越行", lstr_m)
    # tmp = re.sub("{_}", "保留越格", tmp)
    # tmp = re.sub("tbl_start_tag", "保留入表", tmp)
    # tmp = re.sub("tbl_end_tag", "保留出表", tmp)
    # tmp = re.sub("[^一-龥0-9a-zA-Z]", "", tmp, 0, re.I | re.S)  # 剔除无效文字
    # tmp = re.sub("保留越行", "{^^^}", tmp)
    # tmp = re.sub("保留越格", "{_}", tmp)
    # tmp = re.sub("保留入表", "tbl_start_tag", tmp)
    # tmp = re.sub("保留出表", "tbl_end_tag", tmp)
    lstr_w = re.sub("[^一-龥0-9a-zA-Z]", "", lstr_m, 0, re.I | re.S)  # 剔除无效文字
    # 判断是否是Konly
    if longstr == "": return ""
    if SomeWordEndof([":", "："], lstr_m) and len(lstr_m) < 10:
        return "Konly"
    if SomeWordsIn([":", "："], lstr_m):
        return ""
    if re.search(restr4, lstr_w, re.I | re.S):
        return "Konly"
    elif not re.search(restr3, lstr_w, re.I | re.S):
        return "Vonly"
    return ""


# 剔除不相关的行
def DelUnrelatedLines(Lines):
    ses = []
    istart = None
    iend = None
    NN = "abckefghijklmnopqrstuvwxyz"
    for i, line in enumerate(Lines):
        LINENBR = FindFirst("^(?:\s|{_})*([0-9](?:[0-9.]+[0-9])?|[一二三四五六七八九十]+)(?![0-9一二三四五六七八九十])", line)
        if LINENBR == "": continue
        if LINENBR == NN:
            iend = i
            ses.append([istart, iend])
            istart = None
            iend = None
            NN = "abckefghijklmnopqrstuvwxyz"
        if istart is None and len(re.findall("[一-龥]", line)) < 20 and SomeWordsIn(["业绩", "项目管理人员&情况", "项目经理&情况"], line):
            istart = i
            NN = NextNumber(LINENBR)
    NewLines = copy(Lines)
    for i in range(len(NewLines) - 1, -1, -1):
        for j in range(len(ses) - 1, -1, -1):
            istart, iend = ses[j][0], ses[j][1]
            if i >= istart and i < iend:
                NewLines.pop(i)
                break
    return NewLines


def NextNumber(numbtext):
    rs = FindFirst("^(.*?)([1-9][0-9]*$|[一二三四五六七八九十]+$)", numbtext)
    txt = rs[0]
    numb = rs[1]
    l = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50", "51", "52", "53", "54", "55", "56", "57", "58", "59", "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "96", "97", "98", "99", "100", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", "二十一", "二十二", "二十三", "二十四", "二十五", "二十六", "二十七", "二十八", "二十九", "三十", "三十一", "三十二", "三十三", "三十四", "三十五", "三十六", "三十七", "三十八", "三十九", "四十", "四十一", "四十二", "四十三", "四十四", "四十五", "四十六", "四十七", "四十八", "四十九", "五十", "五十一", "五十二", "五十三", "五十四", "五十五", "五十六", "五十七", "五十八", "五十九", "六十", "六十一", "六十二",
         "六十三", "六十四", "六十五", "六十六", "六十七", "六十八", "六十九", "七十", "七十一", "七十二", "七十三", "七十四", "七十五", "七十六", "七十七", "七十八", "七十九", "八十", "八十一", "八十二", "八十三", "八十四", "八十五", "八十六", "八十七", "八十八", "八十九", "九十", "九十一", "九十二", "九十三", "九十四", "九十五", "九十六", "九十七", "九十八", "九十九", "一百", "一百零一", "一百零二", "一百零三", "一百零四", "一百零五", "一百零六", "一百零七", "一百零八", "一百零九"]
    if numb in l:
        nextnumb = l[l.index(numb) + 1]
    else:
        nextnumb = ""
    return txt + nextnumb


def FindFirst(restr, txt, parm = re.I | re.S):
    fda = re.findall(restr, txt, parm)
    groupcount = len(re.findall("(?<!\[[^\]]*?)[(](?![?])", restr))
    if groupcount < 2:  # 无分组或只有一个分组,返回字符串
        return (fda or [""])[0]
    elif len(fda) > 0:  # 两个及以上分组,返回第一组结果
        return fda[0]
    else:  # 匹配失败的,根据分组数量的空字符串
        return [""] * groupcount  # [""]*5 : ["","","","",""]


def hstl(html):
    try:
        if "<pre>" in html and "</pre>" in html:
            html = re.sub("(?<=<pre>(?:(?!<pre>|</pre>).)*?)\n(?=(?:(?!<pre>|</pre>).)*?</pre>)", "\n<br>", html, 0, re.I | re.S)
        SplitTags = ["<p[^>]*?>", "<br/?>", "<br(?: [^>]*?)?>", "<tr[^>]*?>", "<ul[^>]*?>", "<ol[^>]*?>", "<li[^>]*?>", "<h1[^>]*?>", "<h2[^>]*?>", "<h3[^>]*?>", "<h4[^>]*?>", "<h5[^>]*?>", "<h6[^>]*?>", "<table[^>]*?>", "<menu[^>]*?>", "<hr[^>]*?>", "<form[^>]*?>", "<div[^>]*?>", "<table[^>]*?>"]
        SplitTags2 = ["</p>", "</tr>", "</ul>", "</ol>", "</li>", "</h1>", "</h2>", "</h3>", "</h4>", "</h5>", "</h6>", "</table>", "</menu>", "</hr>", "</form>", "</div>", "</table>"]
        html = re.sub("\s", " ", html)  # 剔除回车,全部成一行
        html = re.sub("(?<!<td[^<]*?)(?=" + "|".join(SplitTags) + ")", "{^}", html, 0, re.I | re.S)  # &&&_For_Split_&&& 仅作为分隔符
        html = re.sub("(?<=" + "|".join(SplitTags2) + ")(?![^<>]*?</td>)", "{^}", html, 0, re.I | re.S)  # &&&_For_Split_&&& 仅作为分隔符
        html = re.sub("(?=<td[^>]*?>)", "{_}", html)  # 后面是<td>的位置作为cellfirst
        html = re.sub("\s+", " ", html)  # del space \t\r\n\f\v 全角空格[　]
        html = re.sub("(?<=<td(?:(?!<td|</td>).)*?)[ ](?=(?:(?!<td|</td>).)*?</td>)", "", html, 0, re.I | re.S)
        html = re.sub("\s*<[^<>]*?>\s*", "", html)  # del tags
        Lines = html.split("{^}")  # {^} 仅作为分隔符
        for i in range(len(Lines) - 1, -1, -1):
            if re.search("^(?:[ ]|{_})+$", Lines[i]):
                del Lines[i]
        return Lines
    except Exception as e:
        print(sys._getframe().f_code.co_name, e)
        return []


# 识别描述性的包号(枚举) 例如:"第一、三、五包" -> "包一 包三 包五"
def FillPkgNumber_Enum(longstr = "", rtn_replaced_str = True):  # 仅限2017版的regex模块
    restr = """
    (第?
    (?P<TYPE>标段号|标段|标项|分包|分项|分标号?|品目|标包|包组号|包组|包号|包件|(?<!承)包)?
    ((?:\s*[A-Za-z0-9一二三四五六七八九十廿]+\s*[ 　,、]*)+)\s*
    (?(TYPE)(?<=.)|(?P<TYPE>标段号|标段|标项|分包|分项|分标号?|品目|标包|包组号|包组|包号|包件|(?<!承)包)))
    """
    rs = re.findall(restr, longstr, re.I | re.S)
    # print('111111111111')
    if len(rs) == 0: return longstr
    # print('222222222222')
    newlongstr = longstr
    rs = list(rs)
    rs.sort(key = lambda x: len(x[0]), reverse = True)
    # print('3333333333333')

    for r in rs:
        subcon = r[0]
        T = r[1]
        nbrs = re.findall("[a-z0-9一二三四五六七八九十廿]+", r[2], re.I | re.S)
        newstr = " ".join([T + nbr for nbr in nbrs])

        if rtn_replaced_str:
            newlongstr = newlongstr.replace(subcon, newstr)
    if rtn_replaced_str:
        return newlongstr
    return rs


# 识别描述性的包号(范围) 例如:"包A到包C" -> "包A 包B 包C"  例如: "标段一至四" -> "标段一 标段二 标段三 标段四"
def FillPkgNumber_Area(longstr = "", rtn_replaced_str = True):
    PKGTNS_LL = __FindTypePkgTypeAndNumbers(longstr)
    rtnv = []
    for NTN in PKGTNS_LL:
        subcon, startnumber_str, type_str, endnumber_str = NTN
        startnumber_str_left, startnumber_str_right = findfirst("^(.*?)([a-z]+|[0-9]+|[一二三四五六七八九十]+)$", startnumber_str)
        endnumber_str_left, endnumber_str_right = findfirst("^(.*?)([a-z]+|[0-9]+|[一二三四五六七八九十]+)$", endnumber_str)
        if startnumber_str_left != endnumber_str_left: continue
        numb_list = __FillNumber(startnumber_str_right, endnumber_str_right)
        if numb_list == []: continue
        newlongstr = " ".join([(type_str + startnumber_str_left + str(nb)) for nb in numb_list])
        rtnv.append([subcon, newlongstr])
    if rtn_replaced_str:
        newlongstr = longstr
        for l in rtnv:
            newlongstr = newlongstr.replace(l[0], l[1])
        return newlongstr
    return rtnv


def __rep(num = ""):
    if num == "": num = "0"
    num = re.sub("一|壹", "1", num)
    num = re.sub("二|贰|两", "2", num)
    num = re.sub("三|参|叁|叄", "3", num)
    num = re.sub("四|肆", "4", num)
    num = re.sub("五|伍", "5", num)
    num = re.sub("六|陆", "6", num)
    num = re.sub("七|柒", "7", num)
    num = re.sub("八|捌", "8", num)
    num = re.sub("九|玖", "9", num)
    num = re.sub("零|〇", "0", num)
    return int(num, 10)


def __convert_to_number_sec(NUMBER):
    nbr = findfirst("(?:(?:[一二两三四五六七八九壹贰参叁叄肆伍陆柒捌玖][千仟])?(?:[一二两三四五六七八九壹贰参叁叄肆伍陆柒捌玖][百佰])?(?:[一二两三四五六七八九壹贰参叁叄肆伍陆柒捌玖]?[十拾])?(?:[一二两三四五六七八九壹贰参叁叄肆伍陆柒捌玖])?)+", re.sub("零|〇", "", NUMBER))
    all_numbers = re.findall("(?:([一二两三四五六七八九壹贰参叁叄肆伍陆柒捌玖])(千|仟))?(?:([一二两三四五六七八九壹贰参叁叄肆伍陆柒捌玖])(百|佰))?(?:([一二两三四五六七八九壹贰参叁叄肆伍陆柒捌玖]?)(十|拾))?(?:([一二两三四五六七八九壹贰参叁叄肆伍陆柒捌玖])?)", nbr.replace("零", ""))
    if len(all_numbers) == 0: return ""
    numbers = list(all_numbers[0])
    rtnv_number_alb = 0
    rtnv_number_alb += __rep(numbers[0]) * 1000 + __rep(numbers[2]) * 100 + __rep(numbers[4]) * 10 + __rep(numbers[6])
    if (numbers[5] == "十" or numbers[5] == "拾") and numbers[4] == "": rtnv_number_alb += 10  # 十前面可以不是数字,比如"十万"
    return rtnv_number_alb


def ConvertToNumber(NUMBER):  # NUMBER 比如:三千五百二十     一万零八百
    try:
        NUMBER = NUMBER.replace("廿", "二十")
        NUMBER = NUMBER.replace("卅", "三十")
        NUMBER = NUMBER.replace("卌", "四十")
        nbr = re.sub("[.]+(?=$)", "", NUMBER)  # 预处理,剔除多余小数点
        nbr = re.sub("(?<=[0-9])[.](?=[0-9]*?[.](?!$))", "", nbr)  # 预处理,剔除多余小数点
        nbr = re.sub("[ ,，'＇]", "", nbr)  # 预处理,剔除多余点号空格或分隔号
        if findfirst("^[0-9.]+$", nbr) != "": return float(nbr)  # 如果全是数字
        if findfirst("^[0-9.]+[亿万仟千佰百拾]$", nbr) != "":  # 如果是数字和单位 如:7.71768亿
            je = findfirst("^[0-9.]+", nbr)
            dw = findfirst("[亿万仟千佰百拾十]{1,2}$", nbr)
            je_f = float(je)
            if dw in "亿":
                je_f = je_f * 10000 * 10000
            elif dw in "万":
                je_f = je_f * 10000
            elif dw in "仟千":
                je_f = je_f * 1000
            elif dw in "佰百":
                je_f = je_f * 100
            elif dw in "拾十":
                je_f = je_f * 10
            return je_f
        if findfirst("[0-9.]+", nbr) != "": return 0  # 如果不全是数字
        secs = findfirst("^(?:(.*?)亿)?(?:(.*?)万)?(?:(.*?)[点元圆块]?)?$", nbr, re.I | re.S)
        sec_yw = __convert_to_number_sec(secs[0])  # 亿位
        sec_ww = __convert_to_number_sec(secs[1])  # 万位
        sec_gw = __convert_to_number_sec(secs[2])  # 个位

        sec_yw = int(sec_yw) * 100000000  # 亿位
        sec_ww = int(sec_ww) * 10000  # 万位

        return sec_yw + sec_ww + sec_gw  # + sec_xsw
    except:
        print("error", nbr)
        return 0


def __FillNumber(numb1, numb2):
    try:
        if numb1[0] in "0123456789" and numb2[0] in "0123456789":
            numb1, numb2 = ConvertToNumber(numb1), ConvertToNumber(numb2)
            numb1, numb2 = int(numb1), int(numb2)
            numblist = []
            numblist.append([])
            numb_min, numb_max = (numb1, numb2) if numb1 <= numb2 else (numb2, numb1)
            rtnv = [n for n in range(numb_min, numb_max + 1)]
            return rtnv
        elif numb1[0] in "一二三四五六七八九十" and numb2[0] in "一二三四五六七八九十":
            l = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十", "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十", "二十一", "二十二", "二十三", "二十四", "二十五", "二十六", "二十七", "二十八", "二十九", "三十", "三十一", "三十二", "三十三", "三十四", "三十五", "三十六", "三十七", "三十八", "三十九", "四十", "四十一", "四十二", "四十三", "四十四", "四十五", "四十六", "四十七", "四十八", "四十九", "五十", "五十一", "五十二", "五十三", "五十四", "五十五", "五十六", "五十七", "五十八", "五十九", "六十", "六十一", "六十二", "六十三", "六十四", "六十五", "六十六", "六十七", "六十八", "六十九", "七十", "七十一", "七十二", "七十三", "七十四", "七十五", "七十六", "七十七", "七十八", "七十九", "八十", "八十一", "八十二", "八十三", "八十四", "八十五", "八十六", "八十七", "八十八", "八十九", "九十", "九十一", "九十二", "九十三", "九十四", "九十五", "九十六", "九十七", "九十八", "九十九", "一百", "一百零一", "一百零二", "一百零三", "一百零四", "一百零五", "一百零六", "一百零七", "一百零八", "一百零九"]
            numb1_index, numb2_index = l.index(numb1), l.index(numb2)
            return list(l[numb1_index:numb2_index + 1])
        elif numb1[0] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" and numb2[0] in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ":
            l = "abcdefghijklmnopqrstuvwxyz"
            numb1, numb2 = numb1.lower(), numb2.lower()
            numb1_index, numb2_index = l.index(numb1), l.index(numb2)
            return list(l[numb1_index:numb2_index + 1])
        else:
            return []
    except:
        return []


def __FindTypePkgTypeAndNumbers(longstr = ""):
    restr = """
    (?P<LONGSTR>[第从]?
    \s*(?P<START>[A-Za-z0-9一二三四五六七八九十–－─—-]+)
    \s*(?P<TYPE>标段号|标段|标项|分包|分项|分标号?|品目|标包|包组号|包组|包号|包件|(?<!承)包)?
    \s*[至到~～]+ #–－─—- 横线视为包号中的一部分,例如:A-1 A-2 D1-1 D1-2 D2-1 D2-2
    \s*[第]?
    \s*(?P<END>[A-Za-z0-9一二三四五六七八九十–－─—-]+)
    \s*(?P<TYPE>标段号|标段|标项|分包|分项|分标号?|品目|标包|包组号|包组|包号|包件|(?<!承)包)
    |
    (?P<TYPE>标段号|标段|标项|分包|分项|分标号?|品目|标包|包组号|包组|包号|包件|(?<!承)包)
    \s*(?P<START>[A-Za-z0-9一二三四五六七八九十–－─—-]+)
    \s*[至到~～]+ #–－─—- 横线视为包号中的一部分,例如:A-1 A-2 D1-1 D1-2 D2-1 D2-2
    \s*(?P<TYPE>标段号|标段|标项|分包|分项|分标号?|品目|标包|包组号|包组|包号|包件|(?<!承)包)?
    \s*(?P<END>[A-Za-z0-9一二三四五六七八九十–－─—-]+))
    """
    rs = re.findall(restr, longstr, re.I | re.S | re.X)
    return rs



# 根据词库,剔除多余的空格
def KillUnusefulSpace(keywords_list, long_str):
    ress = []
    for kw in keywords_list:
        for i in range(len(kw) - 1):
            s = "(?<=" + ToReStr(kw[i]) + ")(?:\s|[ ]|{_}|&nbsp;)+?(?=" + ToReStr(kw[i + 1]) + ")"
            ress.append(s)
    restr = "|".join(ress)
    return re.sub(restr, "", long_str, 0, re.I | re.S)


# 删除一些指定名称的标签 例:DelTags_self(html,["span"],True) 删除span标签
def DelTags_self(html, taglist = [], OnlyTag = True):
    try:
        html = RepairHtml(html)
        for tagname in taglist:
            if OnlyTag:
                # 只删除标签本身，innerxml不删除。
                html = re.sub("\s*</?" + tagname + "(?: [^>]+?)?>\s*", "", html, 0, re.I | re.S)
            else:
                # 删除标签及内容,包含innerxml也一起删除。
                html = re.sub("""((?P<spaces> *?)<""" + tagname + """(?: [^>]+?)?>.*?(?P=spaces)</""" + tagname + """>)""", "", html, 0, re.I | re.S)
        rtnv = RepairHtml(html)
        return rtnv
    except Exception as e:
        print("函数名：", sys._getframe().f_code.co_name)
        print(e)


def GetIntroduction(content):
    txt = RepairHtml(content)
    txt = re.sub("<style[^>]*?>.*?</style>", "", txt, 0, re.I | re.S)
    txt = re.sub("<[^>]+?>", "", txt, 0, re.I | re.S)
    txt = re.sub("\s+", " ", txt, 0)
    txt = HtmlKillTrans(txt)
    return txt[:150]



# 剔除head标签中的大量样式,仅保留title
def CleanHead(html = ""):
    # title = findfirst_search("<title>.*?</title>", html, re.I | re.S)
    # newhtml = re.sub("<head>.*?</head>", "<head>" + ToReStr(title) + "</head>", html, 0, re.I | re.S)
    newhtml = re.sub("<head>.*?</head>", "", html, 0, re.I | re.S)
    return newhtml



def GetDisplayContent(content, website = ""):
    '''
    先用正则提取正文，如果没提取到用xpath提取
    '''
    # print(content)
    features = Features.get(website, [""])
    # print(features,'features')
    features = [ToReStr(feature) for feature in features]
    # print(features, 'features2')
    xpaths = Xpaths.get(website, [""])
    # print(xpaths,'xpaths')
    content = re.sub("[a-z0-9/+]{100,}=*", "", content, 0, re.I | re.S)
    # print(content)
    content = re.sub("(<=^.{500,})<html [^>]*?>|</html>(?=.{500,}$)|<!doctype[^>]*?>|<img [^>]*?>|<image [^>]*?>", "", content, re.I | re.S)
    # print(content)
    content = re.sub("""<([a-z0-9]+) [^>]*?style=['"\s]+display[:\s]+none[^>]*?>(?:[^<>]+?</\\1>)?""", "", content, re.I | re.S)
    # print(content)
    content = re.sub("""<([a-z0-9]+) [^>]*?type=['"\s]+hidden[^>]*?>(?:[^<>]+?</\\1>)?""", "", content, re.I | re.S)
    # print(content)
    # content = ForJson(content, website)
    # content = RepairHtml(content)
    # if website == "www.ccgp-shanghai.gov.cn":
    #     content = re.sub("<input [^<>]*? value=\"([^<>]*?)\"[^<>]*?>", "", content, 0, re.I | re.S)
    # else:
    content = re.sub("<input [^<>]*? value=\"([^<>]*?)\"[^<>]*?>", "\\1", content, 0, re.I | re.S)
    # content = RepairHtml(content)
    # print(content,'content')

    xmls_x = GetXmlsbyXpaths(content, xpaths,url_tag=website)
    # print(xmls_x,'xmls_x')
    if len(xmls_x) == 1 and xmls_x[0] != content:

        newcontent = "\r\n<br>\r\n".join(xmls_x)
    else:
        xmls_f = GetXmlsByAttrs(content, features)
        # print(xmls_f)
        if len(xmls_f) == 1 and xmls_f[0] != content:
            newcontent = "\r\n<br>\r\n".join(xmls_f)
        else:
            newcontent = "\r\n<br>\r\n".join(xmls_x)
    # print(newcontent,'newcontent')
    if len(re.findall("[一-龥]", newcontent)) > 100:
        content = newcontent
        # 修复html结构
        # print(content)
        # content = RepairHtml(content)
    # print(content,'content')
    # 剔除span标签,剔除注释,剔除脚本
    # content = ConvertPreLable(content)
    #
    # content = re.sub("\s*<span[^<>]*?>\s*|\s*</span>\s*|\s*<!--.*?-->\s*|\s*<script .*?</script>\s*", "", content, 0, re.I | re.S)
    #
    # content = re.sub("(?<=(?:^|>)[^<>]*?)>|&gt;", "", content, re.I | re.S)
    # # print(content)
    # # 剔除带链接的锚
    # # content = DelTags_ByFeatures(content, ["a"], ["href"], [], [], [], ["公司", "设计院", "研究院"])
    # # 剔除无用的词汇,类似"总访问量","办事指南","个人中心","当前位置","次浏览"的词汇
    #
    # content = re.sub("(?<![一-龥])[一-龥]{0,3}(?:财政部唯一指定政府采购信息网络发布媒体 国家级政府采购专业网站|服务热线：400-810-1996|您当前所在的位置|您当前所在位置|暂时没有信息|原文链接地址|您现在的位置|视力保护色|今日访问量|关闭窗口|立即打印|正文内容|点击次数|打印文章|字体大小|浏览文章|打印本页|七天预报|当前位置|信息时间|个人中心|总访问量|办事指南|我要打印|阅读次数|打印页面|信息检索|轮播新闻|上一篇|下一篇|没有了|下一页|上一页|今天是|次浏览|节假日|浏览数|省本级|打印(?!设备|机)|来源|字号|分享|正文|关闭|尾页)+[一-龥]{0,3}(?:[^一-龥]*?(?:[：:]|(?<![a-z一-龥])次(?![一-龥])|(?<![一-龥])大(?![一-龥])|(?<![一-龥])中(?![一-龥])|(?<![一-龥])小(?![一-龥])|(?<![a-z])Loading|…|(?<![<][^>]*?)>|【|】|[|]))?(?![一-龥])", "", content, 0, re.I | re.S)
    # content = HtmlKillTrans(content)
    # # print(content)
    # content = det(content)
    # # print(content)
    # # print(content,'content')
    return newcontent

def HtmlKillTrans(html):
    for k in htmltcs:
        html = html.replace(k, htmltcs[k])
        html = html.replace(k[0:-1], htmltcs[k])  # 有些网站可能含有 &nbsp 的情况等不规则的转义字符,但浏览器会自动补全
    return html


def det(html, taglist = None):
    success = True
    while success:
        if type(taglist) == type([]) or type(taglist) == type(()):
            for tagname in taglist:
                newhtml = re.sub("<(?P<tagname>" + tagname + ")[^>]*?>[^\u4e00-\u9fa50-9a-zA-Z<>]*?</(?P=tagname)>", "", html, 0, re.I | re.S)
                if html == newhtml:
                    success = False
                else:
                    html = newhtml
        else:
            newhtml = re.sub("<(?P<tagname>[\w]+)[^>]*?>[^\u4e00-\u9fa50-9a-zA-Z<>]*?</(?P=tagname)>", "", html, 0, re.I | re.S)
            if html == newhtml:
                success = False
            else:
                html = newhtml
    html = RepairHtml(html)
    return html


# 将一般字串转换为用来拼接正则的STR,可以避免因存在符号而破坏正则代码
def ToReStr(src):
    restr = ""
    for c in src:
        if c in "\\()[]{}.?+*^$|!":
            restr += "\\" + c
        else:
            restr += c
    return restr


def RepairHtml(html, allow_tags = None, remove_tags = None, kill_tags = None):
    if html == "": return ""
    HTML = html
    try:
        cleaner = Cleaner(allow_tags = allow_tags, remove_tags = remove_tags, kill_tags = kill_tags, page_structure = False)
        html = cleaner.clean_html(html)
        # print(html)
        soup = BeautifulSoup(html, "lxml")
        html = soup.prettify()
        return html
    except Exception as e:
        # print("---------------------------------------------------------------------------------------------")
        # print(html)
        # print("函数名：", sys._getframe().f_code.co_name)
        # print(e)
        # print("---------------------------------------------------------------------------------------------")
        return HTML


def GetXmlsByAttrs(html, features = []):  # 只要满足任意一个特征即可
    try:
        if features == ['']: return [html]
        restr = "(((?<=^|[\r\n])(?P<spaces> *?)<(?P<tagname>[\w]+)[^>]*?(?:" + "|".join(features) + ")[^>]*?>.*?(?<=[\r\n])(?P=spaces)</(?P=tagname)>))"
        recs = re.findall(restr, html, re.I | re.S)
        recs = [rec[0] for rec in recs]
        # print(recs,'-----------------------recs---------------------------')
        return recs
    except:
        return [html]


def GetXmlsbyXpaths(html_content = "", XPATHS = [""],url_tag = ''):
    try:
        # print(XPATHS,'XPATHS')
        # print(html_content,'html_content')
        if XPATHS == [""]: return [html_content]
        rtnv = []
        html_obj = etree.HTML(html_content)  # etree.HTML 具有修复标签的能力
        # print(XPATHS,'XPATHS')
        # xml_objs = html_obj.xpath(XPATHS[url_tag])
        # for xml_obj in xml_objs:
        #     b_str = etree.tostring(xml_obj)
        #     u_str = str(b_str, "utf-8")
        #     rtnv.append(htmlpkg.unescape(u_str))
        for XPATH in XPATHS:
            xml_objs = html_obj.xpath(XPATH)
            # print(xml_objs,'xml_objs')
            for xml_obj in xml_objs:
                b_str = etree.tostring(xml_obj)
                u_str = str(b_str, "utf-8")
                rtnv.append(htmlpkg.unescape(u_str))
        # print(rtnv,'rtnv')
        return rtnv
    except Exception as e:
        print("函数名：", sys._getframe().f_code.co_name)
        print(e)
        return [html_content]

def ConvertPreLable(content):
    rs = re.findall("<pre(?: [^>]+?|>).*?</pre>", content, re.I | re.S)
    for r in rs:
        nr = re.sub("\r?\n", "<br>", r)
        content = content.replace(r, nr)
    content = re.sub("<pre(?: [^>]+?>|>)|</pre>", "", content)
    return content


# 转换str list tuple set 为list
def ToStrList(obj):
    if type(obj) == type([]) or type(obj) == type(()) or type(obj) == type({}):
        return [str(itm) for itm in obj]
    else:
        return [str(obj)]


# 根据字符串特征，删除包含指定特征的标签
def DelTags_ByFeatures(html, Tag_Name_list = [], Tag_Attribute_list = [], Tag_Text_list = [], Protect_Tag_Name_list = [], Protect_Tag_Attribute_list = [], Protect_Tag_Text_list = []):
    html = RepairHtml(html)

    Tag_Name_list = ToStrList(Tag_Name_list)
    Tag_Attribute_list = ToStrList(Tag_Attribute_list)
    Tag_Text_list = ToStrList(Tag_Text_list)
    Protect_Tag_Name_list = ToStrList(Protect_Tag_Name_list)
    Protect_Tag_Attribute_list = ToStrList(Protect_Tag_Attribute_list)
    Protect_Tag_Text_list = ToStrList(Protect_Tag_Text_list)

    Tag_Name_list = [ToReStr(tal) for tal in Tag_Name_list]  # 需要时启用
    Tag_Attribute_list = [ToReStr(tal) for tal in Tag_Attribute_list]  # 需要时启用
    Tag_Text_list = [ToReStr(tal) for tal in Tag_Text_list]  # 需要时启用
    Protect_Tag_Name_list = [ToReStr(tal) for tal in Protect_Tag_Name_list]  # 需要时启用
    Protect_Tag_Attribute_list = [ToReStr(tal) for tal in Protect_Tag_Attribute_list]  # 需要时启用
    Protect_Tag_Text_list = [ToReStr(tal) for tal in Protect_Tag_Text_list]  # 需要时启用

    Del_Tag_Names = "(?:" + "|".join(Tag_Name_list) + ")" if len(Tag_Name_list) > 0 else ""
    Del_Tag_Attribute = "(?<=(?:" + "|".join(Tag_Attribute_list) + ")[^>]*?)" if len(Tag_Attribute_list) > 0 else ""
    Del_Tag_Text = "(?<=(?:" + "|".join(Tag_Text_list) + ")).*?" if len(Tag_Text_list) > 0 else ""
    Protect_Tag_Names = "(?!(?:" + "|".join(Protect_Tag_Name_list) + "))" if len(Protect_Tag_Name_list) > 0 else ""
    Protect_Tag_Attributes = "(?![^>]*?(?:" + "|".join(Protect_Tag_Attribute_list) + "))" if len(Protect_Tag_Attribute_list) > 0 else ""
    Protect_Tag_Texts = "(?:" + "|".join(Protect_Tag_Text_list) + ")" if len(Protect_Tag_Text_list) > 0 else ""

    restr = "((?<=^|[\n])(?P<spaces> *?)<Protect_Tag_Names(?P<tagname>Del_Tag_Names)(?= |>)Protect_Tag_Attributes[^>]*?Del_Tag_Attribute>.*?(?<! )(?P=spaces)</(?P=tagname)>)"
    restr = restr.replace("Del_Tag_Names", Del_Tag_Names)
    restr = restr.replace("Del_Tag_Attribute", Del_Tag_Attribute)
    # restr = restr.replace("Del_Tag_Text", Del_Tag_Text)
    restr = restr.replace("Protect_Tag_Names", Protect_Tag_Names)
    restr = restr.replace("Protect_Tag_Attributes", Protect_Tag_Attributes)
    # restr = restr.replace("Protect_Tag_Texts", Protect_Tag_Texts)
    try:
        rs = re.findall(restr, html, re.I | re.S)
        rs_html = [r[0] for r in rs]
        rs_text = [re.sub("<[^>]+?>", "", r[0]) for r in rs]
        # r=re.sub("<[^>]+?>","",r[0])
        for i, r_text in enumerate(rs_text):
            if NoWordIn(Protect_Tag_Text_list, r_text) and SomeWordsIn(Tag_Text_list or [""], r_text):
                html = html.replace(rs_html[i], "", 1)
                # html = re.sub(restr, "", html, 1, re.I | re.S)
    except:
        print("----------------")
    return RepairHtml(html)


def NoWordIn(keywords_list, str_in):
    if type(keywords_list) != type([]) and type(keywords_list) != type(()):
        keywords_list = [keywords_list]
    for keyword in keywords_list:
        if CompoundWordIn(keyword, str_in):
            return False
    return True


def SomeWordsIn(keywords_list, str_in):
    if type(keywords_list) != type([]) and type(keywords_list) != type(()):
        keywords_list = [keywords_list]
    for keyword in keywords_list:
        if CompoundWordIn(keyword, str_in):
            return True
    return False


# 测试“组合关键词”是否被str包含，允许离散和无序，但必须全包含。
def CompoundWordIn(keyword, longword, split_str = "&"):
    kws = keyword.split(split_str)
    for kw in kws:
        if kw not in longword:
            return False
    return True


# 表格转置
def htc_old(html_con, InnerOrder, dlsm_uuid):
    # print(html_con,'html_con')
    if InnerOrder > 10: return html_con
    # if "<table " not in html_con: return html_con
    if NoWordIn(["<table ", "<table>"], html_con): return html_con
    HTMLCON = html_con
    alltrs = re.findall("<tr[ >]", html_con, re.I | re.S)
    if len(alltrs) > 500:  # 针对单个表多于500行,如果多个表共200行也不处理,因为暂无法区别表格数量,这种情况极少
        return HTMLCON
    alltds = re.findall("<td[ >]", html_con, re.I | re.S)
    if len(alltds) > 2000:  # 针对单个表多于2000格,如果多个表共800格也不处理,因为暂无法区别表格数量,这种情况极少
        return HTMLCON
    try:
        # 提取最内层的table标签
        htmlcon = RepairHtml(html_con)
        if htmlcon is None: return HTMLCON
        htmlcon = DelAttrs(htmlcon)  # 剔除标签属性数据除了rowspan和colspan,尽可能减少下两行匹配大表格时出错 20180906修改
        # table_restr = """[\\n \\r]*?[<](?:table [^<>]*?|table)[>](?:(?![<]table).)*?[\\n \\r]*?[<]/table[>]"""
        table_restr = """<(?:table(?: [^<>]*)?)>(?:(?!<table).)*?</table>"""
        tabletags = re.findall(table_restr, htmlcon, re.I | re.S)
        for tabletag in tabletags:
            # 前期处理
            tabletag_tmp = re.sub("rowspan *= *\"?1\"?(?![0-9])", "", tabletag)
            tabletag_tmp = re.sub("colspan *= *\"?1\"?(?![0-9])", "", tabletag_tmp)
            # 提取 border
            border_str = findfirst("<table [^>]*?border *= *\"?([0-9]+)\"?(?![0-9])", tabletag)
            border_str = border_str or "0"
            border = int(border_str)
            if InnerOrder > 2 and border == 0:  # 如果 表格不在最内层 和 次内层 且 线条宽度为0 则 认为此表格仅用于布局 不处理
                continue

            # 表格转LL
            Table_LL = []
            # 表格转LL - 处理colspan
            trs = re.findall("<tr[^<>]*?>.*?</tr>", tabletag_tmp, re.I | re.S)
            for tr_index in range(len(trs)):
                tds = re.findall("<(?:td|th)[^<>]*?>.*?</(?:td|th)>", trs[tr_index], re.I | re.S)
                tmprow = []
                for td_index in range(len(tds)):
                    colspan_str = findfirst("colspan\s*=\s*\"?([0-9]+)\"?", tds[td_index], re.I | re.S)
                    colspan = int(colspan_str) if len(colspan_str) > 0 else 1
                    rowspan = 1  # 插入常量1占位,保证每个单元格都是5个元素[T,D,N,COLSPAN,ROWSPAN]
                    tds[td_index] = re.sub("colspan\s*=\s*\"?([0-9]+)\"?", "", tds[td_index])
                    for i in range(colspan):
                        if re.search("[:：]\s*?$", tds[td_index]):
                            T = "K"
                        elif td_index > 0 and re.search("[:：]\s*?$", tds[td_index - 1]):
                            T = "V"
                        else:
                            T = __Distinguish(tds[td_index], tr_index, td_index)  # 判断是K还是V
                        D = tds[td_index]
                        N = "" if i == 0 else "SameToLeft"
                        tmprow.append([T, D, N, colspan, rowspan])
                Table_LL.append(tmprow)

            # 表格转LL - 处理rowspan
            for ri in range(len(Table_LL)):
                for ci in range(len(Table_LL[ri])):
                    rowspan_str = findfirst("rowspan\s*=\s*\"?([0-9]+)\"?", Table_LL[ri][ci][1], re.I | re.S)
                    rowspan = int(rowspan_str) if len(rowspan_str) > 0 else 1
                    Table_LL[ri][ci][1] = re.sub("rowspan\s*=\s*\"?([0-9]+)\"?", "", Table_LL[ri][ci][1])
                    # Table_LL[ri][ci].append(1)
                    # 只按照rowspan插入
                    for rs in range(rowspan):
                        if rs == 0 and rowspan > 1:
                            Table_LL[ri][ci][4] = rowspan  # 前面使用了1来占位,在此修改为真实值
                        elif rowspan > 1:
                            next_ri = ri + rs  # 下一行索引
                            if next_ri < len(Table_LL):
                                T = Table_LL[ri][ci][0]
                                D = Table_LL[ri][ci][1] if not re.search("(?:[十一二两三四五六七八九][亿万仟千佰百拾元圆角分]|(?![亿万仟千佰百])(?!参[加考与会数照赛见观展评股阅看选议谋])[亿万仟千佰百拾十一二三四五六七八九壹贰参叁肆伍陆柒捌玖零〇廿卅卌点元圆角]{2,}|['0-9.]{3,})", Table_LL[ri][ci][1], re.I | re.S) else ""  # 如果是金额,复制的格子用"空字串"代替
                                N = "SameToTop"
                                COLSPAN = Table_LL[ri][ci][3]
                                ROWSPAN = rowspan
                                Table_LL[next_ri].insert(ci, [T, D, N, COLSPAN, ROWSPAN])
                        else:
                            break
            # 表格转LL完成

            # 剔除长度为0的行，即:剔除空行.
            for ri in range(len(Table_LL) - 1, -1, -1):
                if len(Table_LL[ri]) == 0:
                    Table_LL.pop(ri)  # 如果当前行为[],则从Table_LL中移除

            # print(Table_LL,'Table_LL')

            # 获取表格最大宽度，以前两行为基准最大长度,作为表格的最大宽度,
            longest = 0
            for ri in range(len(Table_LL)):
                if ri < 2 and len(Table_LL[ri]) > longest: longest = len(Table_LL[ri])
                if ri >= 2: break

            # 右侧补齐，每一行的长度不同时,使用最后一个元素,以最大长度为标准,补齐.保证每行长度都相同.
            for ri in range(len(Table_LL)):
                length = longest - len(Table_LL[ri])
                if length > 0:
                    for i in range(length):
                        cell = Table_LL[ri][len(Table_LL[ri]) - 1]
                        Table_LL[ri].append(cell)
                if length < 0:  # 超出表格最大宽度的单元格,做丢弃处理
                    length = abs(length)
                    for i in range(length):
                        Table_LL[ri].pop()  # 剔除最后元素

            # colspan=列数 或 rowspan=行数 的单元格,类型置为 "V"
            for ri in range(len(Table_LL)):
                for ci in range(len(Table_LL[ri])):
                    if Table_LL[ri][ci][3] == longest:
                        Table_LL[ri][ci][0] = "V"
                    if Table_LL[ri][ci][4] == len(Table_LL):
                        Table_LL[ri][ci][0] = "V"

            Table_LL = CheckTablePoint(Table_LL)
            # 拼接成行
            UsedKeys_Index = []
            newlines_pos = []
            newlines = []
            col1_key_count = len(["1" for tmprow in Table_LL if tmprow[0][0] == "K"])
            if len(Table_LL) > 5 and len(Table_LL[0]) == 2 and col1_key_count / len(Table_LL) > 0.6:  # 特殊处理:多行两列的表格,一律按"左列K""右列V"方式处理
                for ri, row in enumerate(Table_LL):
                    K_D = row[0][1]
                    V_D = row[1][1]
                    KLeft = re.sub("<[^>]*?>", "", K_D)  # KLeft 可能会很长
                    KLeft = re.sub("\s+", "", KLeft)
                    if "tbl_start_tag" in KLeft or "tbl_end_tag" in KLeft or "{^^^}" in KLeft:
                        KLeft = ""
                    if len(KLeft) > 30:
                        KLeft = re.sub("[:：](?<=" + restr1 + ").*?$|(?<=" + restr1 + ").*?$", "", KLeft)  # 20101016加入 14261532
                    lines = HTML_SplitToLines(V_D)
                    for line in lines:
                        line = re.sub("<[^>]*?>", "", line)
                        line = re.sub("\s+", "", line)
                        if KLeft == "": newrow = line
                        else: newrow = KLeft + "{_}{_}" + line
                        newlines.append(newrow)
                        newlines_pos.append((ri, 1))
            else:  # 一般表格处理方式
                for ri, row in enumerate(Table_LL):
                    newrow = ""
                    for ci, TDNCR in enumerate(row):
                        # if ri == 3 and ci == 7:  # 留着调试用
                        #     tmp = Table_LL[ri][ci]
                        T = TDNCR[0]  # T:Type
                        D = TDNCR[1]  # D:Data
                        N = TDNCR[2]  # N:Note
                        COLSPAN = TDNCR[3]
                        ROWSPAN = TDNCR[4]
                        KLeft = ""
                        KTop = ""
                        TDNCR_KLeft_RCCR = [-1, -1, 0, 0]  # RRRC: ri ci colspan rowspan
                        TDNCR_KTop_RCCR = [-1, -1, 0, 0]  # RRRC: ri ci colspan rowspan
                        TDNCR_KLeft_Top_RCCR = [-1, -1, 0, 0]  # RRRC: ri ci colspan rowspan
                        TDNCR_KTop_Left_RCCR = [-1, -1, 0, 0]  # RRRC: ri ci colspan rowspan

                        if T == "K" and N != "SameToLeft" and N != "SameToTop":
                            lines = HTML_SplitToLines(D)
                            for line in lines:
                                line = re.sub("\s*<[^>]*?>\s*", "", line)
                                line = re.sub("\s+", "", line)
                                newlines.append(line)
                                newlines_pos.append((ri, ci))
                        if T == "V" and N != "SameToLeft":  # N != "SameToLeft" 因为前面的两个for,是横向遍历的,所以这句只考虑横向表格,没考虑纵向表格,毕竟横向表格较多
                            # Get KLeft
                            KLeft_Pos = None
                            for ti in range(ci, -1, -1):
                                if ti == ci: continue
                                if row[ti][0] == "V" and row[ti][4] < ROWSPAN:
                                    break
                                if row[ti][0] == "K" and row[ti][4] >= ROWSPAN:  # and row[ti][2] == ""
                                    KLeft = re.sub("^\s+|\s+$", "", row[ti][1])
                                    KLeft = re.sub("<[^>]*?>", "", KLeft)
                                    KLeft = re.sub("\s+", "", KLeft)
                                    KLeft_Pos = (ri, ti)
                                    TDNCR_KLeft_RCCR = [ri, ti, Table_LL[ri][ti][3], Table_LL[ri][ti][4]]
                                    for r in range(ri, -1, -1):
                                        if Table_LL[r][ti][2] != "SameToTop":
                                            TDNCR_KLeft_Top_RCCR = [r, ti, Table_LL[r][ti][3], Table_LL[r][ti][4]]
                                            break
                                    break

                            # Get KTop
                            KTop_Pos = None
                            for ti in range(ri, -1, -1):
                                if ti == ri: continue
                                if Table_LL[ti][ci][0] == "V" and Table_LL[ti][ci][3] < COLSPAN:
                                    break
                                if Table_LL[ti][ci][0] == "K" and Table_LL[ti][ci][3] >= COLSPAN:  # and Table_LL[ti][ci][2] == ""
                                    KTop = Table_LL[ti][ci][1]
                                    KTop = re.sub("<[^>]*?>", "", KTop)
                                    KTop = re.sub("\s+", "", KTop)
                                    KTop_Pos = (ti, ci)
                                    TDNCR_KTop_RCCR = [ti, ci, Table_LL[ti][ci][3], Table_LL[ti][ci][4]]
                                    for c in range(ci, -1, -1):
                                        if Table_LL[ti][c][2] != "SameToLeft":
                                            TDNCR_KTop_Left_RCCR = [ti, c, Table_LL[ti][c][3], Table_LL[ti][c][4]]
                                            break
                                    break

                            # check KLeft : 当前列上下colspan相同,上一行左右T相同
                            if KLeft != "" and TDNCR_KLeft_Top_RCCR != [-1, -1, 0, 0] and ci - (TDNCR_KLeft_Top_RCCR[1] + TDNCR_KLeft_Top_RCCR[2] - 1) > 0:
                                for ti in range(ci, TDNCR_KLeft_Top_RCCR[1] + TDNCR_KLeft_Top_RCCR[2] - 1 - 1, -1):
                                    if ti == ci: continue
                                    if ri > 0:
                                        # "临时格的上格colspan">="临时格colspan","临时格的上格T"="临时格的右上格T"
                                        tmp_cell_colspan = Table_LL[ri][ti][3]
                                        up_cell_colspan = Table_LL[ri - 1][ti][3]
                                        up_cell_type = Table_LL[ri - 1][ti][0]
                                        up_right_cell_type = Table_LL[ri - 1][ti + 1][0]
                                        if (Table_LL[ri - 1][ti][3] < Table_LL[ri][ti][3] or (Table_LL[ri - 1][ti][0] != Table_LL[ri - 1][ti + 1][0] and ti > TDNCR_KLeft_Top_RCCR[1] + TDNCR_KLeft_Top_RCCR[2] - 1)):
                                            KLeft = ""
                                            break

                            # check KTop : 当前行左右rowspan相同,前一列上下T相同
                            if KTop != "" and TDNCR_KTop_Left_RCCR != [-1, -1, 0, 0] and ri - (TDNCR_KTop_Left_RCCR[0] + TDNCR_KTop_Left_RCCR[3] - 1) > 0:
                                for ti in range(ri, TDNCR_KTop_Left_RCCR[0] + TDNCR_KTop_Left_RCCR[3] - 1 - 1, -1):
                                    if ti == ri: continue
                                    if ci > 0:
                                        # "临时格的左格rowspan">="临时格rowspan","临时格的左格T"="临时格的左下格T"
                                        tmp_cell_rowspan = Table_LL[ti][ci][4]
                                        left_cell_rowspan = Table_LL[ti][ci - 1][4]
                                        left_cell_type = Table_LL[ti][ci - 1][0]
                                        left_down_cell_type = Table_LL[ti + 1][ci - 1][0]
                                        if (Table_LL[ti][ci - 1][4] < Table_LL[ti][ci][4] or (Table_LL[ti][ci - 1][0] != Table_LL[ti + 1][ci - 1][0] and ti > TDNCR_KTop_Left_RCCR[0] + TDNCR_KTop_Left_RCCR[3] - 1)):
                                            if KLeft != "":
                                                KTop = ""
                                            break

                            if KLeft == "": KLeft_Pos = None
                            if KTop == "": KTop_Pos = None
                            if KLeft_Pos is not None:
                                UsedKeys_Index.append(KLeft_Pos)
                            if KTop_Pos is not None:
                                UsedKeys_Index.append(KTop_Pos)

                            lines = HTML_SplitToLines(D)
                            for line in lines:
                                line = re.sub("\s*<[^>]*?>\s*", "", line)
                                line = re.sub("\s+", "", line)
                                if TDNCR_KTop_Left_RCCR[1] <= TDNCR_KLeft_Top_RCCR[1] + TDNCR_KLeft_Top_RCCR[2] - 1:
                                    newrow = KTop + "{_}" + KLeft + "{_}" + re.sub("^\s+|\s+$", "", line)
                                elif TDNCR_KLeft_Top_RCCR[0] <= TDNCR_KTop_Left_RCCR[0] + TDNCR_KTop_Left_RCCR[3] - 1:
                                    newrow = KLeft + "{_}" + KTop + "{_}" + re.sub("^\s+|\s+$", "", line)
                                elif re.search("[0-9一二三四五六七八九十廿]+", KTop):  # 可能是纵向表格
                                    newrow = KTop + "{_}" + KLeft + "{_}" + re.sub("^\s+|\s+$", "", line)
                                else:  # 一般表格
                                    newrow = KLeft + "{_}" + KTop + "{_}" + re.sub("^\s+|\s+$", "", line)

                                newlines.append(newrow)
                                newlines_pos.append((ri, ci))
                    newlines.append("{^^^}")  # {^^^}与{^^^}之间的数据在源表格中处同一行
                    newlines_pos.append((-1, -1))
            for i in range(len(newlines_pos) - 1, -1, -1):
                if newlines_pos[i] in UsedKeys_Index:
                    newlines.pop(i)
            newlines_con = "\n<br>{^^^}\n<br>" + "\n<br>".join(newlines) + "\n<br>"
            newlines_con = "\n<br>tbl_start_tag" + newlines_con + "\n<br>tbl_end_tag"
            htmlcon = htmlcon.replace(tabletag, newlines_con)
        # 嵌套表格,递归处理
        if "<table" in htmlcon:
            return htc_old(htmlcon, InnerOrder + 1, dlsm_uuid)
        return htmlcon
    except Exception as e:
        print(sys._getframe().f_code.co_name, e)
        print(traceback.print_exc())
        print(dlsm_uuid)
        return HTMLCON


# 20181113
def htc(html_con, dlsm_uuid, killlabels = True):
    # if "<table " not in html_con: return html_con
    if NoWordIn(["<table ", "<table>"], html_con): return html_con
    HTMLCON = html_con
    try:
        # 提取最内层的table标签
        htmlcon = RepairHtml(html_con)
        if htmlcon is None: return HTMLCON
        htmlcon = DelAttrs(htmlcon)
        table_restr = """[\\n \\r]*?<(?:table [^<>]*?|table)>(?:(?!<table).)*?[\\n \\r]*?</table>"""
        tabletags = re.findall(table_restr, htmlcon, re.I | re.S)
        for tabletag in tabletags:
            tabletag_tmp = re.sub("rowspan ?= ?\"?1\"?", "", tabletag)
            tabletag_tmp = re.sub("colspan ?= ?\"?1\"?", "", tabletag_tmp)
            colspan_count = len(re.findall("colspan=", tabletag_tmp, re.I | re.S))
            rowspan_count = len(re.findall("rowspan=", tabletag_tmp, re.I | re.S))
            if colspan_count > 3 and rowspan_count > 3:  # or colspan_count + rowspan_count > 5:  # 认为是乱格式所以不处理,PS:处理风报招投标数据时,把简单的表格变得很复杂,冗余数据超多
                continue
            Table_LL = []
            trs = re.findall("<tr[^<>]*?>.*?</tr>", tabletag_tmp, re.I | re.S)
            for tr_index in range(len(trs)):
                tds = re.findall("<(?:td|th)[^<>]*?>.*?</(?:td|th)>", trs[tr_index], re.I | re.S)
                tmprow = []
                for td_index in range(len(tds)):
                    colspan_str = findfirst("colspan=\"([0-9]+)\"", tds[td_index], re.I | re.S)
                    colspan = int(colspan_str) if len(colspan_str) > 0 else 1
                    tds[td_index] = re.sub("colspan=\"([0-9]+)\"", "", tds[td_index])
                    for i in range(colspan):
                        tmprow.append(tds[td_index])  # 一般字段长度不会超过20
                Table_LL.append(tmprow)

            # 处理rowspan, 注:colspan已经在上面循环中处理完了.
            for ri in range(len(Table_LL)):
                for ci in range(len(Table_LL[ri])):
                    rowspan_str = findfirst("rowspan=\"([0-9]+)\"", Table_LL[ri][ci], re.I | re.S)
                    rowspan = int(rowspan_str) if len(rowspan_str) > 0 else 1
                    Table_LL[ri][ci] = re.sub("rowspan=\"([0-9]+)\"", "", Table_LL[ri][ci])
                    # 只按照rowspan插入
                    for rs in range(rowspan):
                        if rs == 0: continue  # 当前行不做处理
                        next_ri = ri + rs  # 下一行索引
                        if next_ri < len(Table_LL):
                            Table_LL[next_ri].insert(ci, Table_LL[ri][ci])

            # 剔除长度为0的行,即:剔除空行.
            for ri in range(len(Table_LL) - 1, -1, -1):
                if len(Table_LL[ri]) == 0:
                    Table_LL.pop(ri)  # 如果当前行为[],则从Table_LL中移除
            # 以前两行为基准最大长度,作为表格的最大宽度,
            longest = 0
            for ri in range(len(Table_LL)):
                if ri < 2 and len(Table_LL[ri]) > longest: longest = len(Table_LL[ri])
                if ri >= 2: break
            # 每一行的长度不同时,使用最后一个元素,以最大长度为标准,补齐.保证每行长度都相同.
            for ri in range(len(Table_LL)):
                length = longest - len(Table_LL[ri])
                if length > 0:
                    for i in range(length):
                        cell = Table_LL[ri][len(Table_LL[ri]) - 1]
                        Table_LL[ri].append(cell)
                if length < 0:  # 超出表格最大宽度的单元格,做丢弃处理
                    length = abs(length)
                    for i in range(length):
                        Table_LL[ri].pop()  # 剔除最后元素

            # 重新组合成<table>(按照原来的格式)
            cleartable = ""  # 原表格式,但剔除了单元格内部的标签
            for r in Table_LL:
                clearrow = ""
                for b in r:
                    if killlabels:
                        B = re.sub("<[^<>]+?>", "", b)  # 单元格中的标签剔除
                    else:
                        B = b
                    clearrow += "<td>" + B + "</td>"
                cleartable += "<tr>" + clearrow + "</tr>\r\n"
            cleartable = "<table>" + cleartable + "</table>"

            # 重新组合成<table>(按照转置的格式)
            if len(Table_LL) == 0: continue
            newtable_transpose = ""  # 新表格式,但剔除了单元格内部的标签
            Table_LL_TP = [[r[col] for r in Table_LL] for col in range(len(Table_LL[0]))]
            for r in Table_LL_TP:
                clearrow = ""
                for b in r:
                    if killlabels:
                        B = re.sub("<[^<>]+?>", "", b)  # 单元格中的标签剔除
                    else:
                        B = b
                    clearrow += "<td>" + B + "</td>"
                newtable_transpose += "<tr>" + clearrow + "</tr>\r\n"
            newtable_transpose = "<table>" + newtable_transpose + "</table>"
            # 重新组合成<table>
            if len(Table_LL) == 0: continue
            rowlen = len(Table_LL[0])
            tbl = "<table>tblcon</table>"
            title = []
            newtable_L = []
            for i in range(rowlen):
                # tmp = re.sub("<br[^>]*?>|<p(?: [^>]*?)?>|</p>", "", Table_LL[0][i])  # 单元格中的<br><p>标签和空字符剔除
                tmp = re.sub("<[^<>]+?>", "", Table_LL[0][i])  # 单元格中的标签剔除,由上一行改写
                title.append(tmp)
            for i in range(len(Table_LL) - 1):  # 循环程序有问题,待调试.
                for j in range(len(Table_LL[i + 1])):
                    # row = "<tr>" + title[j] + Table_LL[i + 1][j] + "</tr>" # 改写前
                    # row = "<tr>" + re.sub("<br[^>]*?>|<p(?: [^>]*?)?>|</p>", "", title[j]) + re.sub("<br[^>]*?>|<p(?: [^>]*?)?>|</p>", "", Table_LL[i + 1][j]) + "</tr>"  # 单元格中的<br><p>标签和空字符剔除
                    if killlabels:
                        row = "<tr><td>" + re.sub("<[^<>]+?>", "", title[j]) + "</td><td>" + re.sub("<[^<>]+?>", "", Table_LL[i + 1][j]) + "</td></tr>"  # 单元格中的标签剔除,由上一行改写
                    else:
                        row = "<tr><td>" + title[j] + "</td><td>" + Table_LL[i + 1][j] + "</td></tr>"
                    newtable_L.append(row)
            newtable = tbl.replace("tblcon", "\r\n" + "\r\n".join(newtable_L) + "\r\n")
            # htmlcon = htmlcon.replace(tabletag, newtable)

            if rowlen < 3 or len(Table_LL) < 2:
                htmlcon = htmlcon.replace(tabletag, cleartable + "<br>" + newtable)  # 只有一列或两列或一行表的table不处理,并附加一套处理后的表.
            else:
                htmlcon = htmlcon.replace(tabletag, newtable + "<br>" + cleartable + "<br>" + newtable_transpose)  # 多行或多列的表,做转置处理并前置,原表在后.
        return htmlcon
    except Exception as e:
        print(sys._getframe().f_code.co_name, e)
        print(traceback.print_exc())
        print(dlsm_uuid)
        return HTMLCON



def __Distinguish(longstr, ri = None, ci = None):
    if "{_}" in longstr: return "V"
    lstr = re.sub("<[^>]*?>", "", longstr)  # 剔除标签
    lstr_m = re.sub("[(（].*?[）)]", "", lstr, 0, re.I | re.S)  # 剔除括号内容
    lstr_m = re.sub("^\s+|\s+$", "", lstr_m)  # 剔除两端空格
    lstr_w = re.sub("[^一-龥0-9a-zA-Z]", "", lstr_m, 0, re.I | re.S)  # 剔除无效文字
    # lstr_w = re.sub("\s+", "", lstr_m, 0, re.I | re.S)  # 剔除无效文字
    vstr = re.sub(restr, "", lstr_w, 0, re.I | re.S)  # 剔除Key类型的数据,剩下value类型的数据
    l3 = len(lstr_m)  # 全长
    l2 = len(vstr)  # V长
    l1 = l3 - l2  # K长
    zb = re.search('中标金额|成交金额|成交金额(万元)|成交结果|中标结果|中标价格|报价|中标价|中标|中标（成交）金额（单位：元）|中标（成交）金额\(元\)投标报价:|中标（成交）金额\(元\)|中标总价|成交价|总价',lstr)
    zbn = re.search('\d',lstr)
    if re.search('中标金额|成交金额|成交金额(万元)|成交结果|合同价款|中标结果|中标价格|报价|中标价|中标|中标（成交）金额（单位：元）|中标（成交）金额\(元\)投标报价:|中标（成交）金额\(元\)|中标总价|成交价|总价',lstr) and not re.search('\d',lstr): return "K"
    if re.search('成交供应商',lstr) : return "K"
    if l3 == 0 or l3 > 20: return "V"
    if re.search("[一-龥][一-龥].{0,8}?[:：].{0,5}?[一-龥0-9a-zA-Z]+", lstr_m): return "V"
    if SomeWordEndof([":", "："], lstr_m): return "K"
    if SomeWordsIn(["，", "。", ":", "："], lstr_m): return "V"
    ttt = re.search(restr3, lstr_m)
    if (ri == 0 or ci == 0) and ttt: return "K"
    if re.search("详见|详细内容见|见附件", lstr_m): return "V"
    if len(lstr_m) == 1: return "V"
    if l1 / l3 > (0.8 if l3 > 4 else 0.6): return "K"
    return "V"


# 如果str_in以某个词结尾,则返回True
def SomeWordEndof(keywords_list, str_in):
    if type(keywords_list) != type([]) and type(keywords_list) != type(()):
        keywords_list = [keywords_list]
    for keyword in keywords_list:
        if str_in.replace(keyword, '') + keyword == str_in:
            return True
    return False


# 判断表格方向(横着读 or 坚着读)
def CheckTablePoint(TABLE_LL):
    NeedToConvert = False
    for ri, row in enumerate(TABLE_LL):
        cns = 0  # "公司"关键词数量
        for ci, cell in enumerate(row):
            if cell[2] != "": continue
            if isinstance(cell, str):
                data = cell
            elif isinstance(cell, list) or isinstance(cell, tuple):
                data = cell[1]  # TDNCR
            else:
                data = str(cell)
            if re.search("文化传播中心|地质大队|水文总站|监测站|种公猪站|护理院|敬老院|养老院|公寓|总队|大队|中队|地图院|防治所|维修队|检测站|工程部|学校|地质调查院|测绘院|航测遥感院|信息中心|测量队|监测中心站|研训中心|联合体|公司|(?<!原)厂(?![区商址子家房方矿部里长])|经销处|销售处|销售部|经销商|经营部|经营处|经销部|商行|商贸行|批发部|文化城|设计所|研究院|服务社|电脑行|电脑城|广告部|服务部|公证处|超市|商店|场|中心|研究[总分]?院|研究所|工程处|工程队|工程院|设计[总分]?院|检测院|规划院|勘察院|勘查院|事务所|服务社|合作社|检验院|工程局|(?<=勘探|测绘|地质|[一二三四五六七八九十])局|(?<=勘探|测绘|地质)队|家[俱具]行|教[俱具]厂|家[俱具]厂|商场|大队|勘查局|商城|联合体|促进会|鉴定站|推广站|学会|协会|教育报|医院|学院|大学|技术院|基金会|电视台|俱乐部|职业介绍所|信息院|销售行|家电城|建修队|农牧场|集团|食堂|店(?![一-龥])", data, re.I | re.S):
                cns += 1
        if cns > 2:
            NeedToConvert = True
    if NeedToConvert:
        return TableTrans(TABLE_LL)
    return TABLE_LL


# 表格转置
def TableTrans(TABLE_LL):
    NEW_TABLE = []
    for ri in range(len(TABLE_LL)):
        for ci in range(len(TABLE_LL[ri])):
            if len(NEW_TABLE) - 1 < ci:
                NEW_TABLE.append([])
            celldata = TABLE_LL[ri][ci]
            newcelldata = [celldata[0], celldata[1], None, None, None]
            if celldata[2] == "SameToTop": newcelldata[2] = "SameToLeft"
            elif celldata[2] == "SameToLeft": newcelldata[2] = "SameToTop"
            else: newcelldata[2] = ""
            newcelldata[3] = celldata[4]
            newcelldata[4] = celldata[3]
            NEW_TABLE[ci].append(TABLE_LL[ri][ci])
    return NEW_TABLE


def HTML_SplitToLines(html):
    try:
        if "<pre>" in html and "</pre>" in html:
            html = re.sub("(?<=<pre>(?:(?!<pre>|</pre>).)*?)\n(?=(?:(?!<pre>|</pre>).)*?</pre>)", "\n<br>", html, 0, re.I | re.S)
        SplitTags = ["<p[^>]*?>", "<br/?>", "<br(?: [^>]*?)?>", "<tr[^>]*?>", "<ul[^>]*?>", "<ol[^>]*?>", "<li[^>]*?>", "<h1[^>]*?>", "<h2[^>]*?>", "<h3[^>]*?>", "<h4[^>]*?>", "<h5[^>]*?>", "<h6[^>]*?>", "<table[^>]*?>", "<menu[^>]*?>", "<hr[^>]*?>", "<form[^>]*?>", "<div[^>]*?>", "<table[^>]*?>"]
        html = re.sub("\s", " ", html)  # 剔除回车,全部成一行
        html = re.sub("(?<!<td[^<]*?>.*?[一-龥0-9a-z].*?<)(?=" + "|".join([tag for tag in SplitTags if "br" not in tag]) + ")", "{^}", html, 0, re.I | re.S)  # &&&_For_Split_&&& 仅作为分隔符
        html = re.sub("(?=" + "|".join([tag for tag in SplitTags if "br" in tag]) + ")", "{^}", html, 0, re.I | re.S)  # &&&_For_Split_&&& 仅作为分隔符
        html = re.sub("(?=<td[^>]*?>)", "{_}", html)  # 后面是<td>的位置作为cellfirst
        html = re.sub("\s+", " ", html)  # del space \t\r\n\f\v 全角空格[　]
        html = re.sub("(?<=<td(?:(?!<td|</td>).)*?)[ ](?=(?:(?!<td|</td>).)*?</td>)", "", html, 0, re.I | re.S)
        html = re.sub("(?<=<th(?:(?!<th|</th>).)*?)[ ](?=(?:(?!<th|</th>).)*?</th>)", "", html, 0, re.I | re.S)
        html = re.sub("\s*<[^<>]*?>\s*", "", html)  # del tags

        Lines = html.split("{^}")  # {^} 仅作为分隔符
        for i in range(len(Lines) - 1, -1, -1):
            Lines[i] = re.sub("^{_}", "", Lines[i])
            if Lines[i] == "" or Lines[i] == "{_}":
                del Lines[i]
        return Lines
    except Exception as e:
        print(sys._getframe().f_code.co_name, e)
        return []


# 剔除标签属性数据除了rowspan和colspan
def DelAttrs(html):  # 剔除标签属性数据除了rowspan和colspan
    restr = "(?<=(?:<t[hrd] |rowspan\s*=\s*\"?\s*[0-9]+\s*\"?|colspan\s*=\s*\"?\s*[0-9]+\s*\"?))" \
            "(?![\"0-9])(?:(?![<>]|rowspan|colspan).)*?" \
            "(?=(?:rowspan\s*=\s*\"?\s*[0-9]+\s*\"?|colspan\s*=\s*\"?\s*[0-9]+\s*\"?|>))" \
            "|(?<=(?:<table |border\s*=\s*\"?\s*[0-9]+\s*\"?))" \
            "(?![\"0-9])(?:(?![<>]|border).)*?" \
            "(?=(?:border\s*=\s*\"?\s*[0-9]+\s*\"?|>))" \
            "|(?<=<(?!t[hrd]|table)[a-z0-9]+ )[^<>]*?(?=>)"
    newstr = re.sub(restr, " ", html, 0, re.I | re.S)
    newstr = re.sub("(?<=<[a-z0-9]+[^<>]*?)\s+(?=>)", "", newstr, 0, re.I | re.S)
    return newstr


# 返回被包含的词集
def WhichWordsIn(keywords_list, str_in):
    if type(keywords_list) != type([]) and type(keywords_list) != type(()):
        keywords_list = [keywords_list]
    InnerWords = []
    for keyword in keywords_list:
        if CompoundWordIn(keyword, str_in):
            InnerWords.append(keyword)
    return InnerWords


def GetSubproject(content):
    restr = '(?:序号|品目号)(?:{_})?(?:[A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-]){1,3}'
    subproject = re.findall(restr, content, re.I | re.S)
    # print(subproject,'subproject')

    return subproject



def GetPkgs(content):
    restr = '(?<!(?:业绩|案例))(?:(?:标段号|标段|(?<![一-龥])项目|标项|分包|分项|分标号?|品目|标包|包组号|包组|包号|包件|(?<!承)包|(?<![招投中废流])标)\s*(?:[{]_[}])?\s*(?![A-Z]{3,})(?:[A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-]){1,10}(?![期A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-])|(?:标段号|标段|标项|分包|分项|分标号?|标包|包组号|包组|包号|包件|(?<!承)包|(?<![招投中废流])标)\s*(?:[{]_[}])?\s*(?![A-Z]{3,})(?:[A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-]|质量检测|造价管理|施工|监理|设计|采购){1,10}(?![期A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-]))'
    pkgs = re.findall(restr, content, re.I | re.S)
    if len(pkgs) == 0 and SomeWordsIn(["各标段", "各标项", "各标包", "包组号", "各包组", "各分包", "各分项", "各分标", "各包件"], content):
        restr = "(?<!(?:业绩|案例).*?)(?<![A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-])(?:(?:序号)\s*(?:[{]_[}])?\s*(?:[A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-]|质量检测|造价管理|施工|监理|设计|采购){1,10}(?![A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ–－─—-]))"
        pkgs = re.findall(restr, content, re.I | re.S)
    pkgs = list(set(pkgs))
    l = []  # 不允许单独出现的包号
    n = 0  # 数字包号的数量
    w = 0  # 汉字包号的数量
    for pkg in pkgs:
        if re.search("[A-Z0-9一二三四五六七八九十廿ⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ]", pkg, re.I | re.S): n += 1
        if SomeWordsIn(["质量检测", "造价管理", "施工", "监理", "设计", "采购"], pkg): w += 1
        ws = WhichWordsIn(["采购"], pkg)  # 不允许单独出现的包号
        l.extend(ws)
    if n == 0 and w < 3:
        pkgs = []
    if len(l) == 1:
        for i in range(len(pkgs) - 1, -1, -1):
            if l[0] in pkgs[i]:
                pkgs.pop(i)
    return pkgs



if __name__ == '__main__':
    # sss = '<td>\n             <p>\n              <font>\n               中标（成交）\n              </font>\n              <font>\n               金额\n              </font>\n             </p>\n             <p>\n             </p>\n            </td>'
    # __Distinguish(sss,2,0)


    # import requests
    #
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92'
    #                   '.0.4515.159 Safari/537.36',
    # }
    # url = 'https://changsha.hnsggzy.com/jygkzbgg/91274565.jhtml'
    #
    # content = requests.get(url=url, headers=headers).text
    #
    # corexml, tablein, display_content, Introduction, WORDCOUNT = SPL_Preprocessing('12343243242', content,'hnsggzy')
    #
    # # corexml = etree.HTML(corexml).xpath('//text()')
    # # lines, projnumb_lines = SPL_SplitToLines(corexml, tablein)
    # print(corexml, 'corexml')
    # # print(tablein, 'tablein')
    # # print(display_content, 'display_content')
    # # print(Introduction, 'Introduction')
    # # print(WORDCOUNT, 'WORDCOUNT')
    # # print(lines,'lines')
    # # print(projnumb_lines,'projnumb_lines')
    with open('content_test.html','r',encoding='utf8') as r:
        tmp = r.read()
        # print(tmp)
        content = htc_old(tmp, 1, '123')
