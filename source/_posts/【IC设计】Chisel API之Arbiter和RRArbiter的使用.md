---
title: 【IC设计】Chisel API之Arbiter和RRArbiter的使用
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计]
layout: post
---
---
title: 【IC设计】Chisel API之Arbiter和RRArbiter的使用
date: 2026-01-11 15:30:00
categories: IC设计
tags: [IC设计, Chisel, Arbiter, RRArbiter]
layout: post
---

@[TOC]
## 介绍
仲裁器在NoC路由器中是重要的组成部分，虚通道仲裁和交叉开关仲裁都需要使用仲裁器。
Chisel提供了Arbiter和RRArbiter仲裁器
Arbiter是基础的低位优先仲裁器，
RRArbiter初始情况下也是低位优先仲裁（也可以配置成高位优先），但在某个通道仲裁胜出后，下一次仲裁会从获胜通道的下一个通道开始轮询，如果检测到有请求就授权。
**举例：**
假设有3个通道的请求，wire [2:0] req。
第一轮仲裁，初始情况下0优先级最高，1其次，2最低。假设1和2同时请求资源，0没有请求，那么根据低位优先的原则，
通道1获胜。
第二轮仲裁，仲裁器会记住上次获胜的通道1，然后下一次0和2同时请求资源，我们需要从通道1的下一个通道进行轮询，那么通道0获胜。
第三轮仲裁，仲裁器会记住上次获胜的通道0，然后从通道2开始轮询...

## Chisel的Valid和Ready流控
Ready-Valid接口是一种简单的控制流接口，包含：
 1. data：发送端向接收端发送的数据；
 2. valid：发送端到接收端的信号，用于指示发送端是否准备好发送数据；
 3. ready：接收端到发送端的信号，用于指示接收端是否准备好接收数据；
