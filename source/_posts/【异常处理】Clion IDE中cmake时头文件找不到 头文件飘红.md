---
title: 【异常处理】Clion IDE中cmake时头文件找不到 头文件飘红
date: 2026-01-11 15:30:00
categories: 异常处理
tags: [异常处理]
layout: post
---
如图所示是我的clion项目目录
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/8d97ef11d03842da9a1b6514298078f7.png)
我自定义的data_structure.h和func_declaration.h在unit_test.c中无法检索到
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/f5127f74ef204c1f9a7ba04409c28d58.png)
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
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/52eb4ac57afc4e03a26055d3df988edb.png)
![在这里插入图片描述](https://i-blog.csdnimg.cn/direct/6f12c3de4ad448b1b1f3d3b8123e7d6d.png)

