---
title: 【linux学习】软链接与硬链接
date: 2020-10-16 05:18:32
categories: 编程与算法
tags: [链接, Linux]
layout: post
---

> 下面内容是个人理解，仅供参考！

## 类比于windows
linux是一个操作系统，其学习可类比于我们熟悉的windows：
软链接是符号链接，类似于windows中的快捷方式，像这样：
 ![ ](./1.png) -->
硬链接类似于建立一个文件副本，像这样：
 ![ ](./2.png) -->
## 实现：
硬链接使用ln 源文件名 链接名创建，比如已有文件hello.c，链接为haha，即：ln hello.c haha

软链接使用ln -s 源文件名 链接名创建，比如已有文件world.c，链接为wawa，即：ln -s world.c wawa

下面看实验中我们输的命令：
 ![ ](./3.png) -->


执行结果：
 ![ ](./4.png) -->
>PS:上面这个图里ls -il展示的第一个属性是inode节点号，不小心多加了个3
>
 ![ ](./5.png) -->

[ln命令 参考链接](https://www.runoob.com/linux/linux-comm-ln.html)

