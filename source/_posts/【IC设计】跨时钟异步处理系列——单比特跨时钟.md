---
title: 【IC设计】跨时钟异步处理系列——单比特跨时钟
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计]
layout: post
---
@[TOC]
# 建立时间和保持时间
1. 所谓的建立时间或者保持时间都是在描述一种时钟变化的边沿上的数据状态。
2. 建立时间：在时钟的有效沿（以上升沿为例）到来之前，数据的输入端信号必须保持稳定的最短时间
3. 保持时间：在时钟的有效沿（以上升沿为例）到来之后，数据的输入端信号必须保持稳定的最短时间
# 单比特信号的跨时钟处理
## 慢时钟域的信号传输到快时钟域
### 打两拍
## 快时钟域的信号传输到慢时钟域
![在这里插入图片描述](./images/1469bf8aac834bbcbd234c0b6c9c770e.png)
如图所示，第一行是脉冲信号，第二行是慢时钟域的时钟。如果从快时钟域要同步一个脉冲信号到慢时钟域，容易出现上升沿没有采样到脉冲信号的情况。
### 方案一  脉冲展宽+同步   (打拍打拍，进行或)
![在这里插入图片描述](./images/6d3e233447d74efe9c9d7e12d5498abe.png)
#### 代码
```rust
module fast2slow_cdc 
(
    input   i_clk_f     ,
    input   i_pluse_f   ,
    input   i_rst_n     ,
    input   i_clk_s     ,
    output  o_pluse_s  
);
/*
always @(posedge i_clk_f) begin
    r_pluse[0] <= i_pluse_f  ;
    r_pluse[1] <= r_pluse[0] ;
    r_pluse[2] <= r_pluse[1] ;
    r_pluse[3] <= r_pluse[2] ;
    r_pluse[4] <= r_pluse[3] ;
end
*/

reg [2:0]    r_pluse    ;
always @(posedge i_clk_f or negedge i_rst_n) begin
    if(~i_rst_n)    begin
        r_pluse <=  'b0;
    end
    else begin
        r_pluse <= {r_pluse[1:0],i_pluse_f};
    end
end

wire   w_pluse ;
assign  w_pluse = |r_pluse ;


reg   r_pluse_d0  ;
reg   r_pluse_d1  ;
always @(posedge i_clk_s) begin
    r_pluse_d0 <= w_pluse    ;
    r_pluse_d1 <= r_pluse_d0 ;
end

assign  o_pluse_s = r_pluse_d1 ;

endmodule
```
存在的问题：采用脉冲展宽+同步，在或时可能产生毛刺 

#### 原理图
![在这里插入图片描述](./images/08eb5c77ca414820af4e3f91877b83b2.png)
### 方案二  脉冲电平检测+双触发器同步+边沿检测
**优点：** 对时序比较友好
**缺点：** 相邻的脉冲太近时，会检测不到
![在这里插入图片描述](./images/38c276442cb1471cb2e99abc87c6f097.png)
#### 代码
```rust
module fast2slow_cdc2(
	input	i_clk_f			,
	input	i_pluse_f		,
	input	i_clk_s			,
	output	o_pluse_s
);
	reg	r_temp	=	0	;
	always@(posedge i_clk_f)	begin
		if(i_pluse_f)
			r_temp	    <=	~r_temp;
		else
			 r_temp	<=	r_temp;
	end
	reg	r_temp_d0;
	reg	r_temp_d1;
	reg	r_temp_d2;
	always@(posedge i_clk_s)	begin
		r_temp_d0	<=	r_temp		;
		r_temp_d1	<=	r_temp_d0	;
		r_temp_d2	<=	r_temp_d1	;
	end
	assign o_pluse_s	=	r_temp_d2	^	r_temp_d1	;
endmodule
```
#### 原理图
![在这里插入图片描述](./images/c3ffb86d231b4697a68d0b8cca44875e.png)

