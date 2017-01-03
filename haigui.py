#!/usr/bin/python
# -*- coding:utf-8 -*-
# ����

import tushare as ts
import numpy as np

def CalcATR(data):
    TR_List=[]
    for i in range(0,20):
        TR=max(data['high'].iloc[i]-data['low'].iloc[i],abs(data['high'].iloc[i]-data['close'].iloc[i-1]),abs(data['close'].iloc[i-1]-data['low'].iloc[i]))
        TR_List.append(TR)
    ATR=np.array(TR_List).mean()
    return ATR     
    
def qujian(data,T):
    return max(data['high'].iloc[0:T]),min(data['low'].iloc[0:int(T/2)])
     
def CalcUnit(perVAlue,ATR):
    return int((perValue/ATR)/100)*100
    
def haigui(stockid):
    df=ts.get_hist_data(stockid)
    high,low=qujian(df,20)
    price = df['close'].iloc[0]
    atr = CalcATR(df)
    unit = int((3000/atr)/100)*100
    print "Ŀǰ��λ��%.2f������������%.2f������������%.2f" % (price,high,low)
    print "��������Ϊ��%.2f������Ĳ�λΪ��%d��" % (atr,unit)
    
if __name__ == '__main__':
    haigui("002419")
    