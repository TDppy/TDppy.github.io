---
title: 【安装配置】双系统(Win10+Ubuntu)安装方法
date: 2022-07-29 00:06:01
categories: 环境配置
tags: [Windows, 双系统]
layout: post
---

(双系统安装方法)

> 在阅读ubuntu官网的教程并实践后，我成功将自己的win10主机加上了Ubuntu操作系统，实现了开机自由选择win或linux系统。**本教程较为简略，详情请参照参考文献中的官方文档！！**

为了实现该目标，我们需要的软硬件包括：
硬件： 
1.win10电脑一台(或Mac)，具有30G以上空闲磁盘空间。 
2.U盘一个，具有8G以上空闲空间(可能5G也行 建议8G) 
软件： 
1.ubuntu的镜像文件 
2.利用ubuntu镜像制作U盘引导软件(bootable usb stick)的转换软件 

## 第一步，
我们需要下载ubuntu的iso镜像文件到本地， 
[ubuntu-22.04-desktop-amd64.iso下载地址](https://ubuntu.com/download/desktop/thank-you?version=22.04&architecture=amd64)   
## 第二步，
下载镜像-U盘引导的转换软件balenaEtcher-Portable-1.7.9.exe 
[balenaEtcher-Portable-1.7.9.exe 下载地址](https://github.com/balena-io/etcher/releases/download/v1.7.9/balenaEtcher-Portable-1.7.9.exe?d_id=cfc647f4-dee2-44d9-a0f6-7cc0b6a63d23R)
## 第三步，
插入U盘，利用Balena转换软件，将iso镜像文件一键flash到U盘中 
这里**务必注意备份U盘中已有的内容，因为该过程会将U盘清空**，最终只剩下ubuntu的系统引导文件！！！ 
 {% asset_img 1.png   %} 

## 第四步，
关机，在启动时进入bios界面，选择U盘引导 
在这里有两个问题，
一是不同品牌电脑进入bios方式不同，我的联想是在出现lenovo图标时按下F12键，
二是我的电脑需要关闭rst模式才能装ubuntu，其他电脑我不清楚。
## 第五步，
到这里基本上是按照提示下一步下一步即可，
最终可以在开机自由选择系统。
 {% asset_img 2.png   %} 

## 参考文献： 
1.ubuntu系统官方安装教程 
[https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview](https://ubuntu.com/tutorials/install-ubuntu-desktop#1-overview) 
2.双系统安装教程 
[https://medium.com/linuxforeveryone/how-to-install-ubuntu-20-04-and-dual-boot-alongside-windows-10-323a85271a73](https://medium.com/linuxforeveryone/how-to-install-ubuntu-20-04-and-dual-boot-alongside-windows-10-323a85271a73)
