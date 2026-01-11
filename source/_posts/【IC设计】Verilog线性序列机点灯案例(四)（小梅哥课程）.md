---
title: 【IC设计】Verilog线性序列机点灯案例(四)（小梅哥课程）
date: 2026-01-11 15:30:00
categories: 数字IC设计
tags: [Verilog]
layout: post
---
@[TOC]

> 声明：案例和代码来自小梅哥课程，本人仅对知识点做做笔记，如有学习需要请支持官方正版。

# 该系列目录：
[Verilog线性序列机点灯案例（一）](https://blog.csdn.net/qq_42622433/article/details/136727036)
[Verilog线性序列机点灯案例（二）](https://blog.csdn.net/qq_42622433/article/details/136742479)
[Verilog线性序列机点灯案例（三）](https://blog.csdn.net/qq_42622433/article/details/136766843)
[Verilog线性序列机点灯案例（四）](https://blog.csdn.net/qq_42622433/article/details/136796718)
# 设计环境
Vivado2018.3 软件
Zynq-7000 xc7z010clg400-1 板卡
# 设计目标
在案例（三）中提到让一个led根据8个拨码开关的值来循环变化，每个拨码开关负责0.25秒，一共是2秒。
在任务（四）中我们需要在每次动态变化前加入1秒的空闲时间（空闲时间led是熄灭的）
![在这里插入图片描述](/images/5f3242f7654e375b4625600feef45bb1.png)
# 设计思路
1秒的空闲时间需要一个计数器来计算，假设为counter0
2秒的动态变化可以像案例（二）中一样用两个计数器来完成，假设为counter1和counter2
counter1用来计数0.25秒，counter2在counter1每次计满时加1，最后将sw[counter2]输出给led。
需要注意的是，动态变化是从1秒空闲时间后开始的，所以counter1和counter2必须在counter0计满以后才能开始工作。
在动态变化完成后，即counter1和counter2都计满的情况下，counter0再次重新开始工作。

# RTL及Testbench代码
## RTL代码

```rust
module led_ctrl3(
    clk,
    rst_n,
    sw,
    led_out
);
    input clk;
    input rst_n;
    input [7:0] sw;
    output reg led_out;
    
    //counter0用于计数一秒钟
    reg [25:0] counter0;
    
    //counter1用于计数0.25秒
    reg [25:0] counter1;
    
    //counter2用于计数0到7
    reg [2:0] counter2;
    
    //标记可以闪烁了
    reg flag;
    
    //50M cycles
    parameter MCNT1S = 50_000_000;
    
    //12.5M cycles
    parameter MCNT025S = 12_500_000;
    
    //控制flag状态
    //flag为0时为空闲状态，led熄灭，counter0开始计数到1秒
    //flag为1时为忙碌状态，led动态闪烁，counter1和counter2正常计数
    always@(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            flag <= 0;
        end else if(counter0 == MCNT1S -1 ) begin
            flag <= 1;
        end else if( (counter1 == MCNT025S -1) && (counter2 == 7) ) begin
            flag <= 0;
        end else begin
            flag <= flag;
        end
    end
    
    //计数空闲的1秒
    always@(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            counter0 <= 0;
        end else if(flag == 0) begin
            if(counter0 == MCNT1S -1)begin
                counter0 <= 0;
            end else begin
                counter0 <= counter0 + 1;
            end
        end
    end
    
    //负责在flag为1时计算0.25秒
    always@(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            counter1 <= 0;
        end else if(flag == 1) begin
            if(counter1 == MCNT025S - 1) begin
                counter1 <= 0;
            end else begin
                counter1 <= counter1 + 1;
            end
        end
    end
    
    //当flag为1时，counter2每当counter1计满时自增1
    //如果counter1和counter2都计满，则进入空闲时刻
    always@(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            counter2 <= 0;
        end else if(flag == 1) begin
            if(counter1 == MCNT025S - 1) begin
                if(counter2 == 7) begin
                    counter2 <= 0;
                end else begin
                    counter2 <= counter2 + 1;
                end
            end
        end
    end
    
    //负责根据counter2决定led_out输出
    always@(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            led_out <= 0;
        end else begin
            if(flag) begin
                case(counter2)
                    0:led_out <= sw[0];
                    1:led_out <= sw[1];
                    2:led_out <= sw[2];
                    3:led_out <= sw[3];
                    4:led_out <= sw[4];
                    5:led_out <= sw[5];
                    6:led_out <= sw[6];
                    7:led_out <= sw[7];
                endcase
            end
        end
    end
endmodule
```

## Testbench

```rust
`timescale 1ns / 1ps

module tb_led_ctrl3();
    reg clk;
    reg rst_n;
    reg [7:0] sw;
    wire led_out;
    led_ctrl3 led_ctrl3_inst0(
        .clk(clk),
        .rst_n(rst_n),
        .sw(sw),
        .led_out(led_out)    
    );
    defparam led_ctrl3.MCNT1S = 50_000;
    defparam led_ctrl3.MCNT025S = 12_500;
    initial begin
        clk = 1;
    end
    
    always #10 clk=~clk;
    
    initial begin
        rst_n = 0;
        #205;
        rst_n = 1;
        sw = 8'b01010101;
        #3_000_000;
        sw = 8'b11110000;
        #3_000_000;
        $stop;
    end
endmodule

```
## xdc约束

```rust
set_property PACKAGE_PIN T14 [get_ports led_out]
set_property PACKAGE_PIN U18 [get_ports clk]
set_property PACKAGE_PIN F20 [get_ports rst_n]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[7]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[6]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[5]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[4]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[3]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[2]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[1]}]
set_property IOSTANDARD LVCMOS33 [get_ports {sw[0]}]
set_property IOSTANDARD LVCMOS33 [get_ports clk]
set_property IOSTANDARD LVCMOS33 [get_ports led_out]
set_property IOSTANDARD LVCMOS33 [get_ports rst_n]
set_property PACKAGE_PIN E17 [get_ports {sw[7]}]
set_property PACKAGE_PIN D18 [get_ports {sw[6]}]
set_property PACKAGE_PIN H15 [get_ports {sw[5]}]
set_property PACKAGE_PIN F16 [get_ports {sw[4]}]
set_property PACKAGE_PIN J14 [get_ports {sw[3]}]
set_property PACKAGE_PIN G14 [get_ports {sw[2]}]
set_property PACKAGE_PIN L15 [get_ports {sw[1]}]
set_property PACKAGE_PIN K14 [get_ports {sw[0]}]
```


# 仿真结果
![在这里插入图片描述](/images/99ef3792d0b8b56b0218ef3341227c1d.png)



