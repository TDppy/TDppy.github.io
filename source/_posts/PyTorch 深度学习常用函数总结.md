---
title: PyTorch 深度学习常用函数总结
date: 2026-01-11 15:30:00
categories: 
tags: [PyTorch, 深度学习]
layout: post
---
﻿@[toc]

> 近期要做AI编译器相关工作，需要把PyTorch入门下，在Google的Colab云平台上跑了LeNet/ResNet/GoogleNet/MobileNet，通过豆包整理了下所涉及到的函数，形成本文。

# PyTorch 深度学习常用函数总结
### 一、PyTorch 核心操作（基础张量与自动求导）

#### 1. 张量创建与操作



| 函数 / 方法                  | 功能描述                    | 参数说明                                                                   | 返回值                                  | 示例                                                            |
| ------------------------ | ----------------------- | ---------------------------------------------------------------------- | ------------------------------------ | ------------------------------------------------------------- |
| `torch.tensor(data)`     | 从数据（列表、数组等）创建张量         | `data`：输入数据；`dtype`：数据类型（如`torch.float32`，默认自动推断）；`device`：设备（CPU/GPU） | 多维张量（`torch.Tensor`）                 | `torch.tensor([[1,2],[3,4]])` → 形状为`(2,2)`的张量                 |
| `torch.zeros(shape)`     | 创建全零张量                  | `shape`：张量形状（如`(2,3)`）；`dtype`：数据类型                                    | 形状为`shape`的全零张量                      | `torch.zeros((2,3))` → `tensor([[0.,0.,0.],[0.,0.,0.]])`      |
| `torch.ones(shape)`      | 创建全一张量                  | 同`torch.zeros`                                                         | 形状为`shape`的全一张量                      | `torch.ones((3,2))` → `tensor([[1.,1.],[1.,1.],[1.,1.]])`     |
| `torch.rand(shape)`      | 创建 \[0,1) 均匀分布的随机张量     | 同`torch.zeros`                                                         | 形状为`shape`的随机张量                      | `torch.rand((2,2))` → 元素在 \[0,1) 的 2x2 张量                     |
| `torch.randn(shape)`     | 创建均值为 0、方差为 1 的标准正态分布张量 | 同`torch.zeros`                                                         | 形状为`shape`的随机张量                      | `torch.randn((2,2))` → 符合标准正态分布的 2x2 张量                       |
| `tensor.shape`           | 获取张量形状                  | 无参数                                                                    | 形状元组（`torch.Size`）                   | `x = torch.tensor([[1,2]])` → `x.shape` → `torch.Size([1,2])` |
| `tensor.dtype`           | 获取张量数据类型                | 无参数                                                                    | 数据类型（如`torch.int64`、`torch.float32`） | `x = torch.tensor([1.0])` → `x.dtype` → `torch.float32`       |
| `tensor.view(new_shape)` | 重塑张量形状（需保持元素总数不变）       | `new_shape`：新形状（可用`-1`表示自动计算该维度）                                       | 形状为`new_shape`的新张量（与原张量共享数据）         | `x = torch.rand(2,2)` → `x.view(4,1)` → 形状为`(4,1)`的张量         |

#### 2. 张量运算



| 函数 / 运算符             | 功能描述             | 参数说明                                                    | 返回值                          | 示例                                                                         |
| -------------------- | ---------------- | ------------------------------------------------------- | ---------------------------- | -------------------------------------------------------------------------- |
| `a + b` / `a * b`    | 元素级加法 / 乘法       | `a`、`b`：形状相同的张量                                         | 与`a`、`b`同形状的张量，元素为对应位置的和 / 积 | `a=torch.tensor([1,2])`，`b=torch.tensor([3,4])` → `a+b` → `[4,6]`          |
| `torch.matmul(a, b)` | 矩阵乘法（支持高维张量批量运算） | `a`、`b`：符合矩阵乘法维度要求的张量（如`a.shape=(m,n)`，`b.shape=(n,p)`） | 形状为`(m,p)`的张量（矩阵乘积结果）        | `a=torch.tensor([[1,2],[3,4]])` → `torch.matmul(a,a)` → `[[7,10],[15,22]]` |

#### 3. 设备操作



| 函数 / 方法                | 功能描述          | 参数说明                                 | 返回值                  | 示例                                                                      |
| ---------------------- | ------------- | ------------------------------------ | -------------------- | ----------------------------------------------------------------------- |
| `torch.device(device)` | 指定设备（CPU/GPU） | `device`：字符串（如`'cpu'`、`'cuda'`）或设备索引 | 设备对象（`torch.device`） | `device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')` |
| `tensor.to(device)`    | 将张量迁移到指定设备    | `device`：目标设备（`torch.device`对象）      | 迁移到目标设备的新张量          | `x = torch.tensor([1,2])` → `x.to(device)` → 张量移至 GPU（若可用）              |