![在这里插入图片描述](/images/66cf202e8fbd4feb36fea047b5b5f92c.png)
发送端在data准备好之后就会设置valid信号，接收端在准备好接收一个字的数据的时候就会设置ready信号。数据的传输会在两个信号，valid信号和ready信号，都被设置时才会进行。**如果两个信号有任何一个没被设置，那就不会进行数据传输。**
**[更详细的内容参考该博客](https://blog.csdn.net/weixin_43681766/article/details/126112310)**

在对RRArbiter进行测试过程中，由于仲裁器是接收数据的设备，因此valid和data是输入信号，ready是接收信号，需要对valid和data信号设置激励，并查看输出端获胜的数据。

## build.sbt 
程序的build.sbt配置如下：
```bash
ThisBuild / scalaVersion     := "2.13.8"
ThisBuild / version          := "0.1.0"
ThisBuild / organization     := "BATHTUB"

val chiselVersion = "3.6.0"

lazy val root = (project in file("."))
  .settings(
    name := "noc-router-main",
    libraryDependencies ++= Seq(
      "edu.berkeley.cs" %% "chisel3" % chiselVersion,
      "edu.berkeley.cs" %% "chiseltest" % "0.6.0" % "test",
      //包含ChiselTest会自动包含对应版本的ScalaTest
      //导入scalatest的库
      //"org.scalatest" %% "scalatest" % "3.1.4" % "test"
    ),
    scalacOptions ++= Seq(
      "-language:reflectiveCalls",
      "-deprecation",
      "-feature",
      "-Xcheckinit",
      "-P:chiselplugin:genBundleElements",
    ),
    addCompilerPlugin("edu.berkeley.cs" % "chisel3-plugin" % chiselVersion cross CrossVersion.full),
  )
```

## RRArbiter代码示例
以下代码可以直接运行，并给出了详细注释。
输出结果：
![在这里插入图片描述](/images/18970815a68ee3cd8b74fca5fe7c4c4f.png)

```scala
//3个输入的RRArbiter官方API测试
//依次测试001~111请求下的输出数据
//初始情况下默认低位优先，在每次仲裁后，将仲裁胜利的通道置为优先级最低，进行下次仲裁
class OfficialRRArbTest extends AnyFreeSpec with ChiselScalatestTester{
  "OfficialRRArbiter should pass" in {
    test(new RRArbiter(UInt(8.W), 3)).withAnnotations(Seq(WriteVcdAnnotation)) { c =>
      //第一次测试 此时从高到低优先级为0 1 2 通道0发起请求
      c.io.in(0).valid.poke(true.B)
      c.io.in(1).valid.poke(false.B)
      c.io.in(2).valid.poke(false.B)

      //假设在全部测试中通道0的数据为0 通道1的数据为1 通道2的数据为2
      c.io.in(0).bits.poke(0)
      c.io.in(1).bits.poke(1)
      c.io.in(2).bits.poke(2)
      c.io.out.ready.poke(true.B)
      c.clock.step(2)
      //初始状态下接收端已准备好接受in(0),in(1),in(2)  因此ready均为1
      //println(s"${c.io.in(0).ready.peek().litValue},${c.io.in(1).ready.peek().litValue},${c.io.in(2).ready.peek().litValue}")
      //通道0获胜，输出0
      println(s"1\t out.valid=${c.io.out.valid.peek().litValue}, out.bits=${c.io.out.bits.peek().litValue}\n")

      //第二次测试  此时优先级从高到低为1 2 0 通道1发起请求
      c.io.in(0).valid.poke(false.B)
      c.io.in(1).valid.poke(true.B)
      c.io.in(2).valid.poke(false.B)
      c.clock.step(2)
      //通道1获胜，输出1
      println(s"2\t out.valid=${c.io.out.valid.peek().litValue}, out.bits=${c.io.out.bits.peek().litValue}\n")

      //第三次测试  此时优先级从高到低为2 0 1 通道0和1发起请求
      c.io.in(0).valid.poke(true.B)
      c.io.in(1).valid.poke(true.B)
      c.io.in(2).valid.poke(false.B)
      c.clock.step(2)
      //通道0获胜，输出0
      println(s"3\t out.valid=${c.io.out.valid.peek().litValue}, out.bits=${c.io.out.bits.peek().litValue}\n")

      //第四次测试  此时优先级从高到低为2 1 0 通道2发起请求
      c.io.in(0).valid.poke(false.B)
      c.io.in(1).valid.poke(false.B)
      c.io.in(2).valid.poke(true.B)
      c.clock.step(2)
      //通道2获胜，输出2
      println(s"4\t out.valid=${c.io.out.valid.peek().litValue}, out.bits=${c.io.out.bits.peek().litValue}\n")

      //第五次测试  此时优先级从高到低为1 0 2 通道0和2发起请求
      c.io.in(0).valid.poke(true.B)
      c.io.in(1).valid.poke(false.B)
      c.io.in(2).valid.poke(true.B)
      c.clock.step(2)
      //通道0获胜，输出0
      println(s"5\t out.valid=${c.io.out.valid.peek().litValue}, out.bits=${c.io.out.bits.peek().litValue}\n")

      //第六次测试 此时优先级从高到低为1 2 0 通道1和2发起请求
      c.io.in(0).valid.poke(false.B)
      c.io.in(1).valid.poke(true.B)
      c.io.in(2).valid.poke(true.B)
      c.clock.step(2)
      //通道1获胜，输出1
      println(s"6\t out.valid=${c.io.out.valid.peek().litValue}, out.bits=${c.io.out.bits.peek().litValue}\n")

      //第七次测试 此时优先级从高到低为2 0 1 通道2、0、1发起请求
      c.io.in(0).valid.poke(true.B)
      c.io.in(1).valid.poke(true.B)
      c.io.in(2).valid.poke(true.B)
      c.clock.step(2)
      //通道2获胜，输出2
      println(s"7\t out.valid=${c.io.out.valid.peek().litValue}, out.bits=${c.io.out.bits.peek().litValue}\n")
    }
  }
}
```


