#!/usr/bin/python
# -*- coding:utf-8 -*-
# 用于替换 ConfigParser中的写入函数，因为原来的不支持unicode

import codecs
import ConfigParser
import types
import sys

def ini_set(cfgfile,sec,key,value):
    config = ConfigParser.ConfigParser()
    config.readfp(codecs.open(cfgfile, "r", "utf-8"))
    try:
        config.readfp(codecs.open(cfgfile, "r", "utf-8"))
        if not config.has_section(sec):
            temp = config.add_section(sec)
        config.set(sec, key, value)
    except Exception as e:
        print("error",str(e))
    file = codecs.open(cfgfile, "w", "utf-8")
    sections=config.sections()
    for section in sections:
        #print section
        file.write("[%s]\n" % section)
        for (key, value) in config.items(section):
            if key == "__name__":
                continue
            if type(value) in (type(u'') , type('')):
                file.write(key+"="+value)
            elif type(value) == type(1):
                optStr="%s=%d"%(key,value)
                file.write(optStr)
            elif type(value) == type(1.5):
                optStr="%s=%f"%(key,value)
                file.write(optStr)
            else:
                print "do not support this type"
                print value
            file.write("\n")
    file.close()
