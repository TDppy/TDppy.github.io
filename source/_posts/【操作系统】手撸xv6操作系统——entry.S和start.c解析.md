---
title: 【操作系统】手撸xv6操作系统——entry.S和start.c解析
date: 2026-01-11 15:30:00
categories: 操作系统
tags: [操作系统, RISC-V,嵌入式软件开发]
layout: post
---
﻿@[toc]
# entry.S解析和调试
## 代码分析
entry.S是xv6上电后执行的第一段代码，用于设置每个CPU的栈指针并跳转到start函数，每个CPU拥有4KB的栈空间。
```lua
.section .text
_entry:
        la sp, stack0
        li a0, 1024*4
			 csrr a1, mhartid
        addi a1, a1, 1
        mul a0, a0, a1
        add sp, sp, a0
	# jump to start() in start.c
        call start
spin:
        j spin
```
整段代码的作用是令sp = stack0的地址 + 4096 × (当前运行的CPU核心编号 + 1)。
la sp,stack0，la是load address，将stack0的地址赋值到sp寄存器，在RISC-V架构中sp是栈指针寄存器。
li a0,1024*4，li是load immediate，加载立即数4096到a0。
csrr a1,mhartid，是读取mhartid的值到a1中，mhartid是CPU核的编号，比如一共有4个CPU在运行entry.S，那么它们加载到的mhartid就分别是0,1,2,3。
addi a1,a1,1，是让a1等于a1加上立即数1，即a1=a1+1。
mul a0,a0,a1，是让a0 = a0 * a1，我们知道a0刚刚被赋值为4096，而a1等于mhartid+1，所以a0 = 4096 × (mhartid + 1)。
add sp , sp , a0，是让sp = sp + a0，即sp = stack0的地址 + 4096 × (mhartid + 1)。

## gdb调试

 1. 首先启动项目以及gdb调试
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/079835ab84314c1b8425863a8ea00860.png)
 2. 运行到_entry断点处
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d1f7d7af72d541629fa6ed6350e94d75.png)
3.依次查看各条指令执行情况
首先输入layout asm，然后依次执行各条指令，并查看执行结果的寄存器值，验证之前的代码分析。可以看出其实真实执行的汇编和编写的entry.S是有所不同的，因为编写的entry.S中有伪指令，例如la sp,stack0在实际执行时是ld sp,-1552(sp)，call start在实际执行的时候是用jal无条件跳转到start的地址，并将start地址后的0x80000086+4赋值给返回地址寄存器ra中。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/0b7b9c6621db45079db7b0f59f6e980a.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/59afa1c791e24c08bee549582841e0f0.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/d935d3daf3494d988c1553d491a37548.png)

# start.c解析和调试
## start.c解析
首先需要认识到RISC-V架构中，CPU核具有三种模式，机器模式、监督者模式、用户模式，机器模式是任何RISC-V CPU核都需要支持的最高级模式，具有CPU的一切权限，哪怕是嵌入式领域的小mcu也需要支持机器模式。监督者模式也被称为内核模式、内核态，运行操作系统内核程序。
start函数运行在机器模式，它主要做的事情就是将CPU从机器模式切换到监督者模式。
首先读取mstatus寄存器到x中。
```c
  unsigned long x = r_mstatus(); // 读取mstatus寄存器到x
  x &= ~MSTATUS_MPP_MASK;  //riscv.h 定义了 #define MSTATUS_MPP_MASK (3L << 11)
  x |= MSTATUS_MPP_S;      //riscv.h 定义了 #define MSTATUS_MPP_S (1L << 11)
  w_mstatus(x);            // 将x写入mstatus寄存器
```

