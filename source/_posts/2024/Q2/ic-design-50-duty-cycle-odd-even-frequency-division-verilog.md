---
title: 【IC设计】任意倍数占空比为50%的奇数分频和偶数分频（Verilog源码、仿真波形、讲解）
date: 2024-05-19 12:13:31
categories: 数字IC设计
tags: [分频器, Verilog]
layout: post
---
# 任意倍数占空比为50%的偶数分频
以四分频为例，分频后的一个周期是分频前的四个周期，并且分频后的一个周期中，一半是高电平，一半是低电平，这就是占空比为50%的四分频。
要实现该功能，使用一个计数器在0~3之间计数，clk_out在0和2时翻转即可。
```rust
module even_divider
#( parameter DIVIDE_FACTOR = 4 )
(
    input clk_in   ,
    input rst_n    ,
    output reg clk_out
);
    parameter CNT_WIDTH = $clog2(DIVIDE_FACTOR) ;
    reg [CNT_WIDTH : 0] cnt                     ;
    
    // 1.计数器
    always@(posedge clk_in or negedge rst_n) begin
        if( ~rst_n ) begin
            cnt <= 'b0;
        end
        else if( cnt == DIVIDE_FACTOR - 1 ) begin
            cnt <= 'b0;
        end 
        else begin
            cnt <= cnt + 1'b1;        
        end
    end
    
    // 2.输出clk_out  cnt为0和DIVIDE/2时跳变
    always@(posedge clk_in or negedge rst_n) begin
        if(~rst_n) begin
            clk_out <= 1'b0;
        end
        else if( cnt == 0 ) begin
            clk_out <= 1'b1;
        end
        else if( cnt == DIVIDE_FACTOR >> 1 ) begin
            clk_out <= 1'b0;
        end
        else begin
            clk_out <= clk_out;
        end
    end
    
endmodule
```

# 任意倍数占空比为50%的奇数分频
以5分频为例，分频后的一个周期是分频前的五个周期，并且分频后的一个周期中，一半是高电平，一半是低电平，这就是占空比为50%的五分频。
我们先不考虑占空比，那么可以让2个周期为高，3个周期为低，或者1个周期为高，4个周期为低，这样来实现5分频。
如果占空比要求为50%，那么就必须2.5个周期为高，2.5个周期为低，该怎么办？
可以令clk1和clk2都是先2个周期为高，再3个周期为低，然后让他们的相位相差半个周期，然后令clk1和clk2进行或运算，得到最终生成的clk_out。
```rust
/*
*  功能：dividor奇数分频
*  实现：三段论：
*  1.定义计数器从0~dividor - 1之间翻转
*  2.flag_1在上升沿检测cnt==0时为1，cnt==dividor/2时为0
*  3.flag_2在下降沿检测cnt==0时为1，cnt==dividor/2时为0
*  4.令clk_out = flag_1 | flag_2
*/
module odd_divider 
#(    parameter dividor = 3  )
(  
    input clk_in,
    input rst_n,
    output clk_out
);
//定义计数器的位宽,$clog2()为取对数操作，在编译过程中执行完成。因此在模块运行过程中CNT_WIDTH是一个确定的数值。
parameter CNT_WIDTH = $clog2(dividor-1);	

reg flag_1;
reg flag_2;
reg [CNT_WIDTH :0] cnt;

always @(posedge clk_in or negedge rst_n) begin
	if (!rst_n)
		cnt <= 0;
	else if(cnt == dividor - 1)
		cnt <= 0;
	else cnt <= cnt + 1'd1;
end
	
always @(posedge clk_in or negedge rst_n)  begin
	if (!rst_n)
		flag_1 <= 0;
	else if( cnt == 0 )  // cnt == 2
		flag_1 <= ~flag_1;
	else if( cnt == dividor >> 1   )         // cnt == 4
		flag_1 <= ~flag_1;		
	else flag_1 <= flag_1;
end

always @(negedge clk_in or negedge rst_n)  begin
	if (!rst_n)
		flag_2 <= 0;
	else if(cnt == 0 )
		flag_2 <= ~flag_2;
	else if(cnt == dividor >> 1)
		flag_2 <= ~flag_2;
	else flag_2 <= flag_2;	
end

	assign clk_out = flag_1 || flag_2;
endmodule
```

# Testbench
![在这里插入图片描述](./1.png)
```rust
`timescale 1ns / 1ps

module tb_divider();
    reg clk_in,rst_n;
    wire odd_clk_out;
    wire even_clk_out;
    
    initial begin
        clk_in = 1;
        rst_n  = 0;
        #25
        rst_n  = 1;
        #305;
        $finish;
    end
    
    always #10 clk_in = ~ clk_in;
   
    odd_divider odd_divider_u0
    (
        .clk_in  ( clk_in  )          ,
        .rst_n   ( rst_n   )          ,
        .clk_out ( odd_clk_out )              
    );
    
    defparam odd_divider_u0.dividor = 5;
    
       
    even_divider even_divider_u0
    (
        .clk_in  ( clk_in  )          ,
        .rst_n   ( rst_n   )          ,
        .clk_out ( even_clk_out )              
    );
    defparam even_divider_u0.DIVIDE_FACTOR = 4;
endmodule

```


