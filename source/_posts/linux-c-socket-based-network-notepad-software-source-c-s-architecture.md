---
title: 【Linux下C】基于socket的网络记事本软件源码（C_S架构）
date: 2021-01-14 13:56:47
categories: 编程与算法
tags: [C语言, Linux, 多进程]
layout: post
---

> *代码于大三上学期2020/12/10~2020/12/18 期间完成。
> 由于时间紧张和学识有限，代码定有不足之处，大佬勿笑~😀
> 如果需要帮助或有任何建议，加我qq：2287015934*

@[TOC]
如果有相同课题的同学搜到这篇博客，可以先看下面的**演示动图**及**课题要求**，来确认是不是你需要的。如果有

## 课题核心要求:
①用户注册
②用户登录
③编辑记事本
④上传记事本到服务端
⑤从服务端下载记事本
⑥查看服务端记事本列表

## 演示动图(建议[右键->新标签页]食用)
![在这里插入图片描述](/images/a535fa70570a3e711154bb634bd3fdc0.gif)

## 涉及的技术：
1.socket通信
2.Linux对文件和目录处理的系统调用
3.C语言和部分C++函数（如getline函数）
4.make

## 软件架构：
C/S架构，一个客户端，一个服务端，总计约400行代码。将常用的文件包含命令和函数声明放入了_public.h中，并简单的使用了make进行工程管理(其实就写了几行QAQ)。

## 代码实现：
### 客户端：

