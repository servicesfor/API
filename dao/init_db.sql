create database yl_api_db;
use yl_api_db;
create table app_user(
id integer primary key auto_increment,
user_name varchar(16) unique,
auth_string varchar(200),
avatar varchar(200),
sex char(2),
nick_name varchar(16),
phone varchar(15), note text
)