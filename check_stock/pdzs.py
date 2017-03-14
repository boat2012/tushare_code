#!/usr/bin/python
# -*- coding:utf-8 -*-
# 用海龟判断指数目前处于多还是空
# 判断二十天新高与十天新低哪一个离今天比较近，如果二十天新高近，则多，如果十天新低近，则空


__author__ = 'zhenghz'
import tushare as ts
import ConfigParser
from sendwx import sendwx
from cncurrency import cncurrency
import logging
import sys

T = 20
zspool={"中小板指":"399005",
        "创业板指":"399006",
        "上证50":"000016",
        "中证500":"000905"}

def horl(data): #判断最近是多还是空，反回多空，日期，指数值
    for i in range(len(data)):
        high = max(data['high'].iloc[-T-i-1:-i-1])
        low = min(data['low'].iloc[-int(T/2)-i-1:-i-1])
        if data.iloc[-i-1]['high'] >= high:
            return u"多",data.iloc[-i-1].date,data.iloc[-i-1]['high']
        elif data.iloc[-i-1]['low'] <= low:
            return u"空",data.iloc[-i-1].date,data.iloc[-i-1]['low']

def main():
    desp=""
    logging.basicConfig(format="%(asctime)s -  %(message)s",filename="/root/code/tushare_code/check_stock/check_stock.log",level=logging.DEBUG)
    for zs in zspool:
        print zs,zspool[zs]
        df=ts.get_k_data(zspool[zs],index=True)
        result,date,zsvalue=horl(df)
        logging.debug("指数计算，指数%s,%s,日期：%s,%s" % (zspool[zs],result,date,zsvalue))
        desp=desp+"指数计算，指数%s,%s,日期：%s,%s\n" % (zspool[zs],result,date,zsvalue)
    sendwx(title,desp)

if __name__ == '__main__':
    main()