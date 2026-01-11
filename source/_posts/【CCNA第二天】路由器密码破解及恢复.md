---
title: 【CCNA第二天】路由器密码破解及恢复
date: 2026-01-11 15:30:00
categories: 计算机网络
tags: [路由器, 思科, CCNA]
layout: post
---

@[TOC]
## 一、设备基本操作：
### 设备模式
1）用户模式以>开头
2）特权模式以#开头  在模式下可以进行复制操作，全局模式不行
3）全局模式以(config)开头 在全局模式下进行接口的配置，如加ip
不同模式权限不同，用户模式<特权模式<全局模式。

### 路由设备的基本命令
en ///enable 从用户模式进入特权模式
#conf  t  ///完整命令configure  terminal，进入全局
int  f0/0   ///进入接口
no sh //打开接口
ip  add  192.168.1.1  255.255.255.0 ///配置ip地址

**模式退出**：
exit  ///逐级退出，例如：全局——特权——用户
end  ///直接退出，只能到特权，无法进入用户。

模式与命令不匹配，导致设备进入DNS解析，现象
![在这里插入图片描述](/images/843f4d7abb64aa71d97b00c524f54e47.png)

> PS：特权模式下无法使用“end”命令，因此设备认为用户在此输入的是域名，所以会向全网发送DNS解析，设备会卡在DNS解析阶段，需要一段时间自动切换出来。
> 立刻终止DNS解析： Ctrl + shift +6（ctrl+shift同时按住，然后再按6）

**设备查看与保存：**
保存:
wr ///特权模式下保存  
do wr ///全局模式下保存 比如在配置了ip后要保存
查看：
1）show version///用户或特权模式下查看版本 简写sh ver
2）show running-config   ///查看正在运行的配置 sh run  没保存也能看到
3）show startup-config    ///查看设备保存的配置 sh star

**设备优化配置：**
1）ho  +名称  ///全称 hostname  +名称
2）banner motd STR 欢迎语 STR //更改欢迎语
PS：如果欢迎语中出现c，那么就把分隔符“c”换成其他没有出现的字母。分隔符是以什么开头就要以什么结尾。
![在这里插入图片描述](/images/5c58d1a24e91f2c1150544bd38a9f1bc.png)
从用户模式重新进入时：
![在这里插入图片描述](/images/96a662ea1f4abf05ca22abef4d6325f6.png)
3）  接口下软标签：
全局模式下：
 Int  f0/0
 des   +接口描述语句  ///软标签  
 ![在这里插入图片描述](/images/c819db29d14cb9b6ef25cec2227044ec.png)
 
 ## 二、网络设备：路由器基本组件
 RAM：random access memory随机存储器（PC：内存）
Flash：闪存（PC：系统盘）
NVRAM：non-violation random access memory非易失性随机存储器（PC：硬盘）
设备加电开机时，运行过程：
 ![在这里插入图片描述](/images/0f1c4bebff83348f94b7e966770fc58d.png)
 ## 三、 设备的登录方式与安全措施
 ### 登录方式：
 1.console登录，即用console线将路由器和电脑相连，用远程登录软件如SecureCRT进行登录。
 2.远程登录，如果路由器开启了远程登录，那么只需要使用telnet即可。
 ### 安全措施（三种密码）：
 
<font color="red">注意：三种密码均要在全局模式下进行设置</font>
 1. console登录密码的设置

```bash
 line console 0
 password 密码
 login
 do wr
```

 
 2. enable密码的设置
 

```bash
enable password 密码
```

 
 
 3. 远程登录密码的设置

```bash
 line vty 0 4
 password 密码
 login
 do wr
```
## 四、项目案例：路由器密码破解
### <font color="blue">命令简要汇总(详细见图)</font>
> 重启路由器 进入console，使用ctrl+c终端系统加载 
> confreg 0x2142 
> boot 
> en 
> copy
> startup-config running-config 
> show running-config 
> config 0x2102 
> do wr
> reload

### 图解详细步骤
![在这里插入图片描述](/images/a28b1eef7938ef501b36c914f89a022c.png)

 ![在这里插入图片描述](/images/0cee6abedbbe6741797a679783aa3bc4.png)
 ![在这里插入图片描述](/images/f615600d3eb3c84faadf1280d2f48452.png)
 ![在这里插入图片描述](/images/50507480354e7dca7536a4cbab7e9150.png)
 ![在这里插入图片描述](/images/c83035456f5cbfe0a51c4a200462ea74.png)
 ![在这里插入图片描述](/images/ae4977cc650726647f92a6f0f8e12657.png)
