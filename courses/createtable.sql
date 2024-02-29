# 使用数据库 coursedb
# use coursedb;

# 创建表
create table course(
    number int primary key auto_increment,
    id varchar(20),
    name varchar(100),
    department varchar(40),
    credit decimal(3, 1),
    category varchar(20),
    label varchar(40),
    language varchar(20)
);

create index course_id_index
    on course (id);

alter table course
    add constraint course_id_pk
        unique (id);

# sqlite
# create table course(
#     number integer primary key /*autoincrement needs PK*/
#         constraint 表_name_pk
#             unique,
#     id varchar(20),
#     name varchar(100),
#     department varchar(40),
#     credit decimal(3, 1),
#     category varchar(20),
#     label varchar(40),
#     language varchar(20)
# );
#
# create index course_id_index
#     on course (id);


