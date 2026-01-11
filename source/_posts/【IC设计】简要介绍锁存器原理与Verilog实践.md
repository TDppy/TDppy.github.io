---
title: 【IC设计】简要介绍锁存器原理与Verilog实践
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计]
layout: post
---
﻿@[TOC]
# 锁存器原理
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/b52f2ee3e5f1f2a7c9d2dd90dae8389e.png)

 - **当控制信号 C=0 时，Q维持不变**
   根据与非门的逻辑定律，无论 D 输入什么信号，RD 和 SD 信号同时为 1。根据由与非门组成的 RS 锁存器的逻辑定律，RD 和 SD 都同时 等于 1 的话，锁存器的输出端 Q 将维持原状态不变。
 - **当控制信号 C=1 时，Q由D来决定**
    1. 如果此时 D=0，SD 就等于1，RD 就等于 0，根据 RS 锁存器的逻辑规律，电路的结果就为 0 状态；
    2. 如果 D =1，那么 RD 就等于 1，SD 也就等于 0，锁存器的结果就为 1 状态。
也就是说，此时锁存器的状态是由激励输入端 D 来确定的，
并且 D 等于什么，锁存器的状态就是什么，这就是我们前面所说的，将单路数据 D 存入到锁存器之中。

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e0804bf899525b73c386982b57dda79d.png)
在绝大多数设计中我们要避免产生锁存器。它会让您设计的时序出问题，并且它的隐蔽性很强，新人很难查出问题。锁存器最大的危害在于不能过滤毛刺和影响工具进行时序分析。这对于下一级电路是极其危险的。所以，只要能用触发器的地方，就不用锁存器。
# if语句
## if语句不带else
```rust
`timescale 1ns / 1ps

module latch
(
    clk,
    a,
    b,
    y
);
    input clk;
    input a;
    input b;
    output reg y;
    always @(*) begin
        if( a == 1)
            y = b;
    end
endmodule
```

## if语句不带else 对应 RTL原理图
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fd27210307ed34ccae0714117bd9542f.png)
## if语句带else

```rust
`timescale 1ns / 1ps

module latch
(
    clk,
    a,
    b,
    y
);
    input clk;
    input a;
    input b;
    output reg y;
    always @(*) begin
        if( a == 1)
            y = b;
        else 
            y = 0;
    end
endmodule
```

## if语句带else 对应 RTL原理图
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dd72b12b751af61bcc270237966946aa.png)

## if语句带else 对应 RTL原理图

# Case语句
## Case语句不带feault
```rust
`timescale 1ns / 1ps

module latch
(
    clk,
    a,
    b,
    y
);
    input clk;
    input a;
    input b;
    output reg y;
    always @(*) begin
        // a为0时，y更新为b  
        // a为其他值时，y锁存
        case(a)
            0 : y = b;
        endcase
    end
endmodule
```
## Case语句不带feault 对应 RTL原理图
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/0095d752ff527fa4661143a47ecedf53.png)

## Case语句带default
```rust
`timescale 1ns / 1ps

module latch
(
    clk,
    a,
    b,
    y
);
    input clk;
    input a;
    input b;
    output reg y;
    always @(*) begin
        // a为0时，y更新为b  
        // a为其他值时，y锁存
        case(a)
            0 : y = b;
            default : y = 0;
        endcase
    end
endmodule

```

## Case语句不带feault 对应 RTL原理图
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/879fbd6cb572cac891ac051ec7d9c899.png)
# 参考资料
1. [正点原子逻辑设计](http://yuanzige.com)
2. [B站 花几分钟理解锁存器](https://www.bilibili.com/video/BV16w4m1d7Re/?spm_id_from=333.1007.top_right_bar_window_history.content.click)
3. [锁存器与触发器详解1 SR锁存器](https://www.bilibili.com/video/BV1oL411D77D/?spm_id_from=333.1007.top_right_bar_window_history.content.click)
