#! /bin/bash
printf "Please enter the address of the project!\n"
read url
git clone $url MySampleDir
cd ./MySampleDir

#if [[ ! -f "local.properties" ]]; then
  #  echo "sdk.dir=/home/wqc/Android/Sdk" > local.properties
#fi
./gradlew assemble --info


