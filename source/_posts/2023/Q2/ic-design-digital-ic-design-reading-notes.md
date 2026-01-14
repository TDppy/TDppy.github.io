---
title: 【IC设计】数字IC设计读书笔记
date: 2023-06-17 01:35:51
categories: 数字IC设计
tags: []
layout: post
---


> 打算后面将IC设计流程方面的书籍笔记记在这里，近期每天持续更新（~~除非导师换方向~~ ）

## 《专用集成电路设计实用教程》
### 集成电路系统的组成

 1. 数字电路模块：RISC_CORE
 大部分数字电路使用同一个时钟源，经过时钟产生电路，协同各部分运行。即同步电路。
 数字电路大致可以分为数据通路和控制通路。**数据通路**指进行加减乘除的**运算器**，**控制通路**是控制数据流通和信号开关等的**逻辑电路**。
 
 2. 模拟电路模块：A/D
模拟电路相关的有模数转换器ADC，数模转换器DAC，
可编程增益放大器PGA，通过数字电路来控制模拟增益
锁相环PLL，用于产生高频时钟和进行时钟信号的相位校正


 3. IP核模块：MPEG4、DSP、CONDEC、USB
IP核的出现是IC产业分工的结果，使得一些公司写IP，一些公司复用IP，从而IP用的放心，也开发的更快。
USB是IP核，也是输入输出设备。

 4. 内存模块：RAM
内存占据了大部分芯片面积，在低功耗设计中要注意内存功耗在芯片功耗中的比例。

 5. 输入输出PAD
 这里的PAD就是端口的意思，USB接口就是一种I/O PAD。
 由于I/O PAD是直接与外部世界相连接的特殊单元，因此要考虑外部电路的寄生参数影响、静电保护、封装要求、电压转换、过压保护、信号完整等。
 I/O PAD分为：输入PAD、输出PAD、双向PAD。
 
**个人总结：**
 感觉I/O PAD是比较容易被忽略的学习点，在实际工作中可能很重要，因为在招聘中经常看到要懂SPI、I2C、UART，还有高速接口设计，DDR，PCIe,Ethernet,Serdes。
 
 
 
6. 边界扫描模块：JTAG
 相比于传统万用表和示波器测试芯片的“探针”类方法，JTAG是在芯片的边界加上一些寄存器，可以实现对芯片输入输出信号的观察和控制，提供一种不影响芯片运行的调试芯片的方法。

**个人总结：**
感觉就是跟写程序debug一样的功能

7. 互联线
 芯片的模块之间需要互连线来交换信息，互连线包括信号线和电源线，其本质是金属，具有电容、电阻和电感效应，这些称为寄生效应，这些寄生效应会产生连线信号的延迟！

 在超深亚微米设计（180nm以下）中，连线延迟已经和逻辑门的延迟相当，因此在计算时序路径延迟时，不可以再使用线负载模型估算连线的延迟。为解决该问题，Synopsys推出物理综合工具和拓扑综合技术，在书**第七章**介绍。

