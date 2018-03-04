import sys
import tty
import termios

def getch():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
	   tty.setraw(sys.stdin.fileno())
	   ch = sys.stdin.read(1)
	   if(ch == '\x1b'):
			ch = ch + sys.stdin.read(1);
			if(ch == '\x1b['):
				ch = ch + sys.stdin.read(1);
	finally:
	   termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
	return ch

def refresh(text):
	sys.stdout.write('\r' + ' '*len(text));
	sys.stdout.write('\r');
	sys.stdout.write(text);


history_input=[]
history_cursor=0

count=30
input_buf=[]
input_cursor=0
while(count>0):
	ch = getch();
	if(ch.isalnum()):
		input_buf.insert(input_cursor, ch);
		input_cursor=input_cursor+1
		sys.stdout.write(ch);
	else:
		print(type(ch), len(ch), ch);
	count=count-1;
