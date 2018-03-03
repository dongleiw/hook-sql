#!/bin/python
#-*-coding: utf8 -*-
# 提供序列化/反序列化google-protobuf-message的功能
# 提供google-protobuf-enum的转换功能

import sys
import os

import google.protobuf.text_format
import google.protobuf.symbol_database

#sys.path.append(os.path.abspath('./pypb'))

import pypb.pb_init


def parse_data_to_message(data, message_name):
	'''
		实例化一个名为@message_name的message. 反序列化data
		return message-instance
	'''
	pb_symbol_database = google.protobuf.symbol_database.Default()
	msg_class = pb_symbol_database.GetSymbol(message_name);
	msg_inst = msg_class();
	msg_inst.ParseFromString(data);
	return msg_inst;