#### 4. 自动求导（Autograd）



| 函数 / 方法                                  | 功能描述          | 参数说明                                  | 返回值 / 效果                 | 示例                                                          |
| ---------------------------------------- | ------------- | ------------------------------------- | ------------------------ | ----------------------------------------------------------- |
| `torch.tensor(data, requires_grad=True)` | 创建支持梯度计算的张量   | `requires_grad`：是否需要求导（布尔值，默认`False`） | 可求导的张量（叶子节点）             | `x = torch.tensor([2.0], requires_grad=True)`               |
| `tensor.backward()`                      | 反向传播计算梯度      | 可选`gradient`：梯度张量（用于非标量输出，默认`None`）   | 无返回值，梯度存储在`tensor.grad`中 | `z = x**2 + 3*y` → `z.backward()` → 计算`x.grad`和`y.grad`     |
| `tensor.grad`                            | 获取张量的梯度       | 无参数                                   | 梯度张量（与原张量同形状，初始为`None`）  | `x.grad` → `tensor([4.0])`（若`z = x**2`，则梯度为`2x`）            |
| `with torch.no_grad():`                  | 上下文管理器，禁止梯度计算 | 无参数                                   | 块内运算不构建计算图，不更新梯度         | `with torch.no_grad(): e = a*b` → `e.requires_grad`为`False` |

### 二、数据加载与预处理（torchvision + PyTorch）

#### 1. 数据集（`torchvision.datasets`）



| 函数 / 类                  | 功能描述                      | 参数说明                                                                                                | 返回值                                           | 示例                                                                              |
| ----------------------- | ------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------- | ------------------------------------------------------------------------------- |
| `datasets.MNIST(...)`   | 加载 MNIST 手写数字数据集          | `root`：数据存储路径；`train`：`True`加载训练集（60k 样本），`False`加载测试集（10k 样本）；`download`：无数据时自动下载；`transform`：数据变换 | 数据集对象（`Dataset`子类），支持索引访问（返回`(image, label)`） | `datasets.MNIST(root='./data', train=True, download=True, transform=transform)` |
| `datasets.CIFAR10(...)` | 加载 CIFAR-10 彩色图像数据集（10 类） | 同`MNIST`，但图像为 3 通道 32x32                                                                            | 数据集对象，返回`(image, label)`（图像为 3 通道）            | `datasets.CIFAR10(root='./data', train=False, transform=transform)`             |

#### 2. 数据变换（`torchvision.transforms`）



| 函数 / 类                                 | 功能描述                  | 参数说明                                       | 返回值                                                 | 示例                                                      |
| -------------------------------------- | --------------------- | ------------------------------------------ | --------------------------------------------------- | ------------------------------------------------------- |
| `transforms.Compose(transforms)`       | 组合多个变换为流水线            | `transforms`：变换列表（按顺序执行）                   | 组合变换对象，调用时按顺序应用所有变换                                 | `transforms.Compose([ToTensor(), Normalize(...)])`      |
| `transforms.ToTensor()`                | 将 PIL 图像转为 PyTorch 张量 | 无参数                                        | 变换函数，输入 PIL 图像（`(H,W,C)`，0-255），输出张量（`(C,H,W)`，0-1） | `img = Image.open('test.png')` → `ToTensor()(img)` → 张量 |
| `transforms.Normalize(mean, std)`      | 标准化张量                 | `mean`：均值序列（如`(0.1307,)`对应单通道）；`std`：标准差序列 | 变换函数，输出`(input - mean) / std`                       | `Normalize((0.1307,), (0.3081,))`（MNIST 的均值和标准差）        |
| `transforms.RandomCrop(size, padding)` | 随机裁剪图像                | `size`：裁剪后尺寸（如`32`）；`padding`：边缘填充像素（如`4`） | 变换函数，随机裁剪图像至`size x size`                           | `RandomCrop(32, padding=4)`（CIFAR-10 数据增强）              |
| `transforms.RandomHorizontalFlip()`    | 随机水平翻转图像              | 无参数（默认翻转概率 50%）                            | 变换函数，50% 概率水平翻转图像                                   | 用于数据增强，提升模型泛化能力                                         |

#### 3. 数据加载器（`torch.utils.data.DataLoader`）



