---
title: 【操作系统】xv6操作系统中按下键盘回车后发生的事情
date: 2026-01-10 11:58:18
categories: 操作系统
tags: [教学操作系统, xv6, 操作系统]
layout: post
---

# xv6概述与学习价值

xv6是麻省理工学院为MIT 6.S081操作系统课程设计的教学操作系统。总代码量约1万行，主要使用C语言编写，辅以少量汇编代码。它涵盖操作系统核心机制：进程调度、文件系统、中断处理、设备驱动等。

xv6基于Unix V6系统改进设计，"x"表示可扩展(eXtensible)。相比简单嵌入式OS如uC/OS，xv6更接近现代操作系统架构。早期版本基于x86架构，2020年后推出RISC-V版本，本文分析该版本。

学习xv6的价值体现在多个方面：

1. **深入理解系统实现**：通过阅读和修改代码，掌握操作系统核心原理，包括：
   - I/O机制：printf如何输出到屏幕
   - 输入处理：键盘按键如何被捕获和处理
   - 进程管理：操作系统如何调度和管理进程
   - 软硬件接口：软件与硬件的交互方式

2. **应聘技能提升**：操作系统知识是嵌入式开发、固件开发、芯片运行时等岗位的核心要求，可以作为简历上的项目备战招聘。

3. **系统设计思维培养**：操作系统是典型的系统设计课程，我们需要了解其中的系统设计思想，为解决复杂问题提供思路。

本文通过分析按下键盘回车键后的完整执行流程，展示xv6的中断处理机制。
# 场景假设与整体流程

本文分析的场景：启动xv6操作系统后，用户在shell提示符下直接按下回车键（不输入任何命令）。

这个简单动作会触发操作系统中断处理的全流程，涉及硬件、CPU、内核、用户程序多个层次。

**整体流程图：**

```
键盘按键
    ↓
UART接收中断信号
    ↓
PLIC仲裁并转发给CPU
    ↓
CPU执行中断向量(uservec)
    ↓
内核陷阱处理(usertrap → devintr)
    ↓
UART中断处理(uartintr → consoleintr)
    ↓
唤醒shell进程(wakeup)
    ↓
shell读取输入并退出
```

接下来按时间顺序详细分析每个步骤。

# 详细执行流程

## 硬件中断：键盘信号到UART

键盘按键首先被键盘控制器捕获，转换为扫描码，然后通过串口(UART)传输到计算机。

UART(Universal Asynchronous Receiver/Transmitter)是串口通信的核心硬件。它有多个引脚：
- TXD/RXD：数据发送/接收
- GND：地线
- INTR：中断信号线

当UART接收到数据时，INTR引脚从低电平(0V)变为高电平(3.3V或5V)，向CPU的PLIC发出"有数据需要处理"的信号。

## 中断控制器：PLIC仲裁
PLIC 是 RISC-V 平台的中断控制器，负责：
 1. 收集所有外部设备的中断信号
 2. 仲裁多个同时发生的中断的优先级
 3. 分发最高优先级的中断给 CPU

在操作系统初始化时会将PLIC初始化，配置PLIC相关寄存器。PLIC初始化会调用plicinit函数和plicinithart函数，在系统启动时main函数中调用一次，plicinit设置中断请求的优先级，plicinithart则启用中断并设置中断优先级阈值。
如果你不清楚RISC-V中的PLIC，请阅读这篇：[【操作系统】RISC-V PLIC总结](/2026/Q1/operating-system-riscv-plic)
### plicinit函数
每个中断源都有一个优先级值 (0-7 或更高，取决于实现)
- 优先级 = 0: 中断被禁用
- 优先级 > 0: 中断启用，数值越大优先级越高

```c
void plicinit(void)
{
  // 将可能产生的中断请求(Interrupt ReQuest, IRQ)设为非 0
  *(uint32*)(PLIC + UART0_IRQ*4) = 1;
  *(uint32*)(PLIC + VIRTIO0_IRQ*4) = 1;
}
```

