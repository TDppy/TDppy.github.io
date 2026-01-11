---
title: 【蓝桥杯备战】从零开始死磕搜索技术之全排列问题
date: 2026-01-11 15:30:00
categories: 
tags: []
layout: post
---

这篇主要写一下DFS解全排列问题。

![在这里插入图片描述](/images/9787edb69c0f7eca28c2e0cb0c2d7843.png#pic_center)
这题有两种做法，一是DFS，二是利用STL的next_permutation函数，第二种比较简单，分析一下第一种做法。
以N=3为例，结果为：
1 2 3
1 3 2
2 1 3
2 3 1
3 1 2
3 2 1
先上一下搜索结果示意图：
![在这里插入图片描述](/images/8fbfa0591b1be94a7a13988b0668392d.png)
从图中我们可以看到，如果要用深度优先搜索来解决这个问题，当遇到相同的元素时应当避开（题目要求所产生的任一数字序列中不允许出现重复数字。）
![在这里插入图片描述](/images/c9fc37eeb872f3499629a237dbcf225e.png)

因此，我们需要用一个chosen[i]来表示i这个值是否已经被选过。chosen[i]=1时已经被选过，chosen[i]=0时未选过。
此外，对于每一层选中的元素，需要一个order[k]来表示第k层选中元素的值。
下面上代码，读者可以看看代码中的注释并以N=3为例来模拟一下这个过程。

```cpp
#include <iostream>
using namespace std;
//order[K]表示第k层选中的元素 
int order[20];
//chosen[i]表示i这个值是否选中过，例如chosen[1]=1则表示1这个值已选过，等于0则表示没选过。 
int chosen[20];  
int n;
//calc(int k)含义是从第K层搜索到最后一层 
void calc(int k){
	for(int i=1;i<=n;i++){
		//如果这个元素被选过，跳过这个分支。 
		if(chosen[i]) continue;
		//将i选为第k层的元素 
		order[k]=i;
		//标记i已经选过 
		chosen[i]=1;
		//当第k层的元素被选中后，将order数组中的每层元素全部输出。 
		if(k==n){
		    for(int i=1;i<=n;i++){
			cout<<order[i];
			   if(i<n){
				cout<<" ";
			   }
		    }
		    cout<<endl;
	    }else{
	    	//如果还没选到第k层，则继续选下一层。 
		    calc(k+1);
		}
		//回溯操作（如果保持选过的状态，就没法生成其他排列的情况了，因此要回溯。） 
		order[k]=0;
		chosen[i]=0; 
	}
}
int main(){
    cin>>n;
    calc(1);
	return 0;
}
```

