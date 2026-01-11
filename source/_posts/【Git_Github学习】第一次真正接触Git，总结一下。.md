---
title: 【Git_Github学习】第一次真正接触Git，总结一下。
date: 2026-01-11 15:30:00
categories: 编程与算法
tags: [GitHub, Git]
layout: post
---

## ==声明：==
这不是一篇十分完整的Git入门教程，只能算是博主入门的经验总结。
[参考文章](https://blog.csdn.net/qq_37512323/article/details/80693445?utm_medium=distribute.pc_relevant.none-task-blog-baidujs-3)

## 学习Git的必要性： 
1.Github上有很多资源
就凭Github上聚集的大量大神以及它的海量代码资源，也值得我们去认真学习一下这个网站以及Git这个工具。
[Git下载地址](https://git-scm.com/download)

2.版本控制
比如周一写好了登录功能，上传一下，周五项目卡壳了，想看一下周一的代码怎么写的，直接去下载下来看就好了。比本地备份要方便，这就是它的强大之处，可以方便的查看先前版本的代码。

怎样通过Git来上传你的代码？
1.获取密钥

```bash
ssh-keygen-t rsa-C "your_email@youremail.com"
```
这里会让你写下密码什么的如果你写了就要记得

2.将密钥保存到Github上
在右上角头像的setting中有ssh and GPG keys，进入以后new 一个sshkey，将你刚刚获取的密钥粘贴进去

3.查看是否绑定

```bash
ssh -T git@github.com
```
如果显示↓这些东西，说明你之前在获取密钥时设定了密码，输入一下回车就行。

```bash
Enter passphrase for key '/c/Users/Administrator/.ssh/id_rsa
```

4.克隆仓库并上传代码

```bash
 1. ssh -T git@github.com 输入密码并回车
 2. git clone 仓库地址
 3. cd 你克隆到本地的文件夹
 4. 将你写好的项目复制到这个文件夹
 5. git add 你的项目
 6. git commit -m "本次提交到仓库的备注"
 7. git push origin master
 8. 在窗口中输入用户名和密码，点login
 9. 提交成功。可以到仓库中复查一下。
```

 
