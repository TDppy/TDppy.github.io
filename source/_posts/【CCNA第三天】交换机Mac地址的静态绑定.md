---
title: 【CCNA第三天】交换机Mac地址的静态绑定
date: 2026-01-11 15:30:00
categories: CCNA第三天
tags: [CCNA第三天]
layout: post
---

> CCNA第三天主要讲了交换机mac地址的静态绑定，以及这个实验的一些前置知识。

## OSI参考模型：
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/17a493b0a9ae94972fa9c0f4260027c1.png)

这一天我们主要学习前两层：物理层和数据链路层。
### 物理层：
作用：定义线缆标准，例如：电压、线速、规格等。
设备：modem调制解调器、[集线器](https://img-blog.csdnimg.cn/20200709221643823.png)、[中继器](https://img-blog.csdnimg.cn/20200709221809179.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d9ef92a4188872e1fbc92d7dcebc144e.png)
### 数据链路层
作用：定义的是线路物理标准，连接器标准，物理地址。
协议：IEEE 802协议
有线标准：IEEE 802.2、802.3、802.5、FDDI
无线标准：IEEE 802.11(a、b、g、n、ac)，现网中常用的无线标准是IEEE 802.11ac
PS：以太网IEEE 802.3、令牌环网IEEE 802.5、FDDI这三种协议称为局域网大三协议。
设备：交换机
mac地址的学习：
交换机的默认mac地址表为空，在接收到数据帧时，记录下接收的端口和数据源设备的Mac地址。
## Mac地址表的静态绑定
MAC地址表静态绑定
应用场景：办公网络环境中，交换机决定了内网数据的转发，因此交换机的mac地址表稳定是非常重要的，为了安全起见，不至于让交换机即插即用，我们对交换机的mac地址表进行静态映射（绑定）static。然后再启用端口安全，使除了绑定的mac地址这台设备以外，其他所有设备都无法进行数据发送，保证内网安全。
配置：交换机全局模式下
int  range  f0/1  -  4 
///同时进入f0/1到f0/4所有接口，“range”接口范围。接口范围根据交换机上使用的接口来。
 Sw  mode  access
/// 接口设置为接入模式，即此接口用于连接终端设备
exi  
///退出到全局模式
Spanning-tree  portfast  default  
///开启所有access接口的快速转发，此功能可以使交换机的access接口在接上设备之后，接口能够立刻进入转发状态（变绿）
Int  f0/1  ///进入f0/1接口
 Switchport  port-security  ///开启端口安全
 Switchport  port-security  mac-address  +电脑1mac地址  ///静态绑定电脑的mac地址到交换机的f0/1接口上
 Switchport  port-security  violation  shutdown  ///定义端口安全的动作，一旦出现冲突（f0/1接口上的mac地址与绑定的mac地址不一致），接口动作立刻关闭（shutdown）
Int  f0/2
 Sw  po  
 Sw  po  mac  +电脑2mac地址
 Sw  po  vio  sh 
Int  f0/3
 Sw  po  
 Sw  po  mac  +电脑3mac地址
 Sw  po  vio  sh 
Int  f0/4
 Sw  po  
 Sw  po  mac  +电脑4mac地址
 Sw  po  vio  sh 
测试：找一台新电脑，接到已经绑定mac地址的接口上
现象：接口立刻关闭（变红）

