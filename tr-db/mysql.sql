create user 'www'@'%' identified by '$3cureUS';
create database test_cs4501 character set utf8;
grant all on cs4501.* to 'www'@'%';
