#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import fileinput
import re
import config
import os

def errorHandler(errorInfo):
    "错误处理的主入口，根据errorInfo分别处理"
    fixingSuccess = True
    print("start fixing")
    if errorInfo['errorType'] == 'repository_connect_failed': #仓库连接错误
        if errorInfo['errorFlg'] == 1:
            connectTimeOutHandler(errorInfo) #修改不正确的mvn仓库地址
        elif errorInfo['errorFlg'] == 2:
            mvnRepositoryHandler(errorInfo) #mavenCentral()不支持HTTP访问，因此为它添加一个可用的URL地址
    elif errorInfo['errorType'] == 'minifiedEnabled_question': #声明混淆为true导致失败
        if errorInfo['errorFlg'] == 1:
            minifiedEnableQuestionHandler(errorInfo)
    elif errorInfo['errorType'] == 'platform_version_question': #sdk缺少build.gradle指定的platforms版本
        if errorInfo['errorFlg'] == 1:
            platformVersionHandler(errorInfo)
    elif errorInfo['errorType'] == 'buildtools_revision_question': # sdk缺少build.gradle指定的buildtools版本
        if errorInfo['errorFlg'] == 1:
            buildToolsRevisionHandler(errorInfo)
        else:
            fixingSuccess = False
    elif errorInfo['errorType'] == 'ndk_version_question':
        if errorInfo['errorFlg'] == 1:
            ndkVersionHandler(errorInfo)
    elif errorInfo['errorType'] == 'lint_found_errors':
        if errorInfo['errorFlg'] == 1:
            lintErrorsHandler(errorInfo)
    elif errorInfo['errorType'] == 'jvm_heap_errors':
        if errorInfo['errorFlg'] == 1:
            jvmHeapHandler(errorInfo)
    else:
        fixingSuccess = False
    print("fixing end")
    return fixingSuccess

def jvmHeapHandler(errorINfo):
    file = file = os.path.join(config.download_path, 'gradle.properties') # 问题项目下的gradle.properties路径
    fw = open(file, 'a')
    fw.write('org.gradle.jvmargs=-Xmx2048m\n')
    fw.close()

def lintErrorsHandler(errorInfo):
    project = errorInfo['project_name']
    file = os.path.join(config.download_path, project,'build.gradle') # 问题项目下的build.gradle路径
    fw = open(file, 'a')
    fw.write('\nandroid {\n\tlintOptions { abortOnError false }\n}')
    fw.close()

def mvnRepositoryHandler(errorInfo):
    build_gradle_list = os.popen("find -name 'build.gradle'").readlines()
    # print(build_gradle_list)
    for build_gradle in build_gradle_list:
        fr = open(build_gradle[:-1], 'r')
        lines = fr.readlines()
        fr.close()
        fw = open(build_gradle[:-1], 'w')
        for line in lines:
            if line.__contains__("mavenCentral()"):
                line = "\tmaven {url 'https://repo.maven.apache.org/maven2/'}\n" + line
                #print(line)
            fw.writelines(line)
        fw.close()

def ndkVersionHandler(errorInfo):
    "sdk缺少build.gradle指定的ndk版本，将该版本添加到本地, jdk11不可实现"
    ndkVersion = errorInfo['ndk_version']
    os.system(config.sdkmanger_home + " \"ndk;" + ndkVersion + "\"")

def buildToolsRevisionHandler(errorInfo):
    "sdk缺少build.gradle指定的buildtools版本，将该版本添加到本地，jdk11不可实现"
    buildToolsRevision = errorInfo['build_tools_revision']
    os.system(config.sdkmanger_home + " \"build-tools;" + buildToolsRevision + "\"")

def platformVersionHandler(errorInfo):
    "sdk缺少build.gradle指定的platforms版本，将该版本添加到本地，jdk11不可实现"
    hashString = errorInfo['platformVersion']
    os.system(config.sdkmanger_home + " \"platforms;" + hashString + "\"")

def minifiedEnableQuestionHandler(errorInfo):
    "build.gradle中声明混淆为true时有可能导致失败，solution是让混淆为false"
    file = os.path.join(config.download_path,errorInfo['project_name'],'build.gradle') #发生错误的项目
    fr = open(file,'r')
    lines = fr.readlines()
    fr.close()
    fw = open(file,'w')
    for line in lines:
        a = re.sub("minifyEnabled true", "minifyEnabled false", line) #替换混淆那一行
        fw.writelines(a)
    fw.close()

def connectTimeOutHandler(errorInfo):
    "因仓库地址声明错误导致无法连接，对根目录下所有build.gradle文件中关于该仓库地址声明的地方都做替换"
    repository_name = errorInfo['repository_name']
    #print(repository_name)
    replace_repository_name = ""
    if repository_name == 'maven.google.com': #原先的maven仓库地址，不可用
        replace_repository_name = 'dl.google.com/dl/android/maven2/' #替换的maven仓库地址
    build_gradle_list = os.popen("find -name 'build.gradle'").readlines()
    #print(build_gradle_list)
    for build_gradle in build_gradle_list:
        fr = open(build_gradle[:-1],'r')
        lines = fr.readlines()
        '''for i,line in enumerate(lines):
            if line.__contains__("maven.google.com"):
                print(i, line)
                '''
        fr.close()
        fw = open(build_gradle[:-1],'w')
        for line in lines:
            a = re.sub(repository_name, replace_repository_name, line)
            fw.writelines(a)
        fw.close()