### plicinithart函数
plicinithart 为每个 CPU 核心初始化 PLIC（中断控制器）的设置。每个 CPU 核心都需要独立配置，因为中断可以被分配到不同的核心处理。
1. 首先启用中断
PLIC_SENABLE(hart) = PLIC + 0x2080 + (hart)*0x100 作用是控制哪些中断可以发送到这个 CPU 核心的 S-mode（supervisor mode），设置为(1 << UART0_IRQ) | (1 << VIRTIO0_IRQ)意味着：
- UART 中断 (IRQ 10) 被启用
- VirtIO 磁盘中断 (IRQ 1) 被启用
- 其他中断被禁用
2. 然后设置优先级阈值
PLIC_SPRIORITY(hart) = PLIC + 0x201000 + (hart)*0x2000 作用是设置中断优先级阈值，只有优先级高于此值的才会被发送到 CPU，阈值设置为 0 表示接受所有优先级 > 0 的中断。由于 plicinit() 中设置 UART 和 VirtIO 的优先级为 1，所以这些中断会被接受。如果阈值设为 1，则只有优先级 > 1 的中断才会被处理。
```c
void plicinithart(void) {
  int hart = cpuid();
  *(uint32*)PLIC_SENABLE(hart)= (1 << UART0_IRQ) | (1 << VIRTIO0_IRQ);
  *(uint32*)PLIC_SPRIORITY(hart) = 0;
}
```
为什么需要每个 CPU 独立配置：
1. 多核支持: 不同的中断可以路由到不同的 CPU 核心
2. 负载均衡: 可以将中断处理分散到多个核心
3. 隔离性: 每个核心可以独立控制接收哪些中断

优先级阈值的意义
- 阈值 = 0: 接受所有非零优先级中断
- 阈值 = 1: 只接受优先级 > 1 的中断
- 阈值 = 最大值: 屏蔽所有中断

S-mode vs M-mode
- PLIC_SENABLE: 控制 S-mode（supervisor mode）中断
- PLIC_MENABLE: 控制 M-mode（machine mode）中断
- xv6 运行在 S-mode，所以使用 S-mode 设置

## CPU中断响应
一旦 PLIC 决定发送中断，它就会向 CPU 的**外部中断引脚**发送信号。CPU 检测到这个信号后，会暂停当前执行的指令，保存当前的执行状态，然后跳转到一个预先设置好的地址去执行中断处理代码。在 RISC-V 架构中，这个地址叫做 **Supervisor Trap Vector Base Address Register, 简称 stvec**，如果当前 CPU 运行在用户模式，这个地址会指向一个叫做 **uservec** 的函数。
> 为了保证原汁原味，我直接把stvec寄存器的RISC-V官方手册解释贴上。
--- 
 {% asset_img stvec.png  stvec寄存器解释 %}

首先，我们需要了解 CPU 的**外部中断引脚**。在 RISC-V 架构中，有一个专门的引脚叫做 SEI，也就是 Supervisor External Interrupt。当 PLIC 决定发送中断时，它会通过这个引脚向 CPU 发送一个电信号。这个引脚是 CPU 芯片上的物理引脚，平时保持低电平，当有外部中断时会被拉高。

当 CPU 检测到 SEI 引脚的信号变高时，它会立即中断当前的指令执行。这个过程是完全由硬件控制的，不需要软件干预。CPU 会自动做以下几件事：

- **保存pc**:首先，它会保存当前的程序计数器（PC）到 sepc 寄存器。这个寄存器专门用来存储发生异常或中断时的指令地址，这样软件就可以知道中断发生的确切位置。
> 为了保证原汁原味，我直接把sepc寄存器的RISC-V官方手册解释贴上。
--- 
 {% asset_img sepc.png  sepc寄存器解释 %}

- **保存sstatus**:然后，CPU 会保存当前的状态信息到 sstatus 寄存器。这个寄存器包含了很多重要的状态位，比如当前是否在用户模式、是否启用了中断等。
> 为了保证原汁原味，我直接把sstatus寄存器的RISC-V官方手册解释贴上。
--- 
 {% asset_img sstatus1.png  sstatus解释 %}
 {% asset_img sstatus2.png  sstatus官方手册解释 %}

- **保存scause**:同时，CPU 还会将中断的原因编码保存到 scause 寄存器。对于外部中断，scause 的值会是 0x8000000000000009，其中最高位设置为 1 表示这是中断而不是异常，后面的值 9 表示外部中断。
> 为了保证原汁原味，我直接把scause寄存器的RISC-V官方手册解释贴上。
--- 
 {% asset_img scause.png  scause解释 %}

- **跳转到uservec**:做完这些保存工作后，CPU 就会跳转到 stvec 寄存器指向的地址执行。这个跳转是由硬件直接完成的，没有任何条件判断。在 xv6 中，如果 CPU 当前运行在用户态（也叫用户模式/用户空间），stvec 会指向 **trampoline.S** 中的 **uservec 函数**的地址；如果 CPU 当前运行在内核态，则 stvec 会指向 **kernelvec.S** 中的 **kernelvec 函数**的地址。<span style="color:red;">本文以中断前运行在用户态为例来讲解。</span> 

