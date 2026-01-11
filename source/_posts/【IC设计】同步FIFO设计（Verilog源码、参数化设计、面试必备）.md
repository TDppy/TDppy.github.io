---
title: 【IC设计】同步FIFO设计（Verilog源码、参数化设计、面试必备）
date: 2026-01-11 15:30:00
categories: 数字IC设计
tags: [Verilog]
layout: post
---
@[TOC]
# 设计思想
FIFO也就是先进先出的队列，是一种特殊的RAM，特殊在读写地址默认是自增1，所以FIFO内部管理读写地址，不需要暴露读写地址端口。
同步FIFO指读写使用同一个时钟，异步FIFO则读写使用不同的时钟，同步FIFO相对简单一些，异步FIFO还涉及到亚稳态、格雷码和二进制的转化等问题。

**FIFO的难点**在于空满的判断，这里同步FIFO的空满判断有两种方式，一是使用计数器，这个很简单，fifo_cnt等于0就为空，等于深度就满，二是使用读写指针进行判断，这里我使用第一种方式。

下面给出了经典同步fifo设计的源码，用来面试手撕，采用了参数化、$clog2函数，代码很规范也很好记。
总结一下博客，重点强调下记忆的方法，方便面试手撕代码，如有错误的地方恳请指正！
## 端口
分三方面记忆，时钟复位+读+写。注意读写不光有数据，还有使能和空满信号。
## 代码块
一共可以分为六个代码块：
 - 读数据部分有读指针always块、读操作always块；
 - 写数据部分有写指针always块、写操作always块；
 - 空满判断部分有fifo元素数量always块、空满判断assign块；

## 寄存器
包括：
 - fifo_buffer存储数据
 - fifo_cnt记录当前fifo元素数量
 - rd_pointer和wr_pointer指针
# 同步FIFO代码

```rust
module syn_fifo
#
(
	parameter DATA_WIDTH = 8,
	parameter DATA_DEPTH = 8,
)
(
	input clk				,
	input rst_n				,
	
	// read
	output [DATA_WIDTH - 1 ：0] read_data		,
	input  rd_en								,
	output rd_empty								,
	
	// write
	input [DATA_WIDTH - 1 ：0] write_data		,
	input  wr_en								,
	output wr_full								,
);
	
	// Parameters
	parameter DEPTH_WIDTH = $clog2(DATA_DEPTH)  ;

	// Regs
	reg [DATA_WIDTH - 1 ：0] fifo_buffer [0 : DATA_DEPTH - 1]  ;
	reg [DATA_DEPTH     : 0] fifo_cnt						   ;
	reg [DATA_DEPTH - 1 : 0] wr_pointer,rd_pointer			   ;

	// read pointer
	always@(posedge clk or negedge rst_n) begin
		if(~rst_n) begin
			read_pointer <= 'b0;
		end
		else begin
			if( rd_en && !rd_empty) begin
				if( rd_pointer == DATA_DEPTH - 1) begin
					rd_pointer <= 'b0;
				end else begin
					rd_pointer <= rd_pointer + 1'b1;
				end
			end
		
		end
	end
	
	// read operation
	always@(posedge clk or negedge rst_n) begin
		if(~rst_n) begin
			read_data <= 'b0;
		end
		else begin
			read_data <= fifo_buffer[rd_pointer];
		end
	end
	
	// write pointer
	always@(posedge clk or negedge rst_n) begin
		if(~rst_n) begin
			wr_pointer <= 'b0;
		end
		else begin
			if( wr_en && !wr_full) begin
				if( wr_pointer == DATA_DEPTH - 1) begin
					wr_pointer <= 'b0;
				end else begin
					wr_pointer <= wr_pointer + 1'b1;
				end
			end
		
		end
	end
	
	// write operation
	always@(posedge clk or negedge rst_n) begin
		if(~rst_n) begin
			fifo_buffer[wr_pointer] <= 'b0;
		end
		else begin
			fifo_buffer[wr_pointer]  <= read_data;
		end
	end
	
	// current fifo_cnt in fifo_buffer
	always@(posedge clk or negedge rst_n) begin
		if(~rst_n) begin
			fifo_cnt <= 'b0;
		end
		else begin
			fifo_cnt <= fifo_cnt + 1'b1;
		end
	end
	
	
	// empty and full
	assign full   = (fifo_cnt == DATA_DEPTH);
	assign empty  = (fifo_cnt == 0	       );


endmodule
```

