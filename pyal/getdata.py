# -*- coding: utf-8 -*-
"""
获取股票的日线数据
"""

import sys

# import pylab as plt
import pandas as pd
import tushare as ts
import numpy as np
import constant as ct
import time,os
from pandas import DataFrame
from datetime import datetime



universe = ['002419']

def save_data():
    dat = ts.get_industry_classified()
    dat = dat.drop_duplicates('code')
    dat.to_csv('%s/data/code.csv'% ct.BASE_PATH,encoding='utf8')
    inuse = []

    i = 0
    for code in dat['code'].values:
        i+= 1
        print i,code
        print ct.END
        try:
            if not os.path.exists('%s/data/%s.csv'%(ct.BASE_PATH,code)):
                _data_ = ts.get_k_data(code,start=START,end=END)  #默认取3年，code为str，start无效的,start 和end若当天有数据则全都取
                _data_['code']=_data_['code'].astype(str)
                if _data_ is not None:
                    _data_.to_csv('%s/data/%s.csv'%(ct.BASE_PATH,code),encoding='utf8')
                    if _data_.index[0] in ct._start_range and _data_.index[-1] in ct._end_range:                          #筛选一次代码，使用头尾都包含的代码
                        inuse.append(code)
        except IOError:
            pass    #不行的话还是continue
    _df_inuse = DataFrame(inuse,columns={'code'})
    _df_inuse.to_csv('%s/data/code_inuse.csv' % ct.BASE_PATH,encoding='utf8')

#从网络中更新数据,code 必须为str，dat中的为int
def refresh_data(_start_=ct.END,_end_=ct.END):
    dat = pd.read_csv('%s/data/code.csv'% ct.BASE_PATH,dtype={'code': object},index_col=0,encoding='utf8')
    # inuse = pd.read_csv('d:/data/code_inuse.csv',index_col=0,parse_dates=[0],encoding='gbk')
    # new_inuse = []
    # universe = ['002419']
    i=0
    for code in dat['code'].values:
        i+= 1
        print i,code
        try:
            filename = '%s/data/%s.csv'%(ct.BASE_PATH,code)
            _data_ = ts.get_k_data(str(code),_start_,_end_)
            if _data_ is not None and _data_.size != 0:
                if os.path.exists(filename):
                    olddata = pd.read_csv(filename,index_col=0,encoding='utf8')
                    _data_ = pd.concat([_data_,olddata])
                    _data_.groupby('date').apply(lambda x: x.ix[x.volume.idxmax()])
                    _data_=_data_.drop_duplicates(subset='date', keep="last")
                    _data_=_data_.sort_values("date")
                    _data_['code']=_data_['code'].astype(str)
                    _data_.to_csv(filename,encoding='utf8')
                else:
                    _data_.to_csv(filename,encoding='utf8')
        except IOError:
            pass    #不行的话还是continue




if __name__ == '__main__':
    #save_data()
    refresh_data(_start_='2017-01-18')