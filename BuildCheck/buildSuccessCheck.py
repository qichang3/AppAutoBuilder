#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import config

def checkIfBuildSuccess():
    "check if the build process succeed"
    flg = False
    f = open(config.build_log_name, 'r')
    linelist = f.readlines()
    for line in linelist:  # 依次读取每行
        line = line.strip()  # 去掉每行头尾空白
        if line.__contains__(config.success_indicator):  # find success message
            flg = True
            break
    f.close()
    return flg
