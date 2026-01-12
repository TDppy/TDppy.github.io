---
title: 【IC设计】Chisel构建工具Mill的安装（mill脚本执行过慢怎么办？）
date: 2024-10-23 19:21:27
categories: 数字IC设计
tags: [Mill, Chisel]
layout: post
---
@[toc]
# 背景
Chisel传统的项目构建工具是sbt，但是最近我需要学习Rocket Chip SoC Generator中的BOOM处理器核，而Rocket Chip的项目所使用的项目构建工具是Mill，所以我需要安装下mill工具。

# 安装过程
sbt和mill的区别是，sbt工具在项目目录中的配置文件是build.sbt，mill工具在项目目录中的配置文件是build.sc
在mill官方文档中给出了一行命令来安装这个工具，[链接点我](http://mill-build.org/mill/0.11.12/Java_Installation_IDE_Support.html#_manual)

```bash
sh -c "curl -L https://github.com/com-lihaoyi/mill/releases/download/0.11.12/0.11.12 > ~/.local/bin/mill && chmod +x ~/.local/bin/mill"
```
这行命令本质上是去github上下载了mill安装的一个shell脚本，存放在~/.local/bin/mill下，然后按理说我们需要执行这个脚本，**但不推荐这么做！！**

实际上该脚本核心是去maven下载mill的可执行jar包，这个jar包就是我们真正需要执行的mill文件，而它使用的是maven官方仓库，下载的巨无敌慢，所以我选择自己去浏览器下载这个jar包，然后传到linux里面来使用。
![在这里插入图片描述](/images/f0ad0cf93b4e49a6b142be21d7c55e98.png)
# 使用mill构建工程
![在这里插入图片描述](/images/0b224908e993480fb719c4c61d7434e2.png)

