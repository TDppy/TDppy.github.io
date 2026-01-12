---
title: 【字符编码】GB2312、GBK、Unicode
date: 2026-01-11 15:30:00
categories: 编程与算法
tags: [字符编码, GB2312]
layout: post
---

简要整理了下百度百科上关于这几个编码的介绍。
**GB2312：**
GB2312和GB2312-1980是一个意思，CP36和GB2312一样
1980年国家标准总局发布，全称《信息交换用汉字编码字符集——基本集》。
由于有一些罕见字没有录入，因此又出现了GBK，K是'扩'的声母。
**GBK：**
P-Windows32和苹果OS以GB2312为基本汉字编码， Windows 95/98则以GBK为基本汉字编码。
GB2312是简体中文字符集，不支持繁体汉字。
为统一繁体字符集编码，1984年，台湾五大厂商共同制定了一种编码方案，因为其来源被称为五大码，英文写作Big5，目前是繁体中文编码的事实标准。
**Unicode**
Unicode是Universal Multiple-Octet Character Set的简称  UTF-8是Unicode的一种，使用可变长度字节来存储Unicode字符
UTF是Unicode Transformation Format的简称，出现的目的是让能用ascii表示的字符就用1个字节表示，节省存储空间。
