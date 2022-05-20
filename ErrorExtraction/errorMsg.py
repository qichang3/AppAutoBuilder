#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"display the extracted error messasge"
import config

errorInfo = {}
dependency_resolution_failed = False # 是否是dependecy类别的错误
task_execution_failed = False # 是否是task执行的错误
evaluate_script_problem = False #目前这个方法只关注plugin_id的解析
evaluate_project_problem = False #解析project错误
evaluate_root_project_problem = False
task_configuration_problem = False
configuring_project_problem = False
compile_build_file_failed = False
not_found_in_root_project = False
applying_plugin_request_exception = False
repository_connect_failed = False
minifiedEnabled_question = False #当build.gradle中指定MinifiedEnabled = True，即进行混淆时，会出现错误
platform_version_question = False # 目前发生在本地缺少build.gradle中指定的sdk版本时
buildtools_revision_question = False #sdk缺少指定的buildtools
ndk_version_question = False # sdk缺少指定的ndk版本
lint_found_errors = False # lint找到了代码中的错误
jvm_heap_errors = False # jvm堆容量过小导致lint无法正常执行
javaDoc_generate_failed = False # javaDoc生成失败，导致构建失败
dx_found_question = False # sdk的某个build tools缺少dx文件

def dx_found_Msg(isFound):
    if dx_found_question:
        errorInfo = {'errorType': 'dx_found_question'}
        errorInfo['errorFlg'] = isFound
        errorInfo['dx_file_path'] = config.dx_file_path
        return errorInfo

def javaDoc_generate_Msg(isFound):
    if javaDoc_generate_failed:
        errorInfo = {'errorType': 'javaDoc_generate_failed'}
        errorInfo['errorFlg'] = isFound
        return errorInfo


def jvm_heap_errors_Msg(isFound):
    if jvm_heap_errors:
        errorInfo = {'errorType': 'jvm_heap_errors'}
        errorInfo['errorFlg'] = isFound
        return errorInfo

def lint_found_errors_Msg(isFound):
    if lint_found_errors:
        errorInfo = {'errorType': 'lint_found_errors'}
        errorInfo['errorFlg'] = isFound
        return errorInfo

def mvn_repository_Msg(isFound):
    "mvnCentral在2020年后无法直接用http方式访问，因此需要使用一个指定的URL访问"
    if repository_connect_failed:
        errorInfo = {'errorType': 'repository_connect_failed'}
        errorInfo['errorFlg'] = isFound
        return errorInfo

def ndk_version_Msg(isFound):
    "ndk版本号处理"
    if ndk_version_question:
        errorInfo = {'errorType':'ndk_version_question'}
        if isFound:
            errorInfo['errorFlg'] = isFound
            errorInfo['ndk_version'] = config.ndk_version
        return errorInfo

def buildtools_version_Msg(isFound):
    "build tools 版本号处理"
    if buildtools_revision_question:
        errorInfo = {'errorType':'buildtools_revision_question'}
        if isFound:
            errorInfo['errorFlg'] = isFound
            errorInfo['build_tools_revision'] = config.build_tools_revision
        return errorInfo

def platform_version_Msg(isFound):
    "platform版本号处理"
    if platform_version_question:
        errorInfo = {'errorType':'platform_version_question'}
        if isFound:
            errorInfo['errorFlg'] = isFound
            errorInfo['platformVersion'] = config.platform_version
        return errorInfo

def minifiedEnabled_question_Msg(isFound):
    "混淆处理"
    if minifiedEnabled_question:
        errorInfo = {'errorType':'minifiedEnabled_question'}
        if isFound:
            errorInfo['errorFlg'] = isFound
        return errorInfo

def repository_connect_failed_Msg(isFound):
    "仓库地址处理"
    if repository_connect_failed:
        errorInfo =  {'errorType':'repository_connect_failed'}
        errorInfo['errorFlg'] = isFound
        if isFound:
            errorInfo['repository_name'] = config.repository_name
        return errorInfo

##############################################################################
# 以上是关于errorInfo1的函数
# 以下是关于errorInfo2的函数
##############################################################################

def applying_plugin_request_Msg(isFound):
    if applying_plugin_request_exception:
        errorInfo = {'errorType':'applying_plugin_request_exception'}
        errorInfo['errorFlg'] = isFound
        if isFound:
            errorInfo['plugin_id'] = config.plugin_id
            errorInfo['plugin_version'] = config.plugin_version
            errorInfo['plugin_class'] = config.plugin_class
        return errorInfo

def not_found_in_root_project_Msg(isFound):
    if not_found_in_root_project:
        errorInfo = {'errorType':'not_found_in_root_project'}
        errorInfo['errorFlg'] = isFound
        if isFound:
            errorInfo['project_name'] = config.project_name
            errorInfo['task_name'] = config.task_name
        return errorInfo

