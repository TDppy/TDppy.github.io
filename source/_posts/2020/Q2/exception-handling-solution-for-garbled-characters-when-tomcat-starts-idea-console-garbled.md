---
title: 【异常处理】Tomcat启动时乱码、IDEA控制台乱码的解决方案
date: 2020-05-04 21:59:47
categories: 异常处理
tags: [错误解决, 调试]
layout: post
---

[本文的参考文章](https://www.cnblogs.com/wangjiming/p/11070246.html)
**对于Tomcat启动时乱码：**
如下图所示，Intellij IDEA显示中文为乱码。
 {% asset_img 1.png   %} -->

首先使用chcp查看控制台编码，如果显示936说明是GBK，65001则是UTF-8，再到tomcat-conf中的logging.properties文件中将编码更改为和控制台一致，我这里控制台是936，因此将文件的UTF-8全部改为GBK。
 {% asset_img 2.png   %} -->
 {% asset_img 3.png   %} -->
**对于IDEA控制台乱码**

```java
String a="我是乱码";
System.out.println(a);
```
如果这种代码会在控制台输出乱码，请尝试：
第一张图中设置为UTF-8
 {% asset_img 4.png   %} 
 {% asset_img 5.png   %} 
注意将第二张图中，设置为和你控制台一样的编码。
