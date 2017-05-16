##  1. 准备工作

> 程序需要安装pyv8，pvy8安装可直接用二进制文件安装
>### i. 首先访问 https://github.com/emmetio/pyv8-binaries ，选择符合自己机器版本的安装包下载；

>### ii.  解压获取两个文件：一个源码文件，一个二进制动态链接库文件

>> PyV8.py
>>
>>_PyV8.so

> ### iii. 将这两个文件拷贝到python的第三方包的安装目录中

>>```bash
>>cd  pyv8  # 进入目录
>>cp  * /usr/local/lib/python2.7/site-packages/  # 复制到你的python安装目录的第三方包目录中，具体目录根据个人实际情况选择，如虚拟环境的第三方安装包目录
>>```

## 2. 安装说明


> 首先需要安装pip工具, 安装相关依赖如下
>
> **_pip install -r requirements.txt_**
> 
> 需要安装sqlite3，安装教程 http://www.runoob.com/sqlite/sqlite-installation.html

## 3. 运行说明

> 在 ./web目录下, 运行 manager.py文件, 命令如下
>
> **_python manager.py runserver_**


