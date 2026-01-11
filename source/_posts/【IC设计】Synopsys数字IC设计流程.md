---
title: 【IC设计】Synopsys数字IC设计流程
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计]
layout: post
---
@[TOC]
# 数字IC设计流程
数字IC设计流程如下：
需求->芯片定义specification->算法描述（一般用C++)->RTL级描述（Verilog）->HDL功能仿真->逻辑综合（DC）->门级仿真（仿真网表）->形式化验证>物理设计（floor plan，place，cts，route等）->签核（chip finish，StarRC提取寄生RC，PT时序分析，DRC&LVS等）

## 前端设计
### RTL编写和HDL仿真
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c33fa49085488d1e8020ccfeec2d4303.png)

用Verilog实现芯片各个模块的功能，如写一个四位乘法器multipleir.v和它的测试文件tb_multiplier.v并使用VCS编译并仿真，使用Verdi查看波形，通过RTL功能验证。

### 逻辑综合
使用DC（Design Compiler）综合RTL代码，生成门级网表（Gate-Level Netlist）。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f2c18dd2e965e5064f5e8cb386b861eb.png)

具体来说，DC实际上将RTL先翻译成 了内部可识别的GTECH形式的中间代码，然后再根据所提供的**目标库**和**设计约束**来映射和优化出最终的网表文件netlist.v。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/712b74c3a428b41545a741a4ba746000.png)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fecdf4ae29eb6ae43958ff294ee160d6.png)

在使用Synopsys DC进行逻辑综合时，基本可以分为四步：

 1. 预综合过程（设置目标库、链接库等）
 2. 施加设计约束（如信号从0到1需要的transition time）
 3. 设计综合（指使用compile命令后进行编译的过程）
 4. 后综合过程（如将网表文件从内存写出为netlist.v）
 
### 门级仿真
使用VCS编译dc生成的网表文件和tb文件，对门级网表进行仿真，进行该仿真的原因是dc设置了时序约束，该仿真会比HDL仿真更加真实。

### 形式化验证
使用formality进行形式化验证，是对网表文件和RTL代码之间映射的检验，在数学上验证该网表能实现对应RTL的功能。

## 后端设计
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/94aaa8ef90929669b00c4149fb21a502.png)

后端工作的**输入**是前端生成的网表文件和sdc约束文件
后端工作的**输出**的是GDS（Geometry Data Standard）版图，GDS是描述电路版图的格式，包含制造一颗芯片所需的全部信息，芯片制造商（fab）只需要IC设计公司提交GDS用于芯片生产。
后端工作的**目标**是生成符合要求的GDS版图，理想的GDS版图要求包括：
1. 功能上和RTL一样
2. 物理规则上，fab能拿它正常制造
3. PPA，即性能，功耗，面积尽可能达到最优

后端设计的**基本流程（basic flow）**如下图所示：
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/40e7af444f9fe981bf828c78a266298e.png)
### 数据准备
下面将介绍数据准备工作中涉及重要命令及相关概念。
#### set mw_phys_refs *
  set mw_phys_refs *
 物理库文件以LEF为后缀 (Cadence)或以Milkyway database(Synopsys) 形式出现，包含PR 所需的必要 的物理信息和几何信息。
 物理库文件分为两种，一种与工艺相关，包含金属层的所有几何定义，通常foundry 提供不同的金属 层范围供设计者选择。另外一种和IP 包含的CELL 相关， 所有的standard cell 、IO cell 、Macro 都需要提 供相应的物理库文件。
 导入数据时需要导入一个工艺相关的LEF文件和所有CELL 的LEF 文件。
 ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ec5d81347913eade3227219bda85f4cd.png) ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/edf127a984f2f30d7f346a0003c6a7d0.png)
#### set link_library *
•  用于描述物理单元的时序和功耗信息的重要库文 件
•  时序库可以依据不同的延时模型来建库，常用的 有NLDM 和CCS 两种模型， CCS 比NLDM 更精确。 一个IP 库通常提供一套lib 文件，分别对应不同的 PVT corner ，通常lib 文件数量是PVT corner 的各种 排列组合。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/498f01e548b6bc83aa8261a55fb2ea7e.png)
#### 数据准备 (SDC)
•  SDC是一个设计中至关重要的一部分，它对电路的时序、面积、功耗进行约束，是设计的命 脉，决定了芯片是否满足设计要求的规范。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0ed58732b7d05fb232d68fc548778f6b.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/adab953c517fa176139224a57a5ca83b.png)
#### 数据准备 (RC Techfile) set_tlu_plus_files
•  RC techfile 包含了对金属层做RC 提取所需的所有信息，通常以qrcTechfile  (Cadence)或者 tluplus  (Synopsys)两种形式出现，保存在foundry 提供的PDK 中。
•  65nm 以下设计需要5种RC corner：typical, cbest, cworst, rcbest,rcworst。 每个corner 对应一份RC techfile，均需要导入PR 工具用以计算线延时。
•  准备好物理文件及时序文件，即可建立相应的database，
如图所示，在做floor plan之前，芯片的IO、Macro全部堆叠在一起。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8d4a34f62b76d50fd0fb8eb5ff64e3da.png)


### floor plan
 整个流程中，除了floorplan阶段需要较多的手工活之外，placement、CTS、routing阶段可以说就是设计者通过修改脚本和约束，然后让工具自动完成工作。这也是IC Compiler工具强大之处。
 
