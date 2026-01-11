---
title: 【IC设计】ICC workshop Lab1 数据准备&基本流程 【脚本总结】 (1)
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计]
layout: post
---
## Task 1 Create a Milkyway library
先进入lab1_data_setup目录，打开icc_shell，创建项目

```bash
create_mw_lib -technology $tech_file -mw_reference_library "$mw_path/sc $mw_path/io $mw_path/ram16x128" -bus_naming_style {[%d]} -open $my_mw_lib
```

然后`ls risc_chip.mw`查看是否创建成功 


## Task 2 Load the Nestlist,TLU+,Constraints and Controls
```bash
import_designs $verilog_file -format verilog -top $top_design
set_tlu_plus_files -max_tluplus $tlup_max -min_tluplus $tlup_min -tech2itf_map $tlup_map
check_library
check_tlu_plus_files
list_libs
source $derive_pg_file
check_mv_design -power_nets
read_sdc $sdc_file
check_timing
report_timing_requirements
report_disable_timing
report_case_analysis
report_clock
report_clock -skew
source $ctrl_file
source sc[TAB]z[TAB]
exec cat zic.timing
remove_ideal_network [get_ports scan_en]
save_mw_cel -as RISC_CHIP_data_setup
```


## Task3 design planning
```bash
read_def $def_file
set_pnet_options -complete {METAL3 METAL4}
save_mw_cel -as RISC_CHIP_floorplanned
```
![在这里插入图片描述](/images/38c269cbca926247d80cb7b765fd1e6c.png#pic_center)

![在这里插入图片描述](/images/4d01888b6afe698ce38d199a5ce9b0ac.png#pic_center)


## Task4 placement
```bash
place_opt
redirect -tee place_opt.timing {report_timing}
report_congestion -grc_based -by_layer -routing_stage global
save_mw_cel -as RISC_CHIP_placed
```
![在这里插入图片描述](/images/358604a3c461c1cbdd82fbe9aed0c237.png#pic_center)


## Task5 CTS

```bash
remove_clock_uncertainty [all_clocks]
set_fix_hold [all_clocks]
clock_opt
redirect -tee clock_opt.timing {report_timing}
save_mw_cel -as RISC_CHIP_cts
```
![在这里插入图片描述](/images/dd8d9ffb7af73c5ef27d33914a609a74.png#pic_center)
![在这里插入图片描述](/images/7f0bf6fee46c6aeb5c2bd9d0cc77abbf.png)

## Task6 Basic Flow:Routing
File->Open design ，risc_chip.mw 
Select RISC_CHIP_cts
相当于`open_mw_cel RISC_CHIP_cts`
```bash
source $ctrl_file
route_opt
view report_timing -nosplit
v rt
v rt -delay min
report_design -physical
save_mw_cel -as RISC_CHIP_routed
exit
```
![在这里插入图片描述](/images/d9c6bea0c705080523589b01820f1775.png#pic_center)

