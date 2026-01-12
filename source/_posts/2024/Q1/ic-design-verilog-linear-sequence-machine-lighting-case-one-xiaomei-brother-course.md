---
title: 【IC设计】Verilog线性序列机点灯案例(一)（小梅哥课程）
date: 2024-03-15 15:02:31
categories: 数字IC设计
tags: [Verilog]
layout: post
---
@[TOC]
> 案例和代码来自小梅哥课程，本人仅对知识点做做笔记，如有学习需要请支持官方正版。
# 该系列目录：
[Verilog线性序列机点灯案例（一）](https://blog.csdn.net/qq_42622433/article/details/136727036)
[Verilog线性序列机点灯案例（二）](https://blog.csdn.net/qq_42622433/article/details/136742479)
[Verilog线性序列机点灯案例（三）](https://blog.csdn.net/qq_42622433/article/details/136766843)
[Verilog线性序列机点灯案例（四）](https://blog.csdn.net/qq_42622433/article/details/136796718)
# 设计目标
让主频50MHz的FPGA每0.25s亮，0.75s灭，如图所示：
可以看到其中1s对应50,000,000个周期，即50MHz，每个周期20ns
50MHz时钟下度过的周期和时间对应关系如下：
|周期数量|对应时间  |
|--|--|
| 12,500,000 | 0.25秒 |
|50,000,000|1秒|
|37,500,000|0.75秒|

![在这里插入图片描述](3912b4c80db37e27cf07af358bc447f9.png)
# 思路
由于需要计数到50,000,000-1，那么我们计数器的位宽可以设置为26位，2^26=67,108,864，足够计数到50,000,000-1。
```verilog
reg [25:0] count;
```
我们的核心目标其实是让led亮12,500,000个周期，然后灭37,500,000个周期，如此反复。
想象下现实中的秒表，从0开始计时，到59，再变为0，刚好是60秒，同理，我们的计数器也是从0开始计数，当上升沿检测到50,000,000-1时，说明已经经历了1秒，所以复位为0

Led灯按照0.5秒闪烁的代码如下，我们在这个基础上改一改
![在这里插入图片描述](065eb3b24d9f51fae10f4c97f6b6f3e0.png)

```rust
module led_ctrl0(
    clk,
    rst_n,
    led_out
);
    input clk;
    input rst_n;
    output reg led_out;
    reg [25:0] counter;
    
    //第一个always负责counter计数器
    always@(posedge clk or negedge rst_n) begin
          if(!rst_n) begin
             counter <= 0;
          end else if(counter == 50_000_000-1) begin
             counter <= 0 ;
          end else begin
             counter <= counter + 1'd1;
          end
    end
    
    //第二个always负责led_out亮灭
    always@(posedge clk or negedge rst_n) begin
          if(!rst_n) begin
             led_out <= 1'b0;
          end else if(counter == 0 ) begin
             led_out <= 1'd1;
          end else if(counter == 1250_0000) begin
             led_out <= 1'd0;
          end
    end
endmodule
```

```rust
`timescale 1ns / 1ps

module led_ctrl_tb();
    reg clk;
    reg rst_n;
    wire led;
    
    led_ctrl0 led_ctrl0_inst0(
        .clk(clk),
        .rst_n(rst_n),
        .led_out(led)
    );
    initial clk = 1;
    always #10 clk = ~clk;
    initial begin
        rst_n = 0;
        #201
        rst_n = 1;
        #2000000000;
        $stop;
    end
    
endmodule

```

# 仿真结果
我们把变量转换的几个时间点看一遍，请注意我截图中黄色的marker：
## 时间点一：201ns
![在这里插入图片描述](7751bf37a3a1269a2752b4ba0cf690d6.png)
201ns时rst_n低电平复位信号由0变成1，即在此之后复位信号就无效了。

## 时间点二：220ns
![在这里插入图片描述](308c7965be477c663c61bf3f4c925bb4.png)
在220ns，
第一个always负责counter计数器，检测到counter为0，自增为1
第二个always负责led_out亮灭，检测到counter为0，令led为1
后面每次上升沿时检测到的counter的值就是led亮了多久

## 时间点三：250,000,220ns
![在这里插入图片描述](5591f556b281a47dd0cf19ec721122a6.png)在250,000,220ns
第一个always负责counter计数器，检测到counter为12,500,000，还没到1秒对应的50,000,000-1，所以继续自增。
第二个always负责led_out亮灭，检测到counter为12,500,000，说明已经亮了0.25秒，所以直接灭掉。

## 时间点四：1,000,000,200ns
![在这里插入图片描述](d586c21ecbc20d2611553baa1960bcc0.png)
第一个always负责counter计数器，检测到counter到了50,000,000-1，所以counter归零。

第二个always负责led_out亮灭，counter为49999999，不是0，所以继续灭。

## 时间点五：1,000,000,220ns
![在这里插入图片描述](f9983b7004d02c95e3c83e3e4dcd2412.png)
第一个always负责counter计数器,检测到counter为0，自增为1
第二个always负责led_out亮灭，counter为0，所以点亮led

# 总结：
从时间点五这个图中可以看出counter计数器当检测到49999999时，实际上已经计数完1秒了，原因是上升沿检测的时候49999999已经持续了一个周期。
led从counter为0到counter为12,500,000刚好亮0.25秒，因为检测到0时实际上会立刻跳变为1，0时刻并不是一个周期，而12,500,000是完整地过了一个周期。然后从12,500,001到49999999，再加上0时刻刚好是0.75秒。所以功能是没问题的。



