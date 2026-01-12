---
title: 【IC设计】DC工具的target、link、synthetic、symbol库
date: 2023-08-01 10:44:49
categories: 数字IC设计
tags: [EDA工具]
layout: post
---
## Specifying Libraries
> You use dc_shell variables to specify the libraries used by Design  Compiler. 
> Table 4-1 lists  the variables for each library type as well  as the typical file extension for the library.

你使用dc_shell变量去指定dc要使用的库。下表列出了每种库以及对应的常用扩展名
|Library type|Variable |Default |File extension |
|--|--|--|--|
|Target library| target_library |{"your_library.db"}|.db |
|Link library|link_library|{"*","your_library.db"}|.db|
|Symbol library|symbol_library|{"your_library.sdb"}|.sdb|
|DesignWare library|synthetic_library|{}|.sldb|
## Specifying Technology Libraries
> To specify technology libraries, you must specify the target library and link library.
 
要指定**工艺库**，就要指定**目标库和链接库**
## Target Library
>Design Compiler uses the target library to build a circuit. During mapping, Design Compiler 
selects functionally correct gates from the target library. It also calculates the timing of the 
circuit, using the vendor-supplied timing data for these gates.
Use the target_library variable to specify the target library. 

DC使用目标库来构建电路。在映射时，DC从目标库中**选择功能正确的门**。它也使用供应商的时序数据来**计算电路的时序**。

## Link Library
> Design Compiler uses the link library to resolve references. For a design to be complete, it 
must connect to all the library components and designs it references. This process is called 
linking the design or resolving references. 

DC使用链接库来解决依赖（reference后面均翻译为依赖）。在一个设计要完成时，它必须连接到所有库元件并且设计它的依赖。这个过程被叫做链接设计或解决依赖。
>During the linking process, Design Compiler uses the link_library system variable, the local_link_library attribute, and the search_path system variable to resolve references. These variables and attribute are described below:

在链接过程中，DC使用link_library,local_link_library和search_path系统变量来解决依赖。这些变量和属性被描述如下:
>• link_library variable
The link_library variable specifies a list of libraries and design files that Design 
Compiler can use to resolve references. When you load a design into memory, Design 
Compiler also loads all libraries specified in the link_library variable.

• link_library variable
link_library变量指定一个库和设计文件的列表，DC用他们来解决依赖。当你加载设计文件到内存中时，DC也加载所有在link_library 变量中指定的库。

>Because the tool loads the libraries while loading the design, rather than during the link 
process, the memory usage and runtime required for loading the design might increase. 
However, the advantage is that you know immediately whether your design can be 
processed with the available memory.

因为工具是在载入设计时加载库，而不是在链接时加载库，所以在加载设计时内存的使用可能会增加。
不过，这么做的好处是你可以根据可用内存立刻知道你的设计是否能被处理。

>An asterisk in the value of the link_library variable specifies that Design Compiler 
should search memory for the reference. 

link_library中的*号指定DC应该在内存中寻找依赖。

• local_link_library attribute
>The local_link_library attribute is a list of design files and libraries added to the 
beginning of the link_library variable during the linking process. Design Compiler 
searches files in the local_link_library attribute first when it resolves references.

local_link_library属性是一个设计文件和在链接过程中要加入到link_library变量开头的库。DC会先在local_link_library属性中搜索文件来解决引用。

• search_path variable
>If Design Compiler does not find the reference in the link libraries, it searches in the 
directories specified by the search_path variable, described in “Specifying a Library 
Search Path” on page 4-8. For more information on resolving references, see “Linking 
Designs” on page 5-13.

**如果DC没有在链接库中找到引用，它会搜索由search_path变量指定的目录**，这部分内容在4-8中的"Specifying a Library Search Path"有描述。更多信息查看"Linking Designs"在5-13。

>If you do technology translation, add the standard cell library for the existing mapped 
gates to the link_library and the standard cell library being translated to the 
target_library.

如果你做了技术转化，为已经存在的映射门添加标准单元库到link_library中，并添加标准单元库到target_library中

>Your target_library specification should only contain those standard cell libraries that you want Design Compiler to use when mapping your design’s standard cells. Standard cells are cells such as combinational logic and registers. Your target_library specification should not include any DesignWare libraries or macro libraries such as pads or memories.

你的目标库应当只包含那些你想要DC在映射你的设计中标准单元时使用的库。标准单元是组合逻辑和寄存器单元。你的目标库应当不包含任何DesignWare库或者宏库，例如pads或memories。（端口或内存）
 
>The target_library is a subset of the link_library and listed first in your list of link 
libraries, as shown in Example 4-1. This example includes the additional_link_lib_files user 
created variable to simplify the link library definition.

**目标库是一个link_library的子集，并且在你的link库的开头列了出来**，如例4-1所示。这个例子包含了用户创建的additional_link_lib_files变量来简化link库的定义。

>Example 4-1 Setting the Target, Synthetic, and Link Libraries
set target_library [list of standard cell library files for mapping]
set synthetic_library [list of sldb files for designware, and so on] 
set additional_link_lib_files [list of additional libraries for linking: pads, macros, and so on]
set link_library [list * $target_library $additional_link_lib_files  $synthetic_library]

>When you specify the files in the link_library variable, consider that Design Compiler searches these files from left to right when it resolves references, and it stops searching when it finds a reference. If you specify the link library as {"*" si_10k.db}, the designs in memory are searched before the lsi_10k library

在link_library变量中指定文件时，要考虑到DC工具搜索文件时遵循从左到右的顺序来解决依赖，在找到依赖时立刻停止搜索。如果指定link library如  {"*" si_10k.db}，在内存中的设计会先于lsi_10k库搜索。

