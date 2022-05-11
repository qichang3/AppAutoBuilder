#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import config
import re
import errorMsg


def getLastError(sublinelist):
    "抽取error log中最后一个以>开头的error信息"
    wrongLineList = []
    for line in sublinelist:
        if line.strip().startswith(">"):
            # print(line.strip()[1:].strip())
            wrongLineList.append(line.strip()[1:].strip())
    # line = sublinelist[0]
    line = None
    if len(wrongLineList) > 0:
        line = wrongLineList[-1]
    return line

def getErrorLog(linelist):
    "从build log中把error log部分抽取出来"
    isWrongIndicatorFound = False
    startLineno = 1  # record the line of the wrong indicator
    for line in linelist:  # 依次读取每行
        line = line.strip()  # 去掉每行头尾空白
        if line.__contains__(config.wrong_indicator):  # find wrong indicator
            isWrongIndicatorFound = True
            break
        startLineno += 1
    endLineno = startLineno
    for line in linelist[endLineno:]:
        if line.__contains__(config.error_end_indicator):  # find wrong indicator
            break
        endLineno += 1
    return isWrongIndicatorFound, linelist[startLineno:endLineno]

def extractLastError(lastError):
    "从最后一个error信息中提取信息"
    isFound = 0  # isFound = 0 represent that the extraction failed
    errorInfo1 = {}
    if lastError.__contains__("failed: connect timed out"):
        errorMsg.repository_connect_failed = True
        isFound = connectTimeOut(lastError)
        errorInfo1 = errorMsg.repository_connect_failed_Msg(isFound)

    elif lastError.__contains__("sentry") and lastError.__contains__("finished with non-zero exit value 1"):
        errorMsg.minifiedEnabled_question = True
        isFound = 1
        errorInfo1 = errorMsg.minifiedEnabled_question_Msg(isFound)

    elif lastError.__contains__("failed to find target with hash string"):
        errorMsg.platform_version_question = True
        isFound = platformVersionFinding(lastError)
        errorInfo1 = errorMsg.platform_version_Msg(isFound)

    elif lastError.__contains__("failed to find Build Tools revision"):
        errorMsg.buildtools_revision_question = True
        isFound = buildtoolsRevivionFinding(lastError)
        errorInfo1 = errorMsg.buildtools_version_Msg(isFound)

    elif lastError.__contains__("No version of NDK matched the requested version"):
        errorMsg.ndk_version_question = True
        isFound = ndkVersionFinding(lastError)
        errorInfo1 = errorMsg.ndk_version_Msg(isFound)

    elif lastError.__contains__("Received status code 501 from server: HTTPS Required"):
        errorMsg.repository_connect_failed = True
        isFound = 2
        errorInfo1 = errorMsg.mvn_repository_Msg(isFound)

    elif lastError.__contains__("Lint found errors in the project; aborting build."):
        errorMsg.lint_found_errors = True
        isFound = 1
        errorInfo1 = errorMsg.lint_found_errors_Msg(isFound)

    elif lastError.__contains__("Lint infrastructure error"):
        errorMsg.jvm_heap_errors = True
        isFound = 1
        errorInfo1 = errorMsg.jvm_heap_errors_Msg(isFound)
    return errorInfo1

