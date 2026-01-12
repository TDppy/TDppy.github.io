---
title: helloworld是怎样被一步步编译为可执行文件的？
date: 2020-07-06 19:52:30
categories: 编程与算法
tags: [C语言, 编程入门]
layout: post
---

@[TOC]
```c
#include<stdio.h>
int main(){
printf("helloworld");
return 0;
}
```
# 概述
在windows中，C语言代码的编译过程由IDE（如vc6、vs等软件）一键生成了可执行文件，但是我们知道编译过程有以下步骤：
预处理、编译、汇编、链接，于是我们可以在linux下用命令来分别执行这些步骤，从而可以查看某步后的内容。
## 1）预处理阶段    

```bash
命令：gcc -E hello.c -o hello.i
```

预处理阶段主要做的有三件事：1.文件包含 2.条件编译 3.宏定义展开
1.文件包含即将stdio.h中的内容复制下来替换#include <stdio.h>
2.条件编译例如#if #ifdef这些语句，实现其功能，这里不再赘述。
3.宏定义展开即如果有#define a 3 那么将会把程序中的a替换为3。
## 2）编译阶段      

```bash
命令：gcc -S hello.i -o hello.s
```

以下是编译的结果：
>         .file   "hello.c"
>         .section        .rodata .LC0:
>         .string "helloworld"
>         .text
>         .globl  main
>         .type   main, @function main: .LFB0:
>         .cfi_startproc
>         pushq   %rbp
>         .cfi_def_cfa_offset 16
>         .cfi_offset 6, -16
>         movq    %rsp, %rbp
>         .cfi_def_cfa_register 6
>         movl    $.LC0, %edi
>         movl    $0, %eax
>         call    printf
>         movl    $0, %eax
>         popq    %rbp
>         .cfi_def_cfa 7, 8
>         ret
>         .cfi_endproc .LFE0:
>         .size   main, .-main
>         .ident  "GCC: (GNU) 4.8.5 20150623 (Red Hat 4.8.5-39)"
>         .section        .note.GNU-stack,"",@progbits
可以看出，编译阶段是将C语言代码变成了汇编的代码，我们知道汇编代码的本质就是用一个个单词来取代0和1，方便记忆，到这一步已经很接近机器代码了。
## 3）汇编阶段	 

```bash
命令：gcc -c hello.s -o hello.o
```

汇编阶段是将汇编代码转变成机器代码，即将汇编的那些单词变成0和1
## 4）链接阶段      

```bash
命令：gcc hello.o -o hello
```

helloworld用到了printf函数，那么问题来了，我们只是调用了这个函数，那么这个函数的实现在哪呢？这就是链接阶段的目的，链接系统库中的函数，从而让这些调用有了实现。

