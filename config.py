#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

user_home = os.environ['HOME'] # env user_home
android_sdk_home = os.environ['ANDROID_HOME']
sdkmanger_home = os.path.join(android_sdk_home, 'tools/bin/sdkmanager')
gradle_home = os.path.join(os.environ['GRADLE_HOME'], 'bin')  # you need to set GRADLE_HOME env in /etc/profile
download_path = os.path.join(user_home, 'AppAutoBuilder/MySampleDir')  # project download path
project_path = os.path.join(user_home, 'AppAutoBuilder')
gradlew_path = os.path.join(download_path, 'gradlew')  # dir of file gradlew
settings_gradle_path = os.path.join(download_path,'settings.gradle') # path of settings.gradle
build_log_name = "app.log" # 记录build log的文件名
build_gradle_path = os.path.join(download_path, 'build.gradle')  # dir of build.gradle of root project

experiment_home = "/home/wqc/experiment/jdk1.8"

wrong_indicator = "* What went wrong:" # 错误指示头
success_indicator = "BUILD SUCCESSFUL" # 构建成功指示头
error_end_indicator = "* Try:" # 一般在错误信息结束后会出现的指示头

project_name = "root project"
task_name = "unknown task" # task名


dependency_project = "root project" # 发生依赖问题的项目
dependency_type = "" # 出现问题的依赖类别，包括test compile等
dependency_group = "" # 依赖的group
dependency_name = "" # 依赖的name
dependency_version = "" # 依赖的版本号
dependency_file = "" #依赖的具体文件名 如shadow.jar

plugin_id = "" #插件的id， 例如 Plugin with id 'nexus' not found.
plugin_version = "" #插件的版本号
plugin_class = "" #插件所在的class

property_name = "" #属性名
property_class = "" #构建时会在指定路径寻找property，本变量指示该路经，如org.gradle.api.plugins.quality.CheckstyleExtension_Decorated@6815a68d
property_project = "root project" #属性出现在哪个project中
property_list = []

report_file_path = "" # 有一种log在发生test失败后会给出报错的文件路径

build_tools_revision = "" # 关于sdk的错误，log会给出build tool的版本：failed to find Build Tools revision 19.0.3
platform_version = "" #本地找不到的sdk版本名
ndk_version = "" # 本地找不到的ndk版本

artifact_group = "" # 工件
artifact_name = ""
artifact_version = ""
artifact = ""

build_file_path = "" #构建文件如build.gradle文件的路径

conflict_module1 = "" #出现dependency问题时可能会报错：两个模块冲突，需要记录两个模块的名字
conflict_module2 = "" #例如A conflict was found between the following modules：

repository_name = "" #仓库的名字

project_list = [] # 当项目中有多个子项目时，保存这些子项目的名称


