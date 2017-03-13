# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 17:28:29 2015
@author: lenovo
"""
from datetime import datetime
import pandas as pd
import sys
from email.mime.text import MIMEText
import smtplib
"""
时间常数
"""
BASE_PATH=sys.path[0]
START='2012-01-01'
END=datetime.now().strftime('%Y-%m-%d')
_start_range = pd.date_range(start=START,periods=7)
_end_range = pd.date_range(end=END,periods=7)

_RATE_FREE_ = 0.05

###############################################
mailto_list=["3223449@qq.com"]
mail_host="smtp.tom.com"  #设置服务器
mail_user="fz.sea"    #用户名
mail_pass="boat1.2012"   #口令
mail_postfix="tom.com"  #发件箱的后缀
################################################
def send_mail(sub,content,to_list = mailto_list):  # to_list：收件人；sub：主题；content：邮件内容
    me="ITV Daily Report"+"<"+mail_user+"@"+mail_postfix+">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='utf-8')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user,mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False

"""
数据库常数
"""
_PATH_CODE_ = 'd:/data/code.csv';
_ENGINE_ = 'postgresql://postgres:root@localhost:5432/tushare'

#数据库参数信息及基础语句，pgres——test用
_DATABASE_ = 'tushare'
_USER_ =  'postgres'
_PASSWORD_ = 'root'
_HOST_ =  '127.0.0.1'

_LOG_FILENAME_ = 'logging.conf' #日志配置文件名
_LOG_CONTENT_NAME_ = 'pg_log' #日志语句提示信息

__SQL1_ = '''CREATE TABLE ts_his(
        date INTEGER,
        sv_productname VARCHAR(32)
        );'''