根据riscv-privilege-v1.9文档，mstatus寄存器格式如下。由图可知，MPP位于mstatus[12:11]，表示machine previous privilege，如果MPP设置为S模式，那么mret命令执行后CPU就会回到S模式。MPP的取值从高（11)到低分别表示如下模式：

 - [ ] M-mode（Machine Mode，机器模式）：最高特权级，无权限限制，负责硬件初始化、特权级配置等底层操作（如 xv6 的start函数初始运行模式）。
 - [ ] H-mode（Hypervisor Mode，虚拟化模式）：可选特权级，用于虚拟化场景，负责管理多个客户机操作系统，普通 xv6 系统不启用该模式。
 - [ ] S-mode（Supervisor Mode，监督者模式）：内核运行模式，负责进程调度、内存管理、外设驱动等核心功能（xv6 内核的主要运行模式）。
 - [ ] U-mode（User Mode，用户模式）：最低特权级，用于运行用户应用程序，访问资源受内核严格限制（如普通的 shell 命令、自定义程序都运行在该模式）。
 由于start函数运行在M模式，希望返回到S模式，后面操作系统内核就可以运行在S模式了，所以应该令MPP为10。
 MSTATUS_MPP_MASK为3L<<11，即1100000000000，取反后为0011111111111，x&=~MSTATUS_MPP_MASK意思是让x其余位不变，MPP位变为00。MSTATUS_MPP_S是1L<<11，即100000000000，x|=MSTATUS_MPP_S意思是让MPP低位为1，即MPP变为01。
 
 因此，这几句话的作用是将mstatus寄存器的MPP位设置为01，从而在执行mret时CPU能够返回到S模式。
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8b0d2c71f2c54728bb783cb22b90c9e0.png)
这行代码的作用是设置mepc寄存器指向main函数的地址，即在执行mret后CPU会开始执行main函数。
```c
w_mepc((uint64)main); // riscv.h中定义了内联函数w_mepc执行asm volatile("csrw mepc, %0" : : "r" (x));
```
这行代码的作用是禁用分页机制，让虚拟地址和物理地址直接等同，简化初始化流程。
```c
w_satp(0);
```
这两行是将机器模式的中断和异常全部交由S模式来处理。medeleg和mideleg是两个寄存器，比特位置 1 表示 “该类型中断委托给 S-mode 处理”，置 0 表示 “该类型中断保留在 M-mode 处理”，这里全部置为1，将机器模式中断和异常全交给S模式处理。
```c
  w_medeleg(0xffff);
  w_mideleg(0xffff);
```
这行的作用是读取sie寄存器，并开启外部中断、定时器中断和软件中断。
```c
  w_sie(r_sie() | SIE_SEIE | SIE_STIE | SIE_SSIE);
```
riscv.h定义了SIE_SEIE，SIE_STIE，SIE_SSIE宏以及r_sie()函数，r_sie()函数读取sie寄存器，SEIE、STIE、SSIE分别代表外部中断、定时器中断和软件中断使能。
```c
#define SIE_SEIE (1L << 9) // external
#define SIE_STIE (1L << 5) // timer
#define SIE_SSIE (1L << 1) // software
static inline uint64
r_sie()
{
  uint64 x;
  asm volatile("csrr %0, sie" : "=r" (x) );
  return x;
}
```
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6db197f2a1f74040b6b082042d20e783.png)

下面几行代码初始化定时器，然后读取mhartid赋值给tp寄存器，tp是thread pointer寄存器，最后执行mret返回到s模式，并执行main函数。
```c
  // ask for clock interrupts.
  timerinit();

  // keep each CPU's hartid in its tp register, for cpuid().
  int id = r_mhartid();  //riscv.h中定义了asm volatile("csrr %0, mhartid" : "=r" (x) );
  w_tp(id); //  riscv.h中定义了w_tp为asm volatile("mv tp, %0" : : "r" (x));

  // switch to supervisor mode and jump to main().
  asm volatile("mret");
```
对于timerinit()函数，先不用管具体实现，需要知道的是当timerinit()初始化执行完成后，定时器中断的处理流程为：
 1. 当MTIME ≥ MTIMECMP时，硬件触发 M-mode 定时器中断；
 2. CPU 根据mtvec寄存器的配置，跳转到timervec汇编函数执行；
 3. timervec先将通用寄存器保存到mscratch0的预留空间（scratch[0..3]）；
 4. timervec从scratch[4]和scratch[5]读取MTIMECMP地址和间隔，更新MTIMECMP的值（当前MTIME + interval），实现周期性中断（否则仅触发一次中断）；
 5. timervec将 M-mode 定时器中断转换为 S-mode 软件中断（通过设置sip寄存器的软件中断位）；
 6. 中断委托机制生效，S-mode 内核接收到软件中断，由trap.c中的devintr()函数处理（最终支撑进程调度等功能）。

