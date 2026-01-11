---
title: 【IC设计】昇腾910架构学习
date: 2024-08-10 19:46:27
categories: 数字IC设计
tags: []
layout: post
---
> 本文内容是参考华为公开资料形成的个人观点，无侵权行为，内容仅供学习！

昇腾910是华为的AI训练卡，基于7nm EUV工艺，其中有16个基于ARMv8定制的CPU，32个Ascend-Max AI加速器，使用4*6的无缓存NoC Mesh进行互联，使用HBM（High Bandwidth Memory）进行存储，提供128通道的视频译码器。

**指标：**
 - 四个HBM总带宽1.2TB/s
 - 相邻节点（我的理解是Ascend-Max核）带宽为1024bit*2GHz=256GB/s
 - 昇腾910每秒提供256万亿次fp16浮点运算，512万亿次int8运算
 - LLC总吞吐量为4TB/s
![在这里插入图片描述](/images/ab01aa7fd7c34b76bdddf40538bf2b91.png)


