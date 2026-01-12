---
title: 【安装配置】Tomcat配置SSL证书步骤(含Element type “Connector“ must be followed by either attribute...的处理方案)
date: 2026-01-11 15:30:00
categories: 环境配置
tags: [Tomcat]
layout: post
---

@[TOC]

> 看完还有什么疑问，可以联系博主QQ1908269843，加的时候直接备注你遇到了什么情况。

想要网站以https://访问，需要将购买的SSL证书配置到Tomcat服务器中。
参考了几篇文章，花了几小时完成了。
<!-- ![在这里插入图片描述](/images/8dccd9f1df4d0deb42c578a63b16d3f9.png) -->
先列出参考文章，然后再给出步骤和我的心得：
1.[Tomcat配置SSL证书](https://www.cnblogs.com/cx-code/p/10059109.html)
2.Element type "Connector" must be followed by either attribute specifications
为了解决这个异常参考了以下两篇文章：http://blog.sina.com.cn/s/blog_5d2054d90102vt7y.html
https://blog.csdn.net/u014000377/article/details/50845920

步骤：
 ## 1. 先购买并下载证书，总结在这篇文章↓。
 [【安装配置】阿里云白嫖免费SSL证书步骤](https://blog.csdn.net/qq_42622433/article/details/114440868)
 ## 2. 使用java jdk将PFX格式证书转换为JKS格式证书

下载的证书文件，解压后是这个样子：只有两个文件的，一个是pfx格式的证书，一个是密码文本。
<!-- ![在这里插入图片描述](/images/3d2819c325ab10ca9df983745209b632.png) -->

在解压后的路径中输入cmd并回车，会进入该目录的命令行界面。
输入以下代码：

```lua
keytool -importkeystore -srckeystore 你的证书名称.pfx -destkeystore domains.jks -srcstoretype PKCS12 -deststoretype JKS
```
domains.jks是生成的jks格式证书名称，可以根据需要改。
回车，会提示你输入三次密码，建议三次都是输入密码文本的密码(复制以后邮件即可粘贴，在控制台不会显示，安心回车)，成功后会在文件夹下生成domains.jks文件

如果是Tomcat9，此时还没完，Tomcat 9强制要求证书别名设置为tomcat。您需要使用以下keytool命令将protocol="HTTP/1.1"转换成protocol="org.apache.coyote.http11.Http11NioProtocol"。

```bash
keytool -changealias -keystore domain name.jks -alias alias -destalias tomcat
```
<!-- ![在这里插入图片描述](/images/845aaabaec4ce0a084039a7b50139dc6.png) -->

## 3. 将jks文件上传到tomcat/conf目录中

这里每个人有自己的工具，不赘述。

## 4. 配置conf中的server.xml

<!--  找到：![在这里插入图片描述](/images/e101af99393bba4b0d9f9b4561b7d422.png) -->
修改成以下代码：（443为https默认访问端口）

```html
<Connector port="443" protocol="HTTP/1.1" SSLEnabled="true"
              maxThreads="150" scheme="https" secure="true"
              keystoreFile="conf/domains.jks"
              keystorePass="80ISkH7c"  //这里是刚刚设定的密码文本
              clientAuth="false" sslProtocol="TLS" />
```
### ↓标题中异常的解决办法↓ 
**①属性间没加空格②复制上面的Connector代码和文件的编码不匹配会报错都会报这个错
Catalina.start using conf/server.xml: Element type "Connector" must be followed by either attribute ！
解决办法是不复制，手敲进去，或者复制进去以后把空格全删掉再加上！**

<!-- 找到：![在这里插入图片描述](/images/063942ff9a50d607ecb570c10b0d63b6.png) -->
<!-- 改成：![在这里插入图片描述](/images/2a1ed3ccd8a926ec14449dd2439336d7.png) -->
找到：
<!-- ![在这里插入图片描述](/images/42cddaf5daf401942385bf2cb191e4dc.png) -->

改成：
<!-- ![在这里插入图片描述](/images/4d1e1e8752539076ed28cd3f4f0842d6.png) -->
保存，退出。
## 5.配置web.xml

编辑web.xml
在该文件</welcome-file-list>标签（一般在文件最末尾）后面加上这样一段：
```html
<login-config>  
    <!-- Authorization setting for SSL -->  
    <auth-method>CLIENT-CERT</auth-method>  
    <realm-name>Client Cert Users-only Area</realm-name>  
</login-config>  
<security-constraint>  
    <!-- Authorization setting for SSL -->  
    <web-resource-collection >  
        <web-resource-name >SSL</web-resource-name>  
        <url-pattern>/*</url-pattern>  
    </web-resource-collection>  
    <user-data-constraint>  
        <transport-guarantee>CONFIDENTIAL</transport-guarantee>  
    </user-data-constraint>  
</security-constraint>
```
<!-- ![在这里插入图片描述](/images/209ed707f4f408c2e65223bd05713251.png) -->
## 6.将443端口加入安全组入口
<!-- ![在这里插入图片描述](/images/edd5ca7de28c536b8979f413c02c12cb.png) -->
我是在阿里云买的服务器，所以到阿里云服务器的安全组改就行了，你在哪个厂商买的就到哪改。
有的可能不叫安全组，叫防火墙，总之把443开着，让用户能进去。

以上步骤都做完以后重启tomcat即可https访问。

> 如果你还有什么疑问，可以联系博主QQ1908269843，加的时候直接备注你遇到了什么情况。

## 7.完整server.xml文件拿去复制
### Server.xml
 1. 其中`keystorePass`要改成自己从阿里云下载的证书文件的密码(解压后一个是pfx证书文件，一个是密码的文件)
 2. 这个文件中使用的是8080端口
 
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Server port="8005" shutdown="SHUTDOWN">
  <Listener className="org.apache.catalina.startup.VersionLoggerListener" />

  <Listener className="org.apache.catalina.core.AprLifecycleListener" SSLEngine="on" />

  <Listener className="org.apache.catalina.core.JreMemoryLeakPreventionListener" />
  <Listener className="org.apache.catalina.mbeans.GlobalResourcesLifecycleListener" />
  <Listener className="org.apache.catalina.core.ThreadLocalLeakPreventionListener" />


  <GlobalNamingResources>

    <Resource name="UserDatabase" auth="Container"
              type="org.apache.catalina.UserDatabase"
              description="User database that can be updated and saved"
              factory="org.apache.catalina.users.MemoryUserDatabaseFactory"
              pathname="conf/tomcat-users.xml" />
  </GlobalNamingResources>


  <Service name="Catalina">


    <Connector port="8080" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="443" />

	<Connector port="443"
    protocol="HTTP/1.1"
    SSLEnabled="true"
    scheme="https"
    secure="true"
    keystoreFile="/webservice/tomcat/tomcat/apache-tomcat-9.0.44/cert/pycxs.jks" 
    keystorePass="改成自己的"   
    clientAuth="false"
    SSLProtocol="TLSv1+TLSv1.1+TLSv1.2"
    ciphers="TLS_RSA_WITH_AES_128_CBC_SHA,TLS_RSA_WITH_AES_256_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA,TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256,TLS_RSA_WITH_AES_128_CBC_SHA256,TLS_RSA_WITH_AES_256_CBC_SHA256"/>

    
    <Connector protocol="AJP/1.3"
               port="8009"
               redirectPort="443" />
    

    <Engine name="Catalina" defaultHost="localhost">

      <Realm className="org.apache.catalina.realm.LockOutRealm">

        <Realm className="org.apache.catalina.realm.UserDatabaseRealm"
               resourceName="UserDatabase"/>
      </Realm>

      <Host name="localhost"  appBase="webapps"
            unpackWARs="true" autoDeploy="true">

        <Valve className="org.apache.catalina.valves.AccessLogValve" directory="logs"
               prefix="localhost_access_log" suffix=".txt"
               pattern="%h %l %u %t &quot;%r&quot; %s %b" />

      </Host>
    </Engine>
  </Service>
</Server>

```

### web.xml

这文件太长了，没必要贴了，反正就是在welcome-file-list后边加点内容：
<!-- ![在这里插入图片描述](/images/a4bba554be7e9eece4cf27556306155d.png) -->