- Floorplan的好坏直接影响到设计频率和布线效率
#### Floorplan阶段的主要内容： 
- 芯片尺寸形状的确定
- IO单元、 filler填充和corner pad的位置摆放
- 宏单元的放置及blockages的规划
- 电源地网络的分布
#### 常用命令：
  - create_floorplan
  - drive_pg_connection
  - add_end_cap
  - insert_stdcell_filler
  - add_tap_cell_array
  - create_power_straps
  - create_fp_placement

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e32391e0829e3b280c44a689ec9915d1.png)

### placement
布局 (Placement)
#### 概念：
布局规划阶段完成芯片的整体规划，而布局阶段主要是软件**自动**进行标准单元的摆放。  
 - 完成布局和时序优化的设置
 - 完成DFT和功耗优化的设置
 - 完成标准单元的摆放(主要是宏单元)
 - 分析拥塞、时序和功耗
 - 优化
#### 常用命令：
• place_opt
- Coarse placement:将标准单元粗略摆放好
- Auto High Fanout Synthesis(AHFS) : 解high fanout操作，优化时序
- Logic Optimization:根据需要个性优化,过程主要有cell sizing, moving, net spitting,
- gate cloning, buffer insertion和area recovery等小步骤组成
- Placement Legalization：标准单元放置在row上，保证所有cell处于legal的状态
  ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5901f97d9107817f757e96f3e551693c.png)


### cts
• 时钟树综合(CTS)
#### 为什么要时钟树综合？
   在大规模集成电路中，大部分时序元件的数据传输是由时钟同步控制的时钟频率决定了数据处理和传输的速度，时钟频率是电路性能的最主要的标志。在集成电路进入深亚微米阶段，决定时钟频率的主要因素有两个，一是组合逻辑部分的最长电路延时，二是同步元件内的时钟偏斜(clock skew),随着晶体管尺寸的减小，组合逻辑电路的开关速度不断提高，时钟偏斜成为影响电路性能的制约因素。时钟树综合的主要目的是减小时钟偏斜。
    **以一个时钟域为例，一个时钟源点(source )最终要扇出到很多寄存器的时钟端(sink)，从时钟源扇出很大，负载很大，时钟源是无法驱动后面如此之多的负载的。这样就需要一个时钟树结构，通过一级一级的buffer去驱动最终的叶子结点(寄存器)。**

#### 时钟树综合的概念
•  时钟树综合是指从clock的root点长到各个sink点的clock buffer/inverter tree。目的是将某个 clock所属的所有sinks尽可能做到相同长度，尽可能的使一个时钟信号到达各个终端节点的 时间相同。
####  一般要求
 clock skew尽量小，特别是对时钟质量要求比较高或者高频时钟；
 clock latency尽量短
#### 常用命令：
  set_clock_tree_exceptions
  remove_clock_tree
  compile_clock_tree
  optimize_clock_tree
  clock_opt
 
时钟树相关连线高亮图如下，其中时钟分4级，分别用黄色、紫色、蓝色、橙色表示，其中时钟源从clk_iopad引出，用黄色表示。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5e6ffba674dcb054fbc2a18bb0cd8743.png)


### route
布线 (Route)
#### 作用：
•  完成标准单元的信号线的连接， 布线工具会自动进行布线拥塞消除、优化时序、减小耦合 效应、消除窜扰、降低功耗、保证信号完整性等问题。
- Track: 黄色和蓝色的虚线。 Track没有实际宽度， 只用于布线走线的轨迹。
-  Pitch:Track之间的间距。定义于TF文件。
- Grid Point:横纵Track的交点
- Trace:相比Track ，Trace是实际的金属线，具有宽度。
#### route_opt:
 - Global routing: 对整块芯片的走线做布局规划，并没有进行任何实际走线
为指定的金属层和Gcells分配线路
 - Track assignment: 将GR设计的每一跟连线分配到track上， 并对连线进行实际布线
这个阶段不做DRC检查
-  Detail routing: 将TA产生的DRC violation移除，使用固定尺寸的switch box来修复违规
-  Search and repair: 通过逐渐增大Sbox的尺寸,寻找和消除Detail routing中没有完全消除的DRC违规。
  ![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/aa965270fcb7f0befe91a404bd1583de.png)
  布线后的图（可以看到除了之前时钟树的连线外，增加了对各个模块的连线）
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7f7ab3b6eebc92218ccb6eef5bdbc712.png)

### 签核（sign off）
签核包括chip finish、后仿工作
#### chip finish
Chip finish 为提高良率和解决物理规则违规做的工作，一般包括插入filler cells、insert metal fill、修复antenna等
#### 后仿
 为什么要后仿？
 后仿的目的在于消除或减小理论结果与实际结果之间的差异 ，前仿的网表中认为**各根连线的电阻电容均为零**，而事实并非如此。如果这些寄生电阻电容效应足够大，那么实际做出的电路就和前仿差别较大。
 ICC将版图生成以后，版图中的连线及连线间的寄生电阻（Resistance），寄生电容（Capacitance），都是前仿中没有添加的。使用StarRC工具抽取ICC写出的电路网表中的寄生参数，接着，使用PrimeTime工具获得寄生参数信息后写出sdf（standard delay format文件），再将该文件反标入ICC的电路网表，输出仿真结果，此时后仿考虑了实际连线的RC延时。
 
#### DRC&LVS
用 Calibre DRC&LVS 物理验证
## 参考资料
1.VLSI数字后端设计入门 ，来自上海科技大学VLSI课程
2.数字IC后端设计技术全局观
3.[Synopsys逻辑综合及DesignCompiler的使用](https://blog.csdn.net/qq_42759162/article/details/105541240)
4.[关于数字IC后端设计的一些基础概念与常识](https://blog.csdn.net/mjwwzs/article/details/77413454)
5.IC Compiler I Lab Guide ，来自Synopsys ICC官方文档

