---
title: 【蓝桥杯备战】位运算（快速幂）与STL（set、vector、全排列）
date: 2020-07-17 22:37:05
categories: 
tags: []
layout: post
---


> 为备战蓝桥杯，我每天把刷题经验总结成博客，鞭策自己学习，争取暑假输出三十篇以上。
> 
 {% asset_img 1.png   %} 
## 位运算与快速幂
位运算有左移、右移、同或、异或、与、或、取反，这里先写个应用，就是快速幂，后面有空再补充例题。
下面图片如果看不清可以右击新标签页打开。
 {% asset_img 2.png   %} 



## STL（set、vector、全排列）
 {% asset_img 3.png   %} 
STL有好多，把今天用到的写一下。
今天主要用到了set 、vector还有next_permutation(字符数组或string)

```cpp
//声明
set<string> a;
//插入
a.insert(var);
//遍历
for(set<string>::iterator it;it!=a.end();it++){cout<<*it;}
//查找是否有元素str,是则输出。
if(a.find(str)!=a.end())cout<<str;
```

set去重我之前知道，还有一个关键特性在今天做题中遇到的就是，把string放进去后会自动按照字典序排好，当做输入文章、按字典序输出不同单词时尤其好用。

//声明10086个值为6个数

```cpp
vector<int> a(10086,6);
a.push_back(var);//插入var
a.earse(i);//删除下标为i的元素
```


```cpp
char a[10];
next_permutation(a，a+n);
```

按照全排列的字典序，获取a的下一个排列，第一次获取到的是其本身。今天我用于判断集合中是否有某个单词在经过重新排列后再次出现。
如果是string，这样写：

```cpp
next_permutation(a.begin(),a.end());
```

如果直接写a,a+n，字符数组可以，string则会报错，估计原因是，对于string，重载参数是其迭代器。

## 实用的函数
此外，还遇到了一些其他实用的函数：

```cpp
swap(a,b);
//交换a和b
isalpha(a[i]);
//判断a[i]是否为字母
a[i]=tolower(a[i]);
//将其转化为小写字母 类似的还有toupper转化为大写字母
```

```cpp
string temp;
while(cin>>temp){
stringstream ss(temp);
//ss的精髓是将string获取到，再流出来时就去了空格
stirng a;
while(ss>>a)cout<<a;
}
```

