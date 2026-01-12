---
title: 【异常处理】Tomcat启动时乱码、IDEA控制台乱码的解决方案
date: 2026-01-11 15:30:00
categories: 异常处理
tags: [错误解决, 调试]
layout: post
---

[本文的参考文章](https://www.cnblogs.com/wangjiming/p/11070246.html)
**对于Tomcat启动时乱码：**
如下图所示，Intellij IDEA显示中文为乱码。
<!-- ![在这里插入图片描述](/images/66e1a97f3132f2c7d4b3f522a6f6ce0f.png#pic_center) -->

首先使用chcp查看控制台编码，如果显示936说明是GBK，65001则是UTF-8，再到tomcat-conf中的logging.properties文件中将编码更改为和控制台一致，我这里控制台是936，因此将文件的UTF-8全部改为GBK。
<!-- ![在这里插入图片描述](/images/8067cf3f14cf951cc04e76ab97642258.png#pic_center) -->
<!-- ![在这里插入图片描述](/images/fe314e749a099e466002f0f39dab650f.png#pic_center) -->
**对于IDEA控制台乱码**

```java
String a="我是乱码";
System.out.println(a);
```
如果这种代码会在控制台输出乱码，请尝试：
第一张图中设置为UTF-8
<!-- ![在这里插入图片描述](/images/80b49ec3d3b1c7016ead2c5b80f8601d.png) -->
<!-- ![在这里插入图片描述](/images/ab21ebc1bac05c61f4855ec02c33eb92.png) -->
注意将第二张图中，设置为和你控制台一样的编码。
