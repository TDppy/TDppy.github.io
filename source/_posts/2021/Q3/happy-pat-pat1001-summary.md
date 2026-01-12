---
title: 【快乐PAT】PAT1001总结
date: 2021-07-05 11:43:47
categories: 
tags: []
layout: post
---

@[TOC]
## [题目(点我)](https://pintia.cn/problem-sets/994805342720868352/problems/994805528788582400)
<!-- ![在这里插入图片描述](/images/e80a263b90e8c1748a2affb287f762d8.png) -->
## 代码与解析
求a+b，难点在每三位用,分割 如1,001,500
详细题解写在下面AC代码注释中了，核心知识点是**利用%和/分割数值**和 **%03d不满3位自动补0**

```cpp
#include <iostream>
#include <cstring>
#include <cstdlib>
#include <cmath>
using namespace std;
/**
 *  PAT 1001
 *  a和b在+1,000,000和-1,000,000之间
 *  这意味着二者之和在-2,000,000到+2,000,000之间
 *  可以根据和的大小分段考虑：
 *  ·如果|sum|∈[0,1k)，无需逗号，直接输出
 *  ·如果|sum|∈[1k,100w)，就加个逗号，利用%和/分割数值。
 *  ·如果|sum|∈[100w,200w],加两个逗号，利用%和/分割数值。
 *
 *  WARN：以1050为例，如果输出1050/1000，1050%1000 则结果为1,50而不是1,050，
 *  因此要用%0md的格式在未满3位时自动在前面补0
 *
 */
int main(){
    int a,b;
	cin>>a>>b;
	int c=a+b;
    if(abs(c)>=1000000){
       //cout<<c/1000000<<","<<abs(c)%1000000/1000<<","<<abs(c)%1000;
	   printf("%d,%03d,%03d",c/1000000,abs(c)%1000000/1000,abs(c)%1000);
	}else if(abs(c)<1000){
	   cout<<c;
	}else{
	   printf("%d,%03d",c/1000,abs(c)%1000);
	}
    return 0;
}
```

## 英语积累
digit 数字

comma	英[ˈkɒmə] 逗号

 
