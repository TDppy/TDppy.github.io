---
title: 【IC设计】ICC1 workshop lab guide 学习笔记——Lab1 Data Setup&Basic Flow
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计]
layout: post
---
@[TOC]
# Lab1 Data Setup&Basic Flow
## 1.1 Create a Milkyway library

lab1_data_setup目录下有
.synopsys_dc.setup
scripts
risc_chip.mw
design_data

其中.synopsys_dc.setup中设置了若干变量，设置了搜索路径、verilog设计、sdc、def、tech_file、tlu、db库等的路径，以方便在后面使用icc时能直接调用。

启动icc_shell后会自动调用.synopsys_dc.setup，可以通过printvar来验证变量是否已设置

了解了.synopsys_dc.setup后，下面就创建设计库（即Milkyway library)
写入库的路径、库名、tf文件路径、添加reference libraries，这些都可以使用刚刚加载的变量名来替代。
其中reference libraries需要添加ref/mw_lib/的sc、ram16x128、io三个库

这些库是Milkyway参考库：
> 信息是以被称为“views”的形式存储的，例如：
> 
> CEL:完整的版图信息
> 
> FRAM:用于布局布线的抽象化的版图物理信息（只有单元大小、端口名称、端口位置等简单的物理信息）
> 
> LM:带有时序和功耗信息的逻辑模型（可选*），该文件对于后端布局布线不是必须的，IC
> Compiler只通过link_library变量来读取指定的(.db)格式的逻辑库。
> 
> 对于那些标准单元库、IO库、Memory或者其他Macro，如果设计中没有CEL View以及FRAM
> View，则可以在Milkway软件中通过简单的read_lef文件的方式生成这些文件。其中lef文件全拼为：Library
> Exchange Format。

创建完成后可以使用ls -a risc_chip.mw来查看库里的东西
有CEL lib lib_1 lib_bck .lock文件

**总结：**
这一节介绍了.synopsys_dc.setup设置了若干变量，该文件会在icc_shell启动时自动执行，进而在使用icc创建库时可以调用这些变量，无需手写。milkyway库保存了后端工作的全部信息，创建时需要指定库的存储路径，名字，参考的其他mw库，创建成功后会生成lib_name.mw，目录下有CEL，lib等文件。

**涉及的相关脚本和命令：**
.synopsys_dc.setup中
suppress_message是压制某些警告，我记得这个在学习java框架SpringBoot时也有相关注解，主要是告诉工具不要输出某些无所谓的警告。
history keep 100 这个应该是控制command.log记录100条最近执行的指令，缺省是20条
set_app_var和set都是设置变量 感觉区别不太大
alias是取别名，属于shell指令，把一些比较长的命令取别名为短的
lappend 变量 路径  这个含义是把该变量当做一个list，在其后增加一条路径，并和前面已有路径用空格隔开
set_min_library 没查过，无非是设置库
sdc_file是dc时可以write出来的，我感觉就是把dc设置的时序参数写出来
def_file是floor plan需要导入的
ctrl_file是opt_ctrl.tcl脚本

## 1.2 Load the Netlist,TLU+,Constraints and Controls
上一节创建了RISC_CHIP库，这里打开该库，导入Verilog设计（是dc出来的网表，一般命名为mapped.v或netlist.v)，
然后导入TLU+文件，有3个文件

```bash
set_tlu_plus_files -max_tluplus $tlup_max \
-min_tluplus $tlup_min \
-tech2itf_map $tlup_map
```
关于TLU+

> TLUPlus is a binary table format that stores the RC coefficients.  The TLUPlus models
enable accurate RC extraction results by including the effects of width, space, density, and
temperature on the resistance coefficients.  For details about modeling these effects in the
Interconnect Technology Format (ITF) file, see the StarRC documentation.

即TLU+是存放RC系数的文件。
检查物理和逻辑库的一致性、检查TLU是否已经加入：
check_library
check_tlu_plus_files
验证指定的link库已被加载
list_libs
定义power/ground的逻辑连接 
source $derive_pg_file
check_mv_design -power_nets
读sdc文件 read_sdc $sdc_file
检查时序 check_timing
添加时序和优化控制
source $ctrl_file
运行零互联时延报告
保存mw_cel

