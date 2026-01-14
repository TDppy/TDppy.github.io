---
title: 【安装配置】IDEA中配置Maven本地仓库后pom.xml飘红
date: 2021-03-06 21:02:36
categories: 环境配置
tags: [Java, IDEA]
layout: post
---

 {% asset_img 1.png   %} 
在IDEA中配置Maven后(如图)，pom.xml一片飘红，显然是依赖没了。
此时IDEA右下角冒出小窗口报错：
`Unable to import maven project: See logs for details`
叫我们看日志，那我们就看一下日志。
<!-- 点击help->Show log in Explorer{% asset_img 2.png 在这里插入图片描述 %} 
点了以后就会打开你的log所在的目录，然后我们点开`idea.log`
 {% asset_img 3.png   %} 

总之可以看出来本地仓库里没这个依赖了。这时候我在想为什么没有这个依赖，Maven不会自动下载呢？
 {% asset_img 4.png   %} 
这时候又看到这个拒绝访问，我就联想到是权限的问题。
于是把maven整个目录的权限都扩大了。
 {% asset_img 5.png   %} 
点应用 、确定。

结果就是不飘红了，能运行了。
**至于原理，我感觉就是Maven下载依赖肯定要有写入权限才能放到本地仓库，所以必须要把Maven目录给Users这个权限。**

> 如果你仍然不能运行，可以联系我QQ来帮你看看：
> QQ:2287015934