def dependency_resolution_Msg(isFound):
    if dependency_resolution_failed:
        errorInfo = {'errorType':'dependency_resolution_failed'}
        errorInfo['errorFlg'] = isFound
        if isFound == 3:  # find all message
            errorInfo['dependency_project'] = config.dependency_project
            errorInfo['dependency_type'] = config.dependency_type
            errorInfo['dependency_group'] = config.dependency_group
            errorInfo['dependency_name'] = config.dependency_name
            errorInfo['dependency_version'] = config.dependency_version
        elif isFound == 2:  # find dependency concrete message
            errorInfo['dependency_group'] = config.dependency_group
            errorInfo['dependency_name'] = config.dependency_name
            errorInfo['dependency_version'] = config.dependency_version
        elif isFound == 1:  # find dependency basic message
            errorInfo['dependency_project'] = config.dependency_project
            errorInfo['dependency_type'] = config.dependency_type
        elif isFound == 4:  # find artifact related message
            errorInfo['artifact_group'] = config.artifact_group
            errorInfo['artifact_name'] = config.artifact_name
            errorInfo['artifact_version'] = config.artifact_version
        elif isFound == 5:  # find project name and artifact related message
            errorInfo['dependency_project'] = config.dependency_project
            errorInfo['dependency_type'] = config.dependency_type
            errorInfo['artifact_group'] = config.artifact_group
            errorInfo['artifact_name'] = config.artifact_name
            errorInfo['artifact_version'] = config.artifact_version
        elif isFound == 6:  # find project name and artifact related message
            errorInfo['dependency_project'] = config.dependency_project
            errorInfo['dependency_type'] = config.dependency_type
            errorInfo['artifact'] = config.artifact
            errorInfo['artifact_group'] = config.artifact_group
            errorInfo['artifact_name'] = config.artifact_name
            errorInfo['artifact_version'] = config.artifact_version
        elif isFound == 8:  # find project name and confilct modules
            errorInfo['dependency_project'] = config.dependency_project
            errorInfo['dependency_type'] = config.dependency_type
            errorInfo['conflict_module1'] = config.conflict_module1
            errorInfo['conflict_module2'] = config.conflict_module2
        elif isFound == 9:
            errorInfo['project_name'] = config.project_name
            errorInfo['dependency_project'] = config.dependency_project
            errorInfo['dependency_type'] = config.dependency_type
            errorInfo['dependency_file'] = config.dependency_file
            errorInfo['dependency_group'] = config.dependency_group
            errorInfo['dependency_name'] = config.dependency_name
            errorInfo['dependency_version'] = config.dependency_version
        return errorInfo

def task_execution_Msg(isFound):
    if task_execution_failed:
        errorInfo = {'errorType': 'task_execution_failed'}
        errorInfo['errorFlg'] = isFound
        if isFound == 1:  # find project name and task name
            errorInfo['project_name'] = config.project_name
            errorInfo['task_name'] = config.task_name
        elif isFound == 2:  # just find test report file path
            errorInfo['report_file_path'] = config.report_file_path
        elif isFound == 3:  # find project name, task name and  test report file path
            errorInfo['project_name'] = config.project_name
            errorInfo['task_name'] = config.task_name
            errorInfo['report_file_path'] = config.report_file_path
        elif isFound == 4:  # find project name, task name and dependency message
            errorInfo['project_name'] = config.project_name
            errorInfo['task_name'] = config.task_name
            errorInfo['dependency_project'] = config.dependency_project
            errorInfo['dependency_type'] = config.dependency_type
            errorInfo['dependency_group'] = config.dependency_group
            errorInfo['dependency_name'] = config.dependency_name
            errorInfo['dependency_version'] = config.dependency_version
        elif isFound == 5:
            errorInfo['project_name'] = config.project_name
            errorInfo['task_name'] = config.task_name
            errorInfo['artifact_group'] = config.artifact_group
            errorInfo['artifact_name'] = config.artifact_name
            errorInfo['artifact_version'] = config.artifact_version
        elif isFound == 6:  # 与dependency中提取artifact信息的方法同步，都有两种 分别对应isFound=5 6
            errorInfo['project_name'] = config.project_name
            errorInfo['task_name'] = config.task_name
            errorInfo['artifact'] = config.artifact
            errorInfo['artifact_group'] = config.artifact_group
            errorInfo['artifact_name'] = config.artifact_name
            errorInfo['artifact_version'] = config.artifact_version
        elif isFound == 7:  # error_log16
            errorInfo['project_name'] = config.project_name
            errorInfo['property_name'] = config.property_name
            errorInfo['property_class'] = config.property_class
        elif isFound == 8:  # error_log97
            errorInfo['project_name'] = config.project_name
            errorInfo['property_name'] = config.property_name
            errorInfo['property_project'] = config.property_project
        elif isFound == 9:  # error_log155
            errorInfo['project_name'] = config.project_name
            errorInfo['task_name'] = config.task_name
            errorInfo['property_name'] = config.property_name
        return errorInfo

