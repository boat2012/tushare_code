# -*- coding: utf-8 -*-
"""
获取股票的日线数据
下一步计划，判断数据是否已经到本地，如果到的话，不用再写
"""

import pandas as pd
import tushare as ts
import time,os,sys
import logging


BASE_PATH = sys.path[0]

def get_today():
    print "get today"
    df = ts.get_today_all()
    for index,row in df.iterrows():
        filename = '%s/data/%s.csv' % (BASE_PATH,row["code"])
        stoday = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        row = row.rename({"trade":"close"})
        row_a = row[["open","close","high","low","volume","code"]].append(pd.Series([stoday],index=["date"]))

        if os.path.exists(filename):
            _data_ = pd.read_csv(filename,index_col=0,encoding='utf8')
            print row["code"], "file loading"
        else:
            _data_ = pd.DataFrame(columns=["date","open","close","high","low","volume","code"])
            print row["code"]," file not exist."
        _data_ = _data_.append(row_a,ignore_index=True)
        _data_.groupby('date').apply(lambda x: x.ix[x.volume.idxmax()])
        _data_=_data_.drop_duplicates(subset='date', keep="last")
        _data_=_data_.sort_values("date")
        _data_['code']=_data_['code'].astype(str)
        _data_.to_csv(filename,encoding='utf8')





if __name__ == '__main__':

    if time.localtime(time.time()).tm_hour >= 15:
        logging.basicConfig(format="%(asctime)s -  %(message)s",filename=BASE_PATH+"/getdata.log",level=logging.DEBUG)
        logging.debug("gettoday计算：每日收盘开始更新")
        get_today()
    else:
        print "还没有收盘，请在15点后再运行此程序"

