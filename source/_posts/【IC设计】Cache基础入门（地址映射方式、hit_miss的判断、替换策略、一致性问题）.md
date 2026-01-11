---
title: 【IC设计】Cache基础入门（地址映射方式、hit_miss的判断、替换策略、一致性问题）
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计]
layout: post
---
﻿---
title: 【IC设计】Cache基础入门（地址映射方式、hit_miss的判断、替换策略、一致性问题）
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计, Cache]
layout: post
---

﻿@[toc]
# Cache基础
> 为什么要学习Cache？本人是研究NoC总线的，NoC主要应用于大量CPU core的互联，NoC的本质在于利用存储资源构建路由拓扑，将主从机挂在路由器下，实现将计算和通信解耦合。单个路由节点的设计并不复杂，本质就是路由计算+交叉开关，总线的关键难度在于验证，要支持缓存一致性，并且在拓扑复杂、异构负载的情况下保证高可靠性。因此，学习Cache是精通NoC总线的前置知识，这里补充一下相关基础。时间有限，没有绘制精美的图片，有兴趣深入的可以读本文的【参考文献】

CPU所计算的数据要从内存中取，计算的结果要写入到内存。内存价格低，容量大，读写速度慢cache价格高，容量小，读写速度快。
因此，CPU和内存间往往会加Cache，来加速存取数据的速度。


> Cache line：Cache和Memory之间数据传输的最小单位，因为从memory中取数据到cache不会一个byte一个byte取，效率太低。通常一个Cache line是32byte或64byte，在CHI-E中一个Cache line是64 byte

## 内存地址A的数据存在Cache的什么位置？——Cache和Memory的地址映射方式

cpu要读内存一个数据，优先从cache中取，cache中没有再去内存中取，以节省时间。这就涉及到一个问题，内存中的数据存在cache中的什么位置。即cache和memory的地址映射，包括直接相联，全相联，组相联。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/885f9c28278d4836a57ac93415890ea7.png)
**直接映射的概念**
每个存储地址都直接映射到cache的确定位置是直接映射，通常采用（块地址）mod(cache中的数据块数量)来找到对应的数据块。

**tag的作用和位宽计算**
由于cache比memory小，那么每个cache必定对应多个存储地址，如何判断请求的数据字是否在cache中呢？答案是通过tag，以直接映射为例，一个cache地址对应多个存储地址，可以通过tag来标记到底是cache[4]存储的到底是mem[4]还是mem[12]还是别的。
tag所需的位宽是mem地址的高位，例如图1中内存地址从0-23，cache地址从0-7，因此tag所需位宽是Ceil(log2(24/8))=2

**valid的作用**
通过有效位判断cache中的数据块是否保存了有效信息，例如cpu启动时，cache中没有有效数据，valid置为0，或者其他core改了这个数据，那么为了保证缓存一致性，当前core的cache中应该把这个数据valid置为0，需要读的时候从别的core的cache读取。

**index的作用**
索引是cache line的地址，被用来作为访问cache的地址。
## 如何判断内存地址A的数据在不在Cache中？——命中/失效的判断
cpu要取的数据在cache中称为命中（hit），不在称为失效（miss），需要从mem中取。如何判断hit还是miss?
首先要根据cache和memory的映射关系来锁定到cache对应地址，然后由于一个cache地址可能对应多个memory地址，因此需要根据tag号来判断到底匹配的是哪个地址。这里需要注意，cache的存储开销包括数据本身，tag号，以及一些状态信息，如valid，dirty。
## 内存地址A的数据不在Cache中怎么办？——Cache的替换策略
由于memory大，cache小，那么cache一个地址常常对应多个memory地址。在这种情况下，当cpu想读入内存地址A的数据mem[A]，可能Cache中已经存了其他数据，这就需要将mem[A]替换掉Cache中一个数据，下次还要读mem[A]的时候就可以直接从cache中拿。
Cache的替换策略包括随机法、最近最少使用法（LRU）、先进先出法（FIFO）等。

## 多核场景下对私有Cache读写——Cache一致性问题
在多核场景下，每个CPU都有自己的私有Cache，对私有cache的数据更新，其他cache是感知不到的，所以可能会出现同一个内存地址在不同的私有cache中数据不一致的问题。

# 参考资料
1. 计算机组成与设计：软硬件接口 第五版
2. [12 张图看懂 CPU 缓存一致性与 MESI 协议，真的一致吗？](https://cloud.tencent.com/developer/article/2197853)
