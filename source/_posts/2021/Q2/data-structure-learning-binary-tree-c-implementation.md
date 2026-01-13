---
title: 【数据结构学习】二叉树的C实现
date: 2021-04-22 11:16:08
categories: 
tags: []
layout: post
---

 **功能：** 
 *  功能：
 *  遍历(先序遍历、中序遍历、后序遍历)
 *  计算节点总数/叶子节点总数
 *  计算二叉树的高度
 *  交换**所有**左右子树
 *  拷贝二叉树
 *  清空二叉树
 
 **运行截图：**
<!--  ![在这里插入图片描述](./1.png) 

```c
#include <stdio.h>
#include <stdlib.h>

/*   
 *  功能： 
 *  遍历(先序遍历、中序遍历、后序遍历)
 *  计算节点总数/叶子节点总数 
 *  计算二叉树的高度 
 */
 
typedef struct BTNode{
	//节点数据 
	int Data;
	//左孩子 
	struct BTNode *LChild; 
	//右孩子 
	struct BTNode *RChild;
}BTNode;

typedef struct BinaryTree{
	BTNode *root;
}BinaryTree;

//先序规则创建二叉树 
BTNode* PreCreateBt(BTNode *t){
	char ch;
	ch=getchar();
	if(ch=='#') t=NULL;
	else{
		t=(BTNode *)malloc(sizeof(BTNode));
		t->Data=ch;
		t->LChild=PreCreateBt(t->LChild);
		t->RChild=PreCreateBt(t->RChild);
	}
	return t;
}

//建树，传入BinaryTree(实际上就是根节点地址) 
void BuildTree(BinaryTree *tree){
	tree->root=PreCreateBt(tree->root);
} 

//先序遍历二叉树 
void PreOrderTransverse(BTNode *t){
	//根节点为空则返回 
	if(t==NULL){
		return ;
	}
	printf("%c",t->Data);
	//先序遍历左子树 
	PreOrderTransverse(t->LChild);
	//先序遍历右子树 
	PreOrderTransverse(t->RChild);
}

//树的先序遍历 
void TreePreOrder(BinaryTree *tree){
	if(tree){
		PreOrderTransverse(tree->root);
	}
}

//中序遍历二叉树
void InOrderTransverse(BTNode *t){
	if(t==NULL) return ;
	//左 
	InOrderTransverse(t->LChild);
	//根 
	printf("%c",t->Data);
	//右 
	InOrderTransverse(t->RChild);
} 
void TreeInOrder(BinaryTree *tree){
	if(tree){
		InOrderTransverse(tree->root);
	}
}
//后序遍历二叉树
void PostOrderTransverse(BTNode *t){
	if(t==NULL)return ;
	PostOrderTransverse(t->LChild);
	PostOrderTransverse(t->RChild);
	printf("%c",t->Data);
}
//后序遍历 
void TreePostOrder(BinaryTree *tree){
	if(tree){
		PostOrderTransverse(tree->root);
	}
} 
void Clear(BTNode *t){
	if(!t) return ;
	Clear(t->LChild);
	Clear(t->RChild);
	delete t;
}
void TreeClear(BinaryTree *tree){
	if(tree)
	Clear(tree->root);
} 
int Size(BTNode *t){
	if(!t) return 0;
	else return Size(t->LChild)+Size(t->RChild)+1;
}
int TreeSize(BinaryTree *tree){
	if(tree){
		return Size(tree->root);
	}
	return -1;
}
//叶子结点的数量 
int Leaves(BTNode *t){
	if(!t) {
		return 0;
	}
	if(t->LChild==NULL&&t->RChild==NULL){
		return 1;
	}
	return Leaves(t->LChild)+Leaves(t->RChild);
}
int TreeLeaves(BinaryTree *tree){
	if(tree){
		return Leaves(tree->root);
	}
	return -1;
}
//求二叉树的高度
int Height(BTNode *t){
	if(!t){
		return 0;
	}
	int l=Height(t->LChild);
	int r=Height(t->RChild);
	if(l>r){
		return l+1;
	}else{
		return r+1;
	}
}
int TreeHeight(BinaryTree *tree){
	if(tree) {
		return Height(tree->root);
	}
	return -1;
}
BTNode* Copy(BTNode* t){
    if(!t){
        return NULL;
    }
    BTNode* q=(BTNode *)malloc(sizeof(BTNode));
    q->Data=t->Data;
    q->LChild=Copy(t->LChild);
    q->RChild=Copy(t->RChild);
    return q;
}
void TreeCopy(BinaryTree *tree){
	if(tree){
		Copy(tree->root);
	}
}
//交换二叉树的所有左右子树
void Exchange(BTNode* t){
	if(t->LChild==NULL&&t->RChild==NULL){
		return ;
	}
	BTNode *temp;
	temp=t->LChild;
	t->LChild=t->RChild;
	t->RChild=temp;
	
	Exchange(t->LChild);
	Exchange(t->RChild);
}
void TreeExchange(BinaryTree *tree){
	if(tree){
		Exchange(tree->root);
	}
}
int main(){
	printf("先序建树\n");
	BinaryTree tree;
	BuildTree(&tree);
	
	printf("\n先序遍历:");
	TreePreOrder(&tree);
	
	printf("\n中序遍历:");
	TreeInOrder(&tree);
	
	printf("\n后序遍历:");
	TreePostOrder(&tree);
	
	printf("\n该树包含的节点总数: %d\n",TreeSize(&tree));
	printf("该树的高度: %d\n",TreeHeight(&tree));
	printf("该树包含叶子结点的总数: %d\n",TreeLeaves(&tree));
	return 0;
} 

```