# start.c和riscv.h代码
## start.c代码
```c
#include "types.h"
#include "param.h"
#include "memlayout.h"
#include "riscv.h"
#include "defs.h"

void main();
void timerinit();

// entry.S needs one stack per CPU.
__attribute__ ((aligned (16))) char stack0[4096 * NCPU];

// scratch area for timer interrupt, one per CPU.
uint64 mscratch0[NCPU * 32];

// assembly code in kernelvec.S for machine-mode timer interrupt.
extern void timervec();

// entry.S jumps here in machine mode on stack0.
void
start()
{
  // set M Previous Privilege mode to Supervisor, for mret.
  unsigned long x = r_mstatus();
  x &= ~MSTATUS_MPP_MASK;
  x |= MSTATUS_MPP_S;
  w_mstatus(x);

  // set M Exception Program Counter to main, for mret.
  // requires gcc -mcmodel=medany
  w_mepc((uint64)main);

  // disable paging for now.
  w_satp(0);

  // delegate all interrupts and exceptions to supervisor mode.
  w_medeleg(0xffff);
  w_mideleg(0xffff);
  w_sie(r_sie() | SIE_SEIE | SIE_STIE | SIE_SSIE);

  // ask for clock interrupts.
  timerinit();

  // keep each CPU's hartid in its tp register, for cpuid().
  int id = r_mhartid();
  w_tp(id);

  // switch to supervisor mode and jump to main().
  asm volatile("mret");
}

// set up to receive timer interrupts in machine mode,
// which arrive at timervec in kernelvec.S,
// which turns them into software interrupts for
// devintr() in trap.c.
void
timerinit()
{
  // each CPU has a separate source of timer interrupts.
  int id = r_mhartid();

  // ask the CLINT for a timer interrupt.
  int interval = 1000000; // cycles; about 1/10th second in qemu.
  *(uint64*)CLINT_MTIMECMP(id) = *(uint64*)CLINT_MTIME + interval;

  // prepare information in scratch[] for timervec.
  // scratch[0..3] : space for timervec to save registers.
  // scratch[4] : address of CLINT MTIMECMP register.
  // scratch[5] : desired interval (in cycles) between timer interrupts.
  uint64 *scratch = &mscratch0[32 * id];
  scratch[4] = CLINT_MTIMECMP(id);
  scratch[5] = interval;
  w_mscratch((uint64)scratch);

  // set the machine-mode trap handler.
  w_mtvec((uint64)timervec);

  // enable machine-mode interrupts.
  w_mstatus(r_mstatus() | MSTATUS_MIE);

  // enable machine-mode timer interrupts.
  w_mie(r_mie() | MIE_MTIE);
}

```
## riscv.h代码

