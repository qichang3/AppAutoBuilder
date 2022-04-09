#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from git import Repo
import config
import os
import sys



def chooseIfReplaceProject(url):
    while (True):
        changeflg = input("please input 'yes' or 'no': ")
        print(changeflg)
        if (changeflg != 'yes' and changeflg != 'no'):
            print("the input is wrong!")
            continue
        elif (changeflg == "yes"):
            Repo.clone_from(url, to_path=config.download_path)  # clone project from github
            break
        else:
            print("using the existing project as MySampleDir")
            break


def main():
    print("It is a App-Auto-Builder from NWPU")
    print("Please enter the address of the Project!")
    url = input()  # read url
    if (not os.path.exists(config.download_path)):
        Repo.clone_from(url, to_path=config.download_path)  # clone project from github
    else:
        print("current project has MySampleDir!")
        print("do you want to replace old project with the new one?")
        chooseIfReplaceProject(url)

    os.chdir(config.download_path)  # move to project root directory to execute gradlew
    print("We have change to the Dir: " + os.getcwd())

    if (not os.path.exists(config.gradlew_path)):  # we dont process this situation
        print('the project is not complete!')
        sys.exit()
    else:
        print('file gradlew detected')
        print("executing gradlew assemble")
        # print(gradlew_path)
        os.system(config.gradlew_path + ' assemble --quiet >app.log 2>&1')
        

        # settingGradleFile = os.getcwd() + '/settings.gradle' # dir of settings.gradle
        # if not os.path.exists(settingGradleFile):
        #    createSettingGradleFile(settingGradleFile)
        # os.system(gradle_home + '/gradle init')
        # os.system(gradlew_path + ' build')










def createSettingGradleFile(settingGradleFile):  # create file settings.gradle
    # print('test1')
    filename = input('please input the name of project: ')  # get the name of the project to create settings.gradle

    if not os.path.exists(os.getcwd() + '/' + filename):
        return

    f = open(settingGradleFile, 'w')
    # print('include ' + '\':' + filename + '\'')
    f.write('include ' + '\':' + filename + '\'')
    f.close()

if __name__ == "__main__":
    main()