---
uservec 函数首先保存所有寄存器到 trapframe（trapframe可以理解为一片用于保存现场的专用内存空间），然后从用户页表切换到内核页表，最后调用 usertrap() 函数。
下面，让我们详细看看 uservec 函数的具体实现。

### 保存所有寄存器到 trapframe
首先是函数的入口和初始设置：

```riscv
uservec:    
    # swap a0 and sscratch
    # so that a0 is TRAPFRAME
    csrrw a0, sscratch, a0
```

这一开始的注释说明了这个函数的作用：处理来自用户空间的陷阱（traps），包括中断和异常。函数开始时，**sscratch** 寄存器被设置为指向当前进程的 trapframe 结构。`csrrw` 指令交换 a0 和 sscratch 的值，这样 a0 就指向了 trapframe，而原来的 a0 值被保存到 sscratch 中。
> 为了保证原汁原味，我直接把sscratch寄存器的RISC-V官方手册解释贴上。
--- 
 {% asset_img sscratch.png  sscratch解释 %}


接下来是保存用户寄存器到 trapframe：

```riscv
# save the user registers in TRAPFRAME
sd ra, 40(a0)
sd sp, 48(a0)
sd gp, 56(a0)
sd tp, 64(a0)
sd t0, 72(a0)
# ... 继续保存其他寄存器
```

这里使用 `sd` 指令（store double word）将所有用户空间的寄存器保存到 trapframe 结构中。每个寄存器都有固定的偏移量，比如 ra 保存到距离 trapframe 基地址 40 字节的位置，sp 保存到 48 字节的位置。这些偏移量是预定义的，对应 `proc.h` 中 `struct trapframe` 的字段定义。
> **trapframe是什么？**
> trapframe是一个数据结构（在proc.h中定义），专门用来保存和恢复进程在用户态和内核态切换时的寄存器状态。
它就像一个“快照”，记录了用户程序运行时的CPU寄存器值。当发生中断、异常或系统调用时，系统需要保存现场，处理完后再恢复，让程序继续运行。
每个进程都有自己的trapframe，存储在用户页表的一个独立页面中（位于trampoline页下方）。这个页面在内核页表中没有特殊映射，所以内核直接用虚拟地址访问不了它，而是通过**sscratch寄存器**指向它。
```c
// 用于 trampoline.S 中 trap 处理代码的每个进程数据。
// 位于用户页表中 trampoline 页下方的一个独立页面中。在内核页表中未特殊映射。
// sscratch 寄存器指向此处。
// trampoline.S 中的 uservec 将用户寄存器保存到 trapframe 中，
// 然后从 trapframe 的 kernel_sp、kernel_hartid、kernel_satp 初始化寄存器，并跳转到 kernel_trap。
// usertrapret() 和 userret 在 trampoline.S 中设置 trapframe 的 kernel_*，
// 从 trapframe 恢复用户寄存器，切换到用户页表，并进入用户空间。
// trapframe 包括被调用者保存的用户寄存器，如 s0-s11，因为通过 usertrapret() 返回用户的路径不会通过整个内核调用栈。
struct trapframe {
  /*   0 */ uint64 kernel_satp;   // kernel page table
  /*   8 */ uint64 kernel_sp;     // top of process's kernel stack
  /*  16 */ uint64 kernel_trap;   // usertrap()
  /*  24 */ uint64 epc;           // saved user program counter
  /*  32 */ uint64 kernel_hartid; // saved kernel tp
  /*  40 */ uint64 ra;
  /*  48 */ uint64 sp;
  /*  56 */ uint64 gp;
  /*  64 */ uint64 tp;
  /*  72 */ uint64 t0;
  /*  80 */ uint64 t1;
  /*  88 */ uint64 t2;
  /*  96 */ uint64 s0;
  /* 104 */ uint64 s1;
  /* 112 */ uint64 a0;
  /* 120 */ uint64 a1;
  /* 128 */ uint64 a2;
  /* 136 */ uint64 a3;
  /* 144 */ uint64 a4;
  /* 152 */ uint64 a5;
  /* 160 */ uint64 a6;
  /* 168 */ uint64 a7;
  /* 176 */ uint64 s2;
  /* 184 */ uint64 s3;
  /* 192 */ uint64 s4;
  /* 200 */ uint64 s5;
  /* 208 */ uint64 s6;
  /* 216 */ uint64 s7;
  /* 224 */ uint64 s8;
  /* 232 */ uint64 s9;
  /* 240 */ uint64 s10;
  /* 248 */ uint64 s11;
  /* 256 */ uint64 t3;
  /* 264 */ uint64 t4;
  /* 272 */ uint64 t5;
  /* 280 */ uint64 t6;
};
```

