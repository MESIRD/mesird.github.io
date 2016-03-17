---
layout: post
title:  "mysql columns"
date:   2016-03-16 20:50:20 +0800
author: "mesird"
---

Today I found that our project still had no formal database document, so I decided to collect and write one.  
There was a problem happen to me when I wanted to format the data from database client to my document, I mean there were too many tables and it's an hard job for me to copy and paste them one by one by my hand...  
Then I found I can select the useful information from database then copy them to my document table, this is the reason why I write this blog, to share some retained variables of mysql.  
**Followings are mysql columns**  
[**MSDN official document**](https://msdn.microsoft.com/en-us/library/ms188348.aspx)  
`TABLE_SCHEMA`                 数据库名  
`TABLE_NAME`                   表名称  
`COLUMN_NAME`                  列名  
`ORDINAL_POSITION`             位置顺序  
`COLUMN_DEFAULT`               默认值  
`IS_NULLABLE`                  是否为空  
`DATA_TYPE`                    数据类型  
`CHARACTER_MAXIMUM_LENGTH`     字符最大长度  
`CHARACTER_OCTET_LENGTH`       字节最大长度（[两者区别](http://dba.stackexchange.com/questions/74153/difference-between-character-maximum-length-and-character-octet-length)）  
`NUMERIC_PRECISION`            数据精度  
`NUMERIC_SCALE`                （不太清楚）  
`DATETIME_PRECISION`           日期精度  
`CHARACTER_SET_NAME`           字符集名称  
`COLLATION_NAME`               排序规则名  
`COLUMN_TYPE`                  列类型（包含位数）  
`PRIVILEGES`                   权限  
`COLUMN_COMMENT`               列备注  

You can also use the following script to select all retained variables:  
`select * from information_schema.columns where TABLE_NAME = ‘xxx'`