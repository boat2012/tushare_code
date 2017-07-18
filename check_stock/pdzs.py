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
import ConfigParser

sys.path.append(".")
T = 20
zspool={u"中小板指":"399005",
        u"创业板指":"399006",
        u"上证50":"000016",
        u"批发零售":"399236",
        u"中证500":"000905"}

def horl(data): #判断最近是多还是空，反回多空，日期，指数值
    for i in range(len(data)):
        high = max(data['high'].iloc[-T-i-1:-i-1])
        low = min(data['low'].iloc[-int(T/2)-i-1:-i-1])
        if data.iloc[-i-1]['high'] >= high:
            return u"多",data.iloc[-i-1].date,data.iloc[-i-1]['high']
        elif data.iloc[-i-1]['low'] <= low:
            return u"空",data.iloc[-i-1].date,data.iloc[-i-1]['low']

			
SENDWX = False  # 选项，是否用方糖公众号发微信信息
datafile = "/root/code/tushare_code/check_stock/wxinfo.ini"
cfgfile = "E:/code/tushare_code/check_stock/wxinfo.ini"

def main():
    desp=""
    logging.basicConfig(format="%(asctime)s -  %(message)s",filename="E:/code/tushare_code/check_stock/check_stock.log",level=logging.DEBUG)
    conf = ConfigParser.ConfigParser()
    conf.read(cfgfile)
    retmsg = ""
    for zs in zspool:
        # print zs,zspool[zs]
        df=ts.get_k_data(zspool[zs],index=True)
        result,date,zsvalue=horl(df)
        logging.debug(u"指数计算，指数%s,%s,日期：%s,%s" % (zs,result,date,zsvalue))
        retmsg = retmsg + u"%s指数"%date + (u"%s一(%s一)%s一%s\n" % (zs,zspool[zs],result,zsvalue))
		
        if SENDWX :
            sendwx(u"%s指数"%date,u"%s一(%s一)%s一%s" % (zs,zspool[zs],result,zsvalue))
    conf.set("pdzs","info",retmsg.encode("GBK"))
    conf.write(open(cfgfile,"w"))
	
if __name__ == '__main__':
    main()
