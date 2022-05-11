#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import config
from git import Repo
'''f=open('/home/wqc/AppAutoBuilder/MySampleDir/Simplenote/build.gradle','r')
alllines=f.readlines()
f.close()
f=open('/home/wqc/AppAutoBuilder/MySampleDir/Simplenote/build.gradle','r')
for i, line in enumerate(alllines):
    if line.__contains__("21.0.6113669"):
        print(i, line)'''
'''for eachline in alllines:
    a=re.sub('maven.google.com','dl.google.com/dl/android/maven2/',eachline)
    f.writelines(a)
f.close()

os.system('pwd')
apk_list = os.popen("find -name apk -type d").readlines()
os.chdir(apk_list[0][0:-1])
os.system('pwd')
os.system('ls')'''
#build_gradle_list = os.popen("find -name \"*.apk\"").readlines()
#print(build_gradle_list)
#os.system('java -version')
#print(os.path.join(os.environ['ANDROID_SDK_ROOT'],'tools/bin/sdkmanager'))
'''build_gradle_list = os.popen("find -name 'build.gradle'").readlines()
for build_gradle in build_gradle_list:
    print(build_gradle)'''