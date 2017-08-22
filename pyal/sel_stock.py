# -*- coding: utf-8 -*-

import pandas as pd
import tushare as ts
import time,os,sys
import logging


BASE_PATH = "/root/code/tushare_code/pyal"

def sel_stock() :  # 选择收盘价站在所有均线上的股票 ma5/ma10/ma20/ma30/ma60/ma120/ma250)
    xg_filename = BASE_PATH + "/" + time.strftime("%m%d") + "newhigh.csv"
    xg_filename = BASE_PATH + "/0814newhigh.csv"
    xg = pd.read_csv(xg_filename,dtype={'code': object},index_col=0,encoding='utf8')
    hy = xg["c_name"].value_counts().head(1).index[0]
    df = ts .get_today_all()
    df_r = pd.DataFrame()
    for index,row in df.iterrows():
        filename = "%s/data/%s.csv" % (BASE_PATH, row["code"])
        # _sc_ = pd.read_csv("stock_class.csv",dtype={"code":object},index_col=0,encoding="utf8")
        _sc_ =  pd.read_csv('%s/data/code.csv'% BASE_PATH,dtype={'code': object},index_col=0,encoding='utf8')
        if os.path.exists(filename):
            _data_ = pd.read_csv(filename,dtype={"code":object},index_col=0,encoding='utf8')
            _data_['code']=_data_['code'].map(lambda x : x.zfill(6))
            if len(_data_) > 120 :
                if _data_.iloc[-1].close > _data_.tail(5).close.mean() and \
                    _data_.iloc[-1].close > _data_.tail(10).close.mean() and \
                    _data_.iloc[-1].close > _data_.tail(20).close.mean() and \
                    _data_.iloc[-1].close > _data_.tail(30).close.mean() and \
                    _data_.iloc[-1].close > _data_.tail(60).close.mean() and \
                    _data_.iloc[-1].close > _data_.tail(120).close.mean() and \
                    len(_data_.iloc[-4:][_data_.close.diff()>0]) == 2 :
                    df_r=df_r.append(row)
    df_r = pd.merge(df_r,_sc_[["code","c_name"]],how="inner",on="code")
    df_re = df_r.loc[df_r['c_name']==hy]
    print len(df_r),len(df_re)    
    print df_re


if __name__ == '__main__':
    sel_stock()
