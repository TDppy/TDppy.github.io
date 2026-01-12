---
title: 【IC设计】草履虫都能看懂的AXI入门博客（大量图文来袭，手把手教学，波形仿真）
date: 2024-04-21 15:31:42
categories: 数字IC设计
tags: [AXI]
layout: post
---
@[TOC]
> AXI：Advanced eXtensible Interface 高级可扩展接口 
> AXI是AMBA总线协议的一种，AMBA是ARM公司1996年首次推出的微控制器总线协议。

# 概述
## AXI的三类接口
通常所说的AXI指AXI4，有三类接口：
- AXI4-Full:用于高性能内存映射需求。
- AXI4-Lite:用于简单的地吞吐量内存映射通信（例如，进出控制寄存器和状态寄存器）
- AXI4-Stream：用于高速流数据

从Spartan-6和Virtex-6器件开始，Xilinx的IP开始采用AXI接口。后续的UltraScale架构、Zynq-7000系列全部使用AXI总线。
AXI总线在Xilinx产品中被广泛采用，主要是高效、灵活、便捷。

## AXI的特点
**高效：**
通过对AXI接口进行标准化，开发人员只需学习用于IP的单一协议。

**灵活：**
AXI4适用于内存映射接口，仅一个地址阶段就允许高达256个数据传输周期的高吞吐量爆发。
AXI4-Lite是一个轻量级的传输接口，逻辑占用很小，在设计和使用上都是一个简单的接口。
AXI4-Stream完全取消了对地址阶段的要求，并允许无限的数据突发大小。

**便携：**
使用AXI协议，不仅可以访问Vivado IP目录，还可以访问ARM合作伙伴的全球社区。许多IP提供商支持AXI协议。
一个强大的第三方AXI工具供应商集合，提供许多验证、系统开发和性能表征工具。

## AXI的五个通道
AXI4和AXI4-Lite接口都有5个不同的通道组成，每个通道有若干个接口信号。
- 读地址通道
- 写地址通道
- 读数据通道
- 写数据通道
- 写响应通道

# AXI的时序
为了理解AXI的读写时序，首先需要理解基于valid-ready的握手机制，然后理解AXI的读/写流程，接着理解给出AXI所有接口信号的含义，
最后理解AXI读写的时序图，并以一个简单的AXI接口的block design为例进行仿真，查看波形图。

## AXI的握手机制
AXI 基于valid-ready的握手机制： 
发送方（主）通过置高 vaild 信号表示地址/数据/控制信息已准备好，并保持在消息总线上； 
接收方（从）通过置高 ready 信号表示接收方已做好接收的准备。在 ACLK 上升沿，若 vaild、ready 同时为高，则进行数据传输。 

**注意①：** 
valid和ready不能相互依赖，避免产生相互等待的死锁， 通常建议ready和valid完全独立，这样主从双方都有终止通信的能力。 若想要从机接收全部的来自主机的数据，可设 ready = H 。

**注意②：**
根据 valid、ready 到达时间，可以分为 3 种情况，如右图。 应当注意到，在 valid 置高的同时，发送方就应该给出有效数据，并将有效数据保持在总线，而在之后的 ACLK 上升沿，若 valid、ready 均有效，则应更新有效数据。

![在这里插入图片描述](643805d340bc262afe99969eefb83202.png)
![在这里插入图片描述](25c80ea0a77be13ade07867a89034663.png)


**关键时序图形的约定**
![在这里插入图片描述](8b8b5365ebb5f9c3be79e4a3eec97efa.png)

## AXI的读写流程
### 写操作
写流程如图，涉及到写地址通道 AWC、写数据通道 DWC、写回复通道 RC 三个通道。
 1. 首先， master 在 **写地址通道** 上给出写地址和控制信息。
 2. 然后，在 **写数据通道** 上传输数据，AXI 的数据传输是突发性的，一次可传输多个数据，在传输最后一个数据时，须同步给出 last 信号以表示数据传输即将终止。
 3. 最后， slave 将在 **写响应通道** 上给出写响应消息，对本次数据传输表示确认。
![在这里插入图片描述](f1eeccfe03a0871ba2033cc222331731.png)
### 读操作
**读流程如图，**涉及读地址通道 ARC、读数据通道 DRC 两个通道。
 4. 首先， master 在 读地址通道 上给出读地址和控制消息， 
 5. 然后，slave 将在 读数据通道 上给出数据。 
值得注意的是，读数据通道 集成了读回复功能，且是从 slave 发送给 master 的，在 slave 完成数据传输后，会在读数据通道 上给出回复消息，标志一次读取结束。

 此外，AXI 可以连接成多对多的拓扑，这可以借助 AXI Interconnect IP 来实现。
