# AppAutoBuilder

AppAutoBuilder是一个面向Android移动应用的自动化构建工具，可以接收用户输入的GitHub仓库地址，对Android项目进行自动化构建，并最终返回生成的Apk文件。

## 环境

1. 在**Linux**操作系统上运行

   AppAutoBuilder的开发环境为Ubuntu20.04 LTS，**暂不支持Windows环境**。

2. 需要提前配置**Python3.8**环境

   AppAutoBuilder的开发语言为**Python3.8**

3. 需要提前配置**Android SDK**环境

   SDK环境是构建Android项目必不可少的环境之一，您需要在Linux本地配置SDK环境，**并将SDK主目录地址设置为环境变量ANDROID_HOME**

## 项目下载

您需要将完整AppAutoBuilder项目下载到Linux的**用户主目录home**下，例如在用户主目录下运行命令行：

```shell
git clone https://github.com/Achilles0321/AppAutoBuilder
```
下载后的项目如图所示：

![](https://github.com/Achilles0321/photoForMarkDown/raw/main/AppAutoBuilder/%E9%A1%B9%E7%9B%AE%E4%B8%8B%E8%BD%BD.png)

##  运行项目

使用PyCharm等IDE打开项目，并打开Builder目录下的AppAutoBuilder.py文件，运行其main函数：

![](https://github.com/Achilles0321/photoForMarkDown/raw/main/AppAutoBuilder/main.png)

或者使用命令行运行，在AppAutoBuilder目录下打开命令行运行如下命令：

```shell
python
from Builder import AppAutoBuilder
AppAutoBuilder.main()

```
## 输入

您需要根据提示输入所要构建的项目GitHub地址，请确保输入的地址**正确无误**，例如https://github.com/federicoiosue/Omni-Notes

AppAutoBuilder会将目标项目下载到AppAutoBuilder项目目录下并命名为**MySampleDir**


当AppAutoBuilder目录下无目标项目时，直接输入GitHub地址：

![](https://github.com/Achilles0321/photoForMarkDown/raw/main/AppAutoBuilder/%E6%97%A0%E9%A1%B9%E7%9B%AE%E8%BE%93%E5%85%A5.png)

为了连续多次构建以及方便用户手动修复错误，AppAutoBuilder不主动删除目标项目目录，当工具目录下存在MySampleDir目录时，又用户决定是否用输入的目标项目地址替换原有项目，输入yes则替换原有项目，输入no则直接使用原有项目进行构建：

![](https://github.com/Achilles0321/photoForMarkDown/raw/main/AppAutoBuilder/%E6%8E%A5%E6%94%B6%E8%BE%93%E5%85%A5%E4%B8%8B%E8%BD%BD%E9%A1%B9%E7%9B%AE.png)

## 输出

在项目下载成功后，AppAutoBuilder开始对项目进行构建，如果项目最终构建成功，则**返回构建过程所生成的apk**，如果项目构建失败，AppAutoBuilder会对项目进行修复，并对**错误日志和抽取结果进行记录**，当最终构建成功或判断修复失败时，AppAutoBuilder退出，将所有结果保存在MySampleDir目录下的result文件夹中。

![](https://github.com/Achilles0321/photoForMarkDown/raw/main/AppAutoBuilder/result%E6%96%87%E4%BB%B6%E5%A4%B9.png)

其中apk文件夹保存构建所生成的apk文件，errorLog目录记录修复过程中Gradle生成的错误日志及AppAutoBuilder对应的抽取结果，如下图所示：

![](https://github.com/Achilles0321/photoForMarkDown/raw/main/AppAutoBuilder/errorlog1andresult.png)

当最终构建失败并且无apk生成时，您可以通过最后一个错误日志提供的信息尝试手动修复错误。




