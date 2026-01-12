---
title: 【环境配置】基于Docker配置Chisel-Bootcamp环境
date: 2026-01-11 15:30:00
categories: 
tags: []
layout: post
---
@[TOC]
## Chisel是什么
Chisel是Scala语言的一个库，可以由Scala语言通过import引入。
Chisel编程可以生成Verilog代码或C++仿真代码，目前国内主要由中科院计算所的包云岗老师团队做香山处理器使用，它不仅是一门语言，也代表一个硬件敏捷开发的方向。

## Chisel-Bootcamp是什么
Chisel-Bootcamp是Github上的一个Chisel教程，包含了基于Jupytor的Chisel教学，这篇文章讲一下基于Docker来配置Bootcamp环境，
主要参考资料是[Bootcamp在github上的安装教程](https://github.com/freechipsproject/chisel-bootcamp/blob/master/Install.md)

## 基于Docker配置Chisel-Bootcamp
### 官网下载Docker安装包
首先需要下载Docker-Desktop程序，然后打开这个exe程序安装好，我的感受是Docker安装还是比较友好的。
[点进链接，根据操作系统版本下载](https://docs.docker.com/get-docker/)
我这里安装的是Windows版本的Chisel，安装好后打开Docker-Desktop


### Docker换源
[我参考的这篇文章的方法1](https://blog.csdn.net/Lyon_Nee/article/details/124169099)

### 启动Bootcamp镜像
使用命令安装Chisel-Bootcamp镜像

```bash
docker run -it --rm -p 8888:8888 ucbbar/chisel-bootcamp
```
**对该命令的解释：**
> -i 以交互模式运行容器，通常与 -t 同时使用；
> -t: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；
> --rm:容器退出时就能够自动清理容器内部的文件系统。 举例：docker run --rm ba-208
> -p：指定端口映射，格式为：主机(宿主)端口:容器端口

最后出现这样的界面就对了：
<!-- ![在这里插入图片描述](/images/7ca96c6a2255f561356bc0df88381f56.png#pic_center) -->
把红框框的部分从浏览器打开就可以用jupytor开始学习Chisel了，这里的jupytor的内核是scala编译器，因为chisel本质是scala语言的一个库。

### 常用docker命令
```bash
docker ps // 查看所有正在运行容器
 docker stop containerId // containerId 是容器的ID

 docker ps -a // 查看所有容器
 docker ps -a -q // 查看所有容器ID

 docker start $(docker ps -a -q) // start启动所有停止的容器
 docker stop $(docker ps -a -q) // stop停止所有容器
 docker rm $(docker ps -a -q) // remove删除所有容器
```
例如要停止刚刚的bootcamp镜像就先`docker ps`查看所有运行容器，找到它的容器id，然后使用`docker stop 容器id`就可以了
下次要启动时还是使用
```bash
docker run -it --rm -p 8888:8888 ucbbar/chisel-bootcamp
```
会自动启动本地的bootcamp镜像，而不是从网上下载。

## 可能产生的问题
输入
```bash
docker run -it --rm -p 8888:8888 ucbbar/chisel-bootcamp
```
后报错

> error during connect: This error may indicate that the docker daemon is not running

出现这个问题首先你要保证cmd运行的时候Docker Desktop是打开的，我打开后重新执行就解决了。
[如果还不行的话参考这篇](https://blog.csdn.net/tangcv/article/details/112238084)
