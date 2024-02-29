# 创建数据库 coursedb
create database coursedb;

# 创建用户 coursemaster
create user coursemaster identified by 'coursemasterpasswd';

# 授权用户 coursemaster 对数据库 coursedb 的所有权限
grant all on coursedb.* to coursemaster;

# 刷新权限
flush privileges;

