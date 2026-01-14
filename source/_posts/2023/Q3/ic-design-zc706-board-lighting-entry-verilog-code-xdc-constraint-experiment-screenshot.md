---
title: 【IC设计】ZC706板卡点灯入门（含Verilog代码，xdc约束，实验截图）
date: 2023-09-19 13:16:05
categories: 数字IC设计
tags: [FPGA, Verilog]
layout: post
---

> 这篇博客将针对AMD Zynq 7000 SoC ZC706 Evaluation Kit板卡(对应Vivado创建工程时FPGA型号：XC7Z045ffg900-2)实现基本的点灯程序。
## 假定已知的前置知识
本文对以下内容不再介绍，
 - 使用Vivado进行综合、实现、生成比特流并烧录FPGA
 - FPGA的概念、Verilog的基础语法

{% asset_img 1.png 在这里插入图片描述 %}
## 需求：
板卡时钟为200MHz，让板子上的一个LED灯**保持**0.5秒亮，0.5秒灭。

## 注意点：
①板卡使用JTAG接口烧录时，必须将SW4拨为01，如图所示：
{% asset_img 2.png 在这里插入图片描述 %}
②ZC706的时钟都是差分时钟，必须使用Verilog原语将其转换为单端时钟才可以直接使用：
>     IBUFGDS IBUFGDS_inst(
>         .O(single_clock),    //Clock buffer Output
>         .I(clk_p),  //Diff_p clock buffer input (connect directly to top-level port)
>         .IB(clk_n)  //Diff_n clock buffer input(connect directly to top-level port)
>     );
其中IBUFGDS是Xilinx的原语，不需要引入IP，可以直接使用。

③对于200MHz的时钟，即每秒运行2*10^8个周期，想要每0.5s亮，0.5秒灭，就是要求每0.5秒将led取反一次，
那么应当让计数器，计数到1*10^8个周期时对led取反。

## 代码实现：
### 顶层模块

```haskell
`timescale 1ns / 1ps
module top_module(
    input clk_n,
    input clk_p,
    input rst_b,
    output led
);
    wire single_clock;
    IBUFGDS IBUFGDS_inst(
        .O(single_clock),    //Clock buffer Output
        .I(clk_p),           //Diff_p clock buffer input (connect directly to top-level port)
        .IB(clk_n)           //Diff_n clock buffer input(connect directly to top-level port)
    );
    Hello hello_inst(
        .clock(single_clock),
        .reset(rst_b),
        .io_led(led)    
    );
    
endmodule
```
### led闪烁模块
```haskell
module Hello(
  input   clock,
  input   reset,
  output  io_led
);
  reg [31:0] cntReg; 
  reg  blkReg; 
  wire [31:0] _cntReg_T_1 = cntReg + 32'h1; 
  assign io_led = blkReg; 
  always @(posedge clock) begin
    if (reset) begin 
      cntReg <= 32'h0; 
    end else if (cntReg == 32'd100_000_000) begin 
      cntReg <= 32'h0; 
    end else begin
      cntReg <= _cntReg_T_1; 
    end
    if (reset) begin 
      blkReg <= 1'h0; 
    end else if (cntReg == 32'd100_000_000) begin 
      blkReg <= ~blkReg;
    end
  end
endmodule
```

### xdc约束

```bash
#绑定复位按钮
set_property PACKAGE_PIN AK25 [get_ports rst_b]

#设置复位按钮的IO电压为2.5V
set_property IOSTANDARD LVCMOS25 [get_ports rst_b]

#对Verilog中的led端口和板卡上的Y21灯进行绑定
set_property PACKAGE_PIN Y21 [get_ports led]

#设置IO电压为2.5V
set_property IOSTANDARD LVCMOS25 [get_ports led]

#clk_p和clk_n是两个差分时钟信号，要通过IBUFGDS原语转化到单端时钟再使用
set_property PACKAGE_PIN H9 [get_ports clk_p]
set_property PACKAGE_PIN G9 [get_ports clk_n]
set_property IOSTANDARD LVDS [get_ports clk_p]
set_property IOSTANDARD LVDS [get_ports clk_n]
```

