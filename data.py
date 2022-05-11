#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
f = open('/home/wqc/data.txt','r')
lines = f.readlines()
filedata = ""
res_list = []
for line in lines:
    line = "https://github.com/" + line
    if line not in  res_list:
        res_list.append(line)
        print(line)
        filedata += line
fp = open('/home/wqc/data1.txt','w')
fp.write(filedata)
f.close()
fp.close()