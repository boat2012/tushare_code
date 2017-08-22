# -*- coding: utf-8 -*-
"""
获取股票的日线数据
下一步计划，判断数据是否已经到本地，如果到的话，不用再写
"""

import pandas as pd
import tushare as ts
import time,os,sys
import logging
import constant as ct

BASE_PATH = sys.path[0]

logging.basicConfig(format="%(asctime)s -  %(message)s",filename=BASE_PATH+"/getdata.log",level=logging.DEBUG)

def get_today():
    df = ts.get_today_all()
    oldfile=0
    newfile=0
    for index,row in df.iterrows():
        filename = '%s/data/%s.csv' % (ct.BASE_PATH,row["code"])
        stoday = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        row = row.rename({"trade":"close"})
        row_a = row[["open","close","high","low","volume","code"]].append(pd.Series([stoday],index=["date"]))

        if os.path.exists(filename):
            _data_ = pd.read_csv(filename,index_col=0,encoding='utf8')
            oldfile += 1
            print row["code"], "file loading"
        else:
            _data_ = pd.DataFrame(columns=["date","open","close","high","low","volume","code"])
            newfile += 1
            print row["code"]," file not exist."
            logging.debug("Stock %s file created." % row["code"])
        _data_ = _data_.append(row_a,ignore_index=True)
        _data_.groupby('date').apply(lambda x: x.ix[x.volume.idxmax()])
        _data_=_data_.drop_duplicates(subset='date', keep="last")
        _data_=_data_.sort_values("date")
        _data_['code']=_data_['code'].map(lambda x:str(x).zfill(6))
        _data_.to_csv(filename,encoding='utf8')
    logging.debug("Update successed. %d file alread exist, %d file created" % (oldfile,newfile))


DEBUG=True
# DEBUG=False

if __name__ == '__main__':

    if DEBUG or time.localtime(time.time()).tm_hour >= 15:
        logging.debug("gettoday计算：每日收盘开始更新")
        get_today()
    else:
        print "还没有收盘，请在15点后再运行此程序"

