---
title: 【蓝桥杯备战】闻闻与砖（动态规划）
date: 2020-07-22 10:24:57
categories: 
tags: []
layout: post
---

> 为备战蓝桥杯，我每天把刷题经验总结成博客，鞭策自己学习，争取暑假输出三十篇以上。

本篇是一题动态规划的题目及题解。

## 题目链接
[题目链接](https://nytdoj.com/#/contest/3/problem/D)
 ![ ](./1.png) 
 ![ ](./2.png) 
 ![ ](./3.png) 


## 题解
 ![ ](./4.png) 
## 实现代码：
```cpp
#include <bits/stdc++.h>
using namespace std;
int res[1000005];
int temp[1000005];
int main(){
	int n;
	cin>>n;
	res[1]=1;
	res[2]=2;
	temp[2]=1;
	for(int i=3;i<=n;i++){
		res[i]=(res[i-1]+res[i-2]+2*temp[i-1])%10000;
		temp[i]=(res[i-2]+temp[i-1])%10000;
	}
	cout<<res[n];
	return 0;
} 
```