![在这里插入图片描述](e9c4cfc675a7e837043931b0eff3d211.png)
## AXI-Full的接口信号
为了阅读时序图，需要先了解AXI五个通道具体有哪些接口信号。
包括： 
 1. 全局信号 
 2. 写地址通道信号(Write Address Channel，AW) 
 3. 写数据通道信号(Write Data Channel，W) 
 4. 写响应通道信号(Write Response Channel，B) 
 5. 读地址通道信号(Read Address Channel，AR) 
 6. 读数据通道信号(Read Data Channel，R)


### 1. 全局信号：
**ACLK** 
所有信号必须在时钟的上升沿采样。

**ARESETn**
AXI使用低有效的复位信号ARESETn，复位信号可以异步使能。
在复位过程中，适用于以下接口要求：
①主接口必须驱动ARVALID，AWVALID和WVALID为低
②从接口必须驱动RVALID和BVALID为低
③其他信号可以被驱动为任意值。
④去使能后，主接口的Valid变高至少要等ARESETn为high的上升沿边缘。

### 2. 写地址通道信号
![在这里插入图片描述](774af9a5d32ca3651bf88fe603c8316a.png)
### 3. 写数据通道信号
![在这里插入图片描述](c59dc4825a983d504f1d30b3789f8f52.png)
### 4. 写响应通道信号
![在这里插入图片描述](d348ca2accbdb2f4738e3434dc7d59a4.png)
### 5.读地址通道信号
![在这里插入图片描述](564bc2a4065644bfa82f87bfa852a145.png)
### 6.读数据通道信号
![在这里插入图片描述](fb96102d71e65642520564a0a98a5817.png)
## AXI-Full的读写时序
### 时序图图例
首先我们先读一下时序图的图例，了解各个图形的含义。
![在这里插入图片描述](ac6f8a7e8201a4cc5226e7eefedfd7b2.png)
### 写时序
如图所示，AXI4协议主从设备间的写操作使用写地址、写数据和写响应通道。只需要一个地址就可以执行最大为256的突发长度的写操作。 

 1. 第一步，写地址： 
写操作开始时，主机发送地址和控制信息到写地址通道中。 当地址通道上AWVALID 和 AWREADY 同时为高时，地址 A 被有效的传给设备，然后主机发送写数据到写数据通道中。 

2. 第二步，写数据： 
当 WREADY 和 WVALID 同时为高的时候表明一个有效的写数据。当主机发送最后一个数据时，WLAST 信号变为高电平。 

3. 第三步，写响应： 
当设备接收完所有数据之后，设备会向主机发送一个写响应BRESP来表明写事务完成，当BVALID 和 BREADY 同时为高的时候表明是有效的响应。

![在这里插入图片描述](b185382040926664193ac63bedff812d.png)
### 读时序
如图所示，AXI4协议主从设备间的读操作使用独立的读地址和读数据通道，只需要一个地址就可以执行最大为256的突发长度的读操作。 

1. 第一步 读地址：
主机发送地址和控制信息到读地址通道中，当地址通道上 ARVALID 和 ARREADY 同时为高时，地址 ARADDR被有效的传给设备，之后设备输出的数据将出现在读数据通道上。 

2. 第二步 读数据：
当 RREADY 和 RVALID 同时为高的时候表明有效的数据传输，从图中可以看到传输了 4 个数据。为了表明一次突发式读写的完成，设备 用 RLAST 信号变高电平来表示最后一个被传输的数据，D(A3)是本次突发读的最后一个读数据。

**注意：**在数据读取时，读取的数据从图中可以看到不是连续读取，说明slave是空闲时才传递

![在这里插入图片描述](947c12f58575cab44a0c9a5311ef0a4f.png)

# AXI读写实例
下面将通过Block Design的方式封装一个含有AXI主从接口的IP，然后利用这个自定义IP进行Block Design，创建一个简单的AXI收发实例，最后进行仿真，查看波形图，通过实践验证前面学习的AXI时序。
## 封装自定义AXI IP
首先自己新建一个工程，下面跟着步骤来：
第一步：点击Tools->Create and Package New IP ，创建自定义IP
![在这里插入图片描述](67724cc01bd43d56f890e8e7c71adc1c.png)

第二步：直接点下一步
![在这里插入图片描述](5c65174c030be5c3419302b98879db18.png)
第三步：选中【Create AXI4 Peripheral】，点下一步
![在这里插入图片描述](6bdec48b6d0175fa96eb69326d1aa397.png)
**第四步：**修改IP名称和IP的存储位置。
**注意：**这里存储位置需要记下来，一会导入IP时会用到。这里我放在一个新的文件夹my_ip_repo
![在这里插入图片描述](b8f90d518279be3b83c439baf22f9bde.png)
**第五步：**将现有的一个AXI接口类型修改为full类型，接口模式修改为Master
![在这里插入图片描述](9c1013c980715273f99c6e857aaa92af.png)
**第六步：**添加一个新的AXI接口，接口类型修改为full类型，接口模式修改为Slave
![在这里插入图片描述](d4bb2bb50bc983f9aca6d1a8e87cc351.png)

