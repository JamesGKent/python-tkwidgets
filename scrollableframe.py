####
##	To Do
##		make so that using ScrolledFrame as parent actually uses child frame
##		simplify scrollbar logic if possible
##		test with grid and pack geom managers
####
__all__ = ['ScrolledFrame']

try:
	import tkinter as tk
except ImportError:
	import Tkinter as tk
	
class ScrolledFrame(tk.Frame):
	def __init__(self, master=None, *args, **kwargs):
		self.scrollbars = None
		self.scroll_shown= [False, False]
		if ('scrollbars' in kwargs):
			self.scrollbars = kwargs['scrollbars']
			del kwargs['scrollbars']
			
		tk.Frame.__init__(self, master, *args, **kwargs)
		
		self.grid_columnconfigure(1, weight=1)
		self.grid_rowconfigure(1, weight=1)
		
		self.vsb = tk.Scrollbar(self, orient='vertical')
		self.hsb = tk.Scrollbar(self, orient='horizontal')
		self.vsb.opts = {'column':2, 'row':1, 'sticky':'nesw'}
		self.hsb.opts = {'column':1, 'row':2, 'sticky':'nesw'}
		
		self.canvas = tk.Canvas(self, bd=0, highlightthickness=0,
								yscrollcommand=self.vsb.set,
								xscrollcommand=self.hsb.set)
		self.canvas.grid(column=1, row=1, sticky='nesw')
		
		self.vsb.config(command=self.canvas.yview)
		self.hsb.config(command=self.canvas.xview)
		
		self.canvas.xview_moveto(0)
		self.canvas.yview_moveto(0)
		
		self.canvas.bind('<Configure>', self._reconfigure)
		
		self.frame = tk.Frame(self.canvas)
		
		self.frame_id = self.canvas.create_window(0, 0, window=self.frame, anchor='nw')
		
		self.frame.bind('<Configure>', self._reconfigure)
		
		self.update_idletasks()
		self._showscrollbars()
	
	def _reconfigure(self, event=None):
		f_reqsize = (self.frame.winfo_reqwidth(), self.frame.winfo_reqheight())
#		f_size = (self.frame.winfo_width(), self.frame.winfo_height()) # shouldn't be needed?
#		if (f_size[0] > f_reqsize[0]):
#			self.canvas.itemconfigure(self.frame_id, width=f_reqsize[0])
#		if (f_size[1] > f_reqsize[1]):
#			self.canvas.itemconfigure(self.frame_id, height=f_reqsize[1])
		c_size = (self.canvas.winfo_width(), self.canvas.winfo_height())
		self.canvas.config(scrollregion="0 0 %s %s" % f_reqsize)
		if (f_reqsize[0] < c_size[0]):
			self.canvas.itemconfigure(self.frame_id, width=c_size[0])
		else:
			self.canvas.itemconfigure(self.frame_id, width=f_reqsize[0])
		if (f_reqsize[1] < c_size[1]):
			self.canvas.itemconfigure(self.frame_id, height=c_size[1])
		else:
			self.canvas.itemconfigure(self.frame_id, height=f_reqsize[1])
			
		if (self.scrollbars == 'auto'):
			self._showscrollbars()
			
	def _showscrollbars(self):
		if (self.scrollbars == 'both'):
			self.vsb.grid(**self.vsb.opts)
			self.hsb.grid(**self.hsb.opts)
		elif (self.scrollbars == 'x'):
			self.vsb.grid_remove()
			self.hsb.grid(**self.hsb.opts)
		elif (self.scrollbars == 'y'):
			self.vsb.grid(**self.vsb.opts)
			self.hsb.grid_remove()
		elif (self.scrollbars == 'auto'):
			f_reqsize = (self.frame.winfo_reqwidth(), self.frame.winfo_reqheight())
			c_size = (self.canvas.winfo_width(), self.canvas.winfo_height())
			# start with vertical
			if self.scroll_shown[1] == False: # not showing
				if (f_reqsize[1] > c_size[1]): # height is greater than canvas so show
					self.canvas.configure(width=self.canvas.winfo_width() - self.vsb.winfo_reqwidth())
					self.vsb.grid(**self.vsb.opts)
					self.scroll_shown[1] = True
			else:
				if (f_reqsize[1] <= c_size[1]): # height is less than canvas so don't show
					self.vsb.grid_remove()
					self.canvas.configure(width=self.canvas.winfo_width() + self.vsb.winfo_reqwidth())
					self.scroll_shown[1] = False
					
			# now horizontal
			if self.scroll_shown[0] == False: # not showing
				if (f_reqsize[0] > c_size[0]): # width is greater than canvas so show
					self.canvas.configure(height=self.canvas.winfo_height() - self.hsb.winfo_reqheight())
					self.hsb.grid(**self.hsb.opts)
					self.scroll_shown[0] = True
			else:
				if (f_reqsize[0] <= c_size[0]): # width is less than canvas so don't show
					self.hsb.grid_remove()
					self.canvas.configure(height=self.canvas.winfo_height() + self.hsb.winfo_reqheight())
					self.scroll_shown[0] = False
	
	def resize(self):
		self._reconfigure()
		
if __name__ == '__main__':
	frames = []
	def add_row():
		frame = tk.Frame(sf.frame)
		frame.grid_columnconfigure(1, weight=1)
		frame.grid_columnconfigure(2, weight=1)
		frame.grid_rowconfigure(1, weight=1)
		num = len(frames)
		tk.Label(frame, text='Test %i' % num).grid(column=1, row=1, sticky="nesw")
		tk.Entry(frame).grid(column=2, row=1, sticky="nesw")
		frame.grid(column=1, row=num, sticky='nesw')
		sf.frame.grid_rowconfigure(num, weight=1)
		frames.append(frame)
		sf.resize()
		
	def del_row():
		frame = frames.pop()
		frame.grid_forget()
		frame.destroy()
		num = len(frames)
		sf.frame.grid_rowconfigure(num, weight=0)
		sf.resize()
		
	def add_column():
		pass
		
	def del_column():
		pass
		
	root = tk.Tk()
	
	sf = ScrolledFrame(root, scrollbars='auto')
	sf.frame.grid_columnconfigure(1, weight=1)
	sf.grid(column=1, row=1, columnspan=2, rowspan=2, sticky='nesw')
	tk.Button(root, text='-', command=del_row).grid(column=3, row=1, sticky='nesw')
	tk.Button(root, text='+', command=add_row).grid(column=3, row=2, sticky='nesw')
	tk.Button(root, text='-', command=del_column).grid(column=1, row=3, sticky='nesw')
	tk.Button(root, text='+', command=add_column).grid(column=2, row=3, sticky='nesw')
	
	root.grid_columnconfigure(1, weight=1)
	root.grid_columnconfigure(2, weight=1)
	root.grid_rowconfigure(1, weight=1)
	root.grid_rowconfigure(2, weight=1)
	
	root.mainloop()