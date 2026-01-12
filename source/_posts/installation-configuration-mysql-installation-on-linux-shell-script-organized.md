---
title: 【安装配置】linux下mysql安装 (已整理好shell脚本)
date: 2020-04-14 21:05:19
categories: 环境配置
tags: []
layout: post
---

> ## 教程声明：博主在阿里云CentOS7.3裸机上按照该步骤安装成功。
> 原文参考了[牛客网mysql教程](https://www.nowcoder.com/tutorial/10006/5ca9a6e6d7664ea7b0aa48293147a5d7)，但牛客网的教程，经我测试是有坑的，大家先按照我的做一遍，如果不成功，再参考其他教程。
> 如果不想看过程的可以直接复制粘贴我整理好的shell脚本👉[链接戳这](https://pasteme.cn/64273)👈


## **Linux/UNIX 上安装 MySQL**
安装前，先检测系统是否自带安装 MySQL:

```bash
rpm -qa | grep mysql 
#rpm -qa查看所有安装过的包，| grep mysql在这些包装找出含有“mysql”的。
```

系统已经安装，先卸载掉:

```bash
rpm -e mysql　　
# 普通删除模式
rpm -e --nodeps mysql　　
# 强力删除模式，如果使用上面命令删除时，提示有依赖的其它文件，则用该命令可以对其进行强力删除
```


**安装mysql**
依次执行下列命令，前两个瞬间执行好，第三个和第四个需要确认的时候输入`y`，然后回车。
```bash
wget http://repo.mysql.com/mysql-community-release-el7-5.noarch.rpm #wget命令用来上指定的url下载rpm软件包
rpm -ivh mysql-community-release-el7-5.noarch.rpm #rpm命令安装指定的软件包
yum update #更新升级所有包
yum install mysql-server #安装mysql-server 
```

**注意**
如果执行*yum update* 出现*Errors during downloading metadata for repository 'AppStream'*，问题是centos8下yum需要换源，

```bash
cd /etc/yum.repos.d/
rm -rf *
wget -O /etc/yum.repos.d/CentOS-Base.repo https://mirrors.aliyun.com/repo/Centos-vault-8.5.2111.repo
sed -i 's/mirrors.cloud.aliyuncs.com/url_tmp/g' /etc/yum.repos.d/CentOS-Base.repo && sed -i 's/mirrors.aliyun.com/mirrors.cloud.aliyuncs.com/g' /etc/yum.repos.d/CentOS-Base.repo && sed -i 's/url_tmp/mirrors.aliyun.com/g' /etc/yum.repos.d/CentOS-Base.repo
yum clean all && yum makecache
```




**权限设置：**

```bash
chown mysql:mysql -R /var/lib/mysql
```


**启动 MySQL：**

```bash
systemctl start mysqld
```

**查看 MySQL 运行状态：**


```bash
systemctl status mysqld
```

使用 mysqladmin 命令来检查服务器的版本, 在 linux 上该二进制文件位于 /usr/bin 目录，在 Windows 上该二进制文件位于C:\mysql\bin 。

```bash
[root@host]# mysqladmin --version
```

linux上该命令将输出以下结果，该结果基于你的系统信息：

```bash
mysqladmin  Ver 8.23 Distrib 5.0.9-0, for redhat-linux-gnu on i386
```

如果以上命令执行后未输出任何信息，说明你的Mysql未安装成功。

安装成功后使用`mysql -u root -p` 回车，不用输入密码再回车即可进入mysql命令行。
此外，如果要让你的mysql可以被任意ip连接，
输入以下命令：

```bash
mysql -u root -p密码
use mysql;
grant all privileges on *.* to root@'%'  identified by '你想要设定的连接密码' WITH GRANT OPTION;
flush privileges; 
```


