#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from git import Repo

from BuildCheck import buildSuccessCheck
import config
import os
import sys
import urllib.request
from ErrorHandler import errorHandler
from ErrorExtraction import errorMsgExtraction


def chooseIfReplaceProject(url):
    "询问用户是否用新url中的项目替换现有项目"
    while (True):
        changeflg = input("please input 'yes' or 'no': ")
        if (changeflg != 'yes' and changeflg != 'no'):
            print("the input is wrong!")
            continue
        elif (changeflg == "yes"):
            os.system('rm -rf ./MySampleDir')
            print("start downloading")
            Repo.clone_from(url, to_path=config.download_path)  # clone project from github
            print("download success")
            break
        else:
            print("using the existing project as MySampleDir")
            break

def checkIfUrlValid():
    "检查用户输入的url是否可用"
    while True:
        try:
            url = input("Please enter the address of the Project: ").strip() # read url
            urllib.request.urlopen(url)
            return url
        except Exception as err:
            # print(err)
            print("the input url is invalid, please try again")

def downloadProject():
    url = checkIfUrlValid()
    if not os.path.exists(config.download_path):  # 项目路径MySampleDir不存在
        print("start downloading")
        Repo.clone_from(url, to_path=config.download_path)  # clone project from github
        print("download success")
    else:
        print("current project has MySampleDir!")
        print("do you want to replace old project with the new one?")
        chooseIfReplaceProject(url)
    os.chdir(config.download_path)  # move to project root directory to execute gradlew
    os.system('rm -rf ' + config.build_result)
    os.mkdir(config.build_result)
    os.mkdir(config.apk_result)
    os.mkdir(config.errorlog_result)
    print("We have change to the Dir: " + os.getcwd())
    if os.path.exists(os.path.join(config.download_path, '.gitmodules')):
        os.system("git submodule update --init --recursive")  # 下载子模块

def appAutoBuilder():
    print('file gradlew detected')
    flg = 1
    while True:
        print("executing gradlew assemble")
        os.system(config.gradlew_path + ' assemble > ' + config.build_log_name + ' 2>&1')
        if buildSuccessCheck.checkIfBuildSuccess():  # 执行成功
            print("assemble Succeed!")
            apk_list = os.popen("find -name '*.apk'").readlines()  # 查找所有以.apk结束的文件
            if len(apk_list) > 0:
                for apk in apk_list:  # 查找成功
                    apk = os.getcwd() + apk[1:-1]
                    os.system('cp ' + apk + ' ' + config.apk_result)
            else:  # 查找失败
                print("No Apk Generated!")
            break
        else:  # 执行失败
            print("assemble failed!")
            extractionStatus, errorLog, errorInfo = errorMsgExtraction.errorMessageExtraction()  # 抽取错误信息
            file = os.path.join(config.errorlog_result, 'errorLog' + str(flg) + '.txt')
            f = open(file, 'w')
            f.writelines(errorLog) # 保存错误日志
            if extractionStatus:  # 抽取成功
                print("Extraction Succeed!")
                f.write(str(errorInfo)) # 保存提取出的错误信息
                fixingSuccess = errorHandler.errorHandler(errorInfo)
                if not fixingSuccess:  # 修复失败退出
                    print("Fixing Failed!")
                    break
            else:  # 抽取失败退出
                print("Extraction Failed!")
                break
            f.close()
            flg = flg + 1

def main():
    print("It is a App-Auto-Builder from NWPU")
    downloadProject()
    if not os.path.exists(config.gradlew_path):  # we don't process this situation
        print('the project is not complete!')
        sys.exit()
    else:
        appAutoBuilder()

if __name__ == "__main__":
    main()