# -*- coding: utf-8 -*-
"""
在股票价格创新高，同时股票价格处于低位时买入（在一年的最高价与最低价的1-0.618以下），然后持有1个月卖出
@author: zhz
"""

from pyalgotrade import plotter
from pyalgotrade.barfeed import yahoofeed
from pyalgotrade.stratanalyzer import returns,sharpe,drawdown,trades
from datetime import datetime
from matplotlib.pyplot import plot
from compiler.ast import flatten
import pyalg_test
import constant as ct
import pandas as pd
import json
import pyalg_utils,getdata
from utils import dataFramefeed

start_date="2015-01-01"
end_date="2016-01-18"

def turtle_test(code="002419"):
    filename = '%s/data/%s.csv'%(ct.BASE_PATH,code)

    #从K线数据中读取数据
    dat = pd.read_csv(filename,index_col=0,encoding='utf8')
    feed = dataFramefeed.Feed()
    dat['volume']=dat['volume']*100
    dat=dat[(dat.date>start_date) & (dat.date<end_date)]
    feed.addBarsFromDataFrame("thsc", dat)

    # Evaluate the strategy with the feed's bars.
    #myStrategy = pyalg_test.SMACrossOver(feed, "orcl", 20)
    myStrategy = pyalg_test.turtle(feed, "thsc")
    # Attach a returns analyzers to the strategy.
    returnsAnalyzer = returns.Returns()
    myStrategy.attachAnalyzer(returnsAnalyzer)

    # Attach the plotter to the strategy.
    plt = plotter.StrategyPlotter(myStrategy)
    # Plot the simple returns on each bar.
    plt.getOrCreateSubplot("returns").addDataSeries("Simple returns", returnsAnalyzer.getReturns())

    if dataString =='pyalg_util':
        ds = pyalg_utils.dataSet(myStrategy)   #抽取交易数据集语句，若使用系统自带画图功能则不需要该项
    myStrategy.run()
    myStrategy.info("Final portfolio value: $%.2f" % myStrategy.getResult())

    if dataString =='pyalg_util':
        rs = ds.getDefault()       #获取默认的交易信息，dic格式
        plot(rs["cumulativeReturns"][:,0],rs["cumulativeReturns"][:,1])  #简单作图示例

    plt.plot()


if __name__ == '__main__':
    #vwap(True)
    turtle_test()