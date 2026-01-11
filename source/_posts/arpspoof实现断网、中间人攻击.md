---
title: arpspoof实现断网、中间人攻击
date: 2026-01-11 15:30:00
categories: 
tags: []
layout: post
---

@[toc]
## 一、安装kali
安装完成kali后出现了一个问题，虚拟机界面只有光标闪烁，没有其他GUI界面。如下图所示
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/35f4129a659a2abb1ee42d2704b7002b.png)
解决方案：在下图中不要选择Enter device manually，而是选第二个/dev/sda就可以了。(我安装时是英文的，下图是网上找的。)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e6a4daa5eeb5756d0cb14e8cf05250ea.png)
配置桥接模式主要分为以下几步：                                             
1.获取宿主机网络配置信息                                             
2.修改VMware虚拟网络编辑器信息                                             
3.修改虚拟机网络配置信息  
这里先查看宿主机(就是虚拟机所在的主机)的网络相关信息，因为配置虚拟机桥接模式时需要与本机一致。 
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/edf4b765367c123323e0920d3a7556fe.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f913595c979cf1a50240c1f574eaf5ad.png)
然后修改VMware虚拟网络编辑器信息   
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/38b121736312484e3e3a7876ce6bd315.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ee7046d35c50d6ec9ca42662ccad0778.png)
再修改虚拟机网络配置信息
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/aae8a06ede12d59c14a02d39c9b6497d.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dfd451642288b44c72fb7b76d60cd3e2.png)

## 二、使用arpspoof
其实贼简单，核心的就一行命令，只不过要先做一些准备工作。
我要攻击我的主机，就先用ipconfig查询到本机ip
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/50f1ba38e692c1908c8fd7fec268918c.png)
然后再用ifconfig查询一下本地Kali虚拟机的ip和默认网关
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/e4e682fd645e80db43fabd3d383d40e6.png)
-后面的第一个是要攻击的ip，是我的主机ip，第二个是默认网关ip
arpspoof -i eth0 -t 192.168.168.141 192.168.168.1
执行一下就行了

/proc/sys/net/ipv4/ip_forward  这个文件中默认是0，0的时候实现的是断网攻击，1的时候实现的是中间人攻击(因为开启了ip分组的转发功能。)
