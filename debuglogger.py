import logging
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

__all__ = ["logging",
		   "StreamToLogger",
		   "DebugLogger"]
 
class StreamToLogger(object):
	def __init__(self, logger, log_level=logging.INFO):
		self.logger = logger
		self.log_level = log_level
		self.error_types = ["AssertionError", "AttributeError",
							"EOFError", "FloatingPointError",
							"GeneratorExit", "ImportError",
							"IndexError", "KeyError",
							"KeyboardInterrupt", "MemoryError",
							"NameError", "NotImplementedError",
							"OSError", "OverflowError",
							"ReferenceError", "RuntimeError",
							"StopIteration", "SyntaxError",
							"IndentationError", "TabError",
							"SystemError", #"SystemExit", #included for completeness, but illogical to log a normal exit
							"TypeError", "UnboundLocalError",
							"UnicodeError", "UnicodeEncodeError",
							"UnicodeDecodeError", "UnicodeTranslateError",
							"ValueError", "ZeroDivisionError",
							"EnvironmentError", "IOError",
							"WindowsError", "BlockingIOError",
							"ChildProcessError", "ConnectionError",
							"BrokenPipeError", "ConnectionAbortedError",
							"ConnectionRefusedError", "ConnectionResetError",
							"FileExistsError", "FileNotFoundError",
							"InterruptedError", "IsADirectoryError",
							"NotADirectoryError", "PermissionError",
							"ProcessLookupError", "TimeoutError",]

	def write(self, buf):
		for line in buf.rstrip().splitlines():
			self.logger.log(self.log_level, line.rstrip())
		for entry in self.error_types:
			if entry in str(buf):
				root = tk.Tk()
				root.withdraw()
				messagebox.showwarning("Warning", "An error has occured,\ncheck error log")
				root.destroy()

	def flush(self):
		pass

class StdOut(object):
	def __init__(self, parent):
		self.parent = parent
	def write(self, buf):
		self.parent.write(buf, 'stdout')
	def flush(self):
		pass
		
class StdErr(object):
	def __init__(self, parent):
		self.parent = parent
	def write(self, buf):
		self.parent.write(buf, 'stderr')
	def flush(self):
		pass

class DebugLogger(object):
	def __init__(self):
		self.GUI = tk.Toplevel()
		self.GUI.protocol('WM_DELETE_WINDOW', self.GUI.withdraw)
		self.GUI.title("Debug Console")

		self.textbox = ScrolledText(self.GUI)
		self.textbox.configure(state = "disabled")
		self.textbox.pack(fill = "both", expand = True)
		self.textbox.tag_config('stdout', foreground='blue')
		self.textbox.tag_config('stderr', foreground='red')
		self.GUI.focus()
		self.stdout = StdOut(self)
		self.stderr = StdErr(self)

	def write(self, buf, type):
		self.textbox.configure(state = "normal")
		self.textbox.insert(tk.END, str(buf), type)
		self.textbox.configure(state = "disabled")
		self.textbox.see("end")

	def flush(self):
		pass

if __name__ == '__main__':
	import os, sys
	sys.argv.append('-d')
	if ("-d" in sys.argv) or ("-D" in sys.argv):
		debugger = DebugLogger()
		sys.stdout = debugger.stdout
		sys.stderr = debugger.stderr
	else:
		logdir = os.getenv("APPDATA") + "\\applicationame\\"
		if not os.path.isdir(logdir):
			os.makedirs(logdir)
		logfile = logdir + "applicationname.log"
		logging.basicConfig(level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(name)s:%(message)s', filename=logfile, filemode='w')
		sys.stdout = StreamToLogger(logging.getLogger('STDOUT'), logging.INFO) 
		sys.stderr = StreamToLogger(logging.getLogger('STDERR'), logging.ERROR)
	print("test")
	raise(Error)
