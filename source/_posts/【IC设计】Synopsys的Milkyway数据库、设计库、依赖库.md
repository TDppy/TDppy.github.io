---
title: 【IC设计】Synopsys的Milkyway数据库、设计库、依赖库
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计]
layout: post
---
﻿## Milkyway database for Synopsys Galaxy Design Platform
Synopsys Galaxy Design Platform（Synopsys银河设计平台）包括的系列工具有：
DC、ICC、StarRC、IC Validator、PrimeRail、Milkyway Environment

Milkyway（银河）数据库是为Synopsys银河设计平台服务的数据库，方便工具直接通过接口对数据库进行读写，而不是以ASCII文件中间文件的形式进行操作。

**不同EDA软件和mw库的交互：**
** DC**
 write_milkyway或write_verilog或write_ddc  即DC的写出可以用mw格式
 
**ICC**
从mw中读入physical design info和library cell info 写出也用mw格式
mw环境可以将GDSII,IASIS和LEF/DEF转换成为新的lib cell，从而成为mw格式

**StarRC**
从mw库中读入物理设计信息来执行寄生RC参数提取，并写回到数据库中，方便ICC读取和使用时序信息。

mw的基本单元是cell，cell可大可小，可以是via，可以是整个芯片
通过使用open_mw_cel打开cell进行编辑，这个cell必须包含在已经打开的mw库中

每个门级标准单元都有CEL view和FRAM view,
FRAM view用于布局布线，里面有Verilog综合后网表调用的IP硬核，而CEL view用于生成最终的掩膜数据流来进行芯片制造。

**PrimeRail：**在mw数据库的RAIL view中存储它的rail分析结果

不要使用操作系统命令如cp或者rm去对mw数据进行增删改查，使用可兼容的工具，例如ICC或者mw环境来对cell view进行操作

**设计库与依赖库：**
创建mw库，创建一个cell，你的所有设计就在这个cell里面，然后这个cell在编辑时可以引用当前mw库里的cell，也可以引用未打开的mw库里的cell，当前正在编辑的库称为设计库，其他引用了cell但未打开mw库的称为依赖库


```bash
#打开库
open_mw_lib

#关闭库
close_mw_lib

#设置引用库
set_mw_lib_reference -mw_reference_library {/mw/LIBS/mw_lib_B /mw/LIBS/mw_lib_B}  /mw/LIBS/mw_lib_A

#报告引用库
report_mw_lib -mw_reference_library mw_lib_A
```