def extractErrorLog(sublinelist):
    "根据error log第一行提取一些信息"
    isFound = 0  # isFound = 0 represent that the extraction failed
    errorInfo2 = {}
    firstline = sublinelist[0]
    #print(firstline)
    if (firstline.__contains__("Execution failed for task") or
          firstline.__contains__("Could not evaluate onlyIf predicate for task") or
          firstline.__contains__("Could not determine the dependencies of task")):
        errorMsg.task_execution_failed = True
        isFound = extractProjectAndTask(sublinelist)
        errorInfo2 = errorMsg.task_execution_Msg(isFound)

    elif firstline.__contains__("Could not resolve all dependencies for configuration"):
        errorMsg.dependency_resolution_failed = True
        isFound = extractDependency(sublinelist)
        errorInfo2 = errorMsg.dependency_resolution_Msg(isFound)

    elif (firstline.__contains__("Some problems were found with the configuration of task") or
          firstline.__contains__("A problem was found with the configuration of task")):  # error_log116
        errorMsg.task_configuration_problem = True
        isFound = configurationOfTask(sublinelist)
        errorInfo2 = errorMsg.task_configuration_Msg(isFound)

    elif firstline.__contains__("A problem occurred evaluating script"):
        errorMsg.evaluate_script_problem = True
        isFound = evaluateScript(sublinelist)
        errorInfo2 = errorMsg.evaluate_script_Msg(isFound)

    elif firstline.__contains__("A problem occurred evaluating project"):
        errorMsg.evaluate_project_problem = True
        isFound = evaluateProject(sublinelist)
        errorInfo2 = errorMsg.evaluate_project_Msg(isFound)

    elif firstline.__contains__("A problem occurred evaluating root project"):
        errorMsg.evaluate_root_project_problem = True
        isFound = evaluateRootProject(sublinelist)
        errorInfo2 = errorMsg.evaluate_root_project_Msg(isFound)

    elif (firstline.__contains__("A problem occurred configuring root project") or
          firstline.__contains__("A problem occurred configuring project")):
        errorMsg.configuring_project_problem = True
        isFound = configuringRootProject(sublinelist)
        errorInfo2 = errorMsg.configuring_project_Msg(isFound)

    elif firstline.__contains__("Could not compile build file"):  # error_log113
        errorMsg.compile_build_file_failed = True
        config.build_file_path = firstline.split(" ")[-1][1:-3]
        isFound = True
        errorInfo2 = errorMsg.compile_build_file_Msg(isFound)

    elif firstline.__contains__("not found in root project"):
        errorMsg.not_found_in_root_project = True
        isFound = notFoundInRootProject(sublinelist)
        errorInfo2 = errorMsg.not_found_in_root_project_Msg(isFound)

    elif firstline.__contains__("An exception occurred applying plugin request"):  # error_log152
        errorMsg.applying_plugin_request_exception = True
        isFound = applyingPluginRequest(sublinelist)
        errorInfo2 = errorMsg.applying_plugin_request_Msg(isFound)

    elif firstline.__contains__("JVM garbage collector thrashing and after running out of JVM memory"):
        errorMsg.jvm_heap_errors = True
        isFound = 1
        errorInfo2 = errorMsg.jvm_heap_errors_Msg(isFound)
    return errorInfo2

def errorMessageExtraction():
    "this function extract the key messages from the build log"
    # print("test1")

    extractionStatus = False
    errorInfo = {}
    f = open(config.build_log_name, 'r')  # open file
    linelist = f.readlines()
    f.close()
    isWrongIndicatorFound, errorLog = getErrorLog(linelist)
    isFound = False
    if isWrongIndicatorFound:
        sublinelist = errorLog # the sub set of linelist continue from the next line of wrong indicator
        print("error log:")
        for line in sublinelist:
            print(line,end='')
        errorInfo2 = extractErrorLog(sublinelist)
        print('errorInfo2 = ', errorInfo2)
        errorInfo.update(errorInfo2)
        lastError = getLastError(sublinelist)
        if lastError != None:
            print('lastError = ' + lastError)
            errorInfo1 = extractLastError(lastError)
            print('errorInfo1 = ', errorInfo1)
            errorInfo.update(errorInfo1)
        else:
            print("lastError is None")
        if errorInfo != {}:
            isFound = errorInfo['errorFlg']
            print('errorInfo = ',errorInfo)
        if isFound:
            extractionStatus = True
        f.close()
    return extractionStatus,errorInfo

def ndkVersionFinding(lastError):
    "从lastError中抽取ndk版本号"
    isFound = 0
    ndkVersion = re.search("No version of NDK matched the requested version (.*)\. ", lastError, flags=0)
    if ndkVersion != None:
        config.ndk_version = ndkVersion.group().strip().split(" ")[-1][:-1]
        isFound = 1
    return isFound

def buildtoolsRevivionFinding(lastError):
    "从lastError中抽取sdk的build tools版本号"
    config.build_tools_revision = lastError.split(" ")[-1]
    isFound = 1
    return 1

def platformVersionFinding(lastError):
    "从lastError中抽取platform版本号，例如android-21"
    isFound = 0
    platformVersion = re.search("'([^\"]*)'", lastError, flags=0)
    if platformVersion != None:
        config.platform_version = platformVersion.group()[1:-1]
        isFound = 1
    return isFound

