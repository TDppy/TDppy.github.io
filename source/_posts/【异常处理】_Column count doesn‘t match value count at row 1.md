---
title: 【异常处理】_Column count doesn‘t match value count at row 1
date: 2026-01-11 15:30:00
categories: 异常处理
tags: [异常处理]
layout: post
---

意思是存储的数据与数据库表的字段类型定义不相匹配.
解决办法：检查段类型是否正确, 是否越界, 有无把一种类型的数据存储到另一种数据类型中.
看看dao层访问数据库的sql语句是否书写错误，赋值的参数是否与字段类型一致
由于类似 insert 语句中，前后列数不等造成的
如1：省略数据库表的列名

```markup
INSERT INTO table_name
VALUES (value1, value2, value3,...)
```

改为：补全列名

```markup
INSERT INTO table_name (column1, column2, column3,...)
VALUES (value1, value2, value3,...)
```

 

如2：列数不相等，则检查相匹配的列数

```markup
INSERT INTO table_name(col_name1, col_name2, col_name3) VALUES('value1','value2');
```

如3：书写错误。

如标点符号，如多出空格等
