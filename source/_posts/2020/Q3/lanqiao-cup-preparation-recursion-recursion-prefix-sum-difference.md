---
title: 【蓝桥杯备战】递推、递归、前缀和、差分
date: 2020-07-16 21:15:35
categories: 
tags: []
layout: post
---

首先是递推，洛谷P1255 数楼梯。
阶梯思路如图：
 {% asset_img 1.png   %} 
但是由于该题N最大能到5000，显然，数值过大会爆掉long long，因此我们需要自己定义个数组自己模拟加法运算，被称为高精度运算。
这里先上代码，然后上模拟这个运算过程的图。

```cpp
#include <iostream>
#include <cstring>
#include <vector> 
#include <cstdio>
using namespace std;
//台阶最大数为5000，我们定义个5005
const int STEP_MAX=5005;
//定义一个二维数组作为表格。tab[n]表示上第n个台阶的方式数量
int tab[STEP_MAX][STEP_MAX];
//len表示当前方法数的位数
int len=1;
void jump(int k){
	//将前面两个台阶的方法数每位相加
	for(int i=1;i<=len;i++){
		tab[k][i]=tab[k-1][i]+tab[k-2][i];
	}
	//进位
	for(int i=1;i<=len;i++){
		if(tab[k][i]>=10){
			tab[k][i+1]+=tab[k][i]/10;
			tab[k][i]=tab[k][i]%10;
		}
		if(tab[k][len+1])len++;
	}
}
int main(){
	int n;
	cin>>n;
	tab[1][1]=1;
	tab[2][1]=2;
	for(int i=3;i<=n;i++){
		jump(i);
	}
	for(int i=len;i>=1;i--){
		cout<<tab[n][i];
	}
	return 0;
}
```
 {% asset_img 2.png   %} 
当求和后超过10时进位，将其十位给右面的元素，个位赋值给自己，进位的同时让len++，表示目前有2位数。
 {% asset_img 3.png   %} 

这题解决了，来看递归的题。
**计蒜客T2116 选数**
从n个数字中任选k个数字求和，和为素数的情况有多少种？
我的写法是递归，函数中不加入元素调用一次，加入元素调用一次，想想相当于一个指数级的递归，虽然AC了，总感觉哪里不得劲。

```cpp
#include <bits/stdc++.h>
using namespace std;
vector <int> chosen,all;
int n,k,cnt=0;
int sum=0;
int prime[20000005];
int countd=0; 
void cal(int x){
	countd++;
    if(x==n){
        if(chosen.size()!=k)return ;
		for(int i=0;i<k;i++)
            sum+=chosen[i];
        int flag=1;
        for(int i=2;i*i<=sum;i++){
        	if(sum%i==0)
        	flag=0;
        }
        if(flag){
        //cout<<sum<<" "<<cnt;
		cnt++;
		}
        sum=0;
        return;
    }
    cal(x+1);
    chosen.push_back(all[x]);
    cal(x+1);
    chosen.pop_back();
}
int main()
{

    cin>>n>>k;
    if(n==1||n==2){
		for(int t=1;t<=n;t++){
			int temp;
			cin>>temp;
    	    int flag=1;
		    for(int i=2;i*i<=temp;i++){
        	if(temp%i==0)
      	  	flag=0;
       	    }
        	if(flag)cnt++;
		}
		cout<<cnt;return 0;
    }
    for(int i=1;i<=n;i++){
    	int temp;
		cin>>temp;
    	all.push_back(temp);
    }
    cal(0);
    cout<<cnt;
    //cout<<"countd=="<<countd<<endl;
	return 0;
}
```
校队的标程是这样的：

```cpp
#include <bits/stdc++.h>
using namespace std;
int n,k,ans,a[30];
bool isprime(int sum){
    for(int i=2;i*i<=sum;i++){
        if(sum%i==0) return false;
    }
    return true;
}
void dfs(int m,int sum,int st){
//m表示选了多少个数
//sum表示当前的和
//st表示起始值 防止算重
    if(m==k){
        if(isprime(sum)) ans++;
        return;
    }
    for(int i=st;i<=n;i++)
        dfs(m+1,sum+a[i],i+1);
}
int main()
{
    cin>>n>>k;
    for(int i=1;i<=n;i++)cin>>a[i];
    dfs(0,0,1);
    cout<<ans;
	return 0;
}
```