def connectTimeOut(lastError):
    "仓库连接超时时，抽取仓库地址，用于后续替换该地址"
    isFound = 0
    repository_name = re.search("\[(.*)\]", lastError, flags=0)
    if repository_name != None:
        config.repository_name = repository_name.group()[1:-1].split('/')[0]
        # print(config.repository_name)
        isFound = 1
    return isFound


def applyingPluginRequest(sublinelist):
    "An exception occurred applying plugin request"

    isFound = 0
    plugin_id = re.search("id: '([^\"\']*)'", sublinelist[0], flags=0)
    plugin_version = re.search("version: '([^\"\']*)'", sublinelist[0], flags=0)
    if plugin_id != None:
        config.plugin_id = plugin_id.group().split(" ")[-1][1:-1]
    if plugin_version != None:
        config.plugin_version = plugin_version.group().split(" ")[-1][1:-1]
    for line in sublinelist:
        if line.__contains__("Failed to apply plugin"):
            plugin_class = re.search("class '([^\"\']*)'", line, flags=0)
            if plugin_class != None:
                config.plugin_class = plugin_class.group()[1:-1]
                isFound = 1
    return isFound


def configurationOfTask(sublinelist):
    "Some problems were found with the configuration of task"
    isFound = 0
    project_name = ""
    task_name = ""
    property_list = []
    projectAndTask = re.search("'([^\"]*)'", sublinelist[0], flags=0)
    if projectAndTask != None:
        # print("2")
        tokens = (projectAndTask.group())[1:-1].split(":") # 项目名和任务名
        if len(tokens) > 1:
            for token in tokens[0:-1]:
                if tokens.index(token) > 1:
                    project_name = project_name + os.sep + token
                else:
                    project_name = project_name + token
            task_name = tokens[-1]
        if project_name != "":
            # print(project_name)
            config.project_name = project_name
        if task_name != "":
            # print(task_name)
            config.task_name = task_name
        isFound = 1
    for line in sublinelist[1:]: #从第二行开始搜索
        if line.__contains__("No value has been specified for property "):
            property = re.search("'([^\"]*)'", line, flags=0)
            if property != None:
                # print(property.group()[1:-1])
                property_list.append(property.group()[1:-1]) # property名
    if len(property_list) > 1:  # error_log103 出现多个property名，组织成列表
        config.property_list = property_list
        isFound = 2
    elif len(property_list) == 1: # 出现一个property名，单独抽取
        config.property_name = property_list[0]
        isFound = 3
    return isFound


def notFoundInRootProject(sublinelist):
    # extract project and task name from error log when situation in error_log50
    isFound = False
    taskAndProject = re.findall("'([^\"\']*)'", sublinelist[0], flags=0)
    if len(taskAndProject) > 1:
        config.task_name = taskAndProject[0]
        config.project_name = taskAndProject[1]  #
        isFound = True
    return isFound


def evaluateRootProject(sublinelist):
    isFound = 0
    project_name = re.search("'([^\"]*)'", sublinelist[0], flags=0) # 抽取第一行中出现的项目名
    if project_name != None:
        config.project_name = project_name.group()[1:-1]
        isFound = 1
    if sublinelist[1].__contains__("Could not find property"):  # error_log16 and error_log97 第二行出现的情况之一
        property_name = re.findall("'([^\"\']*)'", sublinelist[1], flags=0)
        if len(property_name) == 1: # 只出现一个property
            config.property_name = property_name[0] # property名
            config.property_class = sublinelist[1].split(" ")[-1][:-2] # property路径
            isFound = 2
        elif len(property_name) == 2:
            if sublinelist[1].__contains__("on root project"):
                config.property_name = property_name[0]
                config.property_project = property_name[1] # 没有给出property路径，而是给出property所在的项目
                isFound = 3
            elif sublinelist[1].__contains__("on task"):
                config.property_name = property_name[0]
                config.task_name = property_name[1].split(":")[-1] # 给出property所在的任务
                isFound = 4
    elif sublinelist[1].__contains__("No such property"): # 第二行出现的情况之一
        tokens = sublinelist[1].split(": ")
        if len(tokens) > 2:
            config.property_name = tokens[-2].split(" ")[0]
            config.property_class = tokens[-1][:-1]
            isFound = 2
    return isFound


