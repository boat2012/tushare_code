#!/usr/bin/python
# -*- coding:utf-8 -*-
#  检查两天以内新出的股东人数报表，打印出符合以下条件的：
#  一、 股东人数减少超过20%的。
#  二、 股东人数减少超过10%，但近几次记录表示股东人数持续下降的
__author__ = 'zhenghz'
import logging
import re
import json
import os
import pandas as pd
import numpy as np
import datetime
import ConfigParser
import codecs
from ini_set import ini_set

linuxpath = "/root/code/tushare_code/check_stock/"
logpath = "/root/code/tushare_code/check_stock/"
winpath = "C:/Code/tushare_code/check_stock/"
csvfile=linuxpath + "gdrs.csv"
cfgfile = "/root/www/webpy/wxinfo.ini"
SENDWX = False  # 选项，是否用方糖公众号发微信信息

gdrs_dtype={"SecurityCode": object,
      "SecurityName": object,
      "LatestPrice":np.float32,
       "PriceChangeRate":np.float32,
       "HolderNum" : np.int32,
       "PreviousHolderNum" : np.int32,
       "HolderNumChange" : np.int32,
       "HolderNumChangeRate" : np.float32,
       "RangeChangeRate" : np.float32,
       "EndDate" : object,
       "PreviousEndDate" : object,
       "HolderAvgCapitalisation" : np.float32,
       "HolderAvgStockQuantity" : np.float32,
       "TotalCapitalisation" : np.float32,
       "CapitalStock" :np.float32,
       "NoticeDate": object}

def check_gd():
    logging.basicConfig(format="gdrs: %(asctime)s -  %(message)s",filename=logpath + "pdzs.log",level=logging.DEBUG)
    logging.debug("开始")
    # conf = ConfigParser.SafeConfigParser()
    # with codecs.open(cfgfile,'r',encoding="utf-8") as f:
    #    conf.readfp(f)

    today = str(datetime.date.today()-datetime.timedelta(days=2))[0:10]
    df= pd.read_csv(csvfile,index_col=0,dtype=gdrs_dtype,encoding="utf8")
    df_filter = df[(df.NoticeDate>=today) & (df.HolderNumChangeRate<-20)]
    msg = ""
    for index,row in df_filter.iterrows():
         msg = msg + u"%s(%s)，%s股东比%s减少了%.2f%%;" % (row.SecurityName,row.SecurityCode,
                 row.EndDate[5:],row.PreviousEndDate[5:],row.HolderNumChangeRate)
        # msg = msg + u"股票%s(%s)于%s公告，截止到%s为止，股东人数比%s减少了%.2f%%;" % (row.SecurityName,row.SecurityCode,
        #       row.NoticeDate,row.EndDate,row.PreviousEndDate,row.HolderNumChangeRate)
        # msg =  u"股票"
    ini_set(cfgfile,"gdrs","todayinfo",msg)
    ini_set(cfgfile,"gdrs","date",str(datetime.date.today())[0:10])


if __name__ == '__main__':
    check_gd()
