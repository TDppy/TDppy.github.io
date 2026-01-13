---
title: 【异常处理】org.apache.ibatis.binding.BindingException Invalid bound statement (not found)
date: 2021-04-14 16:14:00
categories: 异常处理
tags: [错误解决, 调试]
layout: post
---

 ![ ](./1.png) 
加载表格数据时报了异常，报错：`org.apache.ibatis.binding.BindingException: Invalid bound statement (not found)`
debug了一下，跟到了
 ![ ](./2.png) 
其实问题很简单，mapper忘记写到mybatis-config.xml了。
有时候编程的问题debug会跟到很深，让你一脸懵逼，但是很多时候只是低级错误。