def configuringRootProject(sublinelist):
    "extract project name and dependency-related message from error log"
    flg = 0
    project = re.search("'([^\"]*)'", sublinelist[0], flags=0)
    if project != None:
        config.project_name = project.group()[1:-1].split(":")[-1]
        flg = 1
    if sublinelist[1].__contains__("Could not resolve all dependencies for configuration"):
        ifDependencyFound = extractDependency(sublinelist[1:])
        if ifDependencyFound:
            flg = ifDependencyFound + 1
    elif sublinelist[1].__contains__("failed to find Build Tools revision"):  # error_log23
        config.build_tools_revision = sublinelist[1].split(" ")[-1][:-1]
        flg = 100
    elif sublinelist[1].__contains__("Failed to notify project evaluation listener"):
        if sublinelist[2].__contains__("Could not resolve all dependencies for configuration"):
            ifDependencyFound = extractDependency(sublinelist[2:])
            if ifDependencyFound:
                flg = ifDependencyFound + 1
    return flg


def evaluateProject(sublinelist):
    "extract project name from error log"
    isFound = 0
    project = re.search("'([^\"]*)'", sublinelist[0], flags=0)
    if project != None:
        config.project_name = project.group()[1:-1].split(":")[-1]
        isFound = 1
    for line in sublinelist[1:]:
        if line.__contains__("> Plugin with id"):
            pluginId = re.search("'([^\"]*)'", line, flags=0)
            if pluginId != None:
                plugin_id = pluginId.group()[1:-1]
                if plugin_id != "":
                    config.plugin_id = plugin_id
                    isFound = isFound + 2
    return isFound


def evaluateScript(sublinelist):
    "extract id of the plugin from error log"
    isFound = 0
    plugin_id = ""
    for line in sublinelist[1:]:
        if line.__contains__("> Plugin with id"):
            pluginId = re.search("'([^\"]*)'", line, flags=0)
            if pluginId != None:
                plugin_id = pluginId.group()[1:-1]
                if plugin_id != "":
                    config.plugin_id = plugin_id
                    isFound = 1
    return isFound


def extractProjectAndTask(sublinelist):
    "extract project name and task name from error log"
    # print("1")
    isFound = 0
    project_name = ""
    task_name = ""
    projectAndTask = re.search("'([^\"]*)'", sublinelist[0], flags=0)
    if projectAndTask != None:
        #print("2")
        tokens = (projectAndTask.group())[1:-1].split(":")
        if len(tokens) > 1:
            for token in tokens[0:-1]:
                if tokens.index(token) > 1:
                    project_name = project_name + os.sep + token
                else:
                    project_name = project_name + token
            task_name = tokens[-1]
        if project_name != "":
            # print(project_name)
            config.project_name = project_name
        if task_name != "":
            # print(task_name)
            config.task_name = task_name
        isFound = 1
    for line in sublinelist[1:]:
        if (line.__contains__("There were failing tests.") or
                line.__contains__("Checkstyle rule violations were found")):
            config.report_file_path = line.split(" ")[-1][:-1]
            isFound = isFound + 2  # isFound为2或3
            break
        elif (line.__contains__("Could not resolve all dependencies for configuration") or
              line.__contains__("Could not resolve all task dependencies for configuration") or
              line.__contains__("Could not resolve all artifacts for configuration")):
            extractDependency(sublinelist[1:])
            isFound = 4
            break
    if sublinelist[1].__contains__("Could not download artifact"):  # artifact related message error_log95
        artifact_group = ""
        artifact_name = ""
        artifact_version = ""
        artifact = re.search("'([^\"]*)'", sublinelist[1], flags=0)
        if artifact != None:
            haveArtifact = False
            if artifact.group().__contains__(" "):  # error_log95
                artifactAndTokens = artifact.group().split(" ")
                config.artifact = artifactAndTokens[0][1:]
                tokens = artifactAndTokens[-1][1:-2].split(":")
                haveArtifact = True
                isFound = 6
            else:
                isFound = 5
                tokens = (artifact.group())[1:-1].split(":")
            if len(tokens) > 1:
                for token in tokens[0:-2]:
                    if tokens.index(token) > 0:
                        artifact_group = artifact_group + ":" + token
                    else:
                        artifact_group = artifact_group + token
                if not haveArtifact:
                    artifact_version = tokens[-2]
                    artifact_name = tokens[-1]
                else:
                    artifact_version = tokens[-1]
                    artifact_name = tokens[-2]
            if artifact_group != "":
                config.artifact_group = artifact_group
            if artifact_name != "":
                config.artifact_name = artifact_name
            if artifact_version != "":
                config.artifact_version = artifact_version

    elif sublinelist[1].__contains__("Could not find property"):  # error_log_155
        property_name = re.findall("'([^\"\']*)'", sublinelist[1], flags=0)
        if len(property_name) == 1:
            config.property_name = property_name[0]
            config.property_class = sublinelist[1].split(" ")[-1][:-2]
            isFound = 7
        elif len(property_name) == 2:
            if sublinelist[1].__contains__("on root project"):
                config.property_name = property_name[0]
                config.property_project = property_name[1]
                isFound = 8
            elif sublinelist[1].__contains__("on task"):
                config.property_name = property_name[0]
                config.task_name = property_name[1].split(":")[-1]
                isFound = 9
    return isFound


