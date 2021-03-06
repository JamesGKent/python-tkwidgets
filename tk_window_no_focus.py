#!python3.4

import tkinter as tk
from ctypes import windll, wintypes

GWL_STYLE = -16
GWL_EXSTYLE = -20

WS_CHILD = 0x40000000

WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
WS_EX_NOACTIVATE = 0x08000000

SWP_FRAMECHANGED = 0x0020
SWP_NOACTIVATE = 0x0010
SWP_NOMOVE = 0x0002
SWP_NOSIZE = 0x0001

#TODO fix imports to automatically pic 32 bit or 64 bit versions depending on windows version
# write short names for functions and specify argument and return types
GetWindowLong = windll.user32.GetWindowLongW
GetWindowLong.restype = wintypes.ULONG
GetWindowLong.argtpes = (wintypes.HWND, wintypes.INT)

SetWindowLong = windll.user32.SetWindowLongW
SetWindowLong.restype = wintypes.ULONG
SetWindowLong.argtpes = (wintypes.HWND, wintypes.INT, wintypes.ULONG)

SetWindowPos = windll.user32.SetWindowPos

def find_root_window(win): # takes tkinter window ref
	w_id = win.winfo_id() # gets handle
	style = GetWindowLong(w_id, GWL_STYLE) # get existing style
	newstyle = style & ~WS_CHILD # remove child style
	res = SetWindowLong(w_id, GWL_STYLE, newstyle) # set new style
	res = SetWindowPos(w_id, 0, 0,0,0,0, SWP_FRAMECHANGED | SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE)
	hwnd = int(root.wm_frame(), 16) # find handle of parent
	res = SetWindowLong(w_id, GWL_STYLE, style) # set back to old style
	res = SetWindowPos(w_id, 0, 0,0,0,0, SWP_FRAMECHANGED | SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE)
	return hwnd # return parents handle

def set_no_focus(hwnd):
	style = GetWindowLong(hwnd, GWL_EXSTYLE) # get existing style
	style = style & ~WS_EX_TOOLWINDOW # remove toolwindow style
	style = style | WS_EX_NOACTIVATE | WS_EX_APPWINDOW
	res = SetWindowLong(hwnd, GWL_EXSTYLE, style)
	res = SetWindowPos(hwnd, 0, 0,0,0,0, SWP_FRAMECHANGED | SWP_NOACTIVATE | SWP_NOMOVE | SWP_NOSIZE)
    
def push_me():
	print('you pushed me!')

def focus_me(event):
	root.focus_force()
	
root = tk.Tk()
root.wm_attributes("-topmost", 1)
tk.Button(root, text="Push me", command=push_me).pack()
e = tk.Entry(root)
e.pack()
e.bind('<Button-1>', focus_me) # if we have a widget that must have focus it needs to be bound
root.update() # for some reason, window style is messed with after window creation, update to get past this
hwnd = find_root_window(root)
if hwnd:
	set_no_focus(hwnd)
root.mainloop()
