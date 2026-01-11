---
title: 【异常处理】sbt构建Chisel库时出现extracting structure failed_build status_error的解决办法
date: 2026-01-11 15:30:00
categories: 异常处理
tags: [错误解决, 调试, Chisel]
layout: post
---
@[TOC]
# 报错背景：
最近在写Chisel时，构建项目常常需要等待很久，然后报错extracting structure failed:build status:error
这个报错实际上告诉我们，在build.sbt中**指定的依赖没有下载到**，导致依赖的结构无法实现。
![在这里插入图片描述](/images/0fb7ac24301b85a05f75cda273f9e241.png)

# 解决思路：
chisel库的资源是基于build.sbt配置文件给出的信息，使用sbt去maven网站上下载的，那么首先要确保sbt已经使用国内镜像源，以加快下载速度，其次根据报错信息，通过maven仓库网站查看缺少的文件，找到兼容的版本号，并修改build.sbt文件。
## ①IDEA中配置本地的SBT进行下载
打开IDEA的**File-Settings**，找到**sbt**，按照如图配置。
默认情况下Launcher是Bundle，即IDEA内置的SBT，默认从maven官方下载，我们将其指定为本地的sbt下bin目录中的sbt-launch.jar，并将VM parameters写入，方便后面更改为国内maven镜像站。

```bash
-Dsbt.override.build.repos=true
```

![在这里插入图片描述](/images/07d7ee342a15b61deaca5f3278a6cb95.png)
## ②更改下载源为华为的镜像站

### 1. 修改sbtconfig.txt
 在**安装的sbt目录\conf\sbtconfig.txt** 中写入

> -Dsbt.override.build.repos=true

为true表示sbt构建的仓库下载源将自定义。
![在这里插入图片描述](/images/452156f37bd5612bc839458b986e3600.png)


### 2. 增加repositories文件
 在当前用户目录\.sbt 下新建repositories文件，无需扩展名，并写入：
```bash
[repositories]
local
huaweicloud-maven: https://repo.huaweicloud.com/repository/maven/
maven-central: https://repo1.maven.org/maven2/
sbt-plugin-repo: https://repo.scala-sbt.org/scalasbt/sbt-plugin-releases, [organization]/[module]/(scala_[scalaVersion]/)(sbt_[sbtVersion]/)[revision]/[type]s/[artifact](-[classifier]).[ext]
```
![在这里插入图片描述](/images/28e0b63f5e43c61d216ef44fab9e16d3.png)

## ③查看报错信息

```bash
scalaVersion := "2.13.8"

scalacOptions ++= Seq(
  "-deprecation",
  "-feature",
  "-unchecked",
  "-Xfatal-warnings",
  "-language:reflectiveCalls",
)


libraryDependencies += "edu.berkeley.cs" %% "chiseltest" % "0.5.6"
val chiselVersion = "3.4.3"
libraryDependencies += "edu.berkeley.cs" %% "chisel3" % chiselVersion
```

![在这里插入图片描述](/images/ab2816c3ccb1e8008310369afe96d8f4.png)
查看红框中第三行报错信息，可以看到sbt在maven仓库中没有找到build.sbt指定的库

> **[error]   not found: https://repo1.maven.org/maven2/edu/berkeley/cs/chisel3_2.13/3.4.3/chisel3_2.13-3.4.3.pom**

我们通过浏览器查看有没有这个库，可以看到在**https://repo1.maven.org/maven2/edu/berkeley/cs/** 下有chisel3 2.11到2.13的库
点进chisel3 2.13中发现确实没有3.4.3
![在这里插入图片描述](/images/a54a99a23f960a9c096338118abc900e.png)
![在这里插入图片描述](/images/ab0cc26f439178b4f4acda38993a1b19.png)
返回，去看chisel3 2.11的目录 发现确实有3.4.3的chisel适配版本
![在这里插入图片描述](/images/bc497e8e9faa91b303db0007d15de436.png)
因此报错原因就找到了——build.sbt中指定的scala版本和chisel版本不匹配，如果想继续使用chisel 3.4.3版本，就应该更改build.sbt中scala版本为2.11系列，如果想继续使用2.13版本的scala，就必须更改chisel库版本为2.13库下的3.5.0到3.6.0系列。
可以下载的scala版本在https://repo.huaweicloud.com/repository/maven/org/scala-lang/scala-library/ 可以查看

# 总结
说了这么多，其实针对我的问题，最终解决办法就是把build.sbt中的scala版本更改为2.11系列即可，我修改成了2.11.9。
读者面对这个异常需要掌握这套方法，确保idea绑定了本地的sbt，并修改sbt的下载源，根据下载源的报错查找scala和chisel对应版本是否匹配，最终根据官方源中兼容的库去修改版本号。

这里给出我整理的Scala版本对应兼容的Chisel和Chiseltest版本信息：

> scala 2.11系列兼容的chisel版本为兼容的chisel版本3.0.0到3.4.4，chiseltest版本为0.2.0到0.3.4
> scala 2.12系列兼容的chisel版本为兼容的chisel版本3.0.0到3.6.0，chiseltest版本为0.2.0到0.6.1
> scala 2.13系列兼容的chisel版本为兼容的chisel版本3.5.0到3.6.0，chiseltest版本为0.5.0到0.6.2    5.0.0到5.0.2  以及6.0.0

具体的scala小版本信息，请查看[这里](https://repo.huaweicloud.com/repository/maven/org/scala-lang/scala-library/)
具体的chisel和chiseltest小版本信息请查看[这里](https://repo1.maven.org/maven2/edu/berkeley/cs/)

## 整理的Scala-Chisel-Chiseltest版本信息对应表
这里我整理出的对应表放入了网盘中，请自取：

> 链接：https://pan.baidu.com/s/1tk_mW7Z_RTwhFH_YLgUOsQ?pwd=z52s 
提取码：z52s 
--来自百度网盘超级会员V5的分享

