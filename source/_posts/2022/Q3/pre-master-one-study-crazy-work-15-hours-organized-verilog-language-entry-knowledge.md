---
title: 【准研一学习】狂肝15小时整理的Verilog语言入门知识
date: 2022-08-19 05:46:24
categories: 编程与算法
tags: [FPGA, Verilog]
layout: post
---

@[TOC]
## 闲言稍叙
Verilog和VHDL就是目前使用最多的两个硬件描述语言(HDL)，如果阅读本文的你也是Verilog新手，这部分闲言或许对你有所启发。

作者本科是计算机科学与技术专业，现在是准研一，方向和硬件相关。
由于学艺不精，只会点C、Java，电路、信号、单片机等硬件课程都只懂皮毛。由于课题组研究需要，学习了Verilog语言并总结为本文。

C语言是软件描述语言，编码的核心目的在于经过**编译、链接**后能够产生机器能够识别的指令序列，进而完成代码功能。而Verilog是硬件描述语言，编码的核心目的在于描述门与门之间的连接，通过**综合、实现**所写的代码，产生可以转化为芯片的图纸，交由厂商通过光刻来生产所设计的电路，最终经过**封装、测试**，即通常所称的芯片。

要学习Verilog首先需要一个**编程平台**，有Vivado、Modelsim等，其中Vivado是用的最多的，但是运行比较慢，Modelsim运行的快，但是界面丑，这个看个人喜好安装就好。

有编程平台后，通过在网站上刷题和看书，逐渐就可以上手了。那么下面列举出我学习Verilog所使用过的网站、书籍：