>Design Compiler uses the first technology library found in the link_library variable as the main library. It uses the main library to obtain default values and settings used in the absence of explicit specifications for operating conditions, wire load selection group, wire load mode, and net delay calculation. Design Compiler obtains the following default values and settings from the main library:

DC使用在link_libary变量中找到的第一个工艺库作为主库。它使用主库在缺乏操作条件、线负载选择组、线负载模式和网络延迟计算时进行默认的值和设置。DC从主库中获得下面的默认值和设置：
-  Unit definitions
-  Operating conditions
-  K-factors
-  Wire load model selection
-  Input and output voltage
-  Timing ranges
-  RC slew trip points
-  Net transition time degradation tables
 
> If other libraries have units different from the main library units, Design Compiler converts all units to those that the main library uses.

如果其他库有单元不同于主库单元，DC转化所有单元为那些主库使用的单元。
> If you are performing simultaneous minimum and maximum timing analysis, the logic libraries specified by the link_library variable are used for both maximum and minimum timing information, unless you specify separate minimum timing libraries by using the set_min_library command. The set_min_library command associates minimum timing libraries with the maximum timing libraries specified in the link_library variable. 
> For example, 
dc_shell> set link_library "* maxlib.db"
dc_shell> set_min_library maxlib.db -min_version minlib.db

如果你在同时执行最大、最小时序分析，在link_library变量中指定的逻辑库会被用于最大最小时序信息，除非你通过set_min_library命令分别单独指定最小时序库。set_min_library 命令将最小时序库和在link_library变量中指定的最大时序库链接在一起。

>To find out which libraries have been set to be the minimum and maximum libraries, use the list_libs command. In the generated report, the letter "m" appears next to the minimum library and the letter "M" appears next to the maximum library.

为了找到哪个库被用于设置最大最小库，使用list_libs命令。在生成的报告中，小写m旁边的是最小库，大写字母M旁边的是最大库。

## Specifying DesignWare Libraries
>You do not need to specify the standard synthetic library, standard.sldb, that implements the built-in HDL operators. The software automatically uses this library.If you are using additional DesignWare libraries, you must specify these libraries by using the synthetic_library variable (for optimization purposes) and the link_library variable (for cell resolution purposes).

你不需要指定标准synthetic library，standard.sldb，那会被内置的HDL运算符实现。这个软件会自动地使用这个库。
如果你正在使用额外的DesignWare库，你必须通过使用synthetic_library变量和link_library变量来指定这些库（出于优化的目的）。

>For more information about using DesignWare libraries, see the DesignWare documentation.

更多关于DesignWare库的信息，参见DesignWare文档。

## Specifying a Library Search Path
>You can specify the library location by using either the complete path or only the file name. 
If you specify only the file name, Design Compiler uses the search path defined in the search_path variable to locate the library files. By default, the search path includes the current working directory and $ SYNOPSYS/libraries/syn, where $ SYNOPSYS is the path to the installation directory. Design Compiler looks for the library files, starting with the leftmost 
directory specified in the search_path variable, and uses the first matching library file it finds.

你可以通过绝对路径或仅使用文件名的方式来指定库的路径。
如果你仅通过文件名指定库的路径，DC会使用预定义的search_path变量来定位库文件。默认情况下，search path包含当前的工作目录和`$SYNOPSYS/libraries/syn`目录，其中`$SYNOPSYS`指的是安装目录的路径。DC寻找库文件从search_path变量的最左侧开始，并使用第一个匹配的库文件。

>For example, assume that you have technology libraries named my_lib.db in both the lib directory and the vhdl directory. If the search path contains (in order) the lib directory, the vhdl directory, and the default search path, Design Compiler uses the my_lib.db file found in the lib directory, because it encounters the lib directory first.

例如，假定你在lib目录和vhdl目录下都有名为my_lib.db的工艺库。如果搜索路径包含lib目录，vhdl目录和默认的搜索路径，DC会使用在lib目录下找到的my_lib.db，因为DC最先搜索到lib目录。

>You can use the which command to see which library files Design Compiler finds (in order).

你也可以使用which命令来看DC按照顺序会找到什么库。

dc_shell> which my_lib.db
/usr/lib/my_lib.db, /usr/vhdl/my_lib.db
## 总结
DC涉及的库有：
目标库target_library、链接库link_library、算数运算库synthetic_library(就是DesignWare library，是同一个东西)、符号库symbol_library

DC在读文件时会读入所有需要的库，先在**链接库**里按照【从左到右】的顺序找对应的标准单元进行替换，如果找到就**停止**，如果找不到再到**search_path**里找库进行替换，earch path包含当前的工作目录和`$SYNOPSYS/libraries/syn`目录。可以通过`which name.db`来查看会先找到哪个目录下的库。

target libray和link library是工艺库，扩展名是.db，target libary定义了standard cell相关的信息。target library的内容需要写在link library中。

link_library变量中指定的逻辑库会被用于最大最小时序信息的分析，为了找到哪个库被用于设置最大最小库，使用list_libs命令。在生成的报告中，小写m旁边的是最小库，大写字母M旁边的是最大库。

**link_library和target_library的区别：**
target_library是综合时要映射的标准单元库，是link_library的子集，link_library包含target_library、synthetic_library、购买的硬核IP、IO Pad。

synthetic_library是算术运算库，扩展名是.sldb，DC初始化时默认使用standard.sldb来实现算术运算。例如加法，默认综合会使用串行进位的加法器来实现，如果需要超前进位加法器，就需要设置synthetic library。同时，synthetic_library需要添加到link_library中，以方便在链接时DC能找到对应运算符的实现。

symbol_library是工艺库单元显示原理图（Schematic）的库，扩展名.sdb，在使用design_analyzer或design_vision分析电路时会用到该库，缺省情况下会使用默认的符号库。