特别需要注意的是 a0 的处理：

```riscv
# save the user a0 in p->trapframe->a0
csrr t0, sscratch
sd t0, 112(a0)
```

由于 a0 在一开始就被交换了，这里需要从 sscratch 中读取原始的 a0 值，然后保存到 trapframe 的 112 字节偏移位置。
### 从用户态切换到内核态
保存完用户状态后，开始恢复内核环境：

```riscv
# 从 p->trapframe->kernel_sp 读到内核栈指针，赋值给sp
ld sp, 8(a0)

# 从 p->trapframe->kernel_hartid 读到硬件线程id，赋值给tp
ld tp, 32(a0)
```

`ld` 指令（load double word）从 trapframe 中读取内核栈指针和 hart ID。sp 设置为内核栈指针，这样后续的函数调用就会使用内核栈。tp 设置为当前 CPU 核心的 ID，这在多核系统中很重要。

### 用户页表切换到内核页表
接下来是关键的页表切换：

```riscv
# 从 p->trapframe->kernel_satp 中读到stap，切换页表到内核态
ld t1, 0(a0)
csrw satp, t1
sfence.vma zero, zero
```

这里从 trapframe 中读取内核页表的地址，写入 satp 寄存器，然后执行 `sfence.vma` 指令刷新 TLB。这个操作将页表从用户页表切换到内核页表，确保后续代码使用正确的地址映射。

### 跳转到 usertrap 函数
最后是跳转到 C 函数：

```riscv
# load the address of usertrap(), p->trapframe->kernel_trap
ld t0, 16(a0)

# jump to usertrap(), which does not return
jr t0
```

从 trapframe 中读取 usertrap 函数的地址，然后无条件跳转。这个跳转将控制权转移给 C 语言编写的 usertrap 函数，继续处理具体的陷阱类型。

整个 uservec 函数展示了从硬件中断到软件处理的无缝衔接。它精确地保存了用户状态，恢复了内核环境，然后将控制权交给更高层次的处理函数。这种设计既保证了性能，又确保了安全性。每个指令都有其特定的作用，共同构成了操作系统中断处理的基础设施。

通过这个函数，xv6 能够在发生中断时安全地从用户模式切换到内核模式，处理各种异步事件，然后在适当的时候恢复用户程序的执行。这种机制是现代操作系统能够可靠运行的关键。

---


 
## 内核中断处理
下面简要说明usertrap函数、devintr函数、UART和控制台处理的流程，然后再具体讲解他们的工作细节。

### usertrap函数：陷阱分类

uservec跳转到usertrap函数(位于kernel/trap.c)，该函数分析中断类型。

首先验证是从用户模式进入，然后切换stvec指向kernelvec。

保存程序计数器后，通过scause判断：
- scause == 8：系统调用
- 其他：调用devintr()处理设备中断

### devintr函数：设备中断识别

devintr函数识别外部中断(scause最高位为1，低8位为9)。

调用plic_claim()获取中断号：
- UART0_IRQ(10)：调用uartintr()
- VIRTIO0_IRQ(1)：磁盘中断处理

处理完成后调用plic_complete()通知PLIC。

### UART和控制台数据处理

uartintr()循环读取UART数据，调用consoleintr()处理每个字符。

consoleintr()将字符存储到控制台缓冲区，当遇到换行符时：
- 更新写指针cons.w
- 调用wakeup(&cons.r)唤醒等待输入的进程

### 工作细节
usertrap 函数首先会验证当前确实是从用户模式进入的中断。如果不是，它会直接 panic，因为这说明系统状态出现了异常。然后它会立即切换 stvec 寄存器，将其指向 kernelvec（位于 `kernel/kernelvec.S`)。函数接下来会获取当前进程的指针，并保存发生中断时的程序计数器。这个计数器指向用户程序中被中断的指令位置，对于系统调用来说，这个位置需要调整，因为 ecall 指令执行完后，程序计数器应该指向下一条指令。

现在到了关键的判断部分。usertrap 通过检查 scause 寄存器来确定中断或异常的类型。如果 scause 等于 8，就表示这是一个系统调用。如果是其他值，就需要进一步检查是否是设备中断。

