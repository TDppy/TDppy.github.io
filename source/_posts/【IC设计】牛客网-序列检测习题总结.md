---
title: 【IC设计】牛客网-序列检测习题总结
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计]
layout: post
---
@[toc]
# 状态机基础知识
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/48c7de50cbf4e18d5b809dcfadcdc800.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/a6f14d648949f8feb8937672dc666214.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bf69660ba20f63ddabb9b32883b39832.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8385b621bd9124fb95a9b9bbf62df8b3.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/51e7c17e42e12325a1eefa38a47f9f01.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/76de4a48b28228c6225895a0ebbe1f16.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/5950f39d8cbc17c388519243fbf7c5b6.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/55b6a9a18e3ac2b438b49b15431cb267.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ad22ebcc44ddf0c0d5a5fdf33b67927f.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/67284cf714b68ce6402516a8760baa0f.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/1894ff140f2858d7321def3234c6364c.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/47bed8a4f46688b46e457504095d3323.png)


# VL25 输入序列连续的序列检测
```rust
`timescale 1ns/1ns
module sequence_detect(
	input clk,
	input rst_n,
	input a,
	output reg match
	);
     
    //这题就是普通的状态机，需要注意的是：
    //  @当输入不能跳转到下一个状态时，可以复用前面的序列
    //  @这题是的Moore状态机，输出只和当前状态有关
	//定义状态空间(状态参数、状态寄存器)
	parameter IDLE = 0 ;
    parameter S0   = 1 ;
	parameter S1   = 2 ;
	parameter S2   = 3 ;
	parameter S3   = 4 ;
	parameter S4   = 5 ; 
	parameter S5   = 6 ;
	parameter S6   = 7 ;
	parameter S7   = 8 ;
	reg [3:0] curr_state,next_state;

	// 1.打一拍更新现态
    always@(posedge clk or negedge rst_n) begin
		if(~rst_n) begin
			curr_state <= IDLE;
		end else begin
			curr_state <= next_state;
		end
	end

	// 2.组合逻辑根据现态和输入生成次态
	always@(*) begin
		case(curr_state)
			IDLE :  next_state = (a == 0) ? S0 : IDLE ;
			S0   :  next_state = (a == 1) ? S1 : S0   ;
			S1   :  next_state = (a == 1) ? S2 : S0   ;
			S2   :  next_state = (a == 1) ? S3 : S0   ;
			S3   :  next_state = (a == 0) ? S4 : S0   ;
			S4   :  next_state = (a == 0) ? S5 : S1   ;
			S5   :  next_state = (a == 0) ? S6 : S1   ;
			S6   :  next_state = (a == 1) ? S7 : S1   ;
			S7   :  next_state = (a == 0) ? IDLE:S2   ;
			default: next_state = IDLE;
		endcase
	end

	// 3.Moore型FSM，根据当前状态生成输出
    always@(posedge clk or negedge rst_n) begin
		if(~rst_n) begin
			match <= 0;
		end else if(curr_state == S7) begin
			match <= 1;
		end else begin
			match <= 0;
		end
	end
endmodule
```

# VL26 含有无关项的序列检测
两种方法：
法一、用寄存器维护一个存储序列的寄存器
法二、用状态机来做
这里我用寄存器来做。

```rust
`timescale 1ns/1ns
module sequence_detect(
	input clk,
	input rst_n,
	input a,
	output reg match
	);

	reg [8:0] curr_seq;

	// 1.维护存储序列的寄存器
	always@(posedge clk or negedge rst_n) begin
		if(~rst_n) begin
			curr_seq <= 9'bxxx_xxx_xxx;
		end else begin
			curr_seq <= {curr_seq[7:0],a};
		end
	end
  
	// 2.判断序列是否模式匹配
	always@(posedge clk or negedge rst_n) begin
		if(~rst_n) begin
			match <= 0;
		end else if(curr_seq[2:0] == 3'b110 && curr_seq[8:6] == 3'b011) begin
			match <= 1;
		end else begin
			match <= 0;
		end
	end
endmodule
```

# VL27 不重叠序列检测
通过计数器进行分组序列检测，每组判断一次
**注意点：**
 - 计数器计算到6时才进行判断
 - 在分组中一旦错误，直接FAIL
 - 注意需要处理FAIL的状态跳转
 - 注意寄存器的初始值,要计数6个就1~6,初值为0