| 函数 / 类                     | 功能描述    | 参数说明                                                                                                  | 返回值                                  | 示例                                                       |
| -------------------------- | ------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------ | -------------------------------------------------------- |
| `DataLoader(dataset, ...)` | 批量加载数据集 | `dataset`：数据集对象；`batch_size`：批次大小（如 64）；`shuffle`：是否打乱数据（训练集用`True`）；`num_workers`：加载数据的进程数（加速，默认为 0） | 迭代器，每次返回`(batch_data, batch_labels)` | `DataLoader(train_dataset, batch_size=64, shuffle=True)` |

### 三、神经网络构建（`torch.nn`）

#### 1. 基础组件



| 类 / 方法                                 | 功能描述                     | 参数说明                                     | 输入 / 输出形状                                                      | 示例                                                                        |
| -------------------------------------- | ------------------------ | ---------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------- |
| `nn.Module`                            | 神经网络基类，所有模型需继承该类         | 需实现`__init__`（定义层）和`forward`（前向传播）       | 无返回值，通过`forward`定义输入到输出的映射                                     | `class CNN(nn.Module): def __init__(self): ... def forward(self, x): ...` |
| `nn.Linear(in_features, out_features)` | 全连接层                     | `in_features`：输入特征数；`out_features`：输出特征数 | 输入`(batch_size, in_features)` → 输出`(batch_size, out_features)` | `nn.Linear(64*7*7, 128)`（输入 3136 维，输出 128 维）                              |
| `nn.ReLU()`                            | ReLU 激活函数（`max(0, x)`）   | 可选`inplace`：是否原地修改（节省内存，默认`False`）       | 输入`(any_shape)` → 输出同形状（负数置 0）                                 | `x = nn.ReLU()(x)`                                                        |
| `nn.Dropout(p)`                        | Dropout 层（随机失活神经元，防止过拟合） | `p`：失活概率（如`0.5`）                         | 输入`(any_shape)` → 输出同形状（部分元素置 0）                               | `nn.Dropout(0.5)`                                                         |
| `nn.BatchNorm2d(num_features)`         | 2D 批归一化（加速训练，稳定梯度）       | `num_features`：输入通道数                     | 输入`(batch_size, num_features, H, W)` → 输出同形状                   | `nn.BatchNorm2d(64)`（用于 64 通道的特征图）                                        |

#### 2. CNN 组件



| 类 / 方法                                                                   | 功能描述           | 参数说明                                                                                          | 输入 / 输出形状                                                                                                              | 示例                                                         |
| ------------------------------------------------------------------------ | -------------- | --------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| `nn.Conv2d(in_channels, out_channels, kernel_size, stride=1, padding=0)` | 2D 卷积层（提取空间特征） | `in_channels`：输入通道数；`out_channels`：输出通道数；`kernel_size`：卷积核大小（如`3`）；`stride`：步长；`padding`：边缘填充 | 输入`(batch, in_channels, H, W)` → 输出`(batch, out_channels, H', W')`（`H' = (H + 2*padding - kernel_size) // stride + 1`） | `nn.Conv2d(1, 32, kernel_size=3, padding=1)`（1→32 通道，保持尺寸） |
| `nn.MaxPool2d(kernel_size, stride=None)`                                 | 2D 最大池化（下采样）   | `kernel_size`：池化核大小；`stride`：步长（默认等于`kernel_size`）                                            | 输入`(batch, C, H, W)` → 输出`(batch, C, H//stride, W//stride)`                                                            | `nn.MaxPool2d(2, 2)`（尺寸减半）                                 |
| `nn.AvgPool2d(...)`                                                      | 2D 平均池化        | 同`MaxPool2d`                                                                                  | 同`MaxPool2d`，但取区域平均值                                                                                                   | `nn.AvgPool2d(2, 2)`（LeNet-5 中使用）                          |

### 四、模型训练与评估

#### 1. 损失函数与优化器



| 类 / 函数                                   | 功能描述                  | 参数说明                                                | 输入 / 输出                                                  | 示例                                                                        |
| ---------------------------------------- | --------------------- | --------------------------------------------------- | -------------------------------------------------------- | ------------------------------------------------------------------------- |
| `nn.CrossEntropyLoss()`                  | 交叉熵损失（分类任务，含 SoftMax） | 可选`weight`：类别权重；`reduction`：损失聚合方式（默认`'mean'`）      | 输入`(batch_size, num_classes)`和标签`(batch_size,)` → 输出标量损失 | `criterion = nn.CrossEntropyLoss()` → `loss = criterion(outputs, labels)` |
| `nn.MSELoss()`                           | 均方误差损失（回归任务）          | 同`CrossEntropyLoss`                                 | 输入`(batch_size, ...)`和目标`(batch_size, ...)` → 输出标量损失     | `criterion = nn.MSELoss()` → 用于线性回归                                       |
| `optim.Adam(params, lr=0.001)`           | Adam 优化器              | `params`：模型参数（`model.parameters()`）；`lr`：学习率        | 优化器对象，用于更新参数                                             | `optimizer = optim.Adam(model.parameters(), lr=0.001)`                    |
| `optim.SGD(params, lr=0.01, momentum=0)` | SGD 优化器               | `momentum`：动量（如`0.9`，加速收敛）；`weight_decay`：权重衰减（正则化） | 优化器对象                                                    | `optim.SGD(model.parameters(), lr=0.1, momentum=0.9)`                     |
| `optimizer.zero_grad()`                  | 清空梯度（避免累积）            | 无参数                                                 | 无返回值，梯度清零                                                | 训练循环中，前向传播前调用                                                             |
| `optimizer.step()`                       | 更新参数（基于梯度）            | 无参数                                                 | 无返回值，按优化器规则更新参数                                          | 反向传播（`loss.backward()`）后调用                                                |

