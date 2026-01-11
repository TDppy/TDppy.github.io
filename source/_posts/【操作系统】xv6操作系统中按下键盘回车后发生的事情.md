---
title: 【操作系统】聊聊xv6操作系统中按下键盘回车后发生的事情
date: 2026-01-11 15:30:00  # 文章发布日期，格式：年-月-日 时:分:秒
categories: 操作系统  # 可选，如：技术分享、生活随笔
tags: [操作系统, RISC-V,嵌入式软件开发]  # 可选，如：[Hexo, GitHub Pages]
layout: post
---
# 学习XV6的意义
xv6是麻省理工学院在MIT6.S081课为教学设计的操作系统，总代码约1W+行，由C语言和部分汇编代码组成，覆盖了进程调度、文件描述符与文件系统、中断与异常处理、设备管理等操作系统的核心内容。命名由来是xv6基于UNIX6的整体风格改进，所以叫v6，x是eXtensible的意思。xv6提供了基本的操作系统原型，相比于uCos这种嵌入式操作系统，xv6更加完善，反应了现代Linux操作系统的基本原理。早期的xv6是基于x86指令系统编写的，随着RISC-V的兴起，在2020年后也推出了RISC-V版本。
学习xv6可以让我们掌握使用C语言实现一个操作系统，一方面这能够让我们了解printf的背后发生了什么、按下键盘后发生了什么、Windows/Linux是如何管理各种进程的、软硬件之间的接口是什么，另一方面，操作系统是嵌入式软件开发岗位常要求的技能，对于应聘要求firmware、bsp、AI芯片运行时等岗位都有意义。从长远角度看，无论是学习什么知识，真正需要掌握的都不是语法和函数调用过程，而是系统设计思想，这样当我们面临新的复杂的系统问题时，便可以从过往的设计思路中得到启迪。
# 全流程概述
**假设我们启动xv6后，什么都不做，直接按下键盘回车，会发生什么？**
键盘的UART控制器发送中断到PLIC，PLIC接收所有设备的中断信号、按照优先级仲裁、发送给CPU，设置CPU的SIE寄存器，CPU检测SIE寄存器发现中断，并执行trampoline.S中的uservec函数，uservec会跳转到trap.c中的usertrap函数，保存用户程序计数器epc、stvec寄存器，然后跳转到devintr()函数去发现是哪个设备发起的中断，发现是uart后执行uartintr()函数，uartintr()函数接收键盘输入的字符并调用consoleintr()函数处理特殊字符。consoleintr()函数会唤醒shell进程，将状态由SLEEPING改为RUNNABLE，并加入到调度队列。

> 键盘按键 → UART接收 → PLIC仲裁 → CPU中断 → trampoline.S/uservec → trap.c/usertrap
> → trap.c/devintr → plic.c/plic_claim → uart.c/uartintr → console.c/consoleintr → proc.c/wakeup
> → Shell进程从SLEEPING → RUNNABLE → 继续执行gets()

# 各步骤详解
## UART
> UART 芯片有多个引脚 (pins)，包括：
> UART 芯片引脚示例：
├── TXD (Transmit Data) - 发送数据线
├── RXD (Receive Data) - 接收数据线  
├── GND (Ground) - 地线
├── INTR (Interrupt) - 中断信号线 ⭐⭐⭐
├── RTS/CTS - 流控制信号
└── 电源引脚
INTR 引脚的作用：
INTR 引脚是 UART 向 CPU 报告"需要注意"的信号线：
常态: 低电平 (0V)
中断时: 高电平 (通常 3.3V 或 5V)

## PLIC
PLIC 是 RISC-V 平台的中断控制器，负责：
 1. 收集所有外部设备的中断信号
 2. 仲裁多个同时发生的中断的优先级
 3. 分发最高优先级的中断给 CPU
## PLIC初始化
```c
void plicinit(void) {
  // 设置 UART 中断优先级为 1 (非零表示启用)
  *(uint32*)(PLIC + UART0_IRQ*4) = 1;
}

void plicinithart(void) {
  // 启用 UART 中断到这个 CPU 的 S-mode
  *(uint32*)PLIC_SENABLE(hart) = (1 << UART0_IRQ);
  // 设置中断优先级阈值为 0 (接受所有中断)
  *(uint32*)PLIC_SPRIORITY(hart) = 0;
}
```

## CPU中断响应
CPU检测到中断，检查当前模式：
 1. 如果在用户模式，stvec指向uservec（用户中断向量），跳转到uservec
 2. 如果在内核模式，stvec指向kernelvec，跳转到kernelvec
对于用户模式的处理（uservec）：
 1. 保存所有用户寄存器到trapframe
 2. 切换到内核栈
 3. 切换到内核页表
 4. 跳转到usertrap()
 对于内核模式，跳转到usertrap()
 
## 内核陷阱处理
检查scause寄存器，找到中断的原因并调用对应函数进行处理。
```c
void usertrap(void) {
  // 检查 scause 寄存器
  uint64 scause = r_scause();
  
  if(scause == 8){
    // 系统调用
  } else if((which_dev = devintr()) != 0){
    // 设备中断
  }
}

```

## 设备中断识别
```c
int devintr() {
  if((scause & 0x8000000000000000L) && (scause & 0xff) == 9){
    // 外部中断
    int irq = plic_claim();  // 询问 PLIC 哪个中断
    
    if(irq == UART0_IRQ){
      uartintr();            // 处理 UART 中断
    }
    
    plic_complete(irq);      // 告诉 PLIC 中断处理完成
    return 1;
  }
}
```

## UART中断处理
```c
void uartintr(void) {
  while(1){
    int c = uartgetc();      // 从 UART 读取字符
    if(c == -1) break;
    consoleintr(c);          // 传递给控制台
  }
}
```

## 控制台字符处理
```c
void consoleintr(int c) {
  // 处理特殊字符 (退格等)
  
  // 存储到缓冲区
  cons.buf[cons.e++ % INPUT_BUF] = c;
  
  // 如果是换行符或缓冲区满
  if(c == '\n' || cons.e == cons.r + INPUT_BUF){
    cons.w = cons.e;        // 标记行结束
    wakeup(&cons.r);        // 唤醒等待的进程！
  }
}

```

 