```cpp
#include "_public.h"
using namespace std;

int sockfd;
struct hostent* h;
struct sockaddr_in servaddr;
const int MAX_SIZE=50005;
char work_name[25];
int main(){
    ui_welcome();
    client_socket();
	int flag;
	cin>>flag;
	if(flag==1){
	   cout<<"请输入自定义用户名:";
       char username[20];
       cin>>username;
	   //创建该用户的专属目录
	   mkdir(username,0755);
	   //在服务端更改工作目录到该用户的目录
	   check(username);
       cout<<"注册成功!\n";
	}else{
	   cout<<"请输入您的用户名:";
	   cin>>work_name;
	   while(!check(work_name)){
	         cout<<"此用户不存在,请输入正确的用户名:\n";
             memset(work_name,0,sizeof(work_name));
		     cin>>work_name;
       }
	   cout<<work_name<<"欢迎回来！"<<endl;
	   //当用户存在时直接跳转到MENU处
	   goto MENU;
	}
MENU:
	while(1){
		ui_menu();
		flag=0;
		cin>>flag;
		switch(flag){
			case 1:EDIT();continue;
			case 2:FIND();continue;
			case 3:DOWN();continue;
			case 4:DELE();continue;
			default:cout<<"输入错误!\n";break;
		}
	}
    return 0;
}
bool check(char *workname){
	 char isexist[5];
	 memset(isexist,0,sizeof(isexist));
	 //发送标志位，表明需要尝试切换到用户的工作目录
	 send(sockfd,"0",5,0);
	 //发送工作目录
	 send(sockfd,workname,sizeof(workname),0);
     recv(sockfd,isexist,sizeof(isexist),0);
     if(atoi(isexist)==1){
	    return true;
	 }
	 return false; 
}


void ui_welcome(){
    cout<<"----------欢迎使用基于Socket的网络记事本系统----------\n";
	cout<<"               1.没有账号?请注册\n";
	cout<<"               2.已有账号?请登录\n";
	cout<<"------------------------------------------------------\n";
}
void ui_menu(){
    cout<<"----------功能菜单----------\n";
	cout<<"       1.编辑新的记事本\n";
	cout<<"       2.读取记事本列表\n";
	cout<<"       3.下载记事本\n";
	cout<<"       4.删除记事本\n";
	cout<<"----------------------------\n";
}

void EDIT(){
	 //filename用于存放要创建的记事本名
	 char filename[25];
	 memset(filename,0,sizeof(filename));
	 cout<<"请输入要创建的记事本名：";
	 cin>>filename;
	 cout<<"创建成功!请输入记事本的内容，以#表示结束(#单独占一行)"<<endl;
	 //tmp临时存放每行读入的记事本内容
     string tmp;
	 //content用于存放记事本的全部内容
	 string content;
	 //c_content和content一个用处，只是将content转化成了字符数组的形式
	 char c_content[1024];
	 memset(c_content,0,sizeof(c_content));
	 while(getline(cin,tmp)&&tmp[0]!='#'){
	       content+=tmp;
		   content+="\n";
	 }
	 cout<<"\""<<filename<<"\"输入完成"<<endl;
	 strcpy(c_content,content.c_str());
	 SAVE(c_content,filename);
}
/**
 *   函数功能：让客户端与服务端建立socket连接
 *   返回值：如果连接成功，返回true，否则返回false
 *   假定的全局变量：
 *   int sockfd
 *   struct hostent* h;
 *   struct sockaddr_in servaddr;
 */
bool client_socket(){
     sockfd=socket(AF_INET,SOCK_STREAM,0);
	 if(sockfd==-1){
	    perror("socket error");
		return false;
	 }
	 h=gethostbyname("127.0.0.1");
	 if(h==0){
	    perror("gethostbyname failed.\n");
		close(sockfd);
	    return false;
	 }
	 servaddr.sin_family=AF_INET;
	 servaddr.sin_port=htons(atoi("5005"));
	 memcpy(&servaddr.sin_addr,h->h_addr,h->h_length);
	 if(connect(sockfd,(struct sockaddr *)&servaddr,sizeof(servaddr))!=0){
	    perror("connect error");
		close(sockfd);
	    return false;
	 }
	 return true;
}
void SAVE(char *c_content,char *filename){
   	 int method;
	 cout<<"1.放弃编辑 2.保存到本地 3.同步至服务端\n";
	 cin>>method;
	 if(method==1){
		cout<<"已放弃该文件\n";
	 }else if (method==2){
		//创建名为filename的文件，并将记事本的全部内容c_content写入到文件中
	    int fd=creat(filename,O_RDWR);
		write(fd,c_content,strlen(c_content));
		cout<<"本地已保存到./"<<filename<<endl;
	 }else{
	    //int fd=creat(filename,O_RDWR);
		//string tmppath;
		//tmppath="./";
		//tmppath+=filename;
		//write(fd,c_content,strlen(c_content));
		//cout<<"本地已保存到./"<<filename<<endl;
		//调用client_socket()连接到服务端
		//client_socket();
		//先发送"1"标志，告诉服务端调用s_SAVE功能
		if(send(sockfd,"1",5,0)<=0){
		   perror("上传失败！请检查网络是否联通");
		}
		//先上传记事本的名字 长度为20字节
		if(send(sockfd,filename,20,0)<=0){
		   perror("上传失败!请检查网络是否连通");
		}
        //然后上传记事本的具体内容	
        if(send(sockfd,c_content,1000,0)<=0){
		   perror("上传失败!请检查网络是否连通");
		}
		cout<<"上传成功！"<<endl;
	 }
}
/**
 *   读取记事本列表实现思路:
 *   1.向客户端发送一个标志位2，表明需要记事本列表.
 *   2.接收客户端发来的文件列表(不超过50005字节)。
 *   3.向用户展示文件列表 
 *
 */
void FIND(){
	//client_socket();
 	if(send(sockfd,"2",5,0)<=0){
	   perror("上传失败！请检查网络是否联通");
	}
	char findAll[MAX_SIZE];
	memset(findAll,0,sizeof(findAll));
	if(recv(sockfd,findAll,MAX_SIZE,0)<=0){
	   cout<<"接收服务端记事本列表出错!"<<endl;
	}
	cout<<"--------"<<"服务端有以下记事本"<<"--------"<<endl;
	cout<<findAll;
}
void DOWN(){
    //client_socket();
	cout<<"请输入要下载的记事本名:"<<endl;
	char filename[25];
	memset(filename,0,sizeof(filename));
	cin>>filename;
	cout<<"="<<filename<<"="<<endl;
	if(send(sockfd,"3",5,0)<=0){
	   perror("下载失败!请检查网络是否联通");
	}
	if(send(sockfd,filename,sizeof(filename),0)<=0){
	   perror("下载失败!请检查网络是否联通");
	}
	char file_content[MAX_SIZE];
	memset(file_content,0,sizeof(file_content));
	if(recv(sockfd,file_content,sizeof(file_content),0)<=0){
	   perror("下载失败!请检查网络是否联通");
	}
	int filedes=open(filename,755);
	write(filedes,file_content,sizeof(file_content));
	cout<<"--------"<<filename<<"下载成功--------"<<endl;
	cout<<file_content<<endl;
	close(filedes);
}

void DELE(){
	 //client_socket();
	 if((send(sockfd,"4",5,0))<=0){
	   cout<<"无法使用删除文件功能，请检查网络连接"<<endl;
	 }
     char rmfname[25];
     memset(rmfname,0,sizeof(rmfname));
     //sprintf(rmfname,"./user/");
     cout<<"请输入要删除的记事本文件名:";
     cin>>rmfname;
	 //strcat(rmfname,)
     if((send(sockfd,rmfname,sizeof(rmfname),0))<=0){
	    cout<<"删除失败!请查看网络连接!"<<endl;
	 }
	 char isDele[5];
     recv(sockfd,isDele,sizeof(isDele),0);
     if(atoi(isDele)==1){
	    cout<<"成功删除\""<<rmfname<<"\"!"<<endl;
	 }else{
	    cout<<"删除失败!请查看网络连接!"<<endl;
	 }
}


```

