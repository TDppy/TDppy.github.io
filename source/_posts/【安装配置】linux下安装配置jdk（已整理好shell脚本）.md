---
title: 【安装配置】linux下安装配置jdk（已整理好shell脚本）
date: 2026-01-11 15:30:00
categories: 安装配置
tags: [安装配置]
layout: post
---

## 本文介绍linux下安装配置java运行环境，主要涉及三个步骤，5分钟之内即可完成：

 1. 清除残存的jdk并上传我提供的jdk压缩包
 2. 配置环境变量
 3. 重新加载并测试

jdk压缩包百度网盘链接

```powershell
链接：https://pan.baidu.com/s/1hFrj97cQaj9IkgkhSNIYig 
提取码：n2vv 
复制这段内容后打开百度网盘手机App，操作更方便哦。
```
懒得看过程的可以直接复制粘贴shell脚本，👉[链接戳这](https://pasteme.cn/64312)👈

> 此外，如果您对linux下安装mysql数据库等感兴趣，可查阅博主的其他文章，如果您对文章中有所疑问，可加博主QQ2287015934交流。

**1.清除残存的jdk并上传我们的jdk**
`rpm -qa | grep java` 将找到的卸载掉。
（卸载命令 `rpm -e --nodeps 替换为找到的文件名`） 

```bash
cd /usr/local
mkdir jdk
```

将的jdk-7u75-linux-x64.tar.gz上传到jdk目录下，可用sftp实现，不再详解。
`tar -zxvf jdk-7u75-linux-x64.tar.gz` 解压上传好的jdk压缩包
出现一个新目录：jdk1.7.0_75   此时jdk已经安装好了，还需要配置环境变量。

**2.配置环境变量**

```bash
vi /etc/profile
```

在**最后面**添加：

```bash
#set java environment
JAVA_HOME=/usr/local/jdk/jdk1.7.0_75
CLASSPATH=.:$JAVA_HOME/lib.tools.jar
PATH=$JAVA_HOME/bin:$PATH
export JAVA_HOME CLASSPATH PATH
```

这里注意，java_home里替换为解压后的自己的jdk的路径，如果你是严格按照我上面讲的操作的，路径应该就是我写的那个，不用改。

**3.重新加载并且测试**

```bash
source /etc/profile    
```

这一步必须做，直接测试会不成功。

```bash
java -version
```
如果能输出java相关的版本信息，说明安装成功，可以跑java程序了。



