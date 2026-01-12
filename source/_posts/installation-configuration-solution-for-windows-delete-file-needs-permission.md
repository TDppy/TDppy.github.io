---
title: 【安装配置】windows删除文件需要权限的解决办法
date: 2021-03-06 18:39:45
categories: 环境配置
tags: []
layout: post
---

Win+X打开Windows Powershell(管理员)，
如果你要删除的东西不在C盘需要先切换盘符，如输入`d:`切换到d盘。

```bash
cd 你要进入的目录名
```
然后`del 文件名`  就ok了，如果要删除整个目录和目录下的所有东西，

```bash
del -r 目录名
```

