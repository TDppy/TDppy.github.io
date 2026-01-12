---
title: 【java学习】面向对象知识点简要总结
date: 2020-05-13 11:28:04
categories: 编程与算法
tags: [面向对象, Java]
layout: post
---

**摒弃繁杂、提纲挈领==把握重点**
**类与对象**
人是类，张三是对象。

**构造方法：**

 1. 概念：在实例化对象时执行的方法。
 2. 如何定义：
    1.不写返回值类型
    2.方法体中没有return语句
    3.方法名和类名相同
 3. 特性：
    1.若不写构造方法，JVM自动加个空参空方法体的构造方法。写了构造方法则不会自动添加。
    2.实例化时会调用相应参数的构造方法。

**封装**

```java
private int age;
public void setAge(int age){this.age=age};
```
以private修饰属性，进而在类外只能通过setAge(3);这样的语句操作属性。

**继承**

```java
class Student extends People
```
使用extends关键字，这样Student就有了People类的属性和方法。

**多态**

```java
Animal a=new Cat();
a.sleep();//此时是猫睡觉
a=new Dog();
a.sleep();//同样是a.sleep() 变成了狗睡觉
```

**四个关键字**
*this*

```java
void setAge(int age){
this.age=age;
}
//this.age指的是类中的age
```
*static*
修饰变量时，被所有实例共享，可用类名.变量名来访问。
修饰方法时，不创建对象也可调用，可用类名.变量名来访问。
修饰代码块时，实例化对象时被执行。

*super*
子类通过super(参数列表)调用父类相应的构造方法

*final*
修饰变量时，只能被赋值一次。
修饰方法时，方法不能被子类重写。
修饰类时，类不能被继承，且变量只能被赋值一次，方法不能被子类重写。

**抽象类**
*抽象方法*：没有方法体的方法是抽象方法，须以abstract修饰。
*抽象类*：抽象类是abstract修饰的类。由于可能包含抽象方法，必须被继承后并覆盖其方法后才能实例化。

**接口**
如果类中所有方法均无方法体，以interface来修饰的类是接口。
*特性：*
接口中的方法默认是public abstract类型的，变量默认是public static final类型的，必须被继承并重写方法才可实例化。




