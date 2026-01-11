---
title: 【异常处理】verilator安装时出现异常 make_ ___ [Makefile_195_ verilator_gantt.1] Error 13
date: 2026-01-11 15:30:00
categories: 异常处理
tags: [异常处理]
layout: post
---
﻿在ubuntu中安装verilator工具时执行make出现该报错。
当我出现这个报错的时候我一脸懵逼，因为网上找不到相关解决办法。
后来想到我的verilator是从github上下载zip，然后解压后传到ubuntu上的，windows上解压我记得会把-替换成_，这可能导致了该问题的出现。所以直接在ubuntu上用git下载项目，避免windows上传源代码到ubuntu上。
[附上verilator的安装教程](https://blog.csdn.net/qq_42622433/article/details/136542855)
