#!/usr/bin/python
# -*- coding:utf-8 -*-

import urllib2
from urllib import quote

def sendwx(title,desp):  # 标题是title ， 内容放在desp中
    url = u"http://sc.ftqq.com/SCU3876Tadcf6e52a9017dfde92f73604d477230582c3ffe9d618.send?text=%s&desp=%s"
    req = urllib2.Request( url % (quote(title),quote(desp)))
    res_data = urllib2.urlopen(req)
    res=res_data.read()
    # print res

if __name__ == '__main__':
    content = "测试"
    desp="2\.1\.2.3.3.2.2"
    sendwx(content,desp)
