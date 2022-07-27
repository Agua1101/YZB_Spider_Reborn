from apscheduler.schedulers.blocking import BlockingScheduler
from sshtunnel import SSHTunnelForwarder
from yzb_conf import config as conf
import subprocess
import sys
import os
from yzb_db_connect import *
import time
from datetime import datetime, date, timedelta


logger = Logger()

conn = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                   charset=conf.charset)


def get_process_id(name):
    child = subprocess.Popen(["pgrep","-f",name+'.py'],stdout=subprocess.PIPE,shell=False)
    response = child.communicate()[0]
    return response


def start_crawler(program_name):
    try:
        pid = get_process_id(program_name)
        # 如果不存在进程，说明程序没有启动
        if not pid:
            logger.info(program_name)
            # 启动程序
            os.system('nohup python -u {}.py >/dev/null 2> ccgp7_1.log 2>&1 &'.format(conf.crawler_file+program_name))
            logger.info('网站爬虫启动')
            pid = get_process_id(program_name)
            # print(pid)
            if pid:
                logger.info('{}启动成功'.format(program_name))

            else:
                # 不存在，则启动失败
                logger.info('pid不存在,启动失败')

        # 如果存在，说明程序已启动
        else:
            logger.info('------------------------程序已启动------------------------------------')

    except Exception as e:
        print(e)
        logger.info('----------------total error！----------------------')
        # 程序报错，启动失败


def task():
    name_list = ['request_ccgp_gov_cn4']
    for i in name_list:
        try:
            program_name = i
            start_crawler(program_name)
        except:
            logger.error('{}启动失败'.format(i))
            logger.error(sys.exc_info())




def main():
    scheduler = BlockingScheduler()

    scheduler.add_job(task, 'cron', hour=0, minute=30)
    scheduler.add_job(task, 'cron', hour=9)
    scheduler.add_job(task, 'cron', hour=12)
    scheduler.add_job(task, 'cron', hour=21)

    # print('定时任务启动！')
    logger.info('定时任务启动！')
    scheduler.start()


if __name__ == '__main__':
    main()



