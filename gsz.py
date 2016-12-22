# -*- coding: utf-8 -*-
# In[2]:

import tushare as ts


# In[3]:

#基本面数据
basic = ts.get_stock_basics()

#行情和市值数据
hq = ts.get_today_all()


# In[4]:

#当前股价,如果停牌则设置当前价格为上一个交易日股价
hq['trade'] = hq.apply(lambda x:x.settlement if x.trade==0 else x.trade, axis=1)

#分别选取流通股本,总股本,每股公积金,每股收益,PE
basedata = basic[['outstanding', 'totals', 'reservedPerShare', 'esp', 'pe']]

#选取股票代码,名称,当前价格,总市值,流通市值
hqdata = hq[['code', 'name', 'trade', 'mktcap', 'nmc']]

#设置行情数据code为index列
hqdata = hqdata.set_index('code')

#合并两个数据表
data = basedata.merge(hqdata, left_index=True, right_index=True)


# In[5]:

# data.head(10)


# In[6]:

#将总市值和流通市值换成亿元单位
data['mktcap'] = data['mktcap'] / 10000
data['nmc'] = data['nmc'] / 10000


# In[17]:

#每股公积金>=5
#res = data.reservedPerShare >= 2
#流通股本<=2亿
out = data.outstanding <= 2
#每股收益>=5毛
eps = data.esp >= 0.5
#总市值<100亿
mktcap = data.mktcap <= 100


# In[18]:

allcrit = out & mktcap
selected = data[allcrit]


# In[19]:

df = selected[['name','trade', 'totals', 'reservedPerShare', 'outstanding', 'esp', 'mktcap', 'nmc', 'pe']]


# In[20]:

df.sort_values('trade')


# In[22]:

yg = ts.profit_data(top=300)
#yg = ts.forecast_data(2016, 4)

print(len(yg))
# In[25]:

#ygdata=yg.sort('shares', ascending=False)
ygdata=yg.sort_values('shares', ascending=False)

print(len(ygdata))
print("\n")


# In[26]:

#ygdata = yg.copy()


# In[27]:

ygdata = ygdata.set_index('code')
print(len(ygdata))


# In[28]:

ygs = df.merge(ygdata, left_index=True, right_index=True)    


# In[30]:

ygs = ygs[['name_x', 'trade', 'pe', 'outstanding', 'totals', 'reservedPerShare', 'esp', 'report_date', 'shares']]


# In[35]:
print(len(ygs))
print(ygs)
#ygs[(ygs.outstanding <= 2) & (ygs.reservedPerShare>=3) & (ygs.esp >= 0.5)].to_csv("gsz.csv")
ygs.to_csv("gsz.csv",encoding="utf8")
