---
title: 【异常处理】测试risc-mini项目出现 Cannot run program “z3“ CreateProcess error=2, 系统找不到指定的文件。
date: 2024-03-08 11:37:31
categories: 异常处理
tags: [错误解决, z3, 调试]
layout: post
---
> riscv-mini是UC Berkeley用Chisel编写的三级流水线RISC-V处理器，它实现了RV32I的用户级2.0版本ISA和机器级1.7版本ISA，是Berkeley著名的Rocket-chip项目的简化版


# 报错场景
下载risc-mini项目，sbt构建完成后，运行ALUTest.scala下的ALUArea测试，结果出现报错：
 ![ ](./1.png) 
报错信息是说在项目目录下无法运行z3，系统找不到指定的文件。
# 报错分析
z3是微软的一个数学求解的工具，这里报错提示在这个目录下没有z3这个程序，所以无法运行是合理的，我们需要做的是安装z3并将其路径加入到系统变量中，然后**重启电脑**，再次运行测试即可通过！

# 解决步骤
如果是ubuntu系统，使用`apt install z3`即可，如果是windows，继续往下看：

 1. 下载z3
<!--  在[这里](https://github.com/Z3Prover/z3/releases/tag/z3-4.12.6)下载z3，我的环境是`windows64位系统`，所以下载了`z3-4.12.6-x64-win.zip`，如图所示：![在这里插入图片描述](./2.png) 


如果你的系统是
这里需要注意，windows 64位系统要下载的是`z3-4.12.6-x64-win.zip`，而不是`z3-4.12.6-x86-win.zip`，x86版本是32位系统需要下载的。

2. 解压z3
下载后解压z3压缩包，可以看到bin目录下有z3.exe，我们把该路径加入到系统PATH变量中。
 ![ ](./3.png) 
3. 将z3.exe所在bin目录的路径加入环境变量
 ![ ](./4.png) 
加入以后重启电脑，再跑测试即可。

4. 测试成功
 ![ ](./5.png) 


# 参考资料
1. [我在github针对该问题上提出的issue](https://github.com/ucb-bar/riscv-mini/issues/61)
2. [z3的下载链接](https://github.com/Z3Prover/z3/releases/tag/z3-4.12.6)
3. [使用pip安装z3](https://blog.csdn.net/huiyu233/article/details/113850216)
4. [risc-mini官方仓库](https://github.com/ucb-bar/riscv-mini)
5. [敏捷硬件开发语言Chisel与数字系统设计](https://m.cxstar.com/book/2b08fd3700069fXXXX)   这本书中对risc-mini的各部分组件做了介绍
