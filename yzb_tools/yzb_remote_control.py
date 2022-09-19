#coding=UTF-8
import os
from yzb_db_connect import *
from yzb_tag_extract import *
import time


class ControPy():
    def __init__(self,file_name,logger,d_save):
        self.file_name = file_name
        self.logger = logger
        self.d_save = d_save

    def spider_opened(self):
        try:
            # 进程号
            print('1111111111111111111111111111111111111111')
            pid = os.getpid()
            # 本文件名（不含后缀.py）
            myfilename = self.file_name
            # 生成关闭进程的脚本文件
            self.produce_stop_bat(pid, myfilename)
            timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.d_save.update_date('start_time',timeNow,self.file_name)
        except Exception as e:
            print(e, 'start')

    def spider_closed(self):
        self.logger.info('spider is closed')
        # print('spider is closed')
        # 指定停止文件路径
        os.startfile(conf.stop_file + self.file_name +'.bat')
        self.d_save.update_spider_status(0, self.file_name)
        timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.d_save.update_date('stop_time', timeNow, self.file_name)

    def produce_stop_bat(self,pid, tmpfile="stop_xxx.bat"):
        # 待写入内容
        stop_cmd = 'taskkill /pid ' + str(pid) + ' /f'  # 关闭指定进程
        del_self_cmd = "del %0"  # 删除自身文件
        # 文件路径和名称
        tmp_all = conf.stop_file + tmpfile + ".bat"
        print(tmp_all)
        # 写入文件
        with open(file=tmp_all, mode="w") as f:
            f.write(stop_cmd + "\n" + del_self_cmd)


class ControPy_linux():
    def __init__(self,file_name,logger,d_save):
        self.file_name = file_name
        self.logger = logger
        self.d_save = d_save

    #启动时
    def spider_opened(self):
        try:
            # 进程号
            print('1111111111111111111111111111111111111111')
            # pid = os.getpid()
            # 本文件名（不含后缀.py）
            # myfilename = self.file_name
            # self.produce_stop_bat(pid, myfilename)
            timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
            self.d_save.update_date('start_time',timeNow,self.file_name)
        except Exception as e:
            print(e, 'start')

    #自动停止时
    def spider_closed(self):
        self.logger.info('spider is closed')
        # print('spider is closed')
        # 指定停止文件路径
        # os.startfile(conf.stop_file + self.file_name +'.bat')

        self.d_save.update_spider_status(0, self.file_name)
        timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        self.d_save.update_date('stop_time', timeNow, self.file_name)


    def produce_stop_bat(self,pid, tmpfile="stop_xxx.bat"):
        # 待写入内容
        stop_cmd = 'taskkill /pid ' + str(pid) + ' /f'  # 关闭指定进程
        del_self_cmd = "del %0"  # 删除自身文件
        # 文件路径和名称
        tmp_all = conf.stop_file + tmpfile + ".bat"
        print(tmp_all)
        # 写入文件
        with open(file=tmp_all, mode="w") as f:
            f.write(stop_cmd + "\n" + del_self_cmd)