def extractDependency(sublinelist):
    "extract dependency related message from error log"

    isFound = 0
    dependency_project = ""
    dependency_type = ""
    artifact_group = ""
    artifact_name = ""
    artifact_version = ""
    firstLine = sublinelist[0]
    dependencyProjectAndDependency = re.search("'([^\"]*)'", firstLine, flags=0)
    if dependencyProjectAndDependency != None:
        tokens = (dependencyProjectAndDependency.group())[1:-1].split(":")
        if len(tokens) > 1:
            for token in tokens[0:-1]:
                if tokens.index(token) > 1:
                    dependency_project = dependency_project + os.sep + token
                else:
                    dependency_project = dependency_project + token
            dependency_type = tokens[-1]
        if dependency_project != "":
            config.dependency_project = dependency_project
        else:
            config.dependency_project = config.project_name
            # print("library_name = " + library_name)
        if dependency_type != "":
            config.dependency_type = dependency_type
            # print("dependency_type = " + dependency_type)
        isFound = 1  # find dependency basic message: project and dependency_type
    for line in sublinelist[1:]:
        if (line.__contains__("> Could not find") or
                line.__contains__("Could not resolve")):  # find dependency concrete message
            dependency = (line.split(" ")[-1])[:-2].split(":")
            if len(dependency) > 2:
                config.dependency_group = dependency[0]
                config.dependency_name = dependency[1]
                config.dependency_version = dependency[2]
                isFound = isFound + 2  # isFound can be 2 or 3
            break
    if sublinelist[1].__contains__("Could not download artifact"):  # artifact related message
        artifact = re.search("'([^\"]*)'", sublinelist[1], flags=0)
        hasArtifact = False
        if artifact != None:
            if artifact.group().__contains__(" "):  # error_log101
                hasArtifact = True
                artifactAndTokens = artifact.group().split(" ")  # 同时出现artifact名字和其完整格式
                config.artifact = artifactAndTokens[0][1:]
                tokens = artifactAndTokens[-1][1:-2].split(":")
                isFound = 6
            else:  # error_log91
                isFound = 5
                tokens = (artifact.group())[1:-1].split(":")  # artifact完整格式 error_log29 32 91
            if len(tokens) > 1:
                for token in tokens[0:-2]:
                    if tokens.index(token) > 0:
                        artifact_group = artifact_group + ":" + token
                    else:
                        artifact_group = artifact_group + token
            if (hasArtifact):
                artifact_version = tokens[-1]
                artifact_name = tokens[-2]
            else:
                artifact_version = tokens[-2]
                artifact_name = tokens[-1]
            if artifact_group != "":
                config.artifact_group = artifact_group
            if artifact_name != "":
                config.artifact_name = artifact_name
            if artifact_version != "":
                config.artifact_version = artifact_version
            # isFound can be  4 5 (6 7), in these situations: 5 is the most common scenario, 6 7 will not happen basiclly
    elif sublinelist[1].__contains__("A conflict was found between the following modules"):
        config.conflict_module1 = sublinelist[2].split("-")[-1].strip()
        config.conflict_module2 = sublinelist[3].split("-")[-1].strip()
        isFound = 8  # isFound can be 4 or 5
    elif sublinelist[1].__contains__("Could not download"):  # error_log161
        tokens = sublinelist[1].split(" ")
        if len(tokens) > 2:
            config.dependency_file = tokens[-2]
            dependency = tokens[-1][1:-2].split(":")
            if len(dependency) > 2:
                config.dependency_group = dependency[0]
                config.dependency_name = dependency[1]
                config.dependency_version = dependency[2]
                isFound = 9
    return isFound

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
