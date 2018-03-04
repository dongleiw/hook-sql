drop database if exists hooksql_test;
create database `hooksql_test` default character set utf8;

use `hooksql_test`;


drop table if exists User;
create table `User`
(
	user_id int primary key,
	equipment blob
);

-- 082a10e70718031802188a01 ->  (compiled by python-protobuf-2.6.1-1.3 amd64 (Ubuntu16.04))
--		equipment:
--			id: 42
--			level: 999
--			properties: 3 properties: 2 properties: 138
-- 
insert into `User` values(1, X'082a10e70718031802188a01');
