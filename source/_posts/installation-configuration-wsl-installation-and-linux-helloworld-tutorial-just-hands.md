---
title: 【安装配置】WSL安装及linux下helloworld教程（有手就行）
date: 2026-01-11 15:30:00
categories: 环境配置
tags: [WSL, Linux]
layout: post
---

先上微软商店下一个wsl  windwos subsystem linux 
（windows下的linux子系统），选择ubuntu，安装。
有的电脑下载好后启动ubuntu可能出现这个报错

```bash
Installing, this may take a few minutes...
WslRegisterDistribution failed with error: 0x8007019e
The Windows Subsystem for Linux optional component is not enabled. Please enable it and try again.
See https://aka.ms/wslinstall for details.
Press any key to continue..
```
**解决方案：**
使用Win键+x 打开Powershell(管理员) 粘贴这一段命令解决上面的报错，然后输入y回车，**注意这里回车会自动重启**

```bash
Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
```


第一次进入系统后：
设定用户名和密码（密码要输两次）

**初始化完用户名和密码要更改下默认下载源：**
linux中使用的C语言编译器是GCC，但是现在wsl里没有gcc，要安装gcc，安装软件默认从国外安装，这会导致下载的数据包有损坏，所以要更改默认下载源为国内的阿里云。下面的命令不懂没事，复制粘贴就行。
**步骤：**
修改数据源配置文件

```bash
sudo vim /etc/apt/sources.list
```

更改为阿里镜像源。
用 vim 编辑/etc/apt/sources.list 文件，可以用下面命令快捷的修改字符：

```bash
:%s/http:\/\/archive.ubuntu.com/https:\/\/mirrors.aliyun.com/
```

修改好后用:x保存并退出
最后，更新配置（更新过程中可能要按y回车确定安装）：

```bash
sudo apt update
```

```bash
sudo apt upgrade
```



**linux下如何用C写helloworld**
vi filename.c          使用vi编辑器创建一个名为filename的c语言文件
按i进入插入模式才可以编辑文档
然后写helloworld的代码

```c
#include <stido.h>
int mainO(){
printf("hello");
return 0;
}
```

按:x并回车，即保存并退出编辑器
使用gcc filename.c -o filename 编译并生成名为filename的可执行文件
例如在创建文件时使用的是vi hello.c 那么编译这个C语言源代码就用 gcc hello.c -o hello 生成了一个可执行程序hello
执行hello ，如果hello在当前目录下 就用 ./hello  回车





