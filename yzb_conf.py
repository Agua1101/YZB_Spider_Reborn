#!/usr/bin/env python3
# coding: utf-8
# 配置文件
import os

class Config(object):  # 默认配置
    DEBUG = False
    # get attribute
    def __getitem__(self, key):
        return self.__getattribute__(key)

class ProductionConfig(Config):# 生产环境
    host = '172.17.60.245'
    port = 3306
    user = 'develop'
    password = 'X02b8H5^FhXOr5Tq'
    db = 'bid'
    charset = 'utf8'
    ml_file = 'C:\\bid\\crawler\\yzb_ml_code\\ml_purcharser_train.xlsx'
    item_file = 'C:\\bid\\crawler\\yzb_ml_code\\item_train.xlsx'
    stop_word = 'C:\\bid\crawler\\yzb_ml_code\\stopwords.txt'
    stop_file = 'C:\\bid\\crawler\\stop_'
    crawler_file = 'C:\\bid\\crawler\\'
    dollar = 7

class DevelopmentConfig(Config):  # 开发环境
    host = '39.107.25.250'
    port = 3306
    user = 'root'
    password = 'jie8#jlfsjd'
    db = 'crawl_test'
    charset = 'utf8'
    ml_file = 'D:\\办公\\yizhaobiao\\my_git\\crawler\\yzb_ml_code\\ml_purcharser_train.xlsx'
    item_file = 'D:\\办公\\yizhaobiao\\my_git\\crawler\\yzb_ml_code\\item_train.xlsx'
    stop_word = 'D:\\办公\\yizhaobiao\\my_git\\crawler\\yzb_ml_code\\stopwords.txt'
    crawler_file = 'D:\\办公\\yizhaobiao\\my_git\\crawler\\'
    dollar = 7
    server = 250


class TestConfig(Config):
    host = '39.107.25.250'
    port = 3306
    user = 'root'
    password = 'jie8#jlfsjd'
    db = 'crawl_test'
    charset = 'utf8'
    ml_file = '/crawler/YZB_Spider_Reborn/yzb_tools/yzb_ml_code/ml_purcharser_train.xlsx'
    item_file = '/crawler/YZB_Spider_Reborn/yzb_tools/yzb_ml_code/item_train.xlsx'
    stop_word = '/crawler/YZB_Spider_Reborn/yzb_tools/yzb_ml_code/stopwords.txt'
    crawler_file = '/crawler/crawler/'
    model = '/crawler/crawler/'
    dollar = 7
    server = 250

# class HomeConfig(Config):  # 开发环境
#     host = '39.107.25.250'
#     port = 3306
#     user = 'root'
#     password = 'jie8#jlfsjd'
#     db = 'crawl_test'
#     charset = 'utf8'
#     tag_py_address = 'D:\\办公\yizhaobiao\\my_git\\yizhaobiao_test\\tag_extract_old.py'
#     db_py_address = 'D:\\办公\\yizhaobiao\\my_git\\yizhaobiao_test\\db_connect_old.py'
#     stop_file = 'D:\\办公\\yizhaobiao\\my_git\\crawler\\stop_'
#     crawler_file = 'D:\\办公\\yizhaobiao\\my_git\\crawler\\'
#     dollar = 7

# class Home_SQL_Config(Config):  # 开发环境
#     host = '127.0.0.1'
#     port = 3306
#     user = 'root'
#     password = 'lucky1101'
#     db = 'ceshi'
#     charset = 'utf8'
#     tag_py_address = 'D:\\办公\yizhaobiao\\my_git\\yizhaobiao_test\\tag_extract_old.py'
#     db_py_address = 'D:\\办公\\yizhaobiao\\my_git\\yizhaobiao_test\\db_connect_old.py'
#     stop_file = 'D:\\办公\\yizhaobiao\\my_git\\hidden_run\\stop_'
#     crawler_file = 'D:\\办公\\yizhaobiao\\my_git\\hidden_run\\'
#     dollar = 7

class Production_home(Config):
    host = '39.107.25.250'
    port = 3306
    user = 'root'
    password = 'jie8#jlfsjd'
    db = 'crawl_test'
    charset = 'utf8'
    ml_file = r'D:\python_project\my_git\crawler\ml_code\ml_purcharser_train.xlsx'
    item_file = r'D:\python_project\my_git\crawler\ml_code\item_train.xlsx'
    stop_word = r'D:\python_project\my_git\crawler\ml_code\stopwords.txt'
    stop_file = r'D:\python_project\my_git\crawler\stop_'
    crawler_file = 'D:\\python_project\\my_git\\crawler\\'
    dollar = 7

class Production_linux(Config):
    host = '172.17.60.245'
    port = 3306
    user = 'develop'
    password = 'X02b8H5^FhXOr5Tq'
    db = 'bid'
    charset = 'utf8'
    ml_file = '/bid/crawler/yzb_ml_code/ml_purcharser_train.xlsx'
    item_file = '/bid/crawler/yzb_ml_code/item_train.xlsx'
    stop_word = '/bid/crawler/yzb_ml_code/stopwords.txt'
    crawler_file = '/bid/crawler/'
    dollar = 7
    server = None

# 环境映射关系
mapping = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    # 'home': HomeConfig,
    # 'home_sql': Home_SQL_Config,
    'test':TestConfig,
    'production_home':Production_home,
    'production_linux':Production_linux,
}

# 一键切换环境
APP_ENV = os.environ.get('APP_ENV', 'test').lower()  # 设置环境变量
config = mapping[APP_ENV]()  # 获取指定的环境