def evaluate_script_Msg(isFound):
    if evaluate_script_problem:
        errorInfo = {'errorType': 'evaluate_script_problem'}
        errorInfo['errorFlg'] = isFound
        if isFound == 1:
            errorInfo['plugin_id'] = config.plugin_id
        return errorInfo

def evaluate_project_Msg(isFound):
    if evaluate_project_problem:
        errorInfo = {'errorType': 'evaluate_project_problem'}
        errorInfo['errorFlg'] = isFound
        if isFound == 1:
            errorInfo['project_name'] = config.project_name
        elif isFound == 2:
            errorInfo['plugin_id'] = config.plugin_id
        elif isFound == 3:
            errorInfo['project_name'] = config.project_name
            errorInfo['plugin_id'] = config.plugin_id
        return errorInfo

def evaluate_root_project_Msg(isFound):
    if evaluate_root_project_problem:
        errorInfo = {'errorType': 'evaluate_root_project_problem'}
        errorInfo['errorFlg'] = isFound
        if isFound == 1:
            errorInfo['project_name'] = config.project_name
        elif isFound == 2:  # error_log16
            errorInfo['project_name'] = config.project_name
            errorInfo['property_name'] = config.property_name
            errorInfo['property_class'] = config.property_class
        elif isFound == 3:  # error_log97
            errorInfo['project_name'] = config.project_name
            errorInfo['property_name'] = config.property_name
            errorInfo['property_project'] = config.property_project
        elif isFound == 4:  # error_log104
            errorInfo['project_name'] = config.project_name
            errorInfo['task_name'] = config.task_name
            errorInfo['property_name'] = config.property_name
        return errorInfo

def task_configuration_Msg(isFound):
    if task_configuration_problem:
        errorInfo = {'errorType': 'task_configuration_problem'}
        errorInfo['errorFlg'] = isFound
        if isFound == 1:
            errorInfo['project_name'] = config.project_name
            errorInfo['task_name'] = config.task_name
        elif isFound == 2:
            errorInfo['project_name'] = config.project_name
            errorInfo['task_name'] = config.task_name
            errorInfo['property_list'] = config.property_list
        elif isFound == 3:
            errorInfo['project_name'] = config.project_name
            errorInfo['task_name'] = config.task_name
            errorInfo['property_name'] = config.property_name
        return errorInfo

def configuring_project_Msg(isFound):
    if configuring_project_problem:
        errorInfo = {'errorType': 'configuring_project_problem'}
        errorInfo['errorFlg'] = isFound
        # flg == 0 represent that the extraction failed
        if isFound == 1:  # just find project name
            errorInfo['project_name'] = config.project_name
        elif isFound == 2:  # find project name and dependency basic message
            errorInfo['project_name'] = config.project_name
            errorInfo['dependency_project'] = config.dependency_project
            errorInfo['dependency_type'] = config.dependency_type
        elif isFound == 3:  # find dependency concrete message, basiclly wont happen
            errorInfo['dependency_group'] = config.dependency_group
            errorInfo['dependency_name'] = config.dependency_name
            errorInfo['dependency_version'] = config.dependency_version
        elif isFound == 4:  # find project name and dependency related all message
            errorInfo['project_name'] = config.project_name
            errorInfo['dependency_project'] = config.dependency_project
            errorInfo['dependency_type'] = config.dependency_type
            errorInfo['dependency_group'] = config.dependency_group
            errorInfo['dependency_name'] = config.dependency_name
            errorInfo['dependency_version'] = config.dependency_version
        elif isFound == 5:  # just find artifact related message
            errorInfo['artifact_group'] = config.artifact_group
            errorInfo['artifact_name'] = config.artifact_name
            errorInfo['artifact_version'] = config.artifact_version
        elif isFound == 6:  # find project name and artifact related message
            # most common, cause artifact and dependency usually wont happen meanwhile
            errorInfo['project_name'] = config.project_name
            errorInfo['dependency_project'] = config.dependency_project
            errorInfo['dependency_type'] = config.dependency_type
            errorInfo['artifact_group'] = config.artifact_group
            errorInfo['artifact_name'] = config.artifact_name
            errorInfo['artifact_version'] = config.artifact_version
        elif isFound == 10:
            errorInfo['project_name'] = config.project_name
            errorInfo['dependency_project'] = config.dependency_project
            errorInfo['dependency_type'] = config.dependency_type
            errorInfo['dependency_file'] = config.dependency_file
            errorInfo['dependency_group'] = config.dependency_group
            errorInfo['dependency_name'] = config.dependency_name
            errorInfo['dependency_version'] = config.dependency_version
        elif isFound == 100:
            errorInfo['project_name'] = config.project_name
            errorInfo['build_tools_revision'] = config.build_tools_revision
        return errorInfo

def compile_build_file_Msg(isFound):
    if compile_build_file_failed:
        errorInfo = {'errorType': 'compile_build_file_failed'}
        errorInfo['errorFlg'] = isFound
        if isFound:
            errorInfo['build_file_path'] = config.build_file_path
        return errorInfo