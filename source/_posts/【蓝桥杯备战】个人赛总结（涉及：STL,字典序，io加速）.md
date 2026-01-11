---
title: 【蓝桥杯备战】个人赛总结（涉及：STL,字典序，io加速）
date: 2026-01-11 15:30:00
categories: 蓝桥杯备战
tags: [蓝桥杯备战]
layout: post
---

> 为备战蓝桥杯，我将每天的学习总结为博客，鞭策自己学习，争取暑期输出三十篇以上博客。

@[TOC]
## 战况总结
昨天是个人赛，战况大概是这样。![在这里插入图片描述](/images/0286d5783f004d598f68736c4225ff53.png)
本来出题人说今天会很友好，实际做起来感觉还是有一些值得学习的地方的。
A题就是直接输出a+b，B题有个多组输入和每组之间的换行需要注意。
C题有两个坑，一个是数据范围，另一个是隐藏的字典序要求。
D题是差分序列。
E题是模拟题。
F题位运算，还不会。
主要提一下C题。
先上一下题面：

Now give you serveral pairs of integers ,your task is to sort this pairs by the first keyword！  
输入 Give you serveral pairs of integers a and b untile the end of file.-2^31<a< 2^31  
Each pair on a single line,and the total num of pairs is no more than 10.-10^21<b< 10^21 
输出 Print all the pairs as the format of input after sort.

```c
标准输入
2 35
3 45
1 111
-1 50
标准输出
-1 50
1 111
2 35
3 45
```
题目其实就一句话，根据前面的数字大小进行排序，输出后面的，通过样例很容易看出来。这里有第一个小坑，后面的数字比较大，要用字符串来处理。
看完题目我就想着用结构体变量存储每组输入的数据，最后sort一下结构体数组，完美解决。
但事实是我交了7个WA。。
这里的第二个坑在于，当前面的int数据相等时，输出的顺序应当按照字典序，而我只按照前面数值进行了排序。

## 字典序到底是什么顺序？
我研究了一下，遵循以下几个原则：
1.按位进行比较ASCII码，如果相同，比较下一位，如果不同，哪个ASCII码小就排在前面。
例如：
“abc”与"abb" 由于abb的第三位是b，ascii比c小，所以abb排在前面。
2.每位ascii都相同，长度短的在前面，
例如：
“abb”与“abbcda”，abb在前面
3.每位ascii都相同且长度相同
这个就是完全相同了，没什么先后之说。
 
 ## io加速

```cpp
ios::sync_with_stdio(0);
```
在主函数第一句加上这个，cin和cout的读写速度会接近与scanf printf。

## STL
我发现，我虽然知道大概有哪些函数，但是在实战中都想不起来用他们，其实还是做题少了。
例如我们需要动态地获取vector的最后一个元素，我一开始想到的是用int来动态更新下有元素的最后一个下标，其实用size()-1就可以了。。

## 代码风格的思考

```cpp
if(flag)
cout<<cnt<<endl;
```
为了省事，如果if判断后是一行代码，常常不加括号。但事实上我发现，有时候后面你又需要在if里多写几条的时候，还得加上去——不加只执行第一条呀。
另外，有时候只有一条语句，可能还会这么写

```cpp
if(flag) cout<<cnt<<endl;
```
昨天就这么写了然后后面由于思路变了，又加了几条语句，忘了加括号。
因此以后只要是if语句，就不要横着写，并且即使只有一条，也要加上花括号。
