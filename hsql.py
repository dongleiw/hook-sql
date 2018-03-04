# -*- coding: utf-8 -*-
# execute hsql with mysql


import sys
import os
import MySQLdb
import getopt
import getpass

class Hook:
	def __init__(self, name, func, from_file):
		self.name = name;
		self.func = func;
		self.from_file = from_file;
	def __str__(self):
		return "name[%s] func[%s] from_file[%s]" %(self.name, self.func, self.from_file);

class HookedColumn:
	def __init__(self, name, hook, args):
		self.name = name;
		self.hook = hook;
		if(args is not None):
			stripped_args = [a.strip() for a in args];
			self.args = stripped_args;
		else:
			self.args = args;
	def __str__(self):
		return "name[%s] hook[%s] args[%s]" %(self.name, self.hook, self.args);

global_hooks={}

def register_hook(name, func, from_file):
	if(name in global_hooks):
		print("hook[%s] from file[%s] already exists. new-from[%s]" %(name, global_hooks[name].from_file, from_file));
		exit();
	global_hooks[name] = Hook(name, func, from_file);
	print("----> hook[%s] from file[%s]" %(name, from_file));

def load_hooks():
	'''
		load all hooks
	'''
	hook_dir = "hooks"
	files=os.listdir(hook_dir);
	for f in files:
		f = f.strip();
		if(f.endswith('.py') and f != '__init__.py'):
			module_name = "%s.%s" %(hook_dir, f.replace('.py', ''));
			print("try to import module[%s]" %module_name);
			mod = __import__(module_name, globals(), locals(), ['hook_map']);
			hook_map = getattr(mod, 'hook_map');
			for (name, func) in hook_map.iteritems():
				register_hook(name, func, hook_dir + "/" + f);


class HSQLParser:
	def DebugPrint(self):
		print('hsql[%s]' %self.hsql);
		print('sql[%s]' %self.sql);
		for h in self.hooked_columns:
			if(h is not None):
				print(str(h));

	@staticmethod
	def parse_hsql(hsql_str):
		'''
			parse hsql
			return None if failed
		'''
		hsqlparser = HSQLParser();
		hsqlparser.hsql=hsql_str;
		hsqlparser.hooked_columns=[]
		hsqlparser.sql=''

		# get output columns from hsql
		select_idx = hsqlparser.hsql.find('select');
		from_idx = hsqlparser.hsql.find('from');

		if(select_idx==-1 or from_idx==-1):
			print('sql[%s] is not valid "select xxx from xxx"' %hsqlparser.hsql);
			return None;

		select_idx = select_idx + len('select');
		from_part = hsqlparser.hsql[from_idx:];
		columns_part = hsqlparser.hsql[select_idx:from_idx].strip();

		#print("part ", columns_part, from_part);


		# split columns_part to column
		columns=[]
		start_idx=0
		parentheses_depth=0;
		for idx in range(0, len(columns_part)):
			ch=columns_part[idx]
			if(ch == '('):
				parentheses_depth=parentheses_depth+1;
			elif(ch == ')'):
				parentheses_depth=parentheses_depth-1;
				assert(parentheses_depth>=0);
			elif(ch == ','):
				if(parentheses_depth==0):
					columns.append( columns_part[start_idx:idx] );
					start_idx=idx+1;
		if(start_idx<len(columns_part)):
			columns.append( columns_part[start_idx:] );
		
		#print(columns);
		columns_removed_hooks=[]
		# get all hooked-columns  (column1, func1(column2,arg1,arg2,arg3), func2(column3)
		for f in columns:
			f=f.strip();
			hooked_column = None;
			original_column_name=f;

			left_parentheses_idx=f.find('(');
			if(left_parentheses_idx>0):
				if(f.find(')')<0):
					print("error with[%s]" %f);
					return None;
				func_name=f[0:left_parentheses_idx];
				if(func_name in global_hooks):
					hook=global_hooks[func_name];

					comma_idx=f.find(',');	
					right_parentheses_idx = f.find(')');
					if(comma_idx > 0): # has other arguments
						original_column_name = f[left_parentheses_idx+1:comma_idx];
						args = f[comma_idx+1: right_parentheses_idx].split(',');
						hooked_column = HookedColumn(original_column_name, hook, args);
					else: # only one arguments
						original_column_name = f[left_parentheses_idx+1:right_parentheses_idx];
						hooked_column = HookedColumn(original_column_name, hook, None);
						
			hsqlparser.hooked_columns.append(hooked_column);
			columns_removed_hooks.append(original_column_name);

		hsqlparser.sql = "select %s %s" %( ','.join(columns_removed_hooks), from_part );

		return hsqlparser;

class HSQL:
	'''

	'''
	def __init__(self, host, user, pswd, db, hsql=""):
		self.host = host;
		self.user = user;
		self.pswd = pswd;
		self.db   = db;
		self.hsql = hsql;

		self.conn=MySQLdb.connect(self.host, self.user, self.pswd, self.db);

		load_hooks();

	def execute(self, hsql_str):
		hsqlparser = HSQLParser.parse_hsql(hsql_str);
		if(hsqlparser is None):
			return
		#hsqlparser.DebugPrint();

		cursor = self.conn.cursor();
		cursor.execute(hsqlparser.sql);

		#print(cursor.description);
		result=""
		for r in cursor:
			for fidx in range(0, len(cursor.description)):
				column_name = cursor.description[fidx][0];
				hooked_column = hsqlparser.hooked_columns[fidx];
				if(hooked_column is not None):
					result = result + "%-20s" %(column_name+":");
					text = hooked_column.hook.func(column_name, r[fidx], hooked_column.args);
					text = text.replace('\n', '\\n');
					result = result + text;
				else:
					result = result + "%-20s%s" %(column_name+":", r[fidx]);
				result = result + "\n";
		return result;


if __name__ == '__main__':
	helpstr='''
--help                      # show this message
-u {mysql.user}             # user of mysql
-p {mysql.password}         # password of mysql
-h {mysql.host}             # host of mysql
-d {mysql.db}               # db of mysql
-e {hsql}                   # execute the hsql and quit
	'''

	# parse arguments
	user=None
	#password=None
	password=None
	db=None
	host='localhost'
	e_hsql=None
	opts, args = getopt.getopt(sys.argv[1:], 'u:p:h:d:e:', ['help'])
	for op,value in opts:
		if op == '-u':
			user = value;
		elif op == '-p':
			password = value;
		elif op == '-h':
			host = value;
		elif op == '-d':
			db = value;
		elif op == '-e':
			e_hsql = value;
		elif op == '--help':
			print(helpstr);
			exit();
		else:
			print("unknown option[%s]", op);
			print(helpstr);
			exit();

	if(user is None or db is None):
		print(helpstr);
		print('you have to give {user} and {db}');
		exit();

	# get password if need
	if(password is None):
		password = getpass.getpass();

	if(e_hsql):
		hsql = HSQL(host, user, password, db);
		hsql.execute(e_hsql);
		exit();

	hsql = HSQL(host, user, password, db);

	input_hsql_str = None
	while(True):
		input_hsql_str = raw_input('>');
		#input_hsql_str = raw_input("MC ID (CTRL-D = done, 0 = sets, ? = lookup): ");
		input_hsql_str = input_hsql_str.strip();
		if(input_hsql_str):
			if(input_hsql_str.lower() == 'quit' or input_hsql_str.lower() == 'exit'):
				break;
			result = hsql.execute(input_hsql_str);
			print(result);

