hook-sql

游戏数据库中的很多数据是有一定格式的二进制数据，这种在查询/修改时就比较麻烦. 为了解决这个问题，在sql之上简单封装了一下，可以自定义一些函数，来进一步处理二进制数据

hooks:
	目录: hooks/
	-------------------示例------------------
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
	-----------------------------------------

	select countrycode(ccode, 'India') from Country;

	func `country_code_to_text` is executed as: 
		country_code_to_text('ccode', [raw_data_returned_from sql], 'India');


current hooks:
	google-protobuf # see ./hooks/google_proto_imp/README


usage:
	# execute hsql directly
	python hsql.py  -uroot -p123456 -hlocalhost -dhooksql_test -e "select user_id, pbm(equipment) from User";

	# use hsql as library
	--------------------
	$ python
	$ >>> import hsql
	$ >>> hsql=hsql.HSQL('localhost', 'root', '123456', 'hooksql_test');
	$ >>> hsql.execute('select user_id, pbm(equipment) from User');