```rust
module sequence_detect(
	input clk,
	input rst_n,
	input data,
	output reg match,
	output reg not_match
);
	//分组序列检测
	//注意点：
	//@计数器计算到6时才进行判断
	//@在分组中一旦错误，直接FAIL
	//@注意需要处理FAIL的状态跳转
	//@注意寄存器的初始值,要计数6个就1~6,初值为0

	// 定义状态空间和状态寄存器
	parameter IDLE = 0 ,
	          S1   = 1 ,
			  S2   = 2 ,
			  S3   = 3 ,
			  S4   = 4 ,
			  S5   = 5 ,
			  S6   = 6 ,
			  FAIL = 7 ;
	reg [2:0] curr_state,next_state;

	reg [2:0] cnt;

	// 利用计数器进行分组
	always@(posedge clk or negedge rst_n ) begin
		if(~rst_n) begin
			cnt <= 'b0;
		end else begin
			if(cnt == 3'd6) cnt <= 'b1;
			else cnt <= cnt + 1;
		end
	end
	
	// 1.次态更新现态
	always@(posedge clk or negedge rst_n) begin
		if(~rst_n) begin
			curr_state = IDLE;
		end else begin
			curr_state = next_state;
		end
	end

	// 2.组合逻辑生成次态
	always@(*) begin
		case(curr_state)
			IDLE : next_state = (data==0) ? S1 : FAIL ;
			S1   : next_state = (data==1) ? S2 : FAIL ;
			S2   : next_state = (data==1) ? S3 : FAIL ;
			S3   : next_state = (data==1) ? S4 : FAIL ;
			S4   : next_state = (data==0) ? S5 : FAIL ;
			S5   : next_state = (data==0) ? S6 : FAIL ;
			S6   : next_state = (data==0) ? S1 : FAIL ;
			FAIL : next_state = (cnt == 6 && data ==0) ? S1 : FAIL;
			default : next_state = IDLE ; 
		endcase
	end 

	// 3.根据现态生成输出，波形match没有打拍直接组合逻辑输出
	always@(*) begin
		if(~rst_n) begin
			match <= 0;
			not_match <= 0;
		end 
		else if(cnt == 6 ) begin
			if(curr_state == S6) begin
				match <= 1;
				not_match <= 0;
			end else begin
				match <= 0;
				not_match <= 1;
			end
		end
		else begin
			match     <= 0;
			not_match <= 0;
		end
	end
endmodule
```


# VL28 输入序列不连续的序列检测

```rust
`timescale 1ns/1ns
module sequence_detect(
	input clk,
	input rst_n,
	input data,
	input data_valid,
	output reg match
);
	//输入数据不连续的序列检测，在状态跳转时需要考虑data_valid
	parameter IDLE = 5'b00001;
	parameter S1   = 5'b00010;
	parameter S2   = 5'b00100;
	parameter S3   = 5'b01000;
	parameter S4   = 5'b10000;
	parameter STATE_WIDTH = 5;
	reg [STATE_WIDTH - 1 : 0] cs;
	reg [STATE_WIDTH - 1 : 0] ns;

	always@(posedge clk or negedge rst_n) begin
		if(!rst_n) begin
			cs <= IDLE;
		end
		else begin
			cs <= ns;
		end
	end

	always@(*) begin
		case(cs)
			IDLE : begin
				if( data_valid ) begin
					ns = data == 0 ? S1 : IDLE ; 
				end 
				else begin
					ns = cs;
				end
			end
			S1   : begin
				if( data_valid ) begin
					ns = data == 1 ? S2 : S1;
				end 
				else begin
					ns = cs;
				end
			end
			S2   : begin
				if( data_valid ) begin
					ns = data == 1 ? S3 : S1;
				end 
				else begin
					ns = cs;
				end
			end
			S3   : begin
				if( data_valid ) begin
					ns = IDLE;
				end 
				else begin
					ns = cs;
				end
			end
		endcase
	end
  
	always@(posedge clk or negedge rst_n) begin
		if(!rst_n) begin
			match <= 0;
		end
		else begin
			if(cs == S3 && data == 0 && data_valid == 1) begin
				match <= 1;
			end
			else begin
				match <= 0;
			end
		end
	end
endmodule
```

# 参考资料
1. [正点原子领航者配套PPT](http://yuanzige.com)
2. [牛客网Verilog刷题](https://www.nowcoder.com/exam/oj?page=1&tab=Verilog%E7%AF%87&topicId=302)
