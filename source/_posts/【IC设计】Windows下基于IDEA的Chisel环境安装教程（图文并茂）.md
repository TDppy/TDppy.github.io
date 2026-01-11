---
title: 【IC设计】Windows下基于IDEA的Chisel环境安装教程（图文并茂）
date: 2026-01-11 15:30:00
categories: 数字IC设计
tags: [Chisel]
layout: post
---
@[TOC](Chisel环境安装教程)

> 传统数字芯片的RTL设计采用Verilog语言为主，Chisel语言的全称是Constructing Harward in Scala Embeded Language，即在Scala语言中导入Chisel3库，即可使用Chisel语言。其特点是面向对象编程，可以方便地参数化定制硬件电路，加快设计流程。目前在RISC-V生态中应用较多，中科院计算所主持的培育下一代处理器设计人才的“[一生一芯](https://ysyx.oscc.cc/project/intro.html)”项目也在极力推进该语言。

涉及到的所有安装包已经放入百度网盘，请全部下载，然后开始阅读这个教程。

> 链接：https://pan.baidu.com/s/1ZOkbCxoLxrpJQQqVQfa-3w?pwd=hduv  
> 提取码：hduv 
> --来自百度网盘超级会员V5的分享

![在这里插入图片描述](/images/01b5241fda8a921150296753a4560517.png)

# 第一步 安装jdk，配置环境变量
如果电脑里还没有java环境，请先下载网盘链接中的jdk压缩包并解压，然后参照[我的这篇文章](https://blog.csdn.net/qq_42622433/article/details/103636986?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522170677616916800222847119%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=170677616916800222847119&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_ecpm_v1~rank_v31_ecpm-1-103636986-null-null.nonecase&utm_term=jdk&spm=1018.2226.3001.4450)配置环境。
# 第二步 安装sbt，不用配置环境变量
双击sbt-1.9.8.msi  下一步下一步安装就好了，环境变量会自动配置好，无需手动配置。
# 第三步 安装idea社区版
开发Chisel主要是基于Scala，我们这里只需要安装idea社区版即可，就是图中的ideaIC开头的压缩包，是免安装版，只需要解压即可。解压后进入bin目录，找到idea64并打开
![在这里插入图片描述](/images/58a14f8a7944b67cf96560327a95442c.png)
# 第四步 离线安装scala的idea插件
打开idea64后点击plugins-设置齿轮按钮-install plugin from disk
离线安装我们的scala插件，选中网盘中提供的scala-intellij-bin-2023.3.19即可。
![在这里插入图片描述](/images/8c0553c384454e44e5aa450b11e450b8.png)

# 第五步 配置sbt换源
## 1.切换目录
在第二步中我们已经装好了sbt，但sbt默认的下载源在国外，下载速度非常慢，我们需要进行换源。
首先，我们进入【C盘】-【用户】，找到【当前登录的用户】，这里我是panych，如图所示：
![在这里插入图片描述](/images/6d226aae463cfe5b3f6c02a31408ac8e.png)
## 2.创建repositories文件
创建目录【.sbt】并进入，然后创建文件【repositories】，无需扩展名，内容如下：
```xml
[repositories]
  local
  huaweicloud-ivy: https://repo.huaweicloud.com/repository/ivy/, [organization]/[module]/(scala[scalaVersion]/)(sbt[sbtVersion]/)[revision]/[type]s/artifact.[ext],allowInsecureProtocol
  huaweicloud-maven: https://repo.huaweicloud.com/repository/maven/,allowInsecureProtocol
```
## 3.配置sbtconfig.txt文件
在 **<sbt安装目录>/conf/sbtconfig.txt** 文件中添加如下内容：
```bash
-Dsbt.override.build.repos=true
```
![在这里插入图片描述](/images/52f59104e63842739aad9c204b6015ac.png)

# 第六步 使用chisel-tutorial工程运行AdderTests测试
## 1.打开chisel-tutorial项目
解压网盘中给出的chisel-tutorial工程，然后使用idea选中chisel-tutorial下的build.sbt打开。

## 2.配置项目的sbt和scala
在【File】-【Settings】中找到sbt并配置为本地sbt中的**sbt-launch.jar**，按照图中进行配置，然后点【OK】
![在这里插入图片描述](/images/d2a8cf40e601a6ac0f06c8f3b7bdb25c.png)
在【File】-【Project Structure】中选择【Global Libraries】，点击【+】，添加【Scala SDK】，
选择网盘中给出的Scala解压后的目录即可。
![在这里插入图片描述](/images/dda9811ebcfec5069d1ed6ccae7a6809.png)

## 3.测试AdderTests.scala
打开AdderTests.scala，点击17行左侧的运行按钮，【Run 'AdderTests'】，得到测试通过的提示就ok了。
![在这里插入图片描述](/images/315194c2942024c308edb01b74843c44.png)
![在这里插入图片描述](/images/048308749d76ba465f6ca7cf25fd4d10.png)


## failed to create lock file 解决办法
如果遇到报错：【failed to create lock file】，请需要前往对应目录赋权，如图所示：
![在这里插入图片描述](/images/c4021ae19741a7ac00e3daeccae62b5e.png)

# 参考资料
1.[华为开源镜像站-SBT](https://mirrors.huaweicloud.com/mirrorDetail/5ebf85de07b41baf6d0882ac)
2.[中科院计算所一生一芯人才培养项目](https://ysyx.oscc.cc/project/intro.html)
