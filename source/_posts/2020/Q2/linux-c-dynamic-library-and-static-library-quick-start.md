---
title: 【linux下C】动态库与静态库快速入门
date: 2020-04-20 10:26:48
categories: 编程与算法
tags: [C语言, 动态库, Linux]
layout: post
---

**为什么要用库：**
我们在写代码时常用的一些功能，为了避免重复造轮子（每次都从头写），我们会把它编译好放到库中，以供写程序时直接调用，提高开发效率。

**静态库快速入门：**
1.新建一个sort.c文件，在其中可以编写一个函数，
例如int outmax(int a,int b)，比较a和b哪个大，并返回较大者的值。
2.编译函数，并将编译后的文件加入静态库中

```bash
gcc -c outmax.c 
```

#编译max.c，生成了outmax.o

```bash
ar -r libmath.a outmax.o 
```

#将上一条命令生成的max.o 文件加入到库中，一般库以lib开头，扩展名为.a
3.编写主程序main.c，在主程序中可以直接使用之前写的max函数，如：

```cpp
#include <stdio.h>
int outmax(int a,int b);  //注意这里声明必须加上
int main(){
    printf("outmax=%d\n",outmax(3,8));
    return 0;
}
```

4.编译主程序时带上静态库

```bash
gcc main.c libmath.a
```

5.此时应生成了一个a.out，

```bash
./a.out #执行a.out
```

**静态库的好处：**
可以使用一些自己编写的函数,编译的时候带上静态库就可以。

**静态库的坏处：**
编译生成的文件会比较大，因为把整个静态库加进去了。

**动态库：**
1.写好你的库函数，如sort.c
2.编译 
`gcc -c -fpic sort.c`
3.将你的函数加入到动态库中 
`gcc -shared sort.o -o libmath.so`
4.编译主程序 `gcc main.c -lmath -L ./`
5.将.so文件移动到/lib目录中(原因是动态库系统自动在/lib下查找) 

```bash
mv libmath.so /lib
```

6.`cat /etc/ld.so.conf`（6 7步先照做吧）
7.`ldconfig`
8.执行程序。
`./a.out`
