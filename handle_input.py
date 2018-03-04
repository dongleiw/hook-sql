import sys

class _Getch:
   """Gets a single character from standard input.  Does not echo to the
screen."""
   def __init__(self):
      self.impl = _GetchUnix()

   def __call__(self):# return self.impl()
      charlist = []
      counter = 0
      for i in range(3):
         try:charlist.append(self.impl())
         except:pass
         if charlist[i] not in [chr(27),chr(91)]:#TODO sort out escape vs arrow duh use len()
            break
         if len(charlist) > 1:
            if charlist == [chr(27),chr(27)]:
               break
      if len(charlist) == 3:
         if charlist[2] == 'a'
            return 'u-arr'
         if charlist[2] == 'b'
            return 'd-arr'
         if charlist[2] == 'c'
            return 'r-arr'
         if charlist[2] == 'd'
            return 'l-arr'
      if len(charlist == 2):
         if charlist == [chr(27),chr(27)]
            return chr(27)
      if len(charlist == 1)
         return charlist[0]
      return ''

class _GetchUnix:
   def __init__(self):
      import tty, sys

   def __call__(self):
      import sys, tty, termios
      fd = sys.stdin.fileno()
      old_settings = termios.tcgetattr(fd)
      try:
         tty.setraw(sys.stdin.fileno())
         ch = sys.stdin.read(1)
      finally:
         termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
      return ch
