#!/bin/bash
# 准备测试hooksql用的db

# 写数据库
sql_file="./user.sql"

host=127.0.0.1
user=root
pswd=123456




mysql -u${user} -p${pswd} -h${host} -e " source ${sql_file}; "


