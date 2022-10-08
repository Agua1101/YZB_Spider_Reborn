from yzb_db_connect import *
import decimal
from yzb_conf import config as conf
import regex as re
from yzb_tag_extract import chinese_to_num
import yzb_TextPreprocessing




class PackageEx():

    def unit_price_ex(self,table_str):
        normal_restr = '(?:单价)(?:\(元\)|（元）)?(?:{_})*([\d.,]*?)(?:{_}|{\^\^\^})'
        million_restr = '(?:单价)(?:\(万元\)|（万元）)?(?:{_})*([\d.,]*?)(?:{_}|{\^\^\^})'

        return self.price_ex(normal_restr,million_restr,table_str)


    def total_price_ex(self,table_str):
        normal_restr = '(?:成交金额|中标金额|总金额|中标价|金额|总价)(?:\(元\)|（元）|:|：|{_})*([\d.,]*?)(?:{_}|{\^\^\^}|[\u4e00-\u9fa5])'
        million_restr = '(?:成交金额|中标金额|总金额|中标价|金额|总价)(?:\(万元\)|（万元）|:|：|{_})*([\d.,]*?)(?:{_}|{\^\^\^}|[\u4e00-\u9fa5])'

        return self.price_ex(normal_restr,million_restr,table_str)


    def price_ex(self,normal_restr,million_restr,table_str):
        # 单位是元
        normal_price = self.normal_price_ex(normal_restr, table_str)
        # 单位是万元
        million_price = self.million_price_ex(million_restr, table_str)

        return normal_price if normal_price else million_price


    def normal_price_ex(self,normal_restr,table_str):
        price_list = re.findall(normal_restr, table_str)
        if set(price_list) != {''} and price_list != []:
            print(price_list,'price_list')
            if '' in price_list:
                price_list.remove('')
            return decimal.Decimal(price_list[0].strip().replace(',', '')) * 100


    def million_price_ex(self,million_restr,table_str):
        price_list = re.findall(million_restr, table_str)
        if set(price_list) != {''} and price_list != []:
            print(price_list, 'price_list')
            return decimal.Decimal(price_list[0].strip().replace(',', '')) * 1000000

    def brand_model_ex(self,table_str):
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

        return self.table_word_filter(brand),self.table_word_filter(model)


    def quantity_ex(self,table_str):
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


    def purchase_details_ex(self,table_str):
        purchase_details_list = re.findall('(?:(?<!供应商)名称|采购内容|主要中标内容)(?:(?:{_})+|(?:：))(.*?)(?:{_}|供应商名称)',table_str)
        # print(purchase_details_list,'purchase_details_list')
        for i in range(len(purchase_details_list)-1,-1,-1):
            if re.search('采购',purchase_details_list[i]):
                purchase_details_list.pop(i)

        purchase_details_list = self.de_duplication(purchase_details_list)

        return self.table_word_filter(''.join(purchase_details_list))


    def winbider_table_ex(self,table_str):
        win_bider_list = re.findall('(?:供应商名称|中标候选人|中标单位)(?:{_}|：|:)*(.*?)(?:{_}|供应商地址)', table_str)
        for i in range(len(win_bider_list)-1,-1,-1):
            win_bider_list[i] = re.sub('{\^\^\^}|{_}', '', win_bider_list[i])
            if re.search('品牌（如有）|规格型号|货物品牌|签订合同|货物名称|单价|数量|序号|详见|工期',win_bider_list[i]):
                win_bider_list.pop(i)

        win_bider_list = self.de_duplication(win_bider_list)


        print(win_bider_list,'win_bider_list')
        return ''.join(win_bider_list)

    def table_word_filter(self,word):
        word = re.sub('{_}|{\^\^\^}', '', word)
        filter_word = '详见标书|详见投标文件|标的|采购'
        if not re.search(filter_word, word):
            return word

    def de_duplication(self,data_list):
        num_list = []
        for num in data_list:
            if num not in num_list:
                num_list.append(num)
        return num_list