```c
// which hart (core) is this?
static inline uint64
r_mhartid()
{
  uint64 x;
  asm volatile("csrr %0, mhartid" : "=r" (x) );
  return x;
}

// Machine Status Register, mstatus

#define MSTATUS_MPP_MASK (3L << 11) // previous mode.
#define MSTATUS_MPP_M (3L << 11)
#define MSTATUS_MPP_S (1L << 11)
#define MSTATUS_MPP_U (0L << 11)
#define MSTATUS_MIE (1L << 3)    // machine-mode interrupt enable.

static inline uint64
r_mstatus()
{
  uint64 x;
  asm volatile("csrr %0, mstatus" : "=r" (x) );
  return x;
}

static inline void 
w_mstatus(uint64 x)
{
  asm volatile("csrw mstatus, %0" : : "r" (x));
}

// machine exception program counter, holds the
// instruction address to which a return from
// exception will go.
static inline void 
w_mepc(uint64 x)
{
  asm volatile("csrw mepc, %0" : : "r" (x));
}

// Supervisor Status Register, sstatus

#define SSTATUS_SPP (1L << 8)  // Previous mode, 1=Supervisor, 0=User
#define SSTATUS_SPIE (1L << 5) // Supervisor Previous Interrupt Enable
#define SSTATUS_UPIE (1L << 4) // User Previous Interrupt Enable
#define SSTATUS_SIE (1L << 1)  // Supervisor Interrupt Enable
#define SSTATUS_UIE (1L << 0)  // User Interrupt Enable

static inline uint64
r_sstatus()
{
  uint64 x;
  asm volatile("csrr %0, sstatus" : "=r" (x) );
  return x;
}

static inline void 
w_sstatus(uint64 x)
{
  asm volatile("csrw sstatus, %0" : : "r" (x));
}

// Supervisor Interrupt Pending
static inline uint64
r_sip()
{
  uint64 x;
  asm volatile("csrr %0, sip" : "=r" (x) );
  return x;
}

static inline void 
w_sip(uint64 x)
{
  asm volatile("csrw sip, %0" : : "r" (x));
}

// Supervisor Interrupt Enable
#define SIE_SEIE (1L << 9) // external
#define SIE_STIE (1L << 5) // timer
#define SIE_SSIE (1L << 1) // software
static inline uint64
r_sie()
{
  uint64 x;
  asm volatile("csrr %0, sie" : "=r" (x) );
  return x;
}

static inline void 
w_sie(uint64 x)
{
  asm volatile("csrw sie, %0" : : "r" (x));
}

// Machine-mode Interrupt Enable
#define MIE_MEIE (1L << 11) // external
#define MIE_MTIE (1L << 7)  // timer
#define MIE_MSIE (1L << 3)  // software
static inline uint64
r_mie()
{
  uint64 x;
  asm volatile("csrr %0, mie" : "=r" (x) );
  return x;
}

static inline void 
w_mie(uint64 x)
{
  asm volatile("csrw mie, %0" : : "r" (x));
}

// machine exception program counter, holds the
// instruction address to which a return from
// exception will go.
static inline void 
w_sepc(uint64 x)
{
  asm volatile("csrw sepc, %0" : : "r" (x));
}

static inline uint64
r_sepc()
{
  uint64 x;
  asm volatile("csrr %0, sepc" : "=r" (x) );
  return x;
}

// Machine Exception Delegation
static inline uint64
r_medeleg()
{
  uint64 x;
  asm volatile("csrr %0, medeleg" : "=r" (x) );
  return x;
}

static inline void 
w_medeleg(uint64 x)
{
  asm volatile("csrw medeleg, %0" : : "r" (x));
}

// Machine Interrupt Delegation
static inline uint64
r_mideleg()
{
  uint64 x;
  asm volatile("csrr %0, mideleg" : "=r" (x) );
  return x;
}

static inline void 
w_mideleg(uint64 x)
{
  asm volatile("csrw mideleg, %0" : : "r" (x));
}

// Supervisor Trap-Vector Base Address
// low two bits are mode.
static inline void 
w_stvec(uint64 x)
{
  asm volatile("csrw stvec, %0" : : "r" (x));
}

static inline uint64
r_stvec()
{
  uint64 x;
  asm volatile("csrr %0, stvec" : "=r" (x) );
  return x;
}

// Machine-mode interrupt vector
static inline void 
w_mtvec(uint64 x)
{
  asm volatile("csrw mtvec, %0" : : "r" (x));
}

// use riscv's sv39 page table scheme.
#define SATP_SV39 (8L << 60)

#define MAKE_SATP(pagetable) (SATP_SV39 | (((uint64)pagetable) >> 12))

// supervisor address translation and protection;
// holds the address of the page table.
static inline void 
w_satp(uint64 x)
{
  asm volatile("csrw satp, %0" : : "r" (x));
}

static inline uint64
r_satp()
{
  uint64 x;
  asm volatile("csrr %0, satp" : "=r" (x) );
  return x;
}

// Supervisor Scratch register, for early trap handler in trampoline.S.
static inline void 
w_sscratch(uint64 x)
{
  asm volatile("csrw sscratch, %0" : : "r" (x));
}

static inline void 
w_mscratch(uint64 x)
{
  asm volatile("csrw mscratch, %0" : : "r" (x));
}

// Supervisor Trap Cause
static inline uint64
r_scause()
{
  uint64 x;
  asm volatile("csrr %0, scause" : "=r" (x) );
  return x;
}

// Supervisor Trap Value
static inline uint64
r_stval()
{
  uint64 x;
  asm volatile("csrr %0, stval" : "=r" (x) );
  return x;
}

// Machine-mode Counter-Enable
static inline void 
w_mcounteren(uint64 x)
{
  asm volatile("csrw mcounteren, %0" : : "r" (x));
}

static inline uint64
r_mcounteren()
{
  uint64 x;
  asm volatile("csrr %0, mcounteren" : "=r" (x) );
  return x;
}

// machine-mode cycle counter
static inline uint64
r_time()
{
  uint64 x;
  asm volatile("csrr %0, time" : "=r" (x) );
  return x;
}

// enable device interrupts
static inline void
intr_on()
{
  w_sstatus(r_sstatus() | SSTATUS_SIE);
}

// disable device interrupts
static inline void
intr_off()
{
  w_sstatus(r_sstatus() & ~SSTATUS_SIE);
}

// are device interrupts enabled?
static inline int
intr_get()
{
  uint64 x = r_sstatus();
  return (x & SSTATUS_SIE) != 0;
}

static inline uint64
r_sp()
{
  uint64 x;
  asm volatile("mv %0, sp" : "=r" (x) );
  return x;
}

// read and write tp, the thread pointer, which holds
// this core's hartid (core number), the index into cpus[].
static inline uint64
r_tp()
{
  uint64 x;
  asm volatile("mv %0, tp" : "=r" (x) );
  return x;
}

static inline void 
w_tp(uint64 x)
{
  asm volatile("mv tp, %0" : : "r" (x));
}

static inline uint64
r_ra()
{
  uint64 x;
  asm volatile("mv %0, ra" : "=r" (x) );
  return x;
}

// flush the TLB.
static inline void
sfence_vma()
{
  // the zero, zero means flush all TLB entries.
  asm volatile("sfence.vma zero, zero");
}


#define PGSIZE 4096 // bytes per page
#define PGSHIFT 12  // bits of offset within a page

#define PGROUNDUP(sz)  (((sz)+PGSIZE-1) & ~(PGSIZE-1))
#define PGROUNDDOWN(a) (((a)) & ~(PGSIZE-1))

#define PTE_V (1L << 0) // valid
#define PTE_R (1L << 1)
#define PTE_W (1L << 2)
#define PTE_X (1L << 3)
#define PTE_U (1L << 4) // 1 -> user can access

// shift a physical address to the right place for a PTE.
#define PA2PTE(pa) ((((uint64)pa) >> 12) << 10)

#define PTE2PA(pte) (((pte) >> 10) << 12)

#define PTE_FLAGS(pte) ((pte) & 0x3FF)

// extract the three 9-bit page table indices from a virtual address.
#define PXMASK          0x1FF // 9 bits
#define PXSHIFT(level)  (PGSHIFT+(9*(level)))
#define PX(level, va) ((((uint64) (va)) >> PXSHIFT(level)) & PXMASK)

// one beyond the highest possible virtual address.
// MAXVA is actually one bit less than the max allowed by
// Sv39, to avoid having to sign-extend virtual addresses
// that have the high bit set.
#define MAXVA (1L << (9 + 9 + 9 + 12 - 1))

typedef uint64 pte_t;
typedef uint64 *pagetable_t; // 512 PTEs

```

