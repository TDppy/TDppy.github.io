---
title: 【数据结构（C语言）第二版慕课版】SingleList例程
date: 2026-01-11 15:30:00
categories: 数据结构（C语言）第二版慕课版
tags: [数据结构（C语言）第二版慕课版]
layout: post
---


## 线性表的概念 ## 

> 线性表指的是元素在**逻辑上连续**的数据结构，具体地说，除了第一个和最后一个元素，每个元素都有一个前驱和一个后继元素。
> 
> 由于线性表只规定了逻辑上连续，在存储结构上没有限制，那么既可以用连续的内存进行实现，也可以用分散的内存实现。
> 采用连续内存实现的线性表是顺序表(Sequence List)，对应课本P11~14，采用分散内存实现的线性表是链表(Linked List)，对应课本P15~23。

这里给出【数据结构（C语言）第二版慕课版 人民邮电出版社】中P15~20中SingleList的例程：

```cpp
/*线性表的链式存储 
**Date:2020/06/06
**Author:Pan Ye cheng
**Title:SingleList
*/ 
**/
#include <bits/stdc++.h>
using namespace std;
#define ERROR 0
#define OK 1
#define Overflow 2
#define Underflow 3
#define NotPresent 4
#define Duplicate 5
typedef int ElemType;
typedef int Status;
//定义节点 
typedef struct node{
	ElemType element; //数据域 
	struct node *link;//指针域 
}Node;
typedef struct singleList{
	Node *first;
	int n;
}SingleList;
//初始化函数 
Status Init(SingleList *L);
//查询函数 
Status Find(SingleList L,int i,ElemType *x);
//插入函数 
Status Insert(SingleList *L,int i,ElemType x);
//删除函数 
Status Delete(SingleList *L,int i);
//输出函数 
Status Output(SingleList *L);
//摧毁函数 
void Destroy(SingleList *L);
int main(){
	int i;
	int x;
	SingleList list;
	Init(&list);
	for(i=0;i<9;i++){
		Insert(&list,i-1,i*10);
	}
	printf("the linklist is:");
	Output(&list);
	Delete(&list,0);
	printf("\nthe linklist is:");
	Output(&list);
	Find(list,0,&x);
	printf("\nthe value is:");
	printf("%d ",x);
	Destroy(&list);
	return 0;
}
Status Init(SingleList *L){
	L->first=NULL;
	L->n=0;
	return OK;
}
Status Find(SingleList L,int i,ElemType *x){
	Node *p;
	int j;
	if(i<0||i>L.n-1){
		return ERROR;
	}
	p=L.first;
	for(j=0;j<i;j++){
		p=p->link;
	}
	*x=p->element;
	return OK;
}
//i>=0时，插入元素x到下标为i的节点后面。如i为0，就是插入到第一个节点后边， 
//i<0时，x节点就是第一个结点。 
Status Insert(SingleList *L,int i,ElemType x){
	Node *p,*q;
	int j;
	if(i<-1||i>L->n-1)
	   return ERROR;
	p=L->first;
	for(j=0;j<i;j++) p=p->link;//p的值在循环结束后是下标为i的节点地址。 

	q=(Node *)malloc(sizeof(Node));//分配一个新节点q 
	q->element=x;//设置节点元素的值 
	if(i>=0){
		q->link=p->link;//让q节点指向p的下一个节点 
		p->link=q;//让p指向q 
	}else{
		q->link=L->first;
		L->first=q;
	}
	L->n++;
	return OK;
}
//函数功能：删除下标为i的结点。
//下标为i的结点，实际上是第i+1个结点，我们先把这个结点存储下来，让它的前一个结点指向它的后一个结点，再把这个结点释放掉即可。 
Status Delete(SingleList *L,int i){
	int j;
	Node *p,*q;
	if(!L->n)
		return ERROR;
	if(i<0||i>L->n-1)
		return ERROR;
	q=L->first;
	p=L->first;
	//循环结束后q是第i个元素的地址 
	for(j=0;j<i-1;j++)
		q=q->link;
	if(i==0)
		L->first=L->first->link;
	else{
		p=q->link;
		q->link=p->link;
	}
	free(p);
	L->n--;
	return OK;
} 
Status Output(SingleList *L){
	Node *p;
	if(!L->n)
		return ERROR;
	p=L->first;
	while(p){
		printf("%d ",p->element);
		p=p->link;
	}
	return OK;
}
void Destroy(SingleList *L){
	Node *p;
	while(L->first){
		p=L->first->link;
		free(L->first);
		L->first=p;
	}
}
 
```
**主要难点在插入函数和删除函数**
**插入函数：**
插入结点时，要先将插入结点指向下一个结点，再将前一个结点指向插入结点。原因是如果先指向插入结点，插入结点后面的结点地址就找不到了。（也就是避免“断链”）
**删除函数：**
删除结点时，要先把要删除的元素存储下来，目的是留作后面释放空间使用。
