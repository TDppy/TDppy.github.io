---
title: 【JavaWeb】理解request.getParameter()的一些细节
date: 2026-01-11 15:30:00
categories: JavaWeb
tags: [JavaWeb]
layout: post
---

![在这里插入图片描述](./images/8c66efdad4c2e5c941594d0107c0c2be.png)
**先捋一下图中这个登录的逻辑**：
表单中的登录按钮的action属性绑定了一个servlet的路径，当点击登录时，可以看到网页的地址栏会跳转到一个servlet，后台程序执行了这个servlet的代码。
这个servlet中，我们可以用request.getParameter()；来获取表单中填写的用户名、密码、验证码，然后再进行查询数据库中是否有这个用户，如果有则登录成功，否则登录失败。

**然后是我们要谈的request.getParameter()**
1.当没有填写用户名时，我用request.getParameter("username");获取到了什么？
答案：是null吗？输出获取到的东西，发现什么也没有输出，实际上这是一个空字符串“”。
2.假设我们没有写表单，却用了request.getParameter()，获取到的是什么？
答案：输出一下，发现是null，当然，图中只有用户名密码和验证码，如果你写request.getParameter("age");获取年龄，自然也是null

**然后是我们要谈的张三（狗头）：**
张三去强奸，由于妹子过于暴力，未遂，客观上没成功，主观上有意愿，你不能说无罪吧？
同理，没写用户名，但只要这个字段存在，那还是获取到了，和良民百姓还是有区别的。

> 有无相生，难易相成——《道德经》