**总结：**
这一节打开了上节创建的RISC_CHIP库，导入网表、TLU，定义了power/ground的逻辑连接，读入sdc文件，添加时序和优化控制，最后输出零互联时延报告，涉及到source脚本，各种check，还是不那么好彻底理解的。但是总体来说还是对项目进行一些基本的配置，然后输出时延报告，还没有进入到floor plan的步骤。

**涉及的相关脚本和命令：**
导入设计:
import_designs $verilog_file -format verilog -top $top_design

设置TLU+ ：
set_tlu_plus_files -max_tluplus $tlup_max \
-min_tluplus $tlup_min \
-tech2itf_map $tlup_map

检查物理和逻辑库的一致性：
check_library

检查TLU+ 文件被添加，通过了检查:
check_tlu_plus_files

验证link libraries已经被加载(我的理解就是sc io ram16x128的db库
list_libs

定义power/ground的管脚和网络之间的逻辑连接
soruce $derive_pg_file   #这个文件路径在./scripts/derive_pg.tcl
check_mv_design -power_nets

应用顶级设计约束
read_sdc $sdc_file

检查时序约束
check_timing

检查时序异常约束
report_timing_requirements

检查是否有路径禁用时序分析
report_disable_timing

检查设计是否被配置为特定模式或者用例
report_case_analysis

验证clocks是否被合适地建模:
report_clock
reprot_clock -skew

应用时序和优化控制
source $ctrl_file

跑0互联时序报告
source sc[TAB]z[TAB]
#The above file scripts/zic_timing.tel contains:
#set_zero_interconnect_delay_mode true
#redirect -tee zic.timing { report_timing }
#set_zero_interconnect_delay_mode false

查看zic.timing内容
exec cat zic.timing

移除理想network
remove_ideal_network [get_ports scan_en]

保存cel
save_mw_cel -as RISC_CHIP_data_setup

涉及到的脚本和命令相当多，需要查iccug，结合实践，加以理解。

## 1.3 Basic Flow:Design Planning
这一节提供了一个DEF格式的预定义好的floor plan file，
读入def文件，read_def $def_file
确保standard cells在power和ground metal routes之上
保存该设计cel，该文件会保存到risc_chip.mw/CEL（也就是说还是在刚刚的项目里操作）

**总结：**
读入预定义好的floor plan file

**涉及的相关脚本和命令：**
read_def $def_file
set pnet options -complete {METAL3 METAL4}
save_mw_cel -as RISC_CHIP_floorplanned


## 1.4 Bsic Flow:Placement
使用place_opt进行布线
分析拥塞
最后保存

**总结：**
疑问是，自动布线，不需要自己动手吗？那我之前上课学到的布线相关的命令是做什么的？

**涉及的相关脚本和命令：**
place_opt
redirect -tee place_opt.timing {report_timing}
report_congestion -grc_based -by_layer \ 
-routing_stage global
save_mw_cel -as RISC_CHIP_placed

## 1.5 Basic Flow:CTS
使用命令进行时钟树综合，然后展示时钟树。
保存cel
退出icc，discard all

**总结：**
似乎看着也很简单，就是几行命令搞定cts，那么后面需要自己动手试一试是否能跑的出来。

**涉及的相关脚本和命令：**
remove_clock_uncertainty [all_clocks]
set_fix_hold [all_clocks] 
clock_opt
redirect -tee clock__opt. timing { report_timing}
save rnw cel -as RISC CHIP cts



## 1.6 Basic Flow:Routing
重新打开icc_shell，打开设计，选择库，重做一遍timing和optimization controls，因为这些步骤中的变量在退出icc后就没了。
然后route_opt进行自动布线
布线后输出时序报告。
保存退出

**总结：**需要对相关的命令查一下iccug，有基本的认知了解，再进行学习可能更好。

**涉及的相关脚本和命令：**
source $ctrl file
route opt
report_design -physical
save_mw_cel -as RISC_CHIP_routed