class PackageMain():
    def __init__(self):
        self.pkg_list = []


    def pkg_details_by_regex(self,table_str,bid_id):
        print(table_str,'table_str')

        # 采购内容
        purchase_details = PackageEx().purchase_details_ex(table_str)
        # 品牌,型号
        brand,model = PackageEx().brand_model_ex(table_str)
        # 数量
        quantity = PackageEx().quantity_ex(table_str)
        # 单价
        unit_price = PackageEx().unit_price_ex(table_str)
        # 总价
        total_price = PackageEx().total_price_ex(table_str)
        # 中标供应商
        win_bider  = PackageEx().winbider_table_ex(table_str)

        print('purchase_details: ',purchase_details)
        print('brand: ',brand)
        print('model: ',model)
        print('quantity: ',quantity)
        print('unit_price: ',unit_price)
        print('total_price: ',total_price)
        print('win_bider: ',win_bider)
        # d_save = '12132213'

        if (brand != None or model != None) and (unit_price != None or total_price != None) and purchase_details:
            self.pkg_list.append({'purchase_details':purchase_details,'brand':brand,'model':model,'quantity':quantity,'unit_price':unit_price,
                             'total_price':total_price,'win_bider':win_bider,'bid_id':bid_id})
            # save_pkg_details(purchase_details, brand, model, quantity, unit_price, total_price, win_bider, bid_id)
        elif purchase_details and total_price and win_bider:
            self.pkg_list.append({'purchase_details': purchase_details, 'brand': brand, 'model': model, 'quantity': quantity,
                             'unit_price': unit_price,
                             'total_price': total_price, 'win_bider': win_bider, 'bid_id': bid_id})



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


    def get_subproject_by_num(self,num_list_rough,content,bid_id):
        num_list = PackageEx().de_duplication(num_list_rough)


        for i in range(len(num_list)):
            if i == len(num_list)-1:
                subproject = re.findall(f'(?:{num_list[i]})(.*?)(?:tbl_end_tag)', content)
            else:
                subproject = re.findall('(?:'+str(num_list[i])+')(?:{_})((?:(?!'+str(num_list[i])+').)*?)(?:'+str(num_list[i+1])+')',content)
            # print(subproject,'subproject')
            if len(subproject) >= 1:
                self.pkg_details_by_regex(''.join(subproject),bid_id)


    def get_subproject_by_tblnum(self,content,bid_id):
        restr = '(?:中标（成交）信息|主要标的信息)(?:tbl_start_tag)(?:.*?)(?:tbl_end_tag)'
        subproject_list = re.findall(restr,content)
        # print(subproject_list,'subproject')
        self.pkg_details_by_regex(''.join(subproject_list),bid_id)


    def get_subproject(self,pkg_num_list,subproject_num_list,content,bid_id):
        if pkg_num_list != [] and subproject_num_list != []:
            # 如果既有分包又有子项目，特殊处理
            pkg_num_set = set([re.sub('[a-zA-Z0-9-]','',i) for i in pkg_num_list])
            if len(pkg_num_set) > 1:
                # 如果拆出来 有的叫包 有的叫标 视为提取错误，按子项目提取
                self.get_subproject_by_num(subproject_num_list, content,bid_id)
            elif len(pkg_num_list) == 1 and len(subproject_num_list) > 1:
                self.get_subproject_by_num(subproject_num_list, content,bid_id)
            else:
                self.get_subproject_by_num(pkg_num_list, content,bid_id)
        elif pkg_num_list != [] and subproject_num_list == []:
            # 有分包，没有子项目
            self.get_subproject_by_num(pkg_num_list, content,bid_id)
        elif pkg_num_list == [] and subproject_num_list != []:
            # 没分包有子项目
            self.get_subproject_by_num(subproject_num_list, content,bid_id)
        else:
            # 没分包没子项目,大概率有一个内容
            self.get_subproject_by_tblnum(content,bid_id)
        return self.pkg_list


def save_pkg_details(pkg_dict,d_save):
    d = {}

    notnull_dict(str(pkg_dict.get('bid_id')), d, 'bid_id')
    notnull_dict(pkg_dict.get('purchase_details'), d, 'purchase_details')
    notnull_dict(pkg_dict.get('brand'), d, 'brand')
    notnull_dict(pkg_dict.get('model'), d, 'model')
    notnull_dict(str(pkg_dict.get('quantity')), d, 'quantity')
    notnull_dict(str(pkg_dict.get('unit_price')), d, 'unit_price')
    notnull_dict(str(pkg_dict.get('total_price')), d, 'total_price')
    notnull_dict(pkg_dict.get('win_bider'), d, 'winning_bidder')

    d_save.insert('t_bid_pkg', d)


def save_package(pkg_list,d_save):
    for pkg_dict in pkg_list:
        save_pkg_details(pkg_dict,d_save)


def win_bider_to_str(pkg_list):
    win_bider_list = [w.get('win_bider') for w in pkg_list if w.get('win_bider') != None and w.get('win_bider') != '']
    # print(win_bider_list, 'win_bider_list')
    if len(win_bider_list) > 1:
        win_bider = ','.join(win_bider_list)
        # print(win_bider, 'win_bider')
        return win_bider
    else:
        return



# 主程序
def pkg_ex(content,bid_id):
    # try:
        print(content,'pre_content')
        pkg_num_list = yzb_TextPreprocessing.GetPkgs(content)
        pkg_num_list.sort()
        print(pkg_num_list,'pkg_num_list')
        subproject_num_list = yzb_TextPreprocessing.GetSubproject(content)
        print(subproject_num_list,'subproject_num_list')


        return PackageMain().get_subproject(pkg_num_list, subproject_num_list, content, bid_id)
    # except Exception as e:
    #     print(e)



if __name__ == '__main__':
    pass
