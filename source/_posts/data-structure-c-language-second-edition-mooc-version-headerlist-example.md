---
title: 【数据结构（C语言）第二版慕课版】HeaderList例程
date: 2020-06-07 11:20:52
categories: 
tags: []
layout: post
---

这里给出【数据结构（C语言）第二版慕课版 人民邮电出版社】中P20~23中HeaderList的例程
```cpp
/**
 *date:2020/06/07
 *auther:Pan Ye cheng
 *title:HeaderList(带表头结点的单链表)
 */
#include <stdio.h>
#include <malloc.h> 
typedef int ElemType;
typedef struct node
{
	ElemType element;
	struct node *link;
}Node;
typedef struct headerList
{
	Node *head;
	int n;
}HeaderList;
//初始化函数 
void Init(HeaderList *h);
//查询函数：返回下标为i的结点元素值 
ElemType Find(HeaderList *h, int i);
//插入函数:在下标为i的结点后插入x结点  实现思路：p初值为表头结点的地址，循环i+1次后p为下标为i的结点，再让q牵手即可。 
void Insert(HeaderList *h, int i,ElemType x);
//删除函数：删除下标为i的结点 实现思路：q初值为表头结点的地址，循环i次后为下标i-1的结点，记录下待删除结点p，让q牵手，p释放即可。 
void Delete(HeaderList *h, int i);
void Output(HeaderList *h);
void Destory(HeaderList *h);
int main()
{
	int i;
	int x;
	HeaderList list;
	Init(&list);
	for(i=0; i<9; i++)
		Insert(&list, i-1, i);
	Output(&list);
	Delete(&list, 0);
	Output(&list);
  	x = Find(&list, 5);
	printf("%d\n", x);
	Destory(&list);
	return 0;
}
void Init(HeaderList *h)
{
	h->head = (Node*)malloc(sizeof(Node));//分配表头节点的内存 
	h->head->link = NULL;//让表头节点的下一个节点为NULL 
	h->n = 0;//当前表内没有元素 
}
void Insert(HeaderList *h, int i,ElemType x)
{
	Node *p, *q;
	int j;
	if(i<-1 || i>h->n-1)//如果等于-1，就是插入第一个元素 
		return;
	p = h->head;//p初值为表头节点的地址 
	for(j=0; j<=i; j++)//循环i+1次后p等于下标为i的结点地址 
		p = p->link;
	q = (Node *)malloc(sizeof(Node));//给待插入结点分配空间 
	q->element = x;
	q->link = p->link;//右手先牵 
	p->link = q;//左手后牵 
	h->n++;
}
//返回下标为i的结点元素值 
ElemType Find(HeaderList *h, int i) 
{
	Node *p;
	int j;
	if(i<0 || i>h->n-1)
		return NULL;
	p = h->head;
	for(j=0; j<=i; j++)
		p = p->link;
	return p->element;
}
//删除下标为i的结点 
void Delete(HeaderList *h, int i)
{
	int j;
	Node *p, *q;
	if(!h->n)
		return;
	if(i<-1 || i>h->n-1)
		return;
	q = h->head;
	for(j=0; j<i; j++)//循环i次后q为下标为i-1的结点地址 
		q = q->link;
	p = q->link;//记录待删除结点的地址 
	q->link = p->link;//让左手结点牵上右手结点 
	free(p);//删除结点 
	h->n--;
}
void Output(HeaderList *h)
{
	Node *p;
	if(!h->head)//为空则返回 
		return;
	p = h->head->link;//p为第一个结点地址 
	while(p)
	{
		printf("%d ", p->element);
		p = p->link;
	}
	printf("\n");	
}
void Destory(HeaderList *h)
{
	Node *p;
	while(h->head)
	{
		p = h->head->link;
		free(h->head);
		h->head = p;
	}
}
```

