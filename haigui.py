﻿#!/usr/bin/python
# -*- coding:utf-8 -*-
# 海龟

import tushare as ts
import numpy as np
import sys
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
    
def haigui(stockid,pri=False): # pri为true 就不管有没有符合突破条件就都打印出来
    logging.basicConfig(format="%(asctime)s -  %(message)s",filename="check_stock.log",level=logging.DEBUG)
    df=ts.get_k_data(stockid)
    if df.iloc[-1].date == last_date:
        high,low=qujian(df,20)
        price = df['close'].iloc[-1]
        atr = CalcATR(df)
        unit = int((3000/atr)/100)*100
        logging.debug(last_date)
        if pri:
            print last_date
            print "股票%s目前价位是%.2f，买入上限是%.2f，卖出下限是%.2f" % (stockid,price,high,low)
            print "波动幅度为：%.2f，买入的仓位为：%d股" % (atr,unit)
            logging.debug("股票%s目前价位是%.2f，买入上限是%.2f，卖出下限是%.2f" % (stockid,price,high,low))
            logging.debug("波动幅度为：%.2f，买入的仓位为：%d股" % (atr,unit))
        if price > high:
            print "股票%s目前价位是%.2f，可以买入，买入上限是%.2f，卖出下限是%.2f" % (stockid,price,high,low)
            print "波动幅度为：%.2f，买入的仓位为：%d股" % (atr,unit)
            logging.debug("股票%s目前价位是%.2f，可以买入，买入上限是%.2f，卖出下限是%.2f" % (stockid,price,high,low))
            logging.debug("波动幅度为：%.2f，买入的仓位为：%d股" % (atr,unit))
        if price < low:
            print "股票%s目前价位是%.2f，应该卖出，买入上限是%.2f，卖出下限是%.2f" % (stockid,price,high,low)
            print "波动幅度为：%.2f，买入的仓位为：%d股" % (atr,unit)
            logging.debug("股票%s目前价位是%.2f，应该卖出，买入上限是%.2f，卖出下限是%.2f" % (stockid,price,high,low))
            logging.debug("波动幅度为：%.2f，买入的仓位为：%d股" % (atr,unit))    
    
if __name__ == '__main__':
    #universe = ['000995', '000611','300029', '002801', '300519', '300268', '002109', '600603', '600306', '603909']
    universe = ['000001', '000002', '000009', '000039', '000060', '000061', '000063', '000069', '000157', '000402', '000425', '000568', '000625', '000630', '000651', '000709', '000778', '000792', '000800', '000858', '600000', '600009', '600010', '600015', '600016', '600019', '600028', '600029', '600030', '600031', '600036', '600050', '600085', '600100', '600104', '600153', '600170', '600177', '600188', '600196', '600221', '600256', '600309', '600362', '600519', '600583', '600585', '600649', '600660', '600690', '600739', '600741', '600795', '600839', '600900', '000538', '002024', '000768', '600383', '600271', '600415', '600875', '601988', '601006', '601398', '600048', '600066', '600068', '600118', '600150', '600489', '600547', '601111', '601628', '601166', '601318', '601600', '601998', '601328', '000876', '600208', '600837', '601333', '601088', '601857', '000338', '000423', '000895', '002142', '600089', '600109', '600111', '601009', '601169', '000686', '000728', '000783', '002202', '600804', '601390', '601601', '601866', '601939', '000100', '000623', '600588', '600674', '601186', '601899', '601958', '600352', '600518', '600718', '601766', '002007', '600369', '601618', '601668', '002304', '600999', '601607', '601688', '601888', '601989', '601288', '000776', '002146', '002385', '002415', '600115', '600276', '600406', '600535', '600703', '600887', '600893', '601818', '002500', '601018', '601118', '601377', '601933', '002594', '600252', '600372', '600783', '600873', '601258', '000725', '002081', '002241', '600827', '601336', '601555', '601633', '601669', '601901', '601928', '000750', '002236', '002673', '600157', '600340', '600637', '600886', '601800', '000156', '000963', '002450', '600060', '600332', '603993', '000333', '000793', '000826', '002065', '002129', '002230', '002456', '600008', '600018', '600648', '600663', '600688', '600705', '603000', '000027', '000413', '000503', '000917', '002008', '002252', '002292', '002465', '002470', '002475', '600023', '600867', '601216', '601225', '000559', '002153', '300015', '300017', '300024', '300027', '300058', '300070', '300124', '300133', '300146', '300251', '600038', '600373', '600485', '600570', '601727', '000166', '000738', '000712', '002736', '300002', '300059', '300104', '600005', '600958', '601021', '601099', '601788', '601919', '000415', '000540', '002195', '002739', '300144', '300315', '600021', '600820', '600895', '600959', '601198', '601211', '601608', '601718', '601872', '601985', '603885', '001979', '000839', '000977', '002027', '002152', '002183', '002424', '002568', '300085', '300168', '600037', '600061', '600074', '600376', '600446', '600582', '600606', '600666', '600685', '600704', '600737', '600816', '600871', '000008', '000555', '000627', '000671', '000718', '000938', '000983', '002049', '002074', '002085', '002131', '002174', '002299', '002310', '002426', '002466', '002714', '002797', '300033', '300072', '300182', '600297', '600482', '600498', '600654', '600754', '601127', '601155', '601611', '601877']
    #universe = ['002419']
    if sys.argv[1] :
       haigui(sys.argv[1],pri=True)
    else:       
       for i in universe:
           haigui(i,pri=False)
    