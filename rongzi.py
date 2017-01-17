#!/usr/bin/python
# -*- coding:utf-8 -*-

import tushare as ts
import pandas as pd
import os
from datetime import datetime

def rongzi(stockid,_start_="2016-06-30",_end_ = datetime.now().strftime('%Y-%m-%d') ): # 获取某支股票的融资数据
    rzdate=[]
    filename = "rz%s.csv" % stockid
    _date_=ts.get_k_data(stockid,_start_,_end_)["date"]
    for _d_ in _date_:
        print u"获取%s的数据" % _d_
        df = ts.sz_margin_details(_d_)
        dat = df[df.stockCode==stockid]
        if os.path.exists(filename):
            dat.to_csv(filename,mode='a',header=None,encoding="GBK")
        else:
            dat.to_csv(filename,encoding="gbk")

if __name__ == '__main__':
    rongzi("002419")