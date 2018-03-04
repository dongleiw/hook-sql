# -*- coding: utf-8 -*-

hook_map={}

from google_proto_imp import pbparse

def google_proto_parse_message(column_name, column_data, message_name=None):
	'''
		使用message解析column_data
		如果message_name是None, 根据column_name生成message
			使用空格和下划线分割得到单词, 所有单词首字母大写
			column_name='friend' -> message_name='Friend'			# 首字母大写
			column_name='friend_info' -> message_name='FriendInfo'  # 将'_'视作空格, 后面单词首字母大写
			column_name='friendinfo' -> message_name='Friendinfo'   # 将friendinfo视作一个单词
	'''
	assert(column_data is not None);
	assert(column_name is not None);
	if(message_name is None):
		parts = column_name.split();
		parts2 = []
		for p in parts:
			parts2.extend( p.split('_') );
		message_name=""
		for p in parts2:
			message_name = message_name + p.capitalize();
		#print('guess messagename is ', message_name);
	else:
		if(len(message_name) != 1):
			return "invalid args message_name";
		message_name = message_name[0];

	msg = pbparse.parse_data_to_message(column_data, message_name);
	return str(msg);
	#return "pbm: %s %s %s" %(column_name, column_data, message_name);


hook_map['google_proto_parse_message'] = google_proto_parse_message
hook_map['pbm'] = google_proto_parse_message
