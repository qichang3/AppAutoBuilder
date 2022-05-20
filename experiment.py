#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from git import Repo

import ErrorExtraction
from BuildCheck import buildSuccessCheck
import config
import os
from ErrorHandler import errorHandler
from ErrorExtraction import errorMsgExtraction


def experiment1():
    buildSuccess = []
    extractSuccess = []
    extractFailure = []
    for id in range(1, 176):
        file = "/home/wqc/experiment/errorlog/error_log" + str(id) + ".txt"
        if buildSuccessCheck.checkIfBuildSuccess(file):
            buildSuccess.append(id)
        else:
            extractionStatus, errorInfo = ErrorExtraction.errorMsgExtraction(file)
            if extractionStatus:
                extractSuccess.append(id)
            else:
                extractFailure.append(id)
    print("build success number = " + str(len(buildSuccess)))
    buildFailureNum = 175 - len(buildSuccess)
    print("build failure number = " + str(buildFailureNum))
    print("extraction success number = " + str(len(extractSuccess)))
    print("extraction failure number = " + str(len(extractFailure)))
    print("accuracy = " + str(float(len(extractSuccess)) / float(buildFailureNum)))
    print("extraction failure id = " + str(extractFailure))

def experiment2():
    f = open('/home/wqc/experiment/data/data0509.txt', 'r')
    lines = f.readlines()
    f.close()
    for line in lines:
        url = line[:-1]
        project = url.split("/")[-1]
        print(url)
        os.chdir(config.project_path)
        os.system("pwd")
        os.system('rm -rf ./MySampleDir')
        print("start downloading")
        Repo.clone_from(url, to_path=config.download_path)  # clone project from github
        print("download success")
        os.chdir(config.download_path)  # move to project root directory to execute gradlew
        if not os.path.exists(config.gradlew_path):  # we don't process this situation
            print('the project is not complete!')
            continue
        else:
            flg = 1
            print('file gradlew detected')
            while True:
                print("executing gradlew build")
                file = os.path.join(config.experiment_home, project + str(flg) + '.txt')
                os.system(config.gradlew_path + ' build > ' + config.build_log_name + ' 2>&1')
                f = open(config.build_log_name,'r')
                lines = f.readlines()
                f.close()
                f = open(file,'w')
                for line in lines:
                    f.write(line)
                f.close()
                flg = flg + 1
                if buildSuccessCheck.checkIfBuildSuccess():  # 执行成功
                    print("build Succeed!")
                    apk_list = os.popen("find -name '*.apk'").readlines()  # 查找所有以.apk结束的文件
                    if len(apk_list) > 0:
                        print("apk path:")
                        for apk in apk_list:  # 查找成功
                            print(os.getcwd() + apk[1:-1])
                    else:  # 查找失败
                        print("No Apk Generated!")
                    break
                else:  # 执行失败
                    print("build failed!")
                    extractionStatus, errorInfo = errorMsgExtraction.errorMessageExtraction()  # 抽取错误信息
                    keys = list(errorInfo.keys())
                    values = list(errorInfo.values())
                    if extractionStatus:  # 抽取成功
                        print("Extraction Succeed!")
                        # print(errorInfo)
                        fixingSuccess = errorHandler.errorHandler(errorInfo)
                        if not fixingSuccess:  # 修复失败退出
                            print("Fixing Failed!")
                            break
                    else:  # 抽取失败退出
                        print("Extraction Failed!")
                        break

if __name__ == "__main__":
    experiment1()