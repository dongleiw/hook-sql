## hook-sql

游戏数据库中的很多数据是有一定格式的二进制数据，这种在查询/修改时就比较麻烦. 为了解决这个问题，在sql之上简单封装了一下，可以自定义一些函数，来进一步处理二进制数据

### hooks:

  hooks所在目录: hooks/
 下面是一个hooks例子. 将country_code转化为string

	hook_map={}
	def country_code_to_text(columnname, country_code, default_text):
		if(country_code == 356):
			return 'India';
		elif(country_code == 252):
			return 'Iceland';
		elif(country_code == 729):
			return 'Sudan';
		else:
			return default_text;

	hook_map['country_code_to_text'] = country_code_to_text;
	hook_map['countrycode'] = country_code_to_text;

  如果执行hsql: ```select countrycode(ccode, 'India') from Country;```
  函数```countrycode```将被调用: ```country_code_to_text('ccode', [raw_data_returned_from sql], 'India');```


### current hooks
  * google-protobuf (hooks/google_proto_imp/README)

    + pbm/google_proto_parse_message

      将google-protobuf序列化后的二进制数据反序列化出来.

    + pbe/google_proto_parse_enum

     还没实现

  * others

### usage
  首先创建数据库

	$ cd example
	$ sh prepare.sh # 创建hooksql_test数据库, 创建User表. 插入一条记录.

  将表User中的数据查询出来. 由于列`equipment`是pb, 二进制数据无法查看, 因此使用pbm反序列化出来.

	python hsql.py  -uroot -p123456 -hlocalhost -dhooksql_test -e "select user_id, pbm(equipment) from User";


 或者将hsql当作库使用

	$ python
	$ >>> import hsql
	$ >>> hsql=hsql.HSQL('localhost', 'root', '123456', 'hooksql_test');
	$ >>> hsql.execute('select user_id, pbm(equipment) from User');



