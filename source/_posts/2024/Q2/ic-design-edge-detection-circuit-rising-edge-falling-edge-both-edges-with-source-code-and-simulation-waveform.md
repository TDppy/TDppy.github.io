---
title: 【IC设计】边沿检测电路（上升沿、下降沿、双沿，附带源代码和仿真波形）
date: 2024-04-25 13:42:04
categories: 数字IC设计
tags: [Verilog]
layout: post
---

# 边沿检测电路的概念
边沿检测指的是检测一个信号的上升沿或者下降沿，如果发现了信号的上升沿或下降沿，则给出一个信号指示出来。
边沿检测电路根据检测边沿的类型一般分为**上升沿检测电路**、**下降沿检测电路**和**双沿检测电路**。

# 上升沿检测电路
![在这里插入图片描述](c4b28a94cd06290e29e8e2521d0d6609.png)

如图所示，我们的目标是当检测到a从0变成1时，令a_posedge为高电平，其余情况a_posedge均为低电平。
要检测a从0变成1，也就是说a的上升沿前是低电平，上升沿后是高电平，那么只需要令边沿前取反，再和边沿后相与，如果结果为1，说明必然是边沿前为0，边沿后为1，确认是上升沿。
实际操作中是让a打一拍并取反，再和a相与，得到a_posedge。

# 下降沿检测电路
![在这里插入图片描述](92e12e6ae84c01eed2b707d675ff6886.png)
下降沿同理，边沿后取反再和边沿前相与，得到1，说明是下降沿。  边沿前电平可以通过a打一拍得到。

# 双边沿检测电路
![在这里插入图片描述](087d2189066e58bebcc374c1ea147776.png)
1. 方法一：
前面会了上升沿和下降沿检测，双边沿检测也就是上升沿和下降沿都拉高，只需要将前面两者的结果进行或运算即可。
2. 方法二：
更为简便的办法是，上升沿和下降沿都是0和1之间的跳变，使用异或运算符，可以直接得到结果。

# 代码和仿真
## RTL代码

```rust
`timescale 1ns / 1ps

module edge_detection
(
    clk,
    rst_n,
    a,
    pos_y,
    neg_y,
    dual_y
);
    input clk;
    input rst_n;
    input a;            //需要检测边沿的信号a
    output pos_y;       //上升沿检测
    output neg_y;       //下降沿检测
    output dual_y;      //双边沿检测
    reg a_delay1;
    
    //将信号a打一拍得到a_delay1
    always@(posedge clk or negedge rst_n) begin
        if( ~rst_n ) begin
            a_delay1 <= 0;       
        end
        else begin
            a_delay1 <= a;
        end
    end
    
    // ~优先级高于&
    assign pos_y = a  & ~a_delay1;
    assign neg_y = ~a & a_delay1;
    assign dual_y = a ^ a_delay1;
endmodule

```
## Testbench代码

```rust
`timescale 1ns / 1ps

//tb的基本思路无非就是：制造时钟、复位、例化、构造数据
module tb_edge_detection();
    reg clk,rst_n,a;
    wire pos_y,neg_y,dual_y;
    initial begin
        a   = 0;
        clk = 0;
        rst_n = 0;
        #50
        rst_n = 1;
        a = 1;
        #30;
        a = 0;
        #40;
        a = 1;
        #50;
        a = 0;
        #40;
        $stop;
    end
    
    edge_detection edge_detection_u0
    (
        .clk(clk),
        .rst_n(rst_n),
        .a(a),
        .pos_y(pos_y),
        .neg_y(neg_y),
        .dual_y(dual_y)
    );
    
    always #5 clk = ~clk;

endmodule

```

## 仿真波形
![在这里插入图片描述](a9464ac8d78457f6198c0a96a317a611.png)

# 参考资料
1. [正点原子逻辑设计教程](http://yuanzige.com)