**网站**：
1.HDLBits
[网站地址](https://hdlbits.01xz.net/wiki/Main_Page)
该网站是全英文的，里面有100多道练习题，题解可以在Github上找到。

2.VLab Verilog OJ
[网站地址](https://verilogoj.ustc.edu.cn/oj/problempage/1)
这是由中科大团队开发的Verilog在线评测系统，类似于软件编程的洛谷等网站。
其中每个题都会给出比较充分的知识点叙述，然后再让你动手编码，目的在于帮助大家学习Verilog。
有挺多的简单题，适合我这样的零基础菜鸟，但这个网站没有题解，网上只能查到前27题的题解。

其他网站：

 - [菜鸟教程](https://www.runoob.com/w3cnote/verilog-tutorial.html)(有Verilog的内容，但没有OJ)
 - [EDA Playground](https://www.edaplayground.com)(英文网站，可以在线运行代码，很流畅)
 
 
**书籍**
 - **《EDA技术与Verilog HDL》** 王金明编著 清华大学出版社
这本书是基于Vivado平台的，讲了Vivado的基本操作、Verilog语法和一些实例，硬件用EGO1实验板。
 - **《自己动手写CPU》** 雷思磊 电子工业出版社
 这本书是基于Modelsim平台的，主要是使用Verilog设计能运行mips32指令的处理器。
 
 - **《Vivado入门与FPGA设计实例》** 廉玉欣 侯博雅编著 电子工业出版社
 这本书也是基于Vivado和EGO1的，介绍了不少组合逻辑和时序逻辑的基本器件设计，如加法器设计。

## 一、简介
  Verilog HDL(Hardware Description Language)是IC设计者常用的两种HDL之一，另一种是VHDL，通过比较Verilog和C语言的区别可以更好地理解它。
  **Verilog和C语言的区别：**

 1. 描述对象不同：
Verilog语法和C接近，但C描述的是算法逻辑，依赖于硬件对其进行实现。而Verilog是硬件描述语言，描述的是硬件本身。
 2. 处理方式不同：
C需要经过**编译、汇编、链接**来将代码转化为可由计算机执行的二进制代码，而Verilog则需要经过**综合**来生成描述门与门之间互联关系的网表文件。
 3. 执行方式不同：
Verilog的部分描述语句可以并行执行，而C只能串行执行。
## 二、模块
### 2.1 模块是Verilog的设计实体
Verilog的基本设计思想是自顶向下（top-down），设计实体是模块，所有Verilog代码都将在模块内书写。
如下图所示，先定义顶层模块，分析顶层模块中所需的各个子模块，然后进一步对各个子模块进行分解和设计，最终可以将一个大的系统分解为多个子系统。
 在Verilog中，成熟的、封装好的模块称为IP(intelligent property)，调用已有IP的本质就是模块实例化。
<!--  ![在这里插入图片描述](/images/568b60b97f8ec399024879e57904f829.png) -->
 
### 2.2 模块声明
  模块是Verilog的基本设计实体，模块声明的第一行指定了模块名称和端口列表，下面若干行指定了每个端口的方向、位宽、数据类型。
  例如定义一个32位加法器模块：

```rust
module add32(in1,in2,out);
  input wire[31:0] in1,in2;
  output wire[31:0] out;
  assign out=in1+in2;
endmodule
```

  其中in1，in2，out是该模块的三个端口，采用上述代码较为简洁，也可以采用如下定义：

```rust
module add32(
  input wire[31:0] in1,
  input wire[31:0] in2,
  output wire[31:0] out
);
  assign out=in1+in2;
endmodule
```

### 2.3 模块的实例化
模块实例化有两种方式，
  一是按照名称：
.模板中端口名称  (要连接到端口的线名)，
  二是按照位置
和定义时一一对应
下面我们将在top_module顶层模块中实例化mod_a，如图所示：
<!-- ![在这里插入图片描述](/images/4eaf0a4293a9102bde53028d6db7b97a.png) -->
其中mod_a实现的功能是将输入的a、b、c、d四个信号相与、相或，赋给out1和out2，mod_a的声明如下：

```rust
module mod_a(
    output out1, out2,
    input in1,in2,in3,in4
);
    assign out1 = in1 & in2 & in3 & in4;
    assign out2 = in1 | in2 | in3 | in4;   
endmodule
```
在top_module中两种实例化mod_a模块的代码如下：

```rust
module top_module( 
    input a, 
    input b, 
    input c,
    input d,
    output out1,
    output out2
);
    //基于端口位置的实例化如下
    mod_a  inst_1(
        out1,out2,a,b,c,d
    );
    //基于端口名称的实例化如下
    mod_a inst_2(
              .out1(out1),
              .out2(out2),
              .in1(a),
              .in2(b),
              .in3(c),
              .in4(d)
    );
endmodule
```
## 三、Verilog基本要素
### 3.1 数字
在Verilog HDL中,整型常量即整常数有以下四种进制表示形式:
1. 二进制整数(b或B)
2. 十进制整数(d或D)
3. 十六进制整数(h或H)
4. 八进制整数(o或O)

数字表达方式有以下三种:
1. <位宽><进制><数字>这是一种全面的描述方式。

2. <进制><数字>在这种描述方式中,数字的位宽采用缺省位宽(这由具体的机器系统决定,但至少32位)。

3. <数字>在这种描述方式中,采用缺省进制十进制。

**举例：**
8'b11000101    相当于十进制的197 
8'h8a          相当于十进制138
12             即十进制的12

### 3.2 变量
声明格式如下：
<数据类型><符号><位宽><变量名>    <元素数>
其中数据类型和变量名是必要的，其余均可省略。
数据类型可以是net型、variable型，

1. net型变量
相当于硬件电路中的物理连接，特点是输出的值随着输入值的变化而变化。
<!-- ![在这里插入图片描述](/images/be61e5e32b35689fcb052cfbdec5bff4.png) -->
2. variable型变量
该变量是有存储功能的数据类型
<!-- ![在这里插入图片描述](/images/7047b9b1a96fb23ff65d0867d8a0441d.png) -->
  当变量声明中的位宽大于1时，对应的变量是向量。
  例：`wire [3:0] bus;` 
  该语句声明了4位的wire型向量bus，其中冒号前面的是最高有效位(MSB,Most Significant Bit)，冒号后面的是最低有效位(LSB,Least Significant Bit)。

### 3.3 运算符
1.算术运算符

```rust
 +,－,×，/,％
```

其中/和%不可综合

2.赋值运算符

```rust
 =,<=
```

3.关系运算符

```rust
<=,>=,>,<
```

4.逻辑运算符

```rust
&&,||,!
```

5.条件运算符

```rust
 ?:
```

6.位运算符

```rust
~,|,^,&,^~或者~^
```

7.移位运算符

```rust
 <<,>>
```

8.位拼接运算符

```rust
{ }
```

9.等式运算符

```rust
 == , != , !==,===
```

其中===和!==不可综合

10.缩位运算符

```rust
&，~&， |， ~|，^，~^,^~)
```
在这些运算符中，多数都很好理解。
因此，后面只对位运算符，位拼接运算符，等式运算符，缩位运算符进行说明。
**对运算符的说明**
 1. 位运算符

```rust
~ ：按位取反   	 	a=1001   ~a=0110
& ：按位与   	 	a=1001   b=0001   a&b=0001
| ：按位或      	 	a=1001   b=0001   a|b=1001
^ ：按位异或	     	a=1001   b=0001   a^b=1000
^~ ：按位同或(异或非) a=1001   b=0001  a^~b=0111
```

 2. 等式运算符中== 和===的区别

```rust
==运算中，如果某些位是x或z，则比较结果是x
===运算中，对于某些位是x或z的，也进行比较，两个操作数必须完全一致，结果才为1
如:
reg [4:0] a=5'b11x01;
reg [4:0] b=5'b11x01;
针对上面的a和b，a==b返回x，而a===b返回1
```

 3. 位拼接运算符

```rust
用来将两个或多个信号的某些位拼接起来。例如，在进行加法运算时，可以将和与进位输出拼接在一起使用：
input [3:0] ina,inb;
output [3:0] sum;
output cout;
assign {cout,sum}=ina+inb;
```

 4. 缩位运算符

```rust
缩位运算符是对单个操作数的递推运算，它放在操作数的前面，能将一个矢量缩减为一个标量。
如：reg [3:0] a;
b=&a; 
该代码等效于b=((a[0]&a[1])&a[2])&a[3]
```
## 四、Verilog行为语句
### 4.1 过程语句
**always过程语句**
always过程语句是重复执行的，可综合的。
格式：
always@(<敏感信号表达式>)
begin
  //语句序列
end
always过程语句是有触发条件的，触发条件写在敏感信号表达式中。

敏感信号表达式的格式：

 1. 电平敏感型

```rust
always@(in1 or in2)
always@(in1,in2)
用or和逗号都表示任一信号可触发事件
```

 2. 边沿敏感性

```rust
posedge表示上升沿，negedge表示下降沿。
为32位加法器添加一个时钟同步信号clk
always@(posedge clk)
begin
  out=in1+in2;
end
在时钟信号的上升沿才会进行加法运算。
```
**initial过程语句**
initial过程语句不带出发条件且仅执行一次。
initial语句通常用于仿真模块中对激励向量的描述，或者用于给寄存器变量赋初值。
它是面向模拟仿真的过程语句，通常不能被逻辑综合工具支持。
### 4.2 块语句
块语句是由块标识符begin-end或者fork-join界定的一组语句，当块语句只包含一条语句时，块标识符可以缺省。
下面分别介绍串行块begin-end和并行块fork-join
**串行块begin-end**
串行块中的语句按串行方式顺序执行

```rust
module wave1
parameter cycle=10;
reg wave;
initial
  begin
  #(CYCLE/2) wave=0;
  #(CYCLE/2) wave=1;
  #(CYCLE/2) wave=0;
  #(CYCLE/2) wave=1;
  end
initial $monitor($time,,,”wave=%b”,wave);
endmodule
```
**并行块fork-join**
并行块fork-join中的所有语句是并发执行的。例如：

```rust
fork
  regb=rega;
  regc=regb;
join
```

用fork-join并行块产生信号波形

```rust
module wave2;
parameter CYCLE=5;
reg wave;
initial
  fork wave=0;
  #(CYCLE) wave=1;
  #(2*CYCLE) wave=0;
  #(3*CYCLE) wave=1;
  #(4*CYCLE) wave=0;
  #(5*CYCLE) wave=1;
  #(6*CYCLE)  $stop;
  join
initial $monitor($time,,,”wave=%b”,wave);
endmodule
```
### 4.3 赋值语句
**1.连续赋值(Continuous Assignment)语句**
用assign对wire型变量进行赋值的语句。
等式右边的任何变化都将随时反映到左边去。

**2.过程赋值(Procedural Assignment)语句**
1）非阻塞赋值（Non-Blocking）
赋值符号为”<=”，是并行执行的
非阻塞赋值在整个过程块结束时才完成赋值操作

2）阻塞赋值(Blocking)
赋值符号为”= “，是串行执行的
<!-- ![在这里插入图片描述](/images/bcf5671829d6d09a0b666bf13099f981.png) -->

### 4.4 条件语句
#### 4.4.1 if-else语句
格式有三种：
<!-- ![在这里插入图片描述](/images/87e05e2a3343ef15834f0068b88ff927.png) -->
其中语句序列可以是单句，可以是多句，多句时要用begin...end块语句括起来。
#### 4.4.2 case语句
格式如下：

```rust
case(敏感表达式)
 值1:语句序列1;
 值2:语句序列2;
 ...
 值n:语句序列n;
 default:语句序列n+1;
endcase
```

根据敏感表达式的值，来选择对应的语句序列进行执行。

==casez==语句中，对于值为高阻z的位无需比较。
==casex==语句中，对于值为z或者x的位无需比较。
此外，在casez和casex中还可以使用？来表示无需比较的位


### 4.5 循环语句

 1. for语句
for(循环变量初始化;循环条件;修改循环变量)
     执行语句序列;
2. forever语句
forever begin
     执行语句序列；
end
3. repeat语句
repeat(循环次数表达式) begin
    执行语句序列
end
4. while语句
while(循环条件) begin
  语句序列
end

### 4.6 编译指示语句

```C
1. 宏替换 `define
格式：`define 宏名 变量或名字
`define可以用简单的宏名替代复杂的表达式

2. `include语句
`include是文件包含语句，它可将一个文件全部包含到另一个文件中，格式如下：
`include “文件名”

3. 条件编译语句`ifdef   `else  `endif
通过条件编译语句可以指定内容进行编译。
`ifdef 宏名
  语句序列
`endif
`ifdef 宏名
  语句序列1
`else
  语句序列2
`endif
```

## 五、Testbench
### 5.1 为什么需要Testbench
Verilog是用来设计电路的，并且模块是Verilog的设计实体，那么设计好的模块需要验证其功能和性能是否符合预期目标，Testbench正是为了满足这一需要产生的。下图展示了Testbench的功能。
**概念：**
Testbench的本质仍是Verilog模块，但它是用于产生激励信号，对所设计的电路进行测试的特殊Verilog模块。
<!-- ![在这里插入图片描述](/images/f6be1de5b9bfe6b299dafa9cb05b841e.png) -->


### 5.2 Testbench的目的和结构

**编写Testbench的目的**
编写Testbench的主要目的是对使用 HDL设计的电路进行仿真验证，测试设计电路的功能、性能是否与预期的目标相符。
编写Testbench进行测试的过程如下：
1）产生激励（就是给被测试模块输入向量）
2）将产生的激励加入到被测试模块并观察其输出响应
3）将输出响应与期望值进行比较

**Testbench的基本结构**
module <Testbench名>;
               <变量定义声明>      
               <使用initial或者always语句产生激励波形> 
               <待测试模块例化>
               <监控和比较输出响应>
endmodule
### 5.3 激励产生的方式
Testbench的激励有几种产生方式，

 1. HDL描述方式
Verilog作为硬件描述语言，既可以用于设计硬件电路，也可以用于产生仿真激励。
 
 2. 文本输入方式
使用HDL来产生复杂数据结构的激励较为麻烦，Verilog提供了读入文本文件的系统函数$readmemb和$readmemh，分别用于从文本文件读入二进制和十六进制数据，存放到Verilog自定义的memory中，Verilog再从memory中取出数据将激励施加到被测模块。
 
 3. 编程语言接口(PLI)方式
仿真工具提供了PLI，PLI指将C程序嵌入到HDL设计中，用户可以用C写扩展的系统任务和函数，扩充了HDL语言的功能。
#### 5.3.1 产生时钟的方式
 1.使用initial方式产生占空比为50%的时钟

```rust
inial
begin
	clk_1=0;
	forever
		#50 clk_1=~clk_1;
end
```

注意:要给时钟赋初值，时钟缺省值为z，取反仍为z，如果没有赋初值，时钟就会一直处于高阻z状态

 2. 使用always方式

```rust
initial 
	clk_2=0;
always
	#50 clk_2=~clk_2;
```
3. 使用repeat产生确定数量的时钟

```rust
initial
begin
	clk_3=0;
	repeat(6)
		#50	clk_3=~clk_3;
end
```

4. 产生占空比非50%的时钟

```rust
initial
	clk_4=0;
always
beign
	#30 clk_4=~clk_4;
	#20 clk_4=~clk_4;
end
```
下图展示了采用上面3种方式生成的时钟，
图中clk_1使用forever产生10MHz时钟，
clk_2使用always产生10MHz时钟，
clk_3使用repeat指定循环6次，产生3个周期的时钟，
clk_4通过设定不同的延时(延时30ns后置1，延时10ns后置0)产生占空比非50%的时钟。
<!-- ![在这里插入图片描述](/images/3dfffaaaf943613863c1598d2e8a044d.png) -->

#### 5.3.2 产生复位信号的方式
**同步复位和异步复位的概念**
> 同步复位指复位信号是否生效依赖于时钟上升沿的到来， 
> 异步复位则无需等待时钟上升沿，只要复位信号有效就能对系统进行复位。

在使用Verilog产生复位信号的激励有如下几种方式：
1)异步复位

```rust
initial
begin
	rst=1;
	#100;
	rst=0;
	#500;
	rst=1;
end
```

2)同步复位

```rust
initial
begin
	rst=1;
	@(negedge clk);
	rst=0;
	#30;
	@(negedge clk);
	rst=1;
end
```

### 5.4 仿真结果分析的方式
运行仿真后，可以通过查看波形、显示信息和LOG文件的方式来分析仿真结果。

**查看波形**是最基本的方式，指的是根据时钟和激励来查看对应时刻的信号的值是否正确。在信号较多时这种方式比较繁琐低效，因此查看波形的分析方式通常在小模块的仿真分析时使用。

**显示信息和LOG文件**的方式是指在设计Testbench时添加一些自检测的程序，将程序运行的状态信息显示到屏幕或LOG文件中，以便后续分析。

### 5.5 Testbench实例
#### 5.5.1 2-4解码器
实现2-4解码器
     根据输入A,B的变化，来改变输出Z的值
源码如下：
<!-- ![在这里插入图片描述](/images/3a6e82971d1363ca82e5797314908987.png) -->
tb核心代码如下(省略例化和信号声明)：

```rust
initial begin
en=0;
a=0;
b=0;
#10 en=1;
#10 b=1;
#10 a=1;
#10 b=0;
#10 a=0;
#10 $stop;
end
always @(en or a or b or z) begin
$display("At time%t,input is %b%b%b,output is %b",$time,a,b,en,z);
end
```
通过系统任务$display将程序执行相关信息输出到控制台
**仿真结果分析**
<!-- ![在这里插入图片描述](/images/77a52d533c731eb1f4e1705cef85d2fe.png) -->
<!-- ![在这里插入图片描述](/images/c3a04ed09bce8357d82dce567e8e33a2.png) -->
通过查看波形可以发现，z随着{a,b}产生对应的编码，因此2-4编码器满足设计要求


#### 5.5.2 时序检测器
下面是一个时序检测器的原码，用于检测数据线上连续3个1的序列，在时钟的每个上升沿检查数据。
源代码如下图所示。
<!-- ![在这里插入图片描述](/images/d509b8c28f2ff6944c989813e01642c0.png) -->

```rust
`timescale 1ns / 1ps
截取核心Testbench如下
    initial
    begin
        Data=0;
        #5 Data=1;
        #40 Data=0;
        #10 Data=1;
        #40 Data=0;
        #20 $stop;
    end

    initial 
        Out_File=$fopen("results.txt");
    always @(posedge Clock)
    begin
        if(Detect==1'b1)
            $fwrite(Out_File,"At time %t,Detect out is 1\n",$time);
            
    end
```
在第一个initial语句中，设置激励
在第二个initial中，将程序执行的相关信息通过文件IO的系统任务$fopen和fwrite写入日志
**仿真结果分析**
<!-- ![在这里插入图片描述](/images/297d03e9b496e64346aa3cf98bb3df8d.png) -->
时钟Clock一个周期为10ns，在Data连续三次上升沿为1后，Detect置为1。时序检测器满足设计要求。
### 5.6 常用的系统函数

```rust
1.$display与$write
$display和$write功能相同，都用于将仿真结果输出控制台，区别是$display输出后自动换行，$write不能。

2.$finish与$stop
$finish和$stop用于控制仿真过程，$finish表示结束仿真，$stop表示中断仿真。

3.$time与$realtime
$time和$realtime用于显示已仿真时间，$time返回整数，$realtime返回浮点数。

4.$monitor与$strobe
$monitor和$strobe也属于输出型函数，$monitor用于实时监控变量并输出，$strobe用于在仿真事件发生后输出。

5.$readmemb和$readmemh
用于从外部文件读取数据并放入存储器中

6.$random
产生随机数的系统任务，返回32位随机整数
```

