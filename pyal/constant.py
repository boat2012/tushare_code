# -*- coding: utf-8 -*-
"""
Created on Sat Aug 01 17:28:29 2015
@author: lenovo
"""
from datetime import datetime
import pandas as pd
import sys
"""
时间常数
"""
BASE_PATH=sys.path[0]
START='2012-01-01'
END=datetime.now().strftime('%Y-%m-%d')
_start_range = pd.date_range(start=START,periods=7)
_end_range = pd.date_range(end=END,periods=7)

_RATE_FREE_ = 0.05



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