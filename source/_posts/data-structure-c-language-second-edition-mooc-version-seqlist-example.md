---
title: 【数据结构（C语言）第二版慕课版】SeqList例程
date: 2026-01-11 15:30:00
categories: 
tags: []
layout: post
---

## 线性表的概念 ## 

> 线性表指的是元素在**逻辑上连续**的数据结构，具体地说，除了第一个和最后一个元素，每个元素都有一个前驱和一个后继元素。
> 
> 由于线性表只规定了逻辑上连续，在存储结构上没有限制，那么既可以用连续的内存进行实现，也可以用分散的内存实现。
> 采用连续内存实现的线性表是顺序表(Sequence List)，对应课本P11~14，采用分散内存实现的线性表是链表(Linked List)，对应课本P15~23。

这里给出【数据结构（C语言）第二版慕课版 人民邮电出版社】中P11~P14中关于SeqList的例程：

```cpp
/*
**Date:2020/06/04
**Author:Pan Ye cheng
**Title:SeqList
*/ 
#include <bits/stdc++.h>
using namespace std;
//宏定义一些返回值，方便以OK、ERROR进行返回 
#define ERROR 0
#define OK 1
#define Overflow 2
#define Underflow 3
#define NotPresent 4
#define Duplicate 5
//将int关键字取别名Status、ElemType
typedef int ElemType; 
typedef int Status;
//定义结构体seqList，并取别名SeqList 
typedef struct seqList{
	int n;
	int maxLength;
	ElemType *element;
}SeqList; 
//初始化函数
Status Init(SeqList *L,int mSize); 
//查询函数 
Status Find(SeqList L,int i,ElemType *x);
//插入函数 
Status Insert(SeqList *L,int i,ElemType x);
//删除函数 
Status Delete(SeqList *L,int i);
//输出函数 
Status Output(SeqList *L);
//摧毁函数 
void Destroy(SeqList *L);
int main()
{
	int i;
	SeqList list;
	Init(&list,10);
	for(i=0;i<10;i++)
		Insert(&list,i-1,i);
	Output(&list);
	Delete(&list,0);
	Output(&list);
	Destroy(&list);
	return 0;
}

Status Init(SeqList *L,int mSize)
{
 L->maxLength=mSize;//将mSize作为最大长度赋值给maxLength 
 L->n=0;            //n是顺序表的当前长度，初始化为0 
 L->element=(ElemType *)malloc(sizeof(ElemType)*mSize);//分配mSize个元素大小的内存，强转为ElemType类型 
 if(!L->element)//如果为空，返回ERROR 
   return ERROR;
 return OK;
}

//查询函数 
Status Find(SeqList L,int i,ElemType *x)
{
  if(i<0||i>L.n-1)
     return ERROR;
  *x=L.element[i];//顺序表是随机存取的，可以直接取对应下标的元素 
  return OK;
}

//插入函数 
Status Insert(SeqList *L,int i,ElemType x)
{
	int j;
	if(i<-1||i>L->n-1)
		return ERROR;
	if(L->n==L->maxLength)
		return ERROR;
	for(j=L->n-1;j>i;j--)
		L->element[j+1]=L->element[j];//插入和删除都通过移动后面的元素来实现。 
	L->element[i+1]=x;
	L->n=L->n+1;
	return OK;
}

//删除函数 
Status Delete(SeqList *L,int i)
{
	int j;
	if(i<0||i>L->n-1)
		return ERROR;
	if(!L->n)
		return ERROR;
	for(j=i+1;j<L->n;j++)
		L->element[j-1]=L->element[j];
	L->n--;
	return OK;
}

//输出函数 
Status Output(SeqList *L)
{
	int i;
	if(L->n==0)
		return ERROR;
	for(i=0;i<=L->n-1;i++)
		printf("%d ",L->element[i]);
	printf("\n");
	return OK;
}

//撤销函数 
void Destroy(SeqList *L)
{
	L->n=0;
	L->maxLength=0;
	free(L->element);
}
 
```

