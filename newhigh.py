#-*-coding=utf-8-*-  
__author__ = 'rocky'  
#获取破指定天数内的新高 比如破60日新高  
import tushare as ts  
import datetime
import time
import os
info=ts.get_stock_basics()  
filename=time.strftime("%m%d")+u"新高股票.csv"
def loop_all_stocks():
    print u"总共有",len(info),u"支股票\n"
    i = 0
    for EachStockID in info.index:
         i = i + 1;
         if is_break_high(EachStockID,60):  
             print u"第",i,u"支股票High price on",
             print EachStockID,  
             print info.ix[EachStockID]['name'].decode('utf-8')
             if os.path.exists(filename):
                info.ix[EachStockID].to_frame(name=EachStockID).T.to_csv(filename, mode='a', encoding="utf8",header=None)
             else:
                info.ix[EachStockID].to_frame(name=EachStockID).T.to_csv(filename,encoding="utf8")

  
  
def is_break_high(stockID,days):  
    end_day=datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)  
    days=days*7/5  
    #考虑到周六日非交易  
    start_day=end_day-datetime.timedelta(days)  
  
    start_day=start_day.strftime("%Y-%m-%d")  
    end_day=end_day.strftime("%Y-%m-%d")  
    df=ts.get_k_data(stockID,start=start_day,end=end_day)  
    if len(df) > 30 :   # 上市一个月以内的不考虑
        period_high=df['high'].max()
        #print period_high
        today_high=df.iloc[-1]['high']
        #这里不能直接用 .values
        #如果用的df【：1】 就需要用.values
        #print today_high
        if today_high>=period_high:
            return True
        else:
            return False
    else:
        return False
  
loop_all_stocks()  
