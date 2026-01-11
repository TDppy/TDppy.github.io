---
title: 【IC设计】Verilog线性序列机点灯案例(二)（小梅哥课程）
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计]
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
我们的FPGA的时钟频率为**50MHz**，即每个周期20ns。
因此，在该时钟下时间和周期数的对应关系为：
| 持续时间 | 对应周期数 |
|--|--|
| 0.25s | 12,500,000 cycles|
|0.5s|25,000,000 cycles|
|0.75s|37,500,000 cycles|
|1s|50,000,000 cycles|

我们的目标是让LED以**【亮0.25秒->灭0.5秒->亮0.75秒->灭1秒】**的规律，持续循环闪烁。
# 设计思路
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/723915cd89e06cb2022176c12d4274bc.png)
为了完成这样的规律性闪烁，需要一个计数器，计数满2.5秒归零，即：当上升沿采样到125,000,000-1时，计数器归零。
然后，led灯根据当前计数器的数值，设置led的亮灭，图中已经标注了led跳变时的counter数值。下面直接上代码

# RTL 及 Testbench
led_ctrl1.v 是RTL代码

```rust
module led_ctrl1(
    clk,
    rst_n,
    led_out
);
    input clk;
    input rst_n;
    output reg led_out;
    
    reg [26:0] counter;
    
    //第一个always负责counter计数器的逻辑
    always@(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            counter <= 0;
        end else if(counter == 125_000_000-1) begin
            counter <= 0;
        end else begin
            counter <= counter + 1;
        end
    end
    
    //第二个always负责led_out闪烁的逻辑
    //亮0.25s->灭0.5秒->亮0.75秒->灭1秒
    always@(posedge clk or negedge rst_n) begin
        if(!rst_n) begin
            led_out <= 0;
        end else if(counter == 0) begin
            led_out <= 1;
        end else if(counter == 12_500_000) begin
            led_out <= 0;
        end else if(counter == 37_500_000) begin
            led_out <= 1;
        end else if(counter == 75_000_000) begin
            led_out <= 0;
        end 
    end
    
endmodule
```

tb_led_ctrl1.v是testbench代码

```rust
`timescale 1ns / 1ns

module tb_led_ctrl1();
    reg clk;
    reg rst_n;
    wire led_out;
    initial clk = 1;
    always #10 clk = ~clk;
    
    led_ctrl1 led_ctrl1_inst0(
        .clk(clk),
        .rst_n(rst_n),
        .led_out(led_out)
    );
    
    initial begin
        rst_n = 0;
        #201;
        rst_n = 1;
        #250_000_000
        $stop;
    end
endmodule
```

# 仿真结果
从图中黄色marker标注下的时间间隔可以看出，仿真结果和预期目标一致。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/3c80ef1a22a6a1a114e18263bb8cc98b.png)

# 存在的问题？
如果到此就结束了，那么案例（二）和（一）并没有多大区别。
实际上，按照刚才的实现方式可以完成功能，但存在如下问题：
1. 仿真时间过长
为了在实际上板时观察到led闪烁的效果，我们的闪烁都是秒级的，vivado仿真一秒时间几乎需要十几秒才能完成，能否减少仿真时间，不影响功能？
2. 可读性较差
在我们的代码中0.25s,0.75s这些时间尺度都是用具体的计数器的周期数来表示的，数字太大，不好理解，如何解决？

针对以上问题，观察我们的需求是让LED以**【亮0.25秒->灭0.5秒->亮0.75秒->灭1秒】**循环，那么最基本的单位可以视为0.25秒，我们可以使用两个计数器，第一个计数器计数到0.25秒（12500_000 - 1个cycles）时第二个计数器加1。按照这个思路，我们在设置led时只需要关注好第二个计数器即可，1亮，2、3灭，4、5、6亮，7、8、9、10灭，显然可读性是比0亮，12_500_000灭好多了。
此外，针对仿真时间过长的问题，我们可以在RTL模块中定义一个parameter时间单元，而在testbench仿真中重新缩小该时间单元1000倍，实际上板时只会烧录RTL模块，这样既节省了仿真时间，又不影响功能。
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c849150d23ff4bdeddda33e085c38f11.png)
# 改善后的代码
## RTL代码
```rust
module led_ctrl1(
    clk,
    rst_n,
    led_out
);
    input clk;
    input rst_n;
    output reg led_out;
    
    parameter MCNT = 12500_000 - 1;
    reg [26:0] counter0;
    
    always@(posedge clk or negedge rst_n) begin
        if(!rst_n)
            counter0 <= 0 ;
        else if(counter0 == MCNT)
            counter0 <= 0;
        else
            counter0 <= counter0 + 1'd1;
    end
    
    reg [3:0] counter1;
    always@(posedge clk or negedge rst_n) begin
        if(!rst_n)
            counter1 <= 0 ;
        else if(counter0 == MCNT) begin
           if(counter1 == 9)
              counter1 <= 0;
           else
              counter1 <= counter1 + 1'd1;
        end
        else
            counter1 <= counter1;
    end
    
    always@(posedge clk or negedge rst_n)
    if(!rst_n)
        led_out <= 0;
    else begin
        case(counter1)
            0:led_out <= 1'd1;
            1:led_out <= 1'd0;
            2:led_out <= 1'd0;
            3:led_out <= 1'd1;
            4:led_out <= 1'd1;
            5:led_out <= 1'd1;
            6:led_out <= 1'd0;
            7:led_out <= 1'd0;
            8:led_out <= 1'd0;
            9:led_out <= 1'd0;
            default:led_out <= led_out;
        endcase
    end
    
endmodule
```

## testbench代码

```rust
`timescale 1ns / 1ns

module tb_led_ctrl1();
    reg clk;
    reg rst_n;
    wire led_out;
    initial clk = 1;
    always #10 clk = ~clk;
    
    led_ctrl1 led_ctrl1_inst0(
        .clk(clk),
        .rst_n(rst_n),
        .led_out(led_out)
    );
    defparam led_ctrl1.MCNT = 12500 - 1; 
    
    initial begin
        rst_n = 0;
        #201;
        rst_n = 1;
        #20_000_000;
        $stop;
    end
endmodule

```
# 仿真结果
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/4211f239f6efe0b282d5a3d52a1732f2.png)