#### 2. 训练与评估流程



| 方法 / 函数                 | 功能描述                               | 参数说明                             | 效果                    | 示例                                                        |
| ----------------------- | ---------------------------------- | -------------------------------- | --------------------- | --------------------------------------------------------- |
| `model.train()`         | 切换模型至训练模式（启用 Dropout、BatchNorm 更新） | 无参数                              | 模型进入训练状态              | 训练循环开始时调用                                                 |
| `model.eval()`          | 切换模型至评估模式（关闭 Dropout、固定 BatchNorm） | 无参数                              | 模型进入推理状态              | 测试前调用                                                     |
| `torch.max(input, dim)` | 沿指定维度取最大值（用于获取预测结果）                | `input`：张量；`dim`：维度（如`1`表示沿类别维度） | 返回`(最大值, 索引)`，索引为预测类别 | `_, predicted = torch.max(outputs, 1)` → `predicted`为预测标签 |

### 五、辅助工具与可视化

#### 1. 模型分析与保存



| 函数 / 方法                                   | 功能描述       | 参数说明                                                    | 输出 / 效果         | 示例                                             |
| ----------------------------------------- | ---------- | ------------------------------------------------------- | --------------- | ---------------------------------------------- |
| `torchsummary.summary(model, input_size)` | 打印网络结构与参数量 | `model`：模型；`input_size`：输入形状（如`(1,28,28)`）              | 打印各层名称、输出形状、参数量 | `summary(model, (1,28,28))`（MNIST 输入）          |
| `torch.save(model.state_dict(), path)`    | 保存模型权重     | `model.state_dict()`：模型参数字典；`path`：保存路径（如`'model.pth'`） | 无返回值，权重保存为文件    | `torch.save(model.state_dict(), 'cnn.pth')`    |
| `model.load_state_dict(torch.load(path))` | 加载模型权重     | `torch.load(path)`：加载保存的参数字典                            | 无返回值，模型加载权重     | `model.load_state_dict(torch.load('cnn.pth'))` |

#### 2. Matplotlib 可视化



| 函数                      | 功能描述               | 参数说明                                        | 示例                                                  |
| ----------------------- | ------------------ | ------------------------------------------- | --------------------------------------------------- |
| `plt.plot(x, y, label)` | 绘制折线图（如损失 / 准确率曲线） | `x`：x 轴数据；`y`：y 轴数据；`label`：图例标签            | `plt.plot(epochs, train_losses, label='训练损失')`      |
| `plt.imshow(img, cmap)` | 显示图像（如 MNIST 样本）   | `img`：图像数据（2D 数组）；`cmap`：颜色映射（如`'gray'`灰度图） | `plt.imshow(images[i].squeeze(), cmap='gray')`      |
| `plt.title(text)`       | 设置图表标题             | `text`：标题文本                                 | `plt.title(f'预测: {predicted[i]}\n真实: {labels[i]}')` |
| `plt.show()`            | 显示图表               | 无参数                                         | 弹出窗口显示绘制的图表                                         |

### 六、核心工作流总结
1.  **数据准备**：用`torchvision.datasets`加载数据集，`transforms`定义预处理，`DataLoader`批量加载。

2.  **模型构建**：继承`nn.Module`，定义卷积层、全连接层等，实现`forward`前向传播。

3.  **训练循环**：

*   切换训练模式（`model.train()`）；

*   前向传播计算输出→计算损失→清零梯度→反向传播→更新参数；

*   记录损失和准确率。

1.  **评估**：切换评估模式（`model.eval()`），用`with torch.no_grad()`禁止梯度计算，计算测试准确率。

2.  **可视化**：用 Matplotlib 绘制训练曲线，展示预测结果；用`torchsummary`和`torch.profiler`分析模型。

通过以上工具的配合，可完成从数据处理到模型部署的完整深度学习任务。
