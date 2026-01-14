---
title: 【C盘炸了】利用分区助手扩充C盘
date: 2021-08-13 16:44:19
categories: 
tags: []
layout: post
---


## 概要：
C盘就剩一百多MB了，平时也没安装软件在C盘，不知道怎么会这样。
不得不研究下怎么把其他盘的空闲空间移动到C盘。
在网上下了分区助手，将E盘移了20多G过去，暂解燃眉之急。
{% asset_img 1.png 在这里插入图片描述 %}

## [分区助手下载链接](https://www2.aomeisoftware.com/download/pacn/PAInstall.zip)
## 移动步骤
下载好以后解压，
{% asset_img 2.png 在这里插入图片描述 %}
点击PACNPro.exe，安装好了以后打开，下面操作很简单，看几个图就知道了。

{% asset_img 3.png 在这里插入图片描述 %}
{% asset_img 4.png 在这里插入图片描述 %}
{% asset_img 5.png 在这里插入图片描述 %}
确定以后点击左上角的提交
{% asset_img 6.png 在这里插入图片描述 %}
点击执行
{% asset_img 7.png 在这里插入图片描述 %}
点执行后，选择windows PE的重启。

## 注意：
如果你不是选择【分配空闲空间】，而是【合并分区】，那至少两个分区都要预留5G，否则会报错。
