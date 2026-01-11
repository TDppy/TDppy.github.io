---
title: 【安装配置】WSL虚拟机导出、导入镜像（涉及到docker无法在wsl下使用的问题）
date: 2026-01-11 15:30:00
categories: 环境配置
tags: [WSL, Linux]
layout: post
---
# 背景
WSL（Windows Subsystem Linux），是微软提供的在Windows下便携地使用Linux系统的方式，它支持使用虚拟化技术（也就是要在bios和控制面板中开启虚拟化支持），完美支持Ubuntu和Windows文件系统之间的使用。相比于VMware，速度更快。

本文主要介绍将已有的wsl环境导出为.tar格式的镜像文件，然后通过U盘或者网盘将tar文件发给另一台电脑，在另一台电脑上只需要导入tar包，无需重新安装和配置环境，就可以无缝衔接工作。（~~主要是我们组没服务器~~ ）

# DOS脚本
在已有wsl的主机上打开windows cmd命令行，

```bash
 wsl --export Ubuntu-22.04 file_path
 # 导出wsl tar镜像    例如我这里filepath写的是D:\chisel_env\wsl_pkg\Ubuntu2204.tar        
```
导出完成如图所示：
![在这里插入图片描述](/images/3ee876f0bfaf012ed6b8f246c001f744.png)
在要安装wsl的主机上打开windows cmd命令行，


设置wsl默认是版本2，否则导入后是版本1。由于wsl1没有彻底的虚拟化，无法使用docker命令
```bash
wsl --set-default 2
```
              
导入wsl镜像 其中Distro是Ubuntu-22.04 installLocation是目标安装位置，提供个文件夹路径就行  FileName是tar所在的位置
```bash 
wsl --import <Distro> <InstallLocation> <FileName> [Options]   
```

列出当前电脑中的wsl及其版本（检查是否为wsl2）
```bash
wsl -l -v    
```

然后就可以再直接开始使用了


