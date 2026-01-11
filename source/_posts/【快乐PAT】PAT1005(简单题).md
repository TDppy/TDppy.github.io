---
title: 【快乐PAT】PAT1005(简单题)
date: 2026-01-11 15:30:00
categories: 快乐PAT
tags: [快乐PAT]
layout: post
---

@[TOC]
## 题目描述
[原题链接点我](https://pintia.cn/problem-sets/994805342720868352/problems/994805519074574336)

![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d163836def2b3d066d3a06bddc67f599.png)
## 题解与代码
将输入的数字串每个数字求个累加和，然后将累加和的每个数字以英文单词的形式输出。
涉及知识点：**字符-48为数字** 和 **sprintf**   这两个是我用到的主要知识点，也可能有别的做法不用sprintf。
**AC代码：**

```cpp
#include <iostream>
#include <cstring>
using namespace std;
int sum;
int calcForSum(char *s){
	int slen=strlen(s);
	for(int i=0;i<slen;i++){
		sum+=*(s+i)-48;
	}
	return sum; 
}
void output(char *arr){
	int len=strlen(arr);
	for(int i=0;i<len;i++){
		if(i>0){
			cout<<" ";
		}	
		switch(*(arr+i)-48){
			case 0:cout<<"zero";continue;
			case 1:cout<<"one";continue;
			case 2:cout<<"two";continue;
			case 3:cout<<"three";continue;
			case 4:cout<<"four";continue;
			case 5:cout<<"five";continue;
			case 6:cout<<"six";continue;
			case 7:cout<<"seven";continue;
			case 8:cout<<"eight";continue;
			case 9:cout<<"nine";continue;
		}
	}
}
int main(){
	//定义输入的字符串
	char inStr[105];
	scanf("%s",inStr);
	//根据输入字符串计算其每个数字的累加和,放入sum中
	calcForSum(inStr);
	char arr[100];
	//将sum放入arr字符数组中
	sprintf(arr,"%d",sum);
	//调用函数output对字符数组中的每个数值进行输出
	output(arr);
	return 0;
}
```

