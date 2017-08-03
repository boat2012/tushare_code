# -*- coding: utf-8 -*-
"""
获取股票的日线数据
下一步计划，判断数据是否已经到本地，如果到的话，不用再写
"""

import pandas as pd
import tushare as ts
import time
import logging
import constant as ct


def get_today():
    print "get today"
    df = ts.get_today_all()
    for index,row in df.iterrows():
        print row


if __name__ == '__main__':

    if time.localtime(time.time()).tm_hour >= 15:
        logging.basicConfig(format="%(asctime)s -  %(message)s",filename=ct.BASE_PATH+"/getdata.log",level=logging.DEBUG)
        logging.debug("gettoday计算：每日收盘开始更新")
        get_today()
    else:
        print "还没有收盘，请在15点后再运行此程序"

