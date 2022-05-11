#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from git import Repo
import config
import os
import sys
import urllib.request
import errorHandler
import errorMsgExtraction


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

def checkIfUrlEmpty():
    "检查用户输入的url是否为空"
    while True:
        try:
            url = input()  # read url
            urllib.request.urlopen(url)
            return url
        except Exception as err:
            print(err)
            print("the input url is invalid, please try again")

def experiment():
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
                if errorMsgExtraction.checkIfBuildSuccess():  # 执行成功
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


def main():
    print("It is a App-Auto-Builder from NWPU")
    url = input("Please enter the address of the Project: ").strip()
    if not os.path.exists(config.download_path): #项目路径MySampleDir不存在
        print("start downloading")
        Repo.clone_from(url, to_path=config.download_path)  # clone project from github
        print("download success")
    else:
        print("current project has MySampleDir!")
        print("do you want to replace old project with the new one?")
        chooseIfReplaceProject(url)
    os.chdir(config.download_path)  # move to project root directory to execute gradlew
    print("We have change to the Dir: " + os.getcwd())

    if not os.path.exists(config.gradlew_path):  # we don't process this situation
        print('the project is not complete!')
        sys.exit()
    else:
        print('file gradlew detected')
        # os.system(config.gradlew_path + ' -Dhttp.proxyHost=127.0.0.1 -Dhttp.proxyPort=7890')
        # os.system(config.gradlew_path + ' -Dhttps.proxyHost=127.0.0.1 -Dhttps.proxyPort=7890')
        while True:
            print("executing gradlew build")
            os.system(config.gradlew_path + ' build > ' + config.build_log_name + ' 2>&1')
            if errorMsgExtraction.checkIfBuildSuccess():  # 执行成功
                print("build Succeed!")
                apk_list = os.popen("find -name '*.apk'").readlines() # 查找所有以.apk结束的文件
                if len(apk_list) > 0:
                    print("apk path:")
                    for apk in apk_list: # 查找成功
                        print(os.getcwd() + apk[1:-1])
                else: # 查找失败
                    print("No Apk Generated!")
                break
            else:    # 执行失败
                print("build failed!")
                extractionStatus,errorInfo = errorMsgExtraction.errorMessageExtraction() # 抽取错误信息
                keys = list(errorInfo.keys())
                values = list(errorInfo.values())
                if extractionStatus: # 抽取成功
                    print("Extraction Succeed!")
                    # print(errorInfo)
                    fixingSuccess = errorHandler.errorHandler(errorInfo)
                    if not fixingSuccess: # 修复失败退出
                        print("Fixing Failed!")
                        break
                else: # 抽取失败退出
                    print("Extraction Failed!")
                    break
    # experiment()

if __name__ == "__main__":
    main()