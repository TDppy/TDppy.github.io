---
title: 【快乐PAT】PAT1002总结
date: 2026-01-11 15:30:00
categories: 快乐PAT
tags: [快乐PAT]
layout: post
---

@[TOC]

## [题目(链接点我)](https://pintia.cn/problem-sets/994805342720868352/problems/994805526272000000)
![在这里插入图片描述](/images/999364d99de2cd8bf65c06f906177fff.png)

## 代码和解析：
详细解析在下面AC代码的注释中已给出，主要的坑在于判断系数是否为0
```cpp
#include <iostream>
using namespace std;
//a[i][0]标记指数i是否使用过  a[i][1]是该指数对应的系数
double a[1005][2];
/**
 * PAT 1002
 * 给出多项式A和B的每项系数和指数，求A+B的每项系数和指数。
 * 输出时注意要和输入时一样，按照指数递减的顺序输出。
 * 
 * WARN：
 * 这题的坑在于，如A式中有2*x^3 ,B式中有-2*x^3，则A+B时x^3项也就不存在了。
 * 因此最后统计多少个不同项和输出时都要注意该项系数是否为0
 * 此外，题目中"Please be accurate to 1 decimal place"的含义是保留1位小数，用.1f
 *
 */
int main(){
	int k,ni,sum=0;
	double ani;
    for(int i=1;i<=2;i++){
		//每次输入k对指数和系数
	    cin>>k;
	    while(k--){
		  //输入指数和系数
		  cin>>ni>>ani;
		  //如果指数没用过
		  if(!a[ni][0]){
		     a[ni][0]=1;
		  }
		  //系数累加
		  a[ni][1]+=ani;
		}	
	}	
	//总计多少个不同项
	for(int i=1000;i>=0;i--){
	    //不为0说明该指数用过
		if(a[i][0]&&a[i][1]){
	   	  sum++;
		}
	}
    cout<<sum;	
    for(int i=1000;i>=0;i--){
	    //不为0说明该指数用过
		if(a[i][0]&&a[i][1]){
          //cout<<" "<<i<<" "<<a[i][1]; 
		  printf(" %d %.1f",i,a[i][1]);
		}
	}
    return 0;
}
```


## 英语积累：
polynomial 多项式
nonzero terms 非零项
exponent 指数
coefficient 系数
be accurate to 1 decimal place 保留1位小数
