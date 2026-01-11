---
title: 【异常处理】Verilator报错Verilator requires a C++14 or newer compiler
date: 2026-01-11 15:30:00
categories: 异常处理
tags: [异常处理]
layout: post
---
> riscv-mini是UC Berkeley用Chisel编写的三级流水线RISC-V处理器，它实现了RV32I的用户级2.0版本ISA和机器级1.7版本ISA，是Berkeley著名的Rocket-chip项目的简化版

@[toc]
# 环境版本：

> Verilator 5.022 
> Ubuntu 22.04.3 
> gcc version 11.4.0

# 报错信息
在对risc-mini项目使用`make verilator`命令时出现
> Verilator requires a C++14 or newer compiler

# 解决办法
解决办法是将项目目录下Makefile中的 CXXFLAG后面的 -std=c++11改成-std=c++14即可
![在这里插入图片描述](/images/814fbba7f713728efd1da018c3e91860.png)

