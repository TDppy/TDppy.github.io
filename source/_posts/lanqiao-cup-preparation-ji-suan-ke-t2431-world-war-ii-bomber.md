---
title: 【蓝桥杯备战】计蒜客T2431 二战轰炸机
date: 2026-01-11 15:30:00
categories: 
tags: []
layout: post
---

> 为备战蓝桥杯，我每天把刷题经验总结成博客，争取暑假输出三十篇以上。

今天是校队训练的第一天，热身赛中10题AC了八题，AB两题没有AC，A题是UVA10285，B题是计蒜客T2431。
A题还没有看，涉及到记忆化搜索，后面再补充，B题AC代码和解题思路如下，题面描述就不再贴了：

```cpp
//AC代码：
#include <iostream>
#include <cstring>
using namespace std;
const int MAXN=5005;
int map[MAXN][MAXN];
int main(){
	int N,R;
	cin>>N>>R;
	while(N--){
		int i,j,v;
		cin>>i>>j>>v;
		map[++i][++j]=v;
	}
	for(int i=1;i<=5000;i++){
		for(int j=1;j<=5000;j++){
			map[i][j]+=map[i-1][j]+map[i][j-1]-map[i-1][j-1];
		}
	}
	int res=0;
	for(int i=R;i<=5000;i++){
		for(int j=R;j<=5000;j++){
			res=max(res,map[i][j]-map[i-R][j]-map[i][j-R]+map[i-R][j-R]);
		}
	}
	cout<<res;
	return 0;
}
```

定义了map数组，map[i][j]存储的是从（0,0）到（i,j）这样一个矩形中的价值和，怎样实现的呢？这里我一开始其实也没搞明白，现在明白了，如果要写的话可能要画图，比较麻烦，本质是容斥原理，我建议是大家用几个数据模拟一下这个循环。


另外还有些小技巧总结如下：
1.数字转字符串
例如今天有一题是给定区间内求指定数字出现的次数，样例输入11，那么1~11中出现了几次1呢，4次。
当数字较小时可以采用**取10的余数、再除10**的办法获取到每位的数字来判断，考虑到数字较大时这样可能比较繁琐，于是我们可以用sprintf函数——
 `int sprintf(char *string, char *format [,argument,...]);`这个函数和printf很类似，只是最前面的参数是一个地址，一般些的是字符数组的首地址，这样的话我们用sprintf(a,"%d",110125552);就可以将110125552类似于这样长的数字输出到字符数组中，下面就可以转化为对字符串的操作了。
2.清空字符串
函数声明：`void *memset(void *s, int ch, size_t n);`
通常这样用：memset(a,0,1000);将数组a的前一千个变为0，可以对字符串操作，也可以对整型数组操作。
3.搞清楚横纵向变量
在dfs时常常会混淆横纵向变量，具体来说，定义的方向数组，dx、dy分别是横向还是纵向的，for循环中的i和j分别是横向还是纵向的，尽量一开始就要搞清楚。
4.max和min

```c++
 max(a,b); 
 min(a,b);
```
这两个函数在algorithm和iostream中都有定义，灵活使用，避免手写。

