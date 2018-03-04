import sys
import tty
import termios

class InputHandler:
	'''
		handle input things
	'''
	def __init__(self):
		pass

	def console_clear(self):
		sys.stdout.write('\r' + ' '*(len(self.current_input)+1));

	def console_refresh(self):
		sys.stdout.write('\r');
		sys.stdout.write( ''.join(self.current_input) );

	def move_cursor(self):
		rep=''.join(self.current_input[:self.current_cursor]);
		sys.stdout.write('\r' + rep);

	def new_line(self):
		sys.stdout.write('\r\n');

	def console_width(self):
		rows, columns = os.popen('stty size', 'r').read().split()
		return columns;

	def process_ch(self, ch):
		'''
			process user input @ch
			return True is `Enter` is hit.
		'''
		if(ch.isalnum()):
			self.current_input.insert(self.current_cursor, ch);
			self.current_cursor=self.current_cursor+1
			sys.stdout.write(ch);
		elif(ch == '\x7f'): #backspace
			if(self.current_cursor>0):
				self.console_clear();
				self.current_cursor=self.current_cursor-1;
				self.current_input.pop(self.current_cursor);
				self.console_refresh();
		elif(ch == '\x1b[A'): # up-arrow
			if(self.history_cursor > 0):
				self.console_clear();
				self.history_cursor=self.history_cursor-1;
				self.current_input=self.history_input[self.history_cursor];
				self.current_cursor=len(self.current_input);
				self.console_refresh();
		elif(ch == '\x1b[B'): # down-arrow
			self.console_clear();
			if(self.history_cursor+1 < len(self.history_input)):
				self.history_cursor=self.history_cursor+1
				self.current_input=self.history_input[self.history_cursor]
				self.current_cursor=len(self.current_input);
			else:
				self.current_input=[]
				self.current_cursor=0
			self.console_refresh();
	
		elif(ch == '\x1b[C'): # right-arrow
			if(self.current_cursor < len(self.current_input)):
				self.current_cursor = self.current_cursor+1;
				self.move_cursor();
		elif(ch == '\x1b[D'): # down-arrow
			if(self.current_cursor>0):
				self.current_cursor = self.current_cursor-1;
				self.move_cursor();
		elif(ch == '\r'): #enter
			self.history_input.append(self.current_input);
			self.history_cursor=len(self.history_input);
			self.input = ''.join(self.current_input);
			self.current_input=[]
			self.current_cursor=0

			self.new_line();
			return True;
		else:
			print(type(ch), ch);
		return False;

	def Run(self, cb, prompt, exitcode=1):
		'''
			@cb -> callback(text):
				  If @exitcode is returned by @cb, exit
		'''

		# init
		self.history_input = [];
		self.history_cursor = 0;
		self.current_input = [];
		self.current_cursor = 0;
		self.input = ""

		fd = sys.stdin.fileno()
		old_settings = termios.tcgetattr(fd)
		try:
			tty.setraw(sys.stdin.fileno())

			while(True):
				# getch
				ch = sys.stdin.read(1)
				if(ch == '\x1b'): # escape
					ch = ch + sys.stdin.read(1);
					if(ch == '\x1b['):
						ch = ch + sys.stdin.read(1);
				need_execute = self.process_ch(ch);
				if(need_execute):
					need_exit = cb(self.input);
					self.console_refresh();
					if(need_exit):
						break;
		finally:
		   termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		return ch


def callback(text):
	print('execute %s' %text);
	return (text == 'exit' or text == 'quit');

input_handler = InputHandler()
input_handler.Run(callback, True);
