#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

user_home = os.environ['HOME'] # env user_home
gradle_home = os.path.join(os.environ['GRADLE_HOME'], 'bin')  # you need to set GRADLE_HOME env in /etc/profile
download_path = os.path.join(user_home, 'AppAutoBuilder/MySampleDir')  # project download path
gradlew_path = os.path.join(download_path, 'gradlew')  # dir of file gradlew