### 服务端：

```cpp
#include "_public.h"
#include <errno.h>


using namespace std;
int listenfd;
struct sockaddr_in servaddr;
int clientfd;
int socklen;
char buffer[1100];
//一个目录下所有文件名的总字节数不超过50005
const int MAX_SIZE=50005;
char findAll[MAX_SIZE];
void s_LOGI();
void s_SAVE();
void s_FIND();
void s_DOWN();
void s_DELE();
int main(){
    //1创建socket
	listenfd=(socket(AF_INET,SOCK_STREAM,0));
	//2绑定地址和端口到socket
	memset(&servaddr,0,sizeof(servaddr));
	servaddr.sin_family=AF_INET;
	servaddr.sin_addr.s_addr=htonl(INADDR_ANY);
	servaddr.sin_port=htons(atoi("5005"));
	bind(listenfd,(struct sockaddr *)&servaddr,sizeof(servaddr));
	//3设置为监听模式
	listen(listenfd,5);
	//4接受客户端的连接
	socklen=sizeof(struct sockaddr_in);
	struct sockaddr_in clientaddr;
	clientfd=accept(listenfd,(struct sockaddr *)&clientaddr,(socklen_t*)&socklen);
	printf("客户端(%s)已连接.\n",inet_ntoa(clientaddr.sin_addr));
	
    //通信
	//先接收一个标志位，看是要调用什么功能
	while(1){
	    memset(buffer,0,sizeof(buffer));
		recv(clientfd,buffer,5,0);
		int flag=atoi(buffer);
		switch(flag){
			case 0:s_LOGI(); continue;
			case 1:s_SAVE(); continue;
			case 2:s_FIND(); continue;
			case 3:s_DOWN(); continue;
			case 4:s_DELE(); continue;
			default:cout<<"服务端无此功能！"<<endl; break;
		}	
	}
	close(listenfd);
	close(clientfd);
	return 0;
}
void s_SAVE(){
	//定义记事本的名称,打开文件后返回的文件描述符
	char filename[80];
	int filedes;
	memset(filename,0,sizeof(filename));
	//接收要保存的记事本名字
	recv(clientfd,filename,20,0);	
	printf("客户端:%s\n",filename);
	//打开文件，如果不存在则创建
	filedes=open(filename,0755);

	//接收记事本的具体内容
	memset(buffer,0,sizeof(buffer));
	recv(clientfd,buffer,1000,0); 

	//将具体内容buffer写入记事本
	write(filedes,buffer,1000);
	printf("已将%s保存至服务端\n",filename);
	close(filedes);
}
void s_DOWN(){
	char filename[25];
	memset(filename,0,sizeof(filename));
	if(recv(clientfd,filename,sizeof(filename),0)<0){
		cout<<"未能接收到文件名"<<endl;
	}
	char file_content[MAX_SIZE];
	memset(file_content,0,sizeof(file_content));
	int filedes;
	if((filedes=open(filename,O_RDONLY))<0){
		cout<<"该文件不存在！"<<endl;
		cout<<errno<<endl;
	}
	read(filedes,file_content,sizeof(file_content));
	if((send(clientfd,file_content,sizeof(file_content),0))<=0){
		cout<<"文件发送失败!"<<endl;
	}
	cout<<"发送完毕!"<<endl;
	close(filedes);
}

void s_DELE(){
	char filename[25];
	char isDele[5];
	memset(filename,0,sizeof(filename));
	memset(isDele,0,sizeof(isDele));
	if((recv(clientfd,filename,sizeof(filename),0))<=0){
		cout<<"未能成功接收到待删除文件名!"<<endl;
	}
	if((remove(filename))==-1){
		cout<<"删除失败!请输入正确的文件名!"<<endl;
		strcpy(isDele,"0");
		send(clientfd,isDele,sizeof(isDele),0);
		exit(0);
	}
	strcpy(isDele,"1");
	send(clientfd,isDele,sizeof(isDele),0);
	cout<<filename<<"删除成功!"<<endl;
}

/**
 *  查找功能分析：
 *  参数：char *路径
 *  根据路径，找到当前路径下的所有文件，并封装到数组
 */
//const int MAX_SIZE=50005;
//char findAll[MAX_SIZE];
void s_FIND(){
	//定义dir结构指针
	DIR *dir;
	//打开目录并让dir指针指向它
	dir=opendir(".");
	struct dirent *rent;
	int cnt=0;
	memset(findAll,0,sizeof(findAll));
	while(rent=readdir(dir)){
		char tmp[100];
		memset(tmp,0,sizeof(tmp));
		//把读取到的rent->name复制到tmp，然后判断一下是否是.
		strcpy(tmp,rent->d_name);
		if(tmp[0]=='.'||tmp[0]=='\n') continue;
		cnt++;
		sprintf(tmp,"%-15s",tmp);
		strcat(findAll,tmp);
		if(cnt%5==0){
			strcat(findAll,"\n");
		}
	}
	strcat(findAll,"\n");
	printf("%s目录有以下文件\n%s",".",findAll);

	if(send(clientfd,findAll,MAX_SIZE,0)<=0){
		cout<<"文件列表发送失败，请检查网络连接"<<endl;
	} 
	cout<<"发送成功!\n";
}
void s_LOGI(){
	char work_name[25];
	char isexist[5];
	memset(work_name,0,sizeof(work_name));
	memset(isexist,0,sizeof(isexist));
	recv(clientfd,work_name,sizeof(work_name),0);
	if(chdir(work_name)!=-1){
		strcpy(isexist,"1");
		send(clientfd,isexist,sizeof(isexist),0); 
	}else{
		strcpy(isexist,"0");
		send(clientfd,isexist,sizeof(isexist),0); 
	}
}


```

### _public.h：

```cpp
#include <iostream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <cstdio>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <netdb.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <dirent.h>
void ui_welcome();
void ui_menu();
bool check(char *workname);
void insertUserFile(char *username);
void EDIT();
void FIND();
void DOWN();
void DELE();
void SAVE(char *c_content,char *filename);
bool client_socket();


```

### makefile

```bash
SERVER CLIENT:SERVER.cpp CLIENT.cpp _public.h
	g++ SERVER.cpp _public.h -o SERVER
	g++ CLIENT.cpp _public.h -o CLIENT
```
## 联系方式
如果需要帮助或有任何建议，加我qq：2287015934

