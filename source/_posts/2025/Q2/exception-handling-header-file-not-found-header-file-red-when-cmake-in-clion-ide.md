---
title: 【异常处理】Clion IDE中cmake时头文件找不到 头文件飘红
date: 2025-04-12 21:26:13
categories: 异常处理
tags: [错误解决, CMake, 调试]
layout: post
---
如图所示是我的clion项目目录
 ![ ](./1.png) 
我自定义的data_structure.h和func_declaration.h在unit_test.c中无法检索到
 ![ ](./2.png) 
cmakelists.txt配置文件如下所示：

```rust
cmake_minimum_required(VERSION 3.30)
project(noc C)
#设置头文件的目录
include_directories(${CMAKE_SOURCE_DIR}/header)

set(CMAKE_C_STANDARD 11)

add_executable(noc
        header/func_declaration.h
        header/data_structure.h
        src/design/router.c
        src/design/main.c
        src/design/memory_oper.c
        src/design/io_utils.c
        src/design/traffic_oper.c
        src/design/initial_utils.c
        src/design/simulate.c
)

add_executable(unit_test
        header/func_declaration.h
        header/data_structure.h
        src/design/router.c
        src/design/memory_oper.c
        src/design/io_utils.c
        src/design/traffic_oper.c
        src/design/initial_utils.c
        src/design/simulate.c
        src/test/unit_test.c
)
```

解决办法：
如图所示，当前处于unit_test.c状态，无法检索到头文件，点unit_test后就可以检索到了
 ![ ](./3.png) 
 ![ ](./4.png) 

