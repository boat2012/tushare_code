#-*-coding=utf-8-*-
# 从ts.get_industry_classified()中取出次新股，然后找出今天已经开板的股票

import pandas as pd
import tushare as ts
import logging
from sendwx import sendwx

logging.basicConfig(format="%(asctime)s -  %(message)s",filename="/root/code/tushare_code/check_stock/check_stock.log",level=logging.DEBUG)
dat = ts.get_industry_classified()

for index,row in dat[dat.c_name==u"次新股"].iterrows() :
    mdata=ts.get_k_data(row.code)
    if len(mdata) > 2:
        if mdata.iloc[-2].high==mdata.iloc[-2].low and mdata.iloc[-1].high != mdata.iloc[-1].low :
            desp = u"股票%s昨天刚开板，最高价为%s，最低价为%s" % (mdata.iloc[-1].code,mdata.iloc[-1].high,mdata.iloc[-1].low)
            sendwx(u"新股开板",desp)
            logging.debug(desp)