**个人总结：**
dc综合时没考虑互连线的寄生效应（或者只是考虑了线负载模型，并不全面），互连线的寄生效应要在后仿时考虑进去，涉及到StarRC和PT工具。
关于负载与RC，这个视频里有讲。
[RC负载与延迟](https://www.bilibili.com/video/BV1ia411L7dU/?spm_id_from=333.337.top_right_bar_window_history.content.click)
{% asset_img 1.png 在这里插入图片描述 %}

### 集成电路的设计流程
其实dc和icc似乎并不是割裂的工具，他们采用的数据格式是互通的，突然发现这一点。
将RTL源代码输入到DC，给设计加约束，进行逻辑综合，得到门级网表，该网表可以以ddc存放，也可以用Milkyway存储。2~9章讲了很多dc的内容。
然后是布图规划（包括供电规划）、布局、时钟树综合、布线，StarRC提取寄生参数，然后输入到PT中进行时序和功耗分析。PrimeTime
( PX是一个可以同时进行时序和功耗分析的签核工具)


### 综合=转化+逻辑优化+映射

 1. 转化： 先将RTL源代码转化为通用的布尔等式——GTECH格式；   
 2. 逻辑优化：然后按照设计的约束对电路进行逻辑综合和优化，使得电路能满足设计的目标或约束；
 3. 映射：最后使用目标工艺库的逻辑单元映射成门级网表。综合的结果包括了电路的时序和面积。

**个人总结：** 
先通过read命令将RTL代码转化为GTECH格式，实际上就是布尔代数的等式，然后在用compile命令时会进行逻辑综合、优化、映射。

### 同步电路和异步电路

同步电路指电路中所有时钟来自同一个时钟源，
异步电路指电路中的时钟来自不同的时钟源。

**个人总结：**
如果来自同一个时钟源，例如300HZ，即使经过3分频，6分频分为100HZ和50HZ两个时钟，相位也必然一致。
如果来自不同的时钟源，相位就不一定一致了。

### 亚稳态
书中解释的不是特别清晰，我又ChatGPT问了以下，懂了：

Setup Time指的是输入信号在时钟上升沿之前必须保持稳定的最小时间间隔。如果输入信号在时钟上升沿之前没有保持足够长的稳定时间，那么电路输出可能无法正确响应。

Hold Time指的是在时钟上升沿之后，输入信号必须保持稳定的最小时间间隔。如果输入信号在时钟上升沿之后没有保持足够长的稳定时间，那么电路输出也可能无法正确响应。

举个例子来说，假设有一个触发器电路，其时钟信号为CLK，数据输入信号为D。该电路的Setup Time为5纳秒，Hold Time为3纳秒。如果输入信号D在CLK的上升沿之前保持稳定状态至少5纳秒，并且在CLK的上升沿之后保持稳定状态至少3纳秒，那么电路输出会正确响应。否则，输出可能会出现错误的值或亚稳态行为。

{% asset_img 2.png 在这里插入图片描述 %}
**个人总结：**
一个D触发器，在时钟上升沿时，D的值要传递给Q，自然就要在时钟上升沿对D进行采样。为了保证采样的值是对的，那就不允许上升沿前后D有变化，上升沿之前这个禁止变化的时间是setup time，上升沿之后的这个时间是hold time。
下降沿也同理。


### 单时钟同步设计的时序约束
D数据在哪？看的不太懂。
**个人总结：**
大意就是从一个io口到另一个io口之间花的时间不能太长，否则等你信号过来了，我这个周期的采样早结束了，功能也就不能在一个周期实现了。

这本书是在Synopsys公司的逻辑综合培训资料基础上编写而成，讲了不少dc的细节，估计就是参考了User Guide的文档。




### 目标库和初始环境设置
#### DC如何计算每个逻辑单元的延迟（Cell Delay）？
单位的时延与输入的逻辑转换时间（Input Transition Time）和输出的负载（Output Load）有关，根据这两个数据，可以在库中的查找表（Look up table）中查出单元的延迟。
延时的计算由线性方法和非线性方法，目前主要用非线性方法。这篇文章写的很清楚：
[Synopsys逻辑综合及DesignCompiler的使用](https://blog.csdn.net/qq_42759162/article/details/105541240)

#### target library
DC中，target_library是保留变量，设置这个变量以指向厂商提供的综合库文件。

#### link library
set link_library "* my_tech.db"
星号表示DC先搜寻其内存里已有的库；一般放在综合库之前。
{% asset_img 3.png 在这里插入图片描述 %}

{% asset_img 4.png 在这里插入图片描述 %}

## 《高级ASIC芯片综合》
下载了pdf，等我看了再总结

## 《数字集成电路物理设计》
据说是国内第一部系统介绍VLSI的书，讲得很好（~~一点看不懂~~ ）



## 《VLSI Circuit Design Methodology Demystified》
### 69. WHAT IS FLOORPLANNING?
#### floor plan的主要工作
Floorplanning is the first major step in physical design. The key tasks in this step include analyzing the die size, selecting the package, placing the I/Os, placing the macro cells (e.g., memory cells, analog cells, and specialfunction cells), planning the distribution of power and the clocks, and partitioning the hierarchy. 
布图规划是物理设计的第一个主要步骤。这一步骤的关键任务包括分析**芯片尺寸(die size)**，**选择封装(package)**，**放置I/O**，**放置宏单元(macro cells)**（例如内存单元，模拟单元和特殊功能单元)，**规划时钟和电源的分布**，并**划分层次结构**。

> 在IC设计的floor plan中，macro cell是指一种由多个标准单元（standard cell）组成的逻辑单元。这些标准单元可以在不同的芯片设计中进行重复利用以提高设计效率和可靠性。
  Macro cell通常由基本的标准单元组合而成，形成一个具有特定功能的单元，比如某种逻辑门、寄存器或者算术单元等。在floor plan中，macro cell通常被看作一种独立的逻辑单元，在布局和连线时可以视为单个实体进行处理。
  与硬宏（hard macro）相比，macro cell通常提供更高的灵活性和可配置性，因为标准单元可以根据需要进行选择、组合和排列。此外，它们通常比硬宏占用更少的面积，并且可以在不同的芯片设计之间进行共享和重用。

Die size estimation often starts from the gate count of the netlist (available from the logic synthesis process) plus the physical size of the I/Os and macros.
芯片尺寸估计通常从网表的门数（可以从逻辑综合中获得）加上I/O和宏的物理大小来开始。

#### 决定芯片物理尺寸的因素
 A design can be characterized as I/O limited, core limited, block limited, or package limited. 
一个设计可以被描述为I/O，核心，块，封装限制。

> 在IC设计的floor plan中，block是指一种被划分出来的功能区域。这些区域通常包含了多个逻辑单元、硬宏或者macro cell，用于执行特定的任务或功能。
  Block的目的是将整个芯片分成若干个较小的部分，并对它们进行分类和组织，以便更好地控制设计复杂度、提高可靠性和测试性。每个block通常具有自己的电源和接口，可以独立地进行测试和验证。
  Block的大小和形状通常根据具体的设计需求来确定，可以是长方形、正方形、圆形等不同的形状。在floor plan中，block通常会被放置在一个固定的位置，并通过适当的间距和连线来与其他的block连接起来，以实现整个芯片的功能。

The die size of an I/O-limited design is determined by its number of I/Os. 
I/O限制设计(I/O limited design)的芯片大小由I/O数量决定。

The full placement of the prime input and output cells will dominate the physical size of this chip. 
主要输入输出单元的完整布局将决定这块芯片的物理尺寸。

On the other hand, in a core-limited design, the size of the chip is governed by the core area or the number of standard and macro cells used.
另一方面，在核心限制设计(core-limited design)中，芯片大小由核心面积或所使用的标准单元和宏单元的数量决定。

 In this case, there is probably room to compensate for a few more I/O signals without increasing the chip size.
在这种情况下，可能由空间在不增加芯片大小的情况下补偿更多的I/O信号。

 In a block-limited design, there usually are a significant number of large blocks, or subchips, and the chip size is dominated by the sizes of those blocks.
 在一个块限制设计（block-limited design）中，通常有相当数量的大区块或子芯片，且芯片大小由这些区块的数量决定。

#### 选择封装
 For a package-limited design, the chip size is driven by the available package. 
对于一个封装限制的设计中，芯片大小由可用的封装来决定。

Package selection is another major issue that affects the physical design.
封装的选择是另一个影响物理设计的重要问题。

The selection is based on a number of factors, such as the number of I/Os, the die size, the chip power consumption, and the price.
该选择基于很多因素，例如I/O数量，芯片尺寸，芯片功耗，价格。
 
To compensate for the slightly different die sizes, there may be several lead frames available for the same package.
为了略微补偿不同的芯片尺寸，对同一个封装可能由若干引线框架（lead frames）。

#### I/O单元的布局
After the package has been fixed, the next crucial step is to arrange the prime input and output cells.
在封装被确定后，下一个关键步骤是去安排重要的输入输出单元。

I/O configuration has a direct impact on the quality of physical layout since the placement of the rest of the standard cells and macros depend on the I/O locations.
I/O配置对物理版图的质量由直接影响，因为其他标准单元和宏的布局取决于I/O位置。

The routability of the chip is also closely tied to the I/O configuration. Among many issues, one of the key issues in I/O configuration is the placement of the power and ground pins. 
芯片的可布线性也和I/O配置密切相关。在I/O配置的诸多问题中，一个关键问题是电源和接地引脚的布局问题。

These pins, which could amount to up to one-third or more of the total number of I/Os, are placed carefully to reduce or eliminate any IR drop or EM problem. 
这些引脚可以达到IO总数的三分之一，甚至更多，他们应被小心地放置，以避免和减少任何IR drop（供电电压减少）和EM问题（电子迁移）。

Additionally, for complicated SoC chips with many analog macros, there are various special power supplies other than VDD (for core) and VDDS (for I/O). 
此外，对于具有许多模拟宏的复杂SoC芯片，除了VDD（用于核心）和VDDS（用于I/O）之外，还有各种特殊电源。

Many of them have to be separated from the main VDD/VSS busses for noise immunization. In such cases, chip I/O planning becomes an even tougher challenge. 
它们中的许多必须要与主要的VDD/VSS总线分离以进行噪声免疫。在这种情况下，芯片I/O规划成为了一个更加艰巨的挑战。

#### 宏单元和特殊单元的布局
Macros such as memories and analog cells are often placed manually by designers based on I/O configuration. 
诸如存储器和模拟单元之类的宏通常由设计人员根据I/O配置**手动放置**。

Designers must reduce overall routing congestion so as not to create major hurdles for meeting the chip timing target. 
设计人员必须减少总体路由拥塞，以免给满足芯片时序目标造成巨大障碍。

The placement of those special cells has a great impact on the overall chip placement quality and, consequently, can significantly affect the chip’s overall routability. 
这些特殊单元的布局对芯片整体布局质量由很大影响，因而可以显著影响芯片的整体可布线性。

In most cases, it takes several iterations to find good locations for those macros.
在大多数情况下，需要多次迭代才能为这些宏找到合适的位置。

#### 供电规划
In a VLSI chip, every single transistor needs power to perform.
在一个超大规模集成芯片中，每个单独的晶体管都需要供电才能工作。

The required power is delivered to the transistors through a power distribution network. 
所需的供电会通过供电分配网络（power distribution network）来传输给晶体管。

This network is called the power plan, or power structure, of the chip. 
该网络被称为芯片的供电规划或供电结构。

This power network must deliver the appropriate voltage level to the transistors within the chip for their entire lifetime. 
供电网络必须在整个寿命期间为芯片内的晶体管提供合适的电压水平。

#### 供电规划的两大问题
The two most critical problems associated with a power network are the IR drop and EM. 
和供电网络相关的重要问题是IR drop和EM。

> 电迁移效应（electro-migration effect）是指金属导线中的电子在大电流的作用下，产生电子迁移的现象。
>  当电子流过金属线时，将同金属线的原子发生碰撞，碰撞导致金属的电阻增大，并且会发热。在一定时间内如果有大量的电子同金属原子发生碰撞，金属原子就会沿着电子的方向进行流动。这将会导致两个问题：第一，移动后的原子将在金属上留下一个空位，如果大量的原子被移动，则连线断开；第二，被移动的原子必须停在某一个地方，在电流方向的末端形成大量堆积。以铜导线为例，电流的趋肤效应导致电子都是在铜导线表面移动。当发生碰撞后，表面的原子不断被撞击的向导线末端移动。原子离开的地方铜线不断变细甚至断开，原子堆积的地方铜线不断变粗甚至有可能和周围铜线接触导致短路。
> IR drop是指在集成电路中电源和地网络上电压下降和升高的一种现象。随着半导体工艺的不断演进，金属互连线的宽度越来越窄，电阻值不断变大（供电电压也越来越小），IR drop的效应越来越明显。因此，现在的芯片最后都把IR drop的分析做为芯片signoff的一个必要步骤。业界的signoff工具大部分采用的是Redhawk。

When the effective resistance of the power network is beyond a certain level (such as that caused by narrow metal lines), the voltage drop (I · R) from the source to the destination could be higher than what is tolerable. 
当供电网络的有效电阻超过一定水平时（例如由狭窄金属线引起的电阻），从源到目的地的电压降可能高于可容忍的范围。

In such cases, the destination transistors might not function correctly. This is the IR drop problem.
在这种情况下，目标晶体管可能无法正常工作。这就是IR下降问题。

In addition to IR drop, the current flowing through the metal line is constantly pushing and moving the metal atoms. 
除了IR下降外，流经金属线的电流不断地推移金属原则。

The magnitude of this action is proportional to the current density. 
这种作用的大小和电流密度成正比。

After a lengthy period of such action, the metal structure can become damaged, and opens or shorts may result. This
is the electromigration (EM) problem. The EM problem will negatively affect a product’s life span. 
经过长期的折中作用，金属结构可能会被损坏，并可能导致打开或短路。这就是电子迁移（EM）问题。EM问题会对产品的寿命产生负面影响。

#### 时钟树综合
In today’s chip operation, almost every action inside the chip is operating on some clock signal. All of the storage elements (flip-flops, latches, and memories) are switched on and off by various clocks. 
在今天的芯片运行中，几乎芯片内部的每一个动作都是在一些时钟信号上操作的。所有存储元件（触发器、锁存器和存储器）都通过各种时钟进行打开和关闭。

Undoubtedly, the entire chip operation is coordinated by clocks (see Chapter 3, Question 25).
毫无疑问，整个芯片的运行都由时钟进行协调。

Delivering the clock signals reliably to the needed elements is a necessity in
physical design. 
在物理设计中，可靠地传输时钟信号给需要的元件是有必要的。

This task is commonly called clock tree synthesis (CTS).
这个任务通常被称为时钟树综合。

#### 时钟树综合的两个基本问题
The two basic concerns in CTS are clock skew and clock tree insertion delay. 
时钟树综合中的两个基本问题是时钟倾斜（clock skew）和时钟树插入延迟（clock tree insertion delay）。

CTS is a very complicated issue since there are many clock domains in a typical SoC design, and each domain has its own requirement. Sometimes,the clock trees between different clock domains must be balanced as well.
时钟树综合是一个非常复杂的问题，因为在一个典型的SoC设计中有许多时钟域，每个域有自己的需求。在不同时钟域之间的时钟树业必须保持平衡。

Furthermore, in the test mode, the cells in various clock domains must be working at the same testing clock speed. This puts additional constraints on the clock structure. 
此外，在测试模式下，不同时钟域的单元必须以相同的测试时钟速度工作。这给时钟结构施加了额外的约束。

#### 层次划分
Another influential issue in floorplanning is hierarchy partition. 
另一个在布图规划中有影响的问题是层次划分。

In some designs, especially large designs, size constraints prevents the entire design from being handled at once by the tools. 
在某些设计中，特别是大型设计中，尺寸限制使工具无法一次处理整个设计。

In such situations, the divide-andconquer strategy is adopted. 
在这种情况下，采用分而治之的策略。

A good partition can turn an otherwise unachievable design into a doable one.
一个好的分区可以把一个无法实现的设计变成一个可行的设计。

It can also help speed up the implementation process significantly by enabling parallelism. 
它还可以通过启用并行性来帮助显著加快实现过程。

However, the trade-off is the efficiency of the area and timing.
然而，权衡的是面积和时间的效率。

In other words, hierarchical design is not as efficient as flat design in terms of area and timing since the place and route tool cannot see the whole picture at once and consequently cannot perform the optimization as one whole piece. 
换句话说，分层设计在面积和时间上不如扁平化设计有效，因为布局布线工具不能一次看到整个版图，因此不能作为一个整体进行优化。

Figure 4.27 is one floorplan example of a real chip.
图4.27是一个真实芯片的布局规划示例。
{% asset_img 5.png 在这里插入图片描述 %}

In this chip, there are almost 400 I/Os, which are located on the chip periphery.About one-third of them are power and ground pins. 
There are five PLLs, one DLL (delaylocked loop), one high-speed DAC, one large, hard macro on-chip processor, and more than 80 SRAM memories in this mixed-signal SoC chip.
这个芯片中，大约有400个I/O，它们位于芯片外围。其中约三分之一是电源和接地引脚。有五个锁相环，一个DLL(延迟锁环)，一个高速DAC，一个大的、硬宏片上处理器，以及超过80个SRAM内存在这个混合信号SoC芯片中。

The central area is reserved for standard cells. As apparent in the figure, there are two levels of physical hierarchies: the top level and the standard cell and macro level. 
中心区域保留给标准单元。如图所示，有两层的物理层次结构：顶层和标准标准单元和宏层（~~这尼玛不是三层吗？~~ ）

As addressed in Question 68, the place and route tool cannot handle the physical hierarchy very efficiently. Having more than two levels
of physical hierarchies degrades the quality of the implementation significantly. 
如问题68所述，布局布线工具不能很有效地处理物理层次结构，拥有两层以上的物理层次结构会显著降低实现的质量。

The five on-chip PLLs are placed carefully with plenty of space in between. This configuration can effectively reduce interference among the PLLs. 
五个片上锁相环被小心地间隔放置在足够的空间里。这个配置会高效降低锁相环之间的干扰。

The large hard macro is placed in the lower right-hand corner to minimize the impact on the chip’s overall routability. 
大的硬宏放在右下角，以减少对芯片整体可路由性的影响。

> 在IC设计的floor plan中，hard macro是指一种被设计成独立单元的固定功能模块。这些模块通常具有较多的连线密度和复杂性，并且被用于执行特定的功能或任务，比如处理器核心、内存控制器、DSP等。
  Hard macro通常由专门的设计师设计，然后可以被其他设计师在整个芯片的不同区域重复使用，以提高设计效率和可靠性。在floor plan中，硬宏通常通过已经定义好的位置和大小来安放，这使得其他普通的逻辑单元可以更容易地与其相互配合并布局。
  相比之下，软宏（soft macro）通常是由标准单元（standard cell）组合而成的，可以在不同的芯片设计中进行重新配置和调整。

The analog DAC is also located in one corner to achieve maximum isolation from the rest of the digital blocks. 
模拟DAC也位于一个角落，以实现和其他数字块的最大隔离。

All of the analog blocks (DAC, PLLs, and DLL) have guard rings embedded in the cell-level layout to minimize noise coupling from the
digital circuitry.
所有模拟块在单元级版图中都嵌入了保护环，以最大程度减少数字电路的噪声耦合。

Moreover, to further trim noise coupling, each analog cell has its own ground, which is not metal-connected to the chip’s main digital
ground (substrate). 
此外，为了进一步减少噪声耦合，每个模拟单元都由自己的接地，而不是金属连接到芯片的主数字接地（基板）。

This floorplan is the starting point for the subsequent place and route steps。
这个布图规划是后续布局布线的起点。

### 个人总结
**floor plan的内容:**
1.确定die size
2.布局I/O(P&G占1/3)
3.布局Macro
4.供电规划和时钟规划
5.层次划分（不是必要的

**明确几个概念：**
 - IR drop和EM
这两个问题都出现在供电规划，一个是电压下降问题，另一个是电子迁移，可能导致短路。

**block最大，其次是macro cell，这包括了软宏和硬宏两类，最后是std cell**

 - macro cell的概念
一个macro cell由多个std cell组成

 - block的概念
一个block是人为划分的一个区域，这些区域通常包含了多个逻辑单元、硬宏或者macro cell。

 - 硬宏的概念
如处理器核心、内存控制器、DSP等，和软宏相比，硬宏的位置和大小基本固定，软宏则可以重新调整和配置。软宏是由多个std cell组成的。


## 《IC Compiler Design Planning User Guide , Version D-2010.03-SP2》
### Creating a Floorplan
本章描述了如何从现有的网表或布局描述中创建和改进布图规划。
- 布图规划描述了核心的大小；
- 标准单元行和路由通道的形状和位置；
- 标准单元防止限制
- 外围I/O、电源、接地、角落、填充pad cell的放置

本章包括以下部分：

-  支持的布图规划类型
-  初始化布图规划
- 精细化布图规划
- 调整I/O布局
- 保存布图规划信息
- 读入现有的布图规划
- 从另一个设计中复制布图规划

#### Supported Types of Floorplans  支持的布图规划类型
这里文档中给出了三种支持的布图规划，分类依据在于块间的间距:
Channel Floorplan 通道型布图规划 块与块之间有一定的间距
Abutted Floorplan 邻接型布图规划 块与块之间紧挨着
Narrow-Channel Floorplan 前两者的均衡

#### Preparing the Design  准备设计
• Connecting Power and
设计中包含电源和接地的宏单元和模块要在初始化floorplan前连接（到对应的net），下面的命令将power，ground和tie-off 引脚连接到power和ground nets
> icc_shell> derive_pg_connection -power_net VDD -power_pin VDD \ 
> -ground_net VSS -ground_pin VSS Ground Ports

• Creating Power and Ground Ports

> The following example connects macro cell pins named VDD to the VDD
> net, pins named  VSS to the VSS net, and creates top-level ports for
> both nets. This command can be used  on a design that contains a
> single power domain. 

下面的例子将macro单元中名为VDD和VSS的引脚连接到VDD net和VSS net，并为所有net创建了顶级port。
该命令可以被使用在包含单电源域的设计上。

> icc_shell> derive_pg_connection -power_net VDD
> -power_pin VDD \  -ground_net VSS -ground_pin VSS -create_ports top

• Adding Power, Ground, and Corner Cells
> Physical-only cells for power, ground, and corner placement might not be part of the 
synthesized netlist and must be added to design. Use the create_cell command to add a 
leaf or hierarchical cell to the current design

用于电源、接地和角落布局的纯物理单元可能不是综合后网表的一部分，必须要加入设计中。
使用create_cell命令为当前设计添加叶子或分层单元。

• Setting the I/O Pad Constraints
> Before initializing the floorplan, you can create placement and spacing settings for I/O pads 
by using the set_pad_physical_constraints command. This command specifies the pad 
cell ordering, orientation, placement side, offset from die edge, and pad-to-pad spacing for 
each I/O pad. After setting the constraints with the set_pad_physical_constraints
command, the initialize_floorplan command places the I/O pad cells accordingly. The 
constraints are stored in the Milkyway database when you save the design.
The initialize_floorplan command places constrained pads first. Any unconstrained 
pads are placed next, using any available pad location. The tool does not place 
unconstrained pads between consecutively ordered constrained pads.
Table 2-2 describes the set_pad_physical_constraints command options. For more 
information about these options, see the man page.

在初始化布图规划之前，可以使用set_pad_physical_constraints命令为I/O pad创建布局和间距设置。该命令指定每个I/O pad单元的顺序、方向、布局方向，和die边缘的偏移量，以及每个I/O pad之间的间距。在使用该命令设计约束后，initialize_floorplan命令将首先布局被约束的pad，接下来将用任何可用的位置来布局所有没约束的pad，该工具不会将不受约束pad连续放置在受约束的pad之间。

• Setting the Pin Constraints
> You can use the set_pin_physical_constraints command to set constraints on individual pins or nets. Use the set_fp_pin_constraints command to set global constraints for a block. If a conflict arises between the individual pin constraints and the global pin constraints, the individual pin constraints have higher priority. The constraints are stored in the Milkyway database

您可以使用set_pin_physical_constraints命令来设置单个引脚或net的约束。使用set_fp_pin_constraints命令为一个块设置全局约束。如果在单个引脚约束和全局引脚约束之间发生冲突，则单个引脚约束具有更高的优先级。约束存储在Milkyway数据库中

• Saving the Pin and Pad Constraints
>You can save the current pin and pad constraints for your design with the write_pin_pad_physical_constraints command. This command creates a constraints file that contains set_pin_physical_constraints and set_pad_physical_constraints commands that you can use to reapply pin and pad constraints. The positional information for the pins and pads is based on their current location in the design.
你可以用write_pin_pad_physical_constraints命令为当前设计保存pin和pad约束。该命令创建一个约束文件包含set_pin_physical_constraints和set_pad_physical_constraints命令，可以使用这些命令重新应用pin和pad约束。引脚和pad位置基于当前在设计中的位置。

• Reading an Existing Pad and Pin Constraints File
>Use the read_pin_pad_physical_constraints command (or by choosing Floorplan > Read Pin/Pad Physical Constraints in the GUI) to read a file that contains set_pin_physical_constraints and set_pad_physical_constraints commands. The read_pin_pad_physical_constraints command applies the constraints to the current design or to another design that you specify.The constraints defined in the file can either remove the current constraints or append to them, based on the behavior you choose. For example, if physical constraints for pin A are 
specified and you do not define any constraints for pin A in the constraints file, the read_pin_pad_physical_constraints command removes the existing physical constraints on pin A by default. To maintain the existing constraints and append new constraints contained in the constraints file, specify the -append option (or click the “Append” check box in the GUI).

读取现有的Pad和Pin约束文件使用read_pin_pad_physical_constraints命令(或通过在GUI中选择Floorplan > Read Pin/Pad Physical Constraints)读取包含set_pin_physical_constraints和set_pad_physical_constraints命令的文件。read_pin_pad_physical_constraints命令将约束应用于当前设计或指定的其他设计。

根据您选择的行为，文件中定义的约束可以删除当前约束或追加约束。例如，如果指定了引脚A的物理约束，并且您没有在约束文件中为引脚A定义任何约束，**则read_pin_pad_physical_constraints命令默认情况下会删除引脚A上现有的物理约束**。要维护现有的约束并附加约束文件中包含的新约束，请指定-append选项(或在GUI中单击“append”复选框)。

• Reporting the Pad and Pin Constraints
>Use the report_pin_pad_physical_constraints command to display a list of set_pin_physical_constraints and set_pad_physical_constraints commands that define the pin and pad constraints for the current design. You can report only pin constraints, only pad constraints, only chip-level pad constraints, or all constraints depending on the command options you specify.

使用report_pin_pad_physical_constraints命令显示set_pin_physical_constraints和set_pad_physical_constraints命令的列表，这些命令定义当前设计的引脚和垫约束。根据您指定的命令选项，您可以仅报告引脚约束、仅报告垫约束、仅报告芯片级垫约束或所有约束

• Removing the Pad and Pin Constraints
>Use the remove_pin_pad_physical_constraints command to remove all constraints 
previously set by using the set_pin_physical_constraints and 
set_pad_physical_constraints commands. You can remove only pin constraints, only 
pad constraints, only chip-level pad constraints, or all constraints based on the command 
options you specify. You can also remove constraints from a design other than the currently 
open design

使用remove_pin_pad_physical_constraints命令删除之前使用set_pin_physical_constraints和set_pad_physical_constraints命令设置的所有约束。您可以根据指定的命令选项仅删除引脚约束、仅删除垫约束、仅删除芯片级垫约束或所有约束。您还可以从当前打开的设计之外的设计中删除约束

### 初始化Floorplan

未完待续~~
