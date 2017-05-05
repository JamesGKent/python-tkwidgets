
__all__ = ["LinkScrolledText"]

try:
	from tkinter import scrolledtext
except ImportError:
	import ScrolledText as scrolledtext
	
class HyperlinkManager(object):
	"""A class to easily add clickable hyperlinks to Text areas.
	Usage:
	  callback = lambda : webbrowser.open("http://www.google.com/")
	  text = tk.Text(...)
	  hyperman = tkHyperlinkManager.HyperlinkManager(text)
	  text.insert(tk.INSERT, "click me", hyperman.add(callback))
	From http://effbot.org/zone/tkinter-text-hyperlink.htm
	"""
	def __init__(self, text, statusfunc=None):
		self.text = text
		self.statusfunc = statusfunc
		self.text.tag_config("hyper", foreground="blue", underline=1)
		self.text.tag_bind("hyper", "<Enter>", self._enter)
		self.text.tag_bind("hyper", "<Leave>", self._leave)
		self.text.tag_bind("hyper", "<Button-1>", self._click)
		self.reset()

	def reset(self):
		self.links = {}

	def add(self, action, tooltip=None):
		"""Adds an action to the manager.
		:param action: A func to call.
		:return: A clickable tag to use in the text widget.
		"""
		tag = "hyper-%d" % len(self.links)
		self.links[tag] = [action, tooltip]
		return ("hyper", tag)

	def _enter(self, event):
		self.text.config(cursor="hand2")
		for tag in self.text.tag_names(tk.CURRENT):
			if (tag[:6] == "hyper-"):
				tooltip = self.links[tag][1]
				if self.statusfunc:
					self.statusfunc(tooltip) # don't care if no tooltip as function clears if it doesn't
				return

	def _leave(self, event):
		self.text.config(cursor="")
		if self.statusfunc:
			self.statusfunc()

	def _click(self, event):
		for tag in self.text.tag_names(tk.CURRENT):
			if (tag[:6] == "hyper-"):
				func = self.links[tag][0]
				if func:
					func()
				return

class LinkScrolledText(scrolledtext.ScrolledText):
	"""A class to add hyperlink functionality to a scrolledtext widget
	the link does not actually have to be an actual hyperlink,
	just a callable action.
	an optional tooltip can be provided that will be displayed in the bottom left
	just like a url would be in a browser when hovering over a link.
	"""
	def __init__(self, master=None, *args, **kwargs):
		scrolledtext.ScrolledText.__init__(self, master, *args, **kwargs)
		self.status = tk.Label(self)
		self._hyper = HyperlinkManager(self, self._showstatus)
		self.reset_links()
		
	def _showstatus(self, status=None):
		if status:
			self.status.configure(text=status)
			self.status.place(relx=0, rely=1, anchor='sw')
		else:
			self.status.place_forget()

	def reset_links(self):
		self._hyper.reset()
		
	def insert_hyperlink(self, position, text, action, tag=None, tooltip=None):
		tags = self._hyper.add(action, tooltip)
		if type(tag) == list:
			tags = tags + tag
		elif tag != None:
			tags.append(tag)
		self.insert(position, text, tags)

if __name__ == "__main__":
	try:
		import tkinter as tk
	except ImportError:
		import Tkinter as tk
	root = tk.Tk()
	tb = LinkScrolledText(root)
	tb.pack(fill="both", expand=True)
	tb.insert_hyperlink("end", "Test", action=None, tooltip="This is a test")
	root.mainloop()