**第七步：** 选择添加到IP仓库，完成创建。
![在这里插入图片描述](8745cdb8dda92eaf567d2858c246e4f8.png)

## Block Design
下面创建block design，导入两个刚刚创建的自定义IP，将两个ip的clock和resetn都连到一起，触发信号init_axi_txn连到一起，一个IP的master和另一个IP的slave连到一起，实现互相收发的功能。见下图：
![在这里插入图片描述](a843108130b8d434cba90fca0f7d942a.png)
![在这里插入图片描述](6de6c90d1ad2229df5f310ccb0e7adb2.png)
![在这里插入图片描述](214d7f077a4579570f922ddda04968b1.png)
![在这里插入图片描述](96c17118288305dc07c5cd7f6e48516c.png)

![在这里插入图片描述](6fd932f8c4004ffda0809da3260f12a8.png)
![在这里插入图片描述](3791883e2cc3c31e11628c52f8c129cd.png)
![在这里插入图片描述](590db9ee6d70adfe68d91be4d6c20307.png)

![在这里插入图片描述](4e8c4f3ddd28340ac828ee278b9a5de7.png)
![在这里插入图片描述](451225e6c1a78256c484aeb4297a96fe.png)

![在这里插入图片描述](c4a5182dd0952bc1dccfd1d77b8b4e19.png)
![在这里插入图片描述](4a6c9be2957a9d3e177e0d74c101ad7f.png)
需要粘贴的代码如下：
```rust
`timescale 1ns / 1ps

module my_axi_test_wrapper_tb();

reg clk,rst_n;
reg txn;
my_axi_test_wrapper my_axi_test_wrapper_u0
(
    .m00_axi_aclk_0        (clk),
    .m00_axi_aresetn_0     (rst_n),
    .m00_axi_init_axi_txn_0(txn)
);

initial begin
    txn   = 0;
    rst_n = 0;
    #100;
    rst_n = 'd1;
    #1000;
    txn   <= 'd1;
end

always begin
    clk <= 'd0;
    #10;
    clk <= 'd1;
    #10;
end
endmodule

```
## 仿真波形
运行tb仿真，
![在这里插入图片描述](a7b6523b10461fe5047192498fcd537c.png)

![在这里插入图片描述](83290c3a71068b8d22b1ea605c1b7336.png)
然后重新运行仿真。
### 写地址
如图所示，主设备将AWVALID和AWREADY都拉高时，地址AWADDR的40000000被写到slave设备。
其中，AWLEN为0f表示要连续写入15+1=16个数据，AWSIZE=2表示每个数据是2^(size)=4 bytes，AWBURST为1表示16个数据按照初始地址40000000递增的顺序依次写入。
![在这里插入图片描述](e1ccbf7a9ed6af62a22e03e130e59e2f.png)
### 写数据
如图所示，WVALID和WREADY都拉高时第一个数据1被写入到指定地址40000000，下面依次按照地址递增顺序写入，最后一个数据16写入时，WLAST拉高。
![在这里插入图片描述](1c1f9070605bbe7223dc2e0b25c2f1d7.png)

### 写响应
如图所示，当BVALID和BREADY同时拉高时，BRESP有效，此时BRESP为0，表示写入成功。
![在这里插入图片描述](910fb00915e29a0fc718fc69c9433cc6.png)

### 读地址
当ARVALID和ARREADY同时拉高时，ADADDR将会被传给Slave设备，之后Slave设备输出的数据将出现在读数据通道上。
![在这里插入图片描述](aa44b3ec104779a758ce08574c5951ce.png)
和写数据同理，其中ARLEN为0f表示读16个数据，ARSIZE为2表示每个数据为2^2 = 4 bytes大小
### 读数据
如图所示，当RVALID和RREADY同时拉高时，读数据有效，当RLAST拉高时表示读最后一个数据。
可以看到从1009到1024是连续的，一共16个数据。
![在这里插入图片描述](3ebb16166baa72c055ae91d1a1277d19.png)
# 总结
本文介绍了AXI协议的几种分类、五个通道、时序图，给出了如何创建一个简单的AXI收发的block design，对波形仿真进行了分析。
由于时间仓促，写的不足的地方多多包涵，后面会继续更新手撕AXI协议以及本文配套讲解视频，感觉有用的点个关注不迷路~~

**参考资料：**
1. [AMBA AXI Specification IHI0022E](https://developer.arm.com/documentation/ihi0022/latest/)
2. [fpga奇哥 如何科学的设计FPGA：实现AXI总线自由之AXI解读](https://www.bilibili.com/video/BV1mD4y1p7UK/?spm_id_from=333.788&vd_source=f198ad494d21a8eeb0ee49b6bb461ac5)
