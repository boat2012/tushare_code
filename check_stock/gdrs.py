#!/usr/bin/python
# -*- coding:utf-8 -*-
# 获得股东人数
# 数据来源：http://data.eastmoney.com/gdhs/0.html
# 数据来源：    URL="http://data.eastmoney.com/DataCenter_V3/gdhs/GetList.ashx?reportdate=&market=&changerate=="\
#    "&range==&pagesize=50&page=%d"\  这个是页数
#    "&sortRule=-1&sortType=NoticeDate&js=var%%20eITCKUoP&param=&rt=49980681"

__author__ = 'zhenghz'

import logging
import re
import json
import os
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
import pandas as pd
import numpy as np


GDRS_COLS = ["SecurityCode","SecurityName","LatestPrice","PriceChangeRate","HolderNum",
             "PreviousHolderNum","HolderNumChange","HolderNumChangeRate","RangeChangeRate",
             "EndDate","PreviousEndDate","HolderAvgCapitalisation","HolderAvgStockQuantity",
             "TotalCapitalisation","CapitalStock","NoticeDate"]  # 来源于页面上的数据列
gdrs_dtype={"SecurityCode": object,
      "SecurityName": object,
      "LatestPrice":np.float32,
       "PriceChangeRate":np.float32,
       "HolderNum" : np.int32,
       "PreviousHolderNum" : np.int32,
       "HolderNumChange" : np.int32,
       "HolderNumChangeRate" : np.float32,
       "RangeChangeRate" : np.float32,
       "EndDate" : object,
       "PreviousEndDate" : object,
       "HolderAvgCapitalisation" : np.float32,
       "HolderAvgStockQuantity" : np.float32,
       "TotalCapitalisation" : np.float32,
       "CapitalStock" :np.float32,
       "NoticeDate": object}  # 数据类型

filename=u"C:/Code/tushare_code/check_stock/股东人数.csv"
excelfile="C:/Code/tushare_code/check_stock/gdrs.xlsx"
tempfile="C:/Code/tushare_code/check_stock/temp.xlsx"
csvfile="/root/code/tushare_code/check_stock/gdrs.csv"
# csvfile="/root/code/tushare_code/check_stock/gdrs.csv"

def _read_gdrs_json(pageNum=1):
    URL="http://data.eastmoney.com/DataCenter_V3/gdhs/GetList.ashx?reportdate=&market=&changerate=="\
    "&range==&pagesize=50&page=%d"\
    "&sortRule=-1&sortType=NoticeDate&js=var%%20eITCKUoP&param=&rt=49980681"
    cururl=URL%pageNum
    print "get data from:", cururl
    try:
        request = Request(cururl)
        text = urlopen(request, timeout=10).read()
        text = text.decode('GBK')
        lines=text.split('=')
        data = "=".join(lines[1:])
        dj = json.loads(data)
        df = pd.DataFrame(dj['data'],columns=GDRS_COLS)
        df['EndDate']=df['EndDate'].map(lambda x: x[0:10])
        df['NoticeDate']=df['NoticeDate'].map(lambda x: x[0:10])
        df['PreviousEndDate']=df['PreviousEndDate'].map(lambda x: x[0:10])
        df["SecurityCode"]=df["SecurityCode"].map(lambda x:str(x).zfill(6))
        # df.to_csv(filename,encoding='UTF8')
        return df
        # print df
    except:
        pass

def main():
    # URL = "http://data.eastmoney.com/gdhs/0.html"
    # URL="http://data.eastmoney.com/DataCenter_V3/gdhs/GetList.ashx?reportdate=&market=&changerate==&range==&pagesize=50&page=1&sortRule=-1&sortType=NoticeDate&js=var%20eITCKUoP&param=&rt=49980681"

    logging.basicConfig(format="gdrs: %(asctime)s -  %(message)s",filename="/root/code/tushare_code/check_stock/mylog.log",level=logging.DEBUG)
    logging.debug("开始")
    df = pd.DataFrame(columns=GDRS_COLS)
    for pageNum in range(1,6):
        print "parse page:", pageNum
        df=pd.concat([df,_read_gdrs_json(pageNum)])
        print "record readed:", len(df)
    if os.path.exists(csvfile):
        olddata = pd.read_csv(csvfile,index_col=0,dtype=gdrs_dtype,encoding="UTF8")
        df = pd.concat([df,olddata])
        df = df.drop_duplicates(subset=['SecurityCode','NoticeDate'],keep='last')
        print "total record:", len(df)
    df["SecurityCode"]=df["SecurityCode"].map(lambda x:str(x).zfill(6))
    df = df.fillna(0)
    # df["TotalCapitalisation"]=df["TotalCapitalisation"].astype(float)
    # df["CapitalStock"]=df["CapitalStock"].astype(float)
    df = df.sort_values("NoticeDate",ascending=False)
    df.index=range(1,len(df)+1)
    # df.fillna(0)
    # df["HolderNumChangeRate"]=df["HolderNumChangeRate"] # .astype(float)/100
    # df["RangeChangeRate"]=df["RangeChangeRate"]
    '''    wb=load_workbook(tempfile)
    ws=wb['Sheet0']
    rows = dataframe_to_rows(df)
    for r_idx, row in enumerate(rows, 1):
        for c_idx, value in enumerate(row, 1):
             ws.cell(row=r_idx, column=c_idx, value=value)
    wb.save(excelfile)'''

    logging.debug("total length: %s" % len(df))
    df.to_csv(csvfile,encoding="utf8")


if __name__ == '__main__':
    main()
