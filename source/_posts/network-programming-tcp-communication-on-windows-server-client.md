---
title: 【网络编程】windows下的TCP通信（server_client）
date: 2020-12-03 04:26:58
categories: 
tags: []
layout: post
---

该程序用C++和socket相关api实现了客户端和服务端的聊天，我使用devcpp成功编译运行（需要在编译选项中添加-lwsock32）。

**server.cpp**
```cpp
#include <iostream>
//#include "stdafx.h"
#include <winsock2.h>
#pragma comment(lib,"ws2_32.lib")
using namespace std;
int main(){
	WSADATA wsaData;
	if(WSAStartup(MAKEWORD(2,2),&wsaData)){
		cout<<"WinSock不能被初始化";
		WSACleanup();
		return 0;
	}
	SOCKET sockSer,sockConn;
	sockSer=socket(AF_INET,SOCK_STREAM,0);
	SOCKADDR_IN addrSer,addrCli;
	addrSer.sin_family=AF_INET;
	addrSer.sin_port=htons(5566);
	addrSer.sin_addr.S_un.S_addr=inet_addr("127.0.0.1");
	bind(sockSer,(SOCKADDR *)&addrSer,sizeof(SOCKADDR));
	listen(sockSer,5);
	int len=sizeof(SOCKADDR);
	cout<<"服务器等待客户端的连接……"<<endl;
	sockConn=accept(sockSer,(SOCKADDR *)&addrCli,&len);
	if(sockConn==INVALID_SOCKET){
		cout<<"服务器接受客户端连接请求失败!"<<endl;
		return 0;
	}
	else{
		cout<<"服务器接受客户端连接请求成功！"<<endl; 
	}
	char sendbuf[256],recvbuf[256];
	while(1){
		if(recv(sockConn,recvbuf,256,0)>0){
			cout<<"客户端说:>"<<recvbuf<<endl;
		}
		else{
			cout<<"客户端已断开连接"<<endl;
			break;
		}
		cout<<"服务器说:>";
		cin>>sendbuf;
		if(strcmp(sendbuf,"bye")==0)	break;
		send(sockConn,sendbuf,strlen(sendbuf)+1,0);
	}
	closesocket(sockSer);
	WSACleanup();
	return 0;
}
```
**client.cpp**

```cpp
#include <iostream>
//#include "stdafx.h"
#include <winsock2.h>
#pragma comment(lib,"ws2_32.lib")
using namespace std;
int main(){
	WSADATA wsaData;
	if(WSAStartup(MAKEWORD(2,2),&wsaData)){
		cout<<"WinSock不能被初始化";
		WSACleanup();
		return 0;
	}
	SOCKET sockCli;
	sockCli=socket(AF_INET,SOCK_STREAM,0);
	SOCKADDR_IN addrSer;
	addrSer.sin_family=AF_INET;
	addrSer.sin_port=htons(5566);
	addrSer.sin_addr.S_un.S_addr=inet_addr("127.0.0.1");
	int res=connect(sockCli,(SOCKADDR *)&addrSer,sizeof(SOCKADDR));
	if(res){
		cout<<"客户端连接服务器失败"<<endl;
		return -1;
	}else{
		cout<<"客户端连接服务器成功"<<endl;
	}
	char sendbuf[256],recvbuf[256];
	while(1){
		cout<<"客户端说:>";
		cin>>sendbuf;
		if(strcmp(sendbuf,"bye")==0)	break;
		send(sockCli,sendbuf,strlen(sendbuf)+1,0);
		if(recv(sockCli,recvbuf,256,0)>0){
			cout<<"服务器说:>"<<recvbuf<<endl;
		}else{
			cout<<"服务器已关闭连接"<<endl;
			break;
		}
	}
	closesocket(sockCli);
	WSACleanup();
	return 0;
}
```

