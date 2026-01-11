---
title: 【OFDM系列】DFT为什么能求频率幅度谱？DFT后的X[k]与x(n)幅度的关系？DFT_IDFT底层数学原理？
date: 2026-01-11 15:30:00
categories: OFDM系列
tags: [OFDM, 通信]
layout: post
---
@[TOC]
## 问题引入
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/c4245f2374669972b1dfcc690cef7fb3.png)
上面是DFT和IDFT的公式，IDFT先不谈。在实践中常使用FFT算法来快速算出DFT，获得时域采样信号x(n)的频率幅度谱。
**例如：**
```c
N=1500;
xn=0.5*sin(2*pi*75/N*n)+3*cos(2*pi*40/N*n)+0.7*sin(2*pi*350/N*n);
```
上面这个时域采样信号xn由三个频率叠加而成，我们知道**频率的概念**是1秒信号经过了多少个周期，
那么我们假设采样率是`fs=1000`，共采样`N=1500`点，那么`0.5*sin(2*pi*75/N*n)`的频率即为`75*fs/N=50`，因此第一个信号频率为50。

通过Matlab进行FFT，可以画出这样一张频率幅度谱：
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/f15297ec74d13b6a0d32ae1ac64e9474.png)
这里就引申出我们的标题：**DFT为什么能求频率幅度谱？DFT后的X[k]与x(n)幅度的关系？DFT/IDFT底层数学原理？**
对于这个问题，我看了不少网上的博客、视频、书籍，总觉得讲的不清不楚，有人说X[k]的结果就是x(n)的幅度，有人说X[k]的结果除以N就是x(n)的幅度，有人说X[k]的结果除以N/2就是x(n)的幅度，就没有一个比较清楚的证明到底X[k]的值和x(n)幅度的关系。
**如果你也对此有疑问，现在我证明给你看！**


## 铺垫一些小公式
要看懂我的证明，首先需要铺垫一些小公式，防止你不知道！
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/8e626dc6968c597f2ae8b9f944fe91bf.png)

## DFT公式证明
我将公式的证明整理成了PPT，下面我直接复制，在证明中使用到了上面铺垫的小公式，注意关联起来看就可以理解了！
### DFT公式分解为4部分
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/bd70c807a23d281d759cc053cc3fd4a0.png)
#### 先考虑k1=0的情况:
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/7ce8da81c906de1256e20ae46e743b79.png)
#### 再考虑k1≠0的情况:
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/14d7f5c35d28e2fa97b11a488cd5c70f.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/93bf801afbbd316d07d185d39781c540.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/fd6805795ecf0b576896897d2685555d.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d7837eeb26648d6ffb6a1fdd0fca65f8.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/ab181746a8c84a4b39d885323267afc1.png)
### DFT计算后，X(k)与x(n)的关系：
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/d4578828ffea0dc39b9264d62f723a9c.png)
可以看到，DFT公式本质上可以完全拆成三角函数的计算，在此过程中利用
**高中的积化和差公式**和**三角函数在若干个周期的累加为0**，
可以得到X[k]和原信号x(n)幅度的关系。

## Matlab FFT示例代码
下面我们给出使用FFT对x(n)进行DFT计算后，绘制频率幅度谱的Matlab代码，看官可以发现，这上述公式的X(k)结果是**完全对应**的！

```c
%功能说明：
%生成时域采样信号0.5sin(2pi*k/N*n)
%通过fft转化到频域，绘制频率幅度谱，横坐标是频率f=k*fs/N，纵坐标是实际幅度
%再通过ifft转化回时域，绘制ifft结果信号，和原信号进行对比
 
 
%采样率1000
fs=1000;
 
%在N个采样点中，一共振动了k个周期
k=75;
 
%采样总点数
N=1500;
 
%n表示采样的第n个点
n=0:N-1;

%xn是采样得到的x(n)时域信号
xn=0.5*sin(2*pi*k/N*n)+3*cos(2*pi*40/N*n)+0.7*sin(2*pi*350/N*n);

xk=fft(xn);

%abs是求模
P2=abs(xk/N);
P1=P2(1:N/2+1);
P1(2:end-1)=2*P1(2:end-1);
 
%半频谱 f=k*fs/N
f=fs*(0:(N/2))/N;
plot(f,P1) 
title("Single-Sided Amplitude Spectrum of X(t)")
xlabel("f (Hz)")
ylabel("|P1(f)|")
```


## IDFT公式证明
![在这里插入图片描述](https://i-blog.csdnimg.cn/blog_migrate/dfbfd3c1ff7f6abfcecd14efa3ad09e0.png)

## Matlab调用FFT/IFFT并绘图

```c
%功能说明：
%生成时域采样信号0.5sin(2pi*k/N*n)
%通过fft转化到频域，绘制频率幅度谱，横坐标是频率f=k*fs/N，纵坐标是实际幅度
%再通过ifft转化回时域，绘制ifft结果信号，和原信号进行对比
 
 
%采样率1000
fs=1000;
 
%在N个采样点中，一共振动了k个周期
k=75;
 
%采样总点数
N=1500;
 
%n表示采样的第n个点
n=0:N-1;

%xn是采样得到的x(n)时域信号
xn=0.5*sin(2*pi*k/N*n)+3*cos(2*pi*40/N*n)+0.7*sin(2*pi*350/N*n);

xk=fft(xn);

%abs是求模
P2=abs(xk/N);
P1=P2(1:N/2+1);
P1(2:end-1)=2*P1(2:end-1);
 
%半频谱 f=k*fs/N
f=fs*(0:(N/2))/N;
plot(f,P1) 
title("Single-Sided Amplitude Spectrum of X(t)")
xlabel("f (Hz)")
ylabel("|P1(f)|")

% 反傅里叶变换
X = ifft(xk, 'symmetric');

% 绘制输入信号和还原信号的图像
figure
subplot(2,1,1)
plot(n, xn)
title('Input Signal')
xlabel('Time (s)')
ylabel('Amplitude')

subplot(2,1,2)
plot(n, X)
title('Signal after IFFT')
xlabel('Time (s)')
ylabel('Amplitude')
```




