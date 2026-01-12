---
title: 【IC设计】Xilinx不同系列的Zynq板卡介绍(Zynq-7000，UltraScale MPSoC_RFSoC，ACAP）
date: 2024-05-06 11:39:54
categories: 数字IC设计
tags: [FPGA]
layout: post
---
@[TOC]
# Xilinx Zynq SoC 系列
针对不同的应用领域，Xilinx 公司设计开发了各种逻辑资源规模和集成各种外设功能的 Zynq SOC 器件，包括专为成本优化的 Zynq-7000 平台，面向高性能实时计算应用领域的 Zynq UltraScale+ MPSoC，面向射频通信的 Zynq UltraScale+ RFSoC，以及具备高度可扩展特性的自适应加速平台 ACAP。
## 专为成本优化的 Zynq-7000 平台
![在这里插入图片描述](f04bddf1148cdba61cf557a05ba9d984.png)
Zynq-7000 SoC 属于成本优化的可扩展 SoC 平台，该系列器件集成了单核或双核的 Arm Cortex-A9，28nm 7 系列可编程逻辑，以及速率高达 12.5G 的收发器。
Zynq-7000 SoC 非常适合以下应用领域：
ADAS
医疗内窥镜
小型蜂窝基带
专业相机
机器视觉
电信级以太网回传
多功能打印机

## 面向高性能实时计算应用领域的 Zynq UltraScale+ MPSoC
Zynq UltraScale+ MPSoC 器件不仅提供 64 位可扩展性处理器，同时还将实时控制与软硬件引擎相结合，支持图形、视频、波形与数据包处理。置于包含通用实时处理器和可编程逻辑的平台上，三个不同变体包括双核应用处理器(CG) 器件、四核应用处理器和 GPU (EG) 器件、以及视频编解码器 (EV) 器件，为 5G 无线、下一代 ADAS 和工业物联网创造了无限可能性。
基于上述特性，Zynq- UltraScale+ MPSoC 非常适合以下应用领域：
下一代 ADAS
5G 无线通信
工业物联网
人工智能
机器视觉

## 面向射频通信的 Zynq UltraScale+ RFSoC
Zynq® UltraScale+™ RFSoC 是在 Zynq® UltraScale+™ MPSoC 基础上，通过集成一个全面的 RF 模数信号链，实现了对射频信号的高性能收发。![在这里插入图片描述](d11949c4f3446fd95d5a802a5c4031ac.png)
Zynq® UltraScale+™ RFSoC 在 SoC 架构中集成数千兆采样 RF 数据转换器和软判决前向纠错 (SD-FEC)。 配 有 ARM® Cortex®-A53 处 理 子 系 统 和UltraScale + 可编程逻辑，该系列是业界唯一单芯片自适应射频平台。
Zynq UltraScale+ RFSoC 系列可为模拟、数字和嵌入式设计提供适当的平台，从而可简化信号链上的校准和同步。多代产品系列包含广泛的器件类型，具有不同的直接 RF 性能，可满足各种频谱需求和使用案例。
目前，Zynq UltraScale+ RFSoC 已经推出了 3 代产品，每代产品都实现了更加优异的射频性能。
### Zynq UltraScale+ RFSoC GEN1
硬件可编程 SoC 上 RF 数据转换器的突破性集成
8x 或 16x 6.554GSPS DAC
8x 4.096GSPS 或 16x 2.058SPS ADC
### Zynq UltraScale+ RFSoC GEN2
及时支持最新的 5G 频段，实现区域部署
16x 6.554GSPS DAC
16x 2.220GSPS ADC
### Zynq UltraScale+ RFSoC GEN3
全面支持 6GHz 以下频段，含扩展的毫米波接口
8x / 16x 9.85GSPS DAC
8x 5.0GSPS 或 16x 2.5GSPS ADC

### Zynq UltraScale+ RFSoC 应用
测试和测量
   设计人员可通过在 Zynq UltraScale+ RFSoC 中使用直接 RF 采样、高灵活、可重构逻辑及软件可编程性，为信号生成和信号分析构建高速度的多功能仪器。
卫星通信
  利用高度集成的 RF-DAC/ADC 和可编程逻辑，设计人员可使用基于 ARM 的处理系统为地面站构建复杂的高带宽连接调制解调器。
LiDAR
   Zynq UltraScale+ RFSoC 集成数据转换器，再加上自适应硬件的灵活性和并行性，可为从ADAS 到高级 3D 成像应用的新兴 LiDAR 技术
提供独特的解决方案。
## 具备高度可扩展特性的自适应加速平台 ACAP
ACAP 是一种自适应计算加速平台，其高度集成的多核计算平台，可适应不断变化的算法，实现异构加速。可在硬件和软件级别进行动态自定义，以适应各种应用和工作负载。ACAP 围绕可编程 NoC 进行设计，软件开发者和硬件程序员可轻松地对其进行编程。
Versal ACAP 为云、网络和边缘应用提供无与伦比的应用和系统级价值。颠覆性的 7nm 架构将异构计算引擎与广泛的硬化内存和接口技术相结合，与同类10nm FPGA 相比，具有卓越的性能功耗比。

#  Zynq-SOC 应用前景
基于 Zynq-SoC 器件强大的硬件特性和便捷的软件功能，用户可获得更智能& 优化 & 最安全的解决方案。
通过运行各种成熟的操作系统（Linux、RTOS），这些成熟的 OS 所提供的中间件、协议栈、加速器和 IP 生态环境等，能为用户提供最简洁高效的应用开发环境。
其中，**Zynq-7000 系列**主要面向传统嵌入式和 FPGA 交叉应用领域，实现复杂 FPGA+ARM 结构的板级简化，让系统设计更加灵活简洁**。Zynq UltraScale+ MPSoC**则主要面向高速数据传输和处理的场景，在拥有强大的 PCIE 数据传输能力的同时，还能实现高性能的数据计算，让传统的数据采集和处理应用不再依赖于 PC+FPGA 加速卡的分体式结构。**Zynq UltraScale+ RFSoC** 则通过自身优异的射频性能，实现了无线通信、信号分析的最优解决方案。

