---
title: 【你未必了解的Java注释知识】从__到文件模板、导出注释
date: 2020-07-26 12:06:50
categories: 编程与算法
tags: [Java, 注释]
layout: post
---

@[TOC]
## 注释
为了使代码便于理解，我们会在程序中加一些注释，java中的注释主要有三种：单行注释、多行注释、文档注释
### 单行注释
单行注释以//开头，一行中//后面的部分是注释部分，不会被编译，//前面的部分正常编译。
如下代码实现了输入一个整数，将其加1后输出。其中a=0被注释了，因此不会起作用。
```java
public class Example01 {
    public static void main(String[] args) {
        int a;
        Scanner in = new Scanner(System.in);
        a=in.nextInt();
        a=a+1;//a=0;
        System.out.println(a);
    }
}
```
### 多行注释
多行注释以`/*`开头，`*/`结尾
示例如下,代码实现输入整数a，输出整数a，其中注释掉了定义String类型的m并输入的两行代码，试想一下，这样的注释方法好吗？这个问题留到注释风格处解答。

```java
public class Example02 {
    public static void main(String[] args) {
        int a;
        Scanner in = new Scanner(System.in);
        a=in.nextInt();
        /*String m;
          in.next();*/
        System.out.println(a);
    }
}
```
### 文档注释
文档注释以`/**`开头`*/`结束，看似与多行注释类似，实际上还是有一定区别的。
实例代码中是一个实现输出九九乘法表的方法，我们在方法的上面使用 文档注释对代码的书写日期、功能、实现进行了注释。

```java
/**
 1.   日期：2020/7/26
 2.   功能：输出九九乘法表
 3.   实现：两重循环，外层循环保证输出9行，
 4.        内层循环中j<=i控制了每行输出的行数。
 */
public void printTable(){
    for(int i=1;i<=9;i++){
        for(int j=1;j<=i;j++){
            System.out.print(j+"*"+i+"="+j*i+" ");
        }
        System.out.println();
    }        
}
```
### 嵌套注释这个小问题
 1. `/* */`可以嵌套在`//外面`
 例如上面的Example01，已有注释`//a=0`，我们可以用`/**/`将其上下几行均注释。

```java
 public class Example01 {
    public static void main(String[] args) {
        /*
        int a;
        Scanner in = new Scanner(System.in);
        a=in.nextInt();
        a=a+1;//a=0;
        System.out.println(a);
        */
    }
}
```

 2. `/* */`不能嵌套在`/* */`外面
 以上面的Example02为例，显然，我们最上方的`/*`和`in.next()`后方的`*/`匹配了，导致`*/`后面的注释失效。
```java
public class Example02 {
    public static void main(String[] args) {
        /*
        int a;
        Scanner in = new Scanner(System.in);
        a=in.nextInt();
        /*String m;
          in.next();*/
        System.out.println(a);
        */
    }
}
```
## 注释进阶，你该知道的
### 规范化注释
前段时间红警开源吹来了一阵风，很多人借此追忆当年，不过我们不妨看一段它的代码

![在这里插入图片描述](/images/d3142e4003c2f2805b22558952c34eed.png)
我们自然看不懂它具体写的是什么逻辑，但依然可以看出注释比代码多、且十分整洁，整洁的原因是什么？
很容易发现，注释符号全部保证了**列对齐，且和下面的语句也对齐**，这样看起来注释就不会有突兀的感觉，起止的位置也十分清晰。
此外，如果根据注释的对象而言，我们可以分为几种：文档级注释、类级注释、方法级注释、行级注释，在写完代码后，我们可以按照这几级来查看是否有添加必要的注释。

### 自定义文件模板
在新建一个类时，多数IDE默认会为你生成类名、package包的代码，自定义文件模板就是设置在新建文件时自动生成的文件内容，方便我们快速开展工作。
![在这里插入图片描述](/images/996c7baeb729762d8302fbd7819adb8e.png)
如果我们想要在类创建时就自动为我们添加好上面2~7行的注释，应该怎么做？
这里介绍下IntelliJ IDEA中的做法，如果使用其他IDE的朋友自行搜索下。
![在这里插入图片描述](/images/c495b42191cb713b2466c16b331a7dc8.png)
![在这里插入图片描述](/images/86a7606927fc972fce7e57c0660ae014.png)
掌握了类模板的自定义方法，其他的文件的操作方法也是类似的，不再赘述了。
### javadoc导出注释
如果我们想把注释导出该怎么做？
例如下面这个程序

```java
 /*
 **    Title:Person类
 **    Date: 2020/7/26
 **    Time: 11:35
 **    Func:通过Person类说明文档注释
 **    @author:ZhangSan
 **    @version:1.0
 */
 public class Person {
    public String name;
    /**
     * 这是Person类的构造方法
     * @param name ZhangSan
     */
    public Person(String name) {
        //执行语句;
    }
     /*
     **这是read()方法的说明
     ** @param bookName 读的书的名字
     ** @param time 读书需要的时间
     ** @return 读书数量
     */
     public int read(String bookName,int time){
         //执行语句
         return 0;
     }
}
```
我们可以进入程序所在的目录，使用javadoc的命令来生成和注释相关的html文档，如图所示
![在这里插入图片描述](/images/1cbe769976d127d5a86e47e00e864d3f.png)
具体怎样操作？
由于不清楚看教程同学的基础，这里以最简单的方式来讲，如果有基础的同学相信能自行变通。

 **1.** 在桌面建立一个文件夹，命名为FILE
 **2.** 复制你的Person.java类到FILE文件夹中
<!--  **3.** 见图![在这里插入图片描述](/images/d468b19a728ae79dbf1353db282fbb68.png) -->
**4.**写好后回车，此时会进入当前目录的控制台，输入这样一条命令并回车：

```bash
javadoc -d . -version -author Person.java
```
<!-- ![在这里插入图片描述](/images/05b3cd27a83bd2682cb5efd67aedbc31.png) -->

**5.**此时FILE文件夹中会有一个index.html，以浏览器打开即可看到相关的注释！

<font color="skyblue">以上便是本文的全部内容了，希望能对读者有益！</font>
