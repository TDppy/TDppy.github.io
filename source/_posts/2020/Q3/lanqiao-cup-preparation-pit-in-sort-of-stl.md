---
title: 【蓝桥杯备战】STL中sort的坑
date: 2020-07-23 09:00:15
categories: 
tags: []
layout: post
---

> 为备战蓝桥杯，我每天把刷题经验总结成博客，鞭策自己学习，争取暑假输出三十篇以上。

```cpp
vector<pair<int ,string>> vec;
sort(vec.begin(),vec.end(),greater<pair<int,string>>());
```
如上所示，vector中的元素是一个pair，sort利用greater进行排序，这里的排序规则是什么呢？
我们知道greater是大的在前小的在后，这里实际上是首先对int进行排序，**在int相同的情况下，还会对string进行降序排序**
**例题：**
[计蒜客T1152](https://nanti.jisuanke.com/t/T1152) 
这一题要求是根据成绩进行降序排序，输出学生的名字和成绩，由于成绩是降序排序，当我们用greater的时候成绩的确是降序排序，但是在成绩相同的情况下string也降序排序了，而一般默认名字我们应该按照升序排序——即字典序排序。
因此这题就要自定义cmp方法，不能轻易使用greater。

