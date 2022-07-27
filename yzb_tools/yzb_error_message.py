#coding=UTF-8
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
from yzb_db_connect import *
from apscheduler.schedulers.blocking import BlockingScheduler
from tools_monitor import campare
from datetime import datetime, date, timedelta
from yzb_conf import config as conf
import sys

logger = Logger()


# 邮件发送工具类
class Send_email():
    def __init__(self,from_addr='bxkf@caigou2003.com',password='Cg123456',to_addr='1137624157@qq.com',smtp_server='smtp.exmail.qq.com',main_text='这是一条测试邮件,请忽略',title='邮件的标题......',from_name='Tracer',to_name='Winston'):
        self.from_addr = from_addr
        self.password = password
        self.to_addr = to_addr
        self.smtp_server = smtp_server
        self.main_text = main_text
        self.title = title
        self.from_name = from_name
        self.to_name = to_name

    def send(self):
        try:
            # 邮件的内容
            msg = MIMEText(self.main_text, 'plain', 'utf-8')
            # [发件人的邮箱昵称、发件人邮箱账号], 昵称随便
            msg['From'] = formataddr([self.from_name, self.from_addr])
            # [收件人邮箱昵称、收件人邮箱账号], 昵称随便
            msg['To'] = formataddr([self.to_name, self.to_addr])

            # 邮件的主题，也就是邮件的标题
            msg['Subject'] = self.title

            # 备注:这里使用的是QQ邮箱的服务器, 加入用腾讯企业邮箱作为发件人的话,请将"smtp.qq.com" 修改为 "smtp.exmail.qq.com"
            # 发件人邮箱中的SMTP服务器，qq端口是465
            server = smtplib.SMTP_SSL(self.smtp_server, port=465)
            # (发件人邮箱账号、邮箱密码)
            server.login(self.from_addr, self.password)
            # (发件人邮箱账号、收件人邮箱账号、发送邮件)
            server.sendmail(self.from_addr, self.to_addr, msg.as_string())

            server.quit()  # 关闭连接
            print("邮件发送成功")
        except Exception as e:
            print("邮件发送失败: ",e)


# 中国政府采购网异常检测
def error():

    d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                   charset=conf.charset)

    yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
    try:
        error_num = d_save.select_where('data_gap','t_compare','date="{}"'.format(str(yesterday)))[0][0]
        print(error_num)
        if error_num > 500:
            main_text = '{}中国政府采购网的数据缺失太多啦！赶快去看看！'.format(yesterday)
            title = '中国政府采购网-爬虫异常'
            mail = Send_email(main_text=main_text, title=title)
            mail.send()
    except:
        logger.error(sys.exc_info())


# 中国政府采购网采购意向公开异常检测
def intention_ob():
    try:
        ccgp_count = campare.get_yxgk_count()
        yzb_count = campare.get_yxgk_yzb_count()
        yesterday = (date.today() + timedelta(days=-1)).strftime("%Y-%m-%d")
        # print(ccgp_count,'ccgp_count')
        # print(yzb_count,'yzb_count')
        if ccgp_count - yzb_count > 50:
            main_text = '{}采购意向公开的数据缺失太多啦！赶快去看看！\nccgp:{}\nyzb:{}'.format(yesterday,ccgp_count,yzb_count)
            title = '意向公开-爬虫异常'
            mail = Send_email(main_text=main_text, title=title)
            mail.send()
            print('发送成功')
    except Exception as e:
        main_text = '采购意向公开检测程序报错，请尽快修复！'
        title = '意向公开-监控异常'
        mail = Send_email(main_text=main_text, title=title)
        mail.send()
        print(e)
        logger.error(sys.exc_info())

# 其他爬虫运行状态监测
def crawler_ob():
    try:
        d_save = MySQL(host=conf.host, port=conf.port, user=conf.user, password=conf.password, db=conf.db,
                       charset=conf.charset)
        error_list = d_save.select_where('mistake_num,stop_time,website_name,id','t_website','is_timer=1')
        timeNow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        # print(timeNow)
        for i in error_list:
            try:
                website_name = i[2]
                error_count = i[0]
                id = i[3]
                now_time = time.mktime(time.strptime(timeNow, "%Y-%m-%d %H:%M:%S"))
                # if error_count > 50:
                #     main_text = '{}{}爬虫错误任务太多了！赶快去看看！一共有{}个错误'.format(timeNow, website_name,error_count)
                #     title = '其他爬虫错误任务过多'
                #     mail = Send_email(main_text=main_text, title=title)
                #     mail.send()
                #     logger.info('发送成功')
                error_date = i[1]
                if error_date:
                    error_time = time.mktime(time.strptime(error_date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))
                    # now_time = time.mktime(time.strptime(timeNow, "%Y-%m-%d %H:%M:%S"))
                    time_gap = int(now_time) - int(error_time)
                    print(time_gap)
                    if time_gap > 86400:
                        main_text = '{}{}爬虫停止运行了！赶快去看看！'.format(timeNow,website_name)
                        title = '其他爬虫停止运行'
                        mail = Send_email(main_text=main_text, title=title)
                        mail.send()
                        logger.info('发送成功')
                last_date = d_save.runSql_select('select create_time from t_website_page_{} order by id DESC limit 1'.format(id))[0][0]
                last_time = time.mktime(time.strptime(last_date.strftime("%Y-%m-%d %H:%M:%S"), "%Y-%m-%d %H:%M:%S"))
                stop_time = int(now_time) - int(last_time)
                if stop_time > 172800:
                    main_text = '{}{}爬虫很久没有新数据了！请及时检查！最新数据{}'.format(timeNow, website_name,last_date)
                    title = '无新数据'
                    mail = Send_email(main_text=main_text, title=title)
                    mail.send()
                    logger.info('发送成功')
            except:
                main_text = '爬虫监控程序运行出错了！请尽快修复！'
                title = '监控停止运行'
                mail = Send_email(main_text=main_text, title=title)
                mail.send()
                logger.error(sys.exc_info())
    except:
        main_text = '爬虫监控程序停止运行了！请尽快修复！'
        title = '监控停止运行'
        mail = Send_email(main_text=main_text, title=title)
        mail.send()
        logger.error(sys.exc_info())

        # print(error_count)
        # print(error_date)

    # print(error_list)




def main():
    error()
    intention_ob()
    crawler_ob()



if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # scheduler.add_job(error, 'cron', hour=12)
    scheduler.add_job(main, 'cron', hour=12)
    # scheduler.add_job(main, 'cron', hour=17, minute=6)
    logger.info('定时任务启动！')
    # print('定时任务启动！')
    scheduler.start()

    # error()
    # intention_ob()
    # crawler_ob()