在我们的按回车键的例子中，这是一个外部中断，所以程序会进入 `devintr()` 函数。这个函数也位于 `kernel/trap.c` 文件中，它专门处理设备中断。devintr 函数通过位运算来识别中断类型。对于外部中断，scause 的最高位是 1，低 8 位是 9。这个模式表明中断来自 PLIC 管理的外部设备。
```c
// usertrap 由 trampoline.S调用,
// 负责处理来自用户态的中断、异常或系统调用
void
usertrap(void)
{
  int which_dev = 0;

  if((r_sstatus() & SSTATUS_SPP) != 0)
    panic("usertrap: not from user mode");

  // 修改stvec，使其指向trap.c中的kerneltrap函数，当再次发生中断时由kerneltrap处理
  w_stvec((uint64)kernelvec);

  struct proc *p = myproc();
  
  // 保存sepc到trapframe中
  p->trapframe->epc = r_sepc();
  
  // 判断引发陷入的原因
  // 如果是系统调用，则sepc此时指向ecall指令，但我们希望返回的时候到下一条指令
  // 所以p->trapframe->epc += 4
  if(r_scause() == 8){
    if(p->killed)
      exit(-1);

    p->trapframe->epc += 4;

    // 中断会改变sstatus和c寄存器，所以不能使能中断
    intr_on();
    // 进入系统调用
    syscall();
  } else if((which_dev = devintr()) != 0){
    // ok
  } else {
    printf("usertrap(): unexpected scause %p pid=%d\n", r_scause(), p->pid);
    printf("            sepc=%p stval=%p\n", r_sepc(), r_stval());
    p->killed = 1;
  }

  if(p->killed)
    exit(-1);

  // 如果是定时器中断，则放弃CPU占用
  if(which_dev == 2)
    yield();

  usertrapret();
}
```

一旦确认是外部中断，函数就会调用 `plic_claim()`（位于 `kernel/plic.c`）来询问 PLIC 当前应该处理哪个中断。在我们的场景中，这个函数会返回 10，也就是 UART0_IRQ。有了中断号之后，devintr 就会根据不同的设备类型调用相应的处理函数。对于 UART 中断，它会调用 `uartintr()`（位于 `kernel/uart.c`）。uartintr 函数会检查 UART 的接收缓冲区，看看有没有新的数据可以读取。在我们的按回车键的例子中，这里应该有字符数据（换行符）。

```c
// kernel/uart.c - uartintr 函数
void uartintr(void) {
  while(1){
    int c = uartgetc();
    if(c == -1)
      break;
    consoleintr(c);  // 位于 kernel/console.c
  }
}
```

从 UART 读取到的每个字符都会被传递给 `consoleintr()` 函数（位于 `kernel/console.c`）。这个函数不仅负责将字符回显到屏幕，还会将其存储到控制台的输入缓冲区。

当 consoleintr 处理到换行符时，它就会更新输入缓冲区的写指针，并唤醒任何正在等待输入的进程。在我们的例子中，被唤醒的就是 shell 进程。

```c
// kernel/console.c - consoleintr 函数片段
void consoleintr(int c) {
  // ... 处理字符 ...
  
  if(c == '\n' || c == C('D') || cons.e == cons.r + INPUT_BUF){
    cons.w = cons.e;
    wakeup(&cons.r);  // 唤醒等待输入的进程
  }
}
```

处理完中断后，usertrap 函数会检查是否需要进行进程调度。在外部中断的情况下，通常不需要立即切换进程，除非这是定时器中断。最后，usertrap 会调用 `usertrapret()` 函数来准备返回用户空间。

```c
// kernel/trap.c - usertrap 函数结尾
if(which_dev == 2)
  yield();  // only for timer interrupts

usertrapret();  // 准备返回用户空间
```

整个中断处理过程就这样完成了。从按下回车键的物理动作开始，经过层层硬件和软件的处理，最终唤醒了 shell 进程，让它能够读取到用户的输入。

## 用户空间响应：Shell进程

### 系统调用与数据读取

shell进程被wakeup()唤醒后，继续执行getcmd()中的gets()调用。

gets()通过read()系统调用读取控制台：
- 用户空间read() → 内核consoleread()
- consoleread()等待缓冲区有数据，读取并返回

### 输入处理与进程退出

consoleread读取换行符后返回，gets()添加\0并返回。

getcmd()移除\n，发现缓冲区为空，返回-1(EOF)。

shell主循环退出，调用exit(0)终止。

这就是按下回车键导致shell退出的完整流程。如果输入命令，shell会解析并执行fork/exec。
