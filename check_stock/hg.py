#!/usr/bin/python
# -*- coding:utf-8 -*-
# 根据海龟原则，计算股票的买入卖出上下限，然后更新stock.ini文件

import tushare as ts
import numpy as np
import ConfigParser
import logging
sz = ts.get_k_data("sh")
last_date=sz.iloc[-1].date
def CalcATR(data):
    TR_List=[]
    for i in range(1,21):
        TR=max(data['high'].iloc[-i]-data['low'].iloc[-i],abs(data['high'].iloc[-i]-data['close'].iloc[-i-1]),abs(data['close'].iloc[-i-1]-data['low'].iloc[-i]))
        TR_List.append(TR)
    ATR=np.array(TR_List).mean()
    return ATR     
    
def qujian(data,T):
    return max(data['high'].iloc[-T-1:-1]),min(data['low'].iloc[-int(T/2)-1:-1])
     
def CalcUnit(perVAlue,ATR):
    return int((perValue/ATR)/100)*100
    
def calc_hg(stockid): # 计算股票的上下限并返回
    df=ts.get_k_data(stockid)
    if df.iloc[-1].date == last_date:
        high,low=qujian(df,20)
    else:
        high,low=0,0
    return high,low

if __name__ == '__main__':

    logging.basicConfig(format="%(asctime)s -  %(message)s",filename="check_stock.log",level=logging.DEBUG)
    Config = ConfigParser.ConfigParser()
    Config.read("stock.ini")
    cfgfile=open("stock.ini",'w')
    for stockid in Config.sections():
        high,low=calc_hg(stockid)
        if high != 0:
            Config.set(stockid,"high",high)
            Config.set(stockid,"low",low)
            logging.debug("计算：股票%s: 上限%s, 下限%s" % (stockid,high,low))
    Config.write(cfgfile)
    cfgfile.close()
    logging.debug("计算：每日收盘更新完毕")

    