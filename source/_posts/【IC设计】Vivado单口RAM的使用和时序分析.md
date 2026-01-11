---
title: 【IC设计】Vivado单口RAM的使用和时序分析
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计]
layout: post
---
﻿@[TOC]
# 创建单口RAM IP
## IP Catalog中选择单口RAM IP
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/baa45c9a16cb7a55c93fd423265843aa.png)

## Basic
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bcf9e49e84ca339e7e87b885212cc2c4.png)
## Port A Options
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/487b3e7d0ddd87aa4b2af37bd35d19a3.png)
## Other Options
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7b551b4afd2ba2e358716f56718ae142.png)

# 仿真
## 找到IP例化原语
IP Sources-Instantiation Template-veo文件中找到IP例化原语
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/52c0f950e509a80f644da3c7612f8859.png)
## 编写Testbench
创建single_port_ram_test.v，代码如下：

```c
`timescale 1ns / 1ps

//功能：测试单口ram
//ena means port a clock enable:
//enables read,write and reset operations through port A.Optional in all configurations.
//wea means port a write enbale:
//enables write operations through port a available in all ram configurations.
module single_port_ram_test();
    reg clk;

    //ena使能
    reg ena;
    
    //write enable a port
    //wea为0时处于读取状态，读取有1个周期的时延，wea为1时处于写入状态
    reg wea;
    
    //地址宽度为10，ram中最多存1024个数据
    reg [9:0] addra;

    //输入数据宽度为32，即4个16进制数据
    reg [31:0] dina;

    //输出数据douta
    wire [31:0] douta;

    reg [3:0] count;
    
    reg rst ;
    
    initial begin
        clk=1;
        rst = 0 ;
        count=4'b0;
        wea=0;
        ena=0;
        @ (negedge clk) ena = 1 ;
        #90;
        dina=32'habcd;
        #20;
        dina=32'h000a;
        #20;
        dina=32'h00ba;
        #20;
        dina=32'h0bcd;
        #20;
        dina=32'hxxxx;
        #120;
        $finish;
    end
    always begin
        #10;
        clk=~clk;
    end

    always @ ( posedge clk , posedge rst ) begin
        if (rst)
            count  <= 'b0 ;
        else if ( count < 'd3  && ena )
            count <= count + 'b1 ;
        else
            count <= 0 ;
    end
    
    //初始状态rst=0,所以将addra置为0
    always @ ( posedge clk , posedge rst ) begin
        if ( rst )
            addra <= 'b0 ;
        //每个上升沿addra+1
        else if ( addra < 3  && ena)
            addra <= addra + 1 ;
        else
            addra <= 'b0 ;
    end
    
    always @ ( posedge clk , posedge rst ) begin
        if (rst)
            wea <= 'b0 ; 
        else if (count == 'd3) 
            wea <= ~ wea ; 
        else
            wea <= wea ;
    end
    
    

    //单口ram实例
    blk_mem_gen_1 single_port_ram_inst (
        .clka(clk),    // input wire clka
        .ena(ena),      // input wire ena
        .wea(wea),      // input wire [0 : 0] wea
        .addra(addra),  // input wire [9 : 0] addra
        .dina(dina),    // input wire [31 : 0] dina
        .douta(douta)  // output wire [31 : 0] douta
    );
endmodule

```

# 波形分析

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e1d824b5d3efd57d450636859ec4272f.png)

