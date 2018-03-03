drop database if exists hooksql_test;
create database `hooksql_test` default character set utf8;

use `hooksql_test`;


drop table if exists User;
create table `User`
(
	user_id int primary key,
	equipment blob
);

insert into `User` values(1, X'082a10e70718031802188a01');
