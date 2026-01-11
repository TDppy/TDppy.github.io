---
title: 【linux学习】软链接与硬链接
date: 2026-01-11 15:30:00
categories: linux学习
tags: [linux学习]
layout: post
---

> 下面内容是个人理解，仅供参考！

## 类比于windows
linux是一个操作系统，其学习可类比于我们熟悉的windows：
软链接是符号链接，类似于windows中的快捷方式，像这样：
![在这里插入图片描述](./images/5043d15bbe9cf71c34d4d8c17b2724cc.png#pic_center)
硬链接类似于建立一个文件副本，像这样：
![在这里插入图片描述](./images/9be08f4de6ec2ab724aac3c7feae9f5f.png#pic_center)
## 实现：
硬链接使用ln 源文件名 链接名创建，比如已有文件hello.c，链接为haha，即：ln hello.c haha

软链接使用ln -s 源文件名 链接名创建，比如已有文件world.c，链接为wawa，即：ln -s world.c wawa

下面看实验中我们输的命令：
![在这里插入图片描述](./images/9b7f53dba489db664a151b19eceee3c4.png#pic_center)


执行结果：
![在这里插入图片描述](./images/f5fc045a3cb60860905dc1e05cbe436c.png#pic_center)
>PS:上面这个图里ls -il展示的第一个属性是inode节点号，不小心多加了个3
>
![在这里插入图片描述](./images/0ddc44e3e5cd2096edaad09bcd68ed5c.png#pic_center)

[ln命令 参考链接](https://www.runoob.com/linux/linux-comm-ln.html)

