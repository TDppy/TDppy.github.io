---
title: 【IC设计】奇数分频与偶数分频 电路设计（含讲解、RTL代码、Testbench代码）
date: 2024-04-24 18:19:14
categories: 数字IC设计
tags: [分频器, Verilog]
layout: post
---
@[TOC]
# 原理分析
分频电路是将给定clk时钟信号频率降低为div_clk的电路，假设原时钟的频率为M Hz，分频后的时钟为N Hz，那么就称该分频电路为M/N分频。

如果M/N是奇数，实现该功能的电路就是奇数分频电路；
如果M/N是偶数，实现该功能的电路就是偶数分频电路。

**频率和周期的对应关系：**
由于频率f=1/T，因此二分频电路即M/N=（1/T1）/(1/T2) = T2/T1 = 2 ，即一个二分频后的时钟周期是原时钟周期的两倍。
同理，一个N分频后的时钟周期是原时钟的M/N倍。

**偶数分频举例：**
以两分频电路为例，由于周期为原先的两倍，那么只需要在clk每个上升沿到来时，div_clk翻转，就可以了。
以四分频电路为例，由于周期为原先的四倍，那么需要在**clk每两个周期div_clk翻转一次**。需要使用计数器来数clk过了几个周期。
同理，一个K分频电路，K为偶数，那么由于周期为原先的K倍，那么需要在**clk每K/2个周期div_clk翻转一次**。

**奇数分频举例：**
以三分频电路为例，周期为原先的三倍。
**如果对占空比（高电平占整个周期的比例）没有要求**，我们可以令out_clk在clk的一个周期为高，两个周期为低，如此反复。

**如果占空比为一半**，那么就是每1.5个周期翻转一次，无法通过检测上升和下降沿来翻转，那么应该怎么做？
如图所示，我们的目标是每1.5个周期翻转一次，那么可以这样做，得到一个占空比为50%的奇数分频。

 1. 构造out_clk1和out_clk2信号，高电平都是1个周期，低电平都是2个周期，两个信号的区别是相差半个周期的相位。
 2. assign out_clk = out_clk1 | out_clk2
 3. out_clk就是分频的结果
![在这里插入图片描述](/images/2935ac82c26f9263734cbd3938195458.png)
同理，任意奇数分频都可以用类似的思路实现。因为3 5 7 9 11...总是可以分解成3=1+2，5=2+3，7=3+4，9=4+5...


# 实现和仿真
## 偶数分频的电路RTL代码

```rust
`timescale 1ns / 1ps

module divide_even
(
    rst_n,
    clk,
    div_clk,
);
    input rst_n;
    input clk;
    output reg div_clk;
    
    //位宽一般用系统函数来确定
    reg [5:0] cnt;
    
    parameter DIVIDE_NUM = 4;
    always@(posedge clk or negedge rst_n) begin
        if( ~rst_n ) begin
            cnt <= 0;
            div_clk <= 0;
        end else if( cnt == DIVIDE_NUM / 2 - 1 ) begin
            div_clk <= ~div_clk;
            cnt <= 0;
        end else begin
            cnt <= cnt + 1;
        end
    end
endmodule

```
## 偶数分频的电路Testbench代码
```rust
`timescale 1ns / 1ps

module tb_divide_even();
    reg clk;
    reg rst_n;
    wire div_clk;
    initial begin
        clk = 0;
        rst_n = 0;
        #48;
        rst_n = 1;
        #203;        
        $stop;
    end    
    divide_even divide_even_u0
    (
        .clk(clk),
        .rst_n(rst_n),
        .div_clk(div_clk)    
    );
    always #5 clk = ~clk;
endmodule

```
## 偶数分频的电路仿真波形
![在这里插入图片描述](/images/a84545e0f89426f7a5c5102d246e58d9.png)


## 占空比为50%的三分频电路RTL代码
```rust
`timescale 1ns / 1ps

module divide_3(
    clk,
    rst_n,
    div_clk
);
    input clk;
    input rst_n;
    output div_clk;
    
    reg out_clk1;
    reg out_clk2;
    
    reg [1:0] cnt1;
    reg [1:0] cnt2;
    
    //第一个always负责out_clk1的值
    always@(posedge clk or negedge rst_n) begin
        if(~rst_n) begin
            cnt1     <= 2'b0;
            out_clk1 <= 0;
        end
        else if(out_clk1 == 1) begin             
            cnt1 <= 2'b0;
            out_clk1 <= ~out_clk1;      
        end else if(out_clk1 == 0) begin
            if(cnt1 == 1) begin
                cnt1 <= 2'b0;
                out_clk1 <= ~out_clk1;
            end else begin
                cnt1 <= cnt1 + 1;
            end
        end
    end
    
    //第二个always负责out_clk2的值
    always@(negedge clk or negedge rst_n) begin
        if(~rst_n) begin
            cnt2     <= 2'b0;
            out_clk2 <= 0;
        end
        else if(out_clk2 == 1) begin 
            cnt2 <= 2'b0;
            out_clk2 <= ~out_clk2;
        end else if(out_clk2 == 0) begin
            if(cnt2 == 1) begin
                cnt2 <= 2'b0;
                out_clk2 <= ~out_clk2;
            end else begin
                cnt2 <= cnt2 + 1;
            end
        end
    end
    
    assign div_clk = out_clk1 | out_clk2;

endmodule

```

## 占空比为50%的三分频电路Testbench代码
```rust
`timescale 1ns / 1ps

module tb_divide_3();
    reg clk,rst_n;
    wire div_clk;
    
    initial begin
        rst_n = 0;
        clk = 0;
        #48;
        rst_n = 1;
        #202;
        $stop;
    end
    
    divide_3 divide_3_u0
    (
        .clk(clk),
        .rst_n(rst_n),
        .div_clk(div_clk)
    );
    
    //10ns一个周期,100MHz
    always #5 clk = ~clk;
    
endmodule

```

## 占空比为50%的三分频电路仿真波形
![在这里插入图片描述](/images/6607ffa2c18e0df38d9e16279549341d.png)
# 参考资料
1. [正点原子逻辑设计指南](http://www.yuanzige.com)
2. [B站 FPGA探索者 牛客Verilog刷题 奇数分频](https://www.bilibili.com/video/BV1A34y1Y7UM/?spm_id_from=333.1007.top_right_bar_window_history.content.click)
