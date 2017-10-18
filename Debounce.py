try:
	import tkinter as tk
except ImportError:
	import Tkinter as tk

__all__ = [
	'Debounce',
	'DebounceTk',
	'DebounceToplevel',
	'DebounceFrame',
]

class Debounce():
	'''
	When holding a key down, multiple key press and key release events are fired in
	succession. Debouncing is implemented in order to squash these repeated events
	and know when the "real" KeyRelease and KeyPress events happen.
	Use by subclassing a tkinter widget along with this class:
		class DebounceTk(Debounce, tk.Tk):
			pass
	'''
	def bind(self, event, function, debounce=True):
		'''
		Override the bind method, acts as normal binding if not KeyPress or KeyRelease
		type events, optional debounce parameter can be set to false to force normal behavior
		'''
		if not hasattr(self, '_binding_dict'):
			self._binding_dict = {}
		if not hasattr(self, '_bind_base_class'):
			for base in self.__class__.__bases__:
				if base.__name__ != 'Debounce':
					self._bind_base_class = base
					break
		ev = event.replace("<", "").replace(">", "").split('-')
		if (('KeyPress' in ev) or ('KeyRelease' in ev)) and debounce:
			if len(ev) == 2:
				evname = ev[1]
			else:
				evname = ev[0]
			if evname in self._binding_dict:
				d = self._binding_dict[evname]
			else:
				d = {'has_prev_key_release':None, 'has_prev_key_press':False}

			d[ev[0]] = function

			self._binding_dict[evname] = d
			if ev[0] == 'KeyPress':
				self._bind_base_class.bind(self, event, self._on_key_press_repeat)
			elif ev[0] == 'KeyRelease':
				self._bind_base_class.bind(self, event, self._on_key_release_repeat)
				
		else:
			self._bind_base_class.bind(self, event, function)
		
	def _get_evdict(self, event):
		'''
		internal method used to get the dictionary that stores the special binding info
		'''
		evdict = None
		generic = False
		if event.type == '2':
			evname = event.keysym
			if evname not in self._binding_dict:
				generic = True
				evname = 'KeyPress'
			evdict = self._binding_dict[evname]
		elif event.type == '3':
			evname = event.keysym
			if evname not in self._binding_dict:
				generic = True
				evname = 'KeyRelease'
			evdict = self._binding_dict[evname]
		return evdict, generic
		
	def _on_key_release(self, event):
		'''
		internal method, called by _on_key_release_repeat only when key is actually released
		this then calls the method that was passed in to the bind method
		'''
		evdict, generic = self._get_evdict(event)
		if not evdict:
			return
		evdict['has_prev_key_release'] = None
		
		evdict['KeyRelease'](event)
		if generic:
			self._binding_dict['KeyPress'][event.keysym] = False
		else:
			evdict['has_prev_key_press'] = False
		
	def _on_key_release_repeat(self, event):
		'''
		internal method, called by the 'KeyRelease' event, used to filter false events
		'''
		evdict, generic = self._get_evdict(event)
		if not evdict:
			return
		evdict["has_prev_key_release"] = self.after_idle(self._on_key_release, event)
		
	def _on_key_press(self, event):
		'''
		internal method, called by _on_key_press_repeat only when key is actually pressed
		this then calls the method that was passed in to the bind method
		'''
		evdict, generic = self._get_evdict(event)
		if not evdict:
			return
		evdict['KeyPress'](event)
		if generic:
			evdict[event.keysym] = True
		else:
			evdict['has_prev_key_press'] = True
		
	def _on_key_press_repeat(self, event):
		'''
		internal method, called by the 'KeyPress' event, used to filter false events
		'''
		evdict, generic = self._get_evdict(event)
		if not evdict:
			return
		if not generic:
			if evdict["has_prev_key_release"]:
				self.after_cancel(evdict["has_prev_key_release"])
				evdict["has_prev_key_release"] = None
			else:
				if evdict['has_prev_key_press'] == False:
					self._on_key_press(event)
		else:
			if (event.keysym not in evdict) or (evdict[event.keysym] == False):
				self._on_key_press(event)
				
				
		
class DebounceTk(Debounce, tk.Tk):
	pass

class DebounceToplevel(Debounce, tk.Toplevel):
	pass
	
class DebounceFrame(Debounce, tk.Frame):
	pass
	
if __name__ == '__main__':
	def press(event):
		print("pressed:", event.keysym, file=sys.stderr)
		
	def release(event):
		print("released:", event.keysym, file=sys.stderr)
		
	def press2(event):
		print("pressed2:", event.keysym, file=sys.stderr)
		
	def release2(event):
		print("released2:", event.keysym, file=sys.stderr)

	root = DebounceTk()
	frame = DebounceFrame(root, width=100, height=100)
	frame.bind("<KeyRelease-a>", release)
	frame.bind("<KeyPress-a>", press)
	frame.bind("<KeyRelease-s>", release)
	frame.bind("<KeyPress-s>", press)

	frame.bind("<KeyRelease>", release2)
	frame.bind("<KeyPress>", press2)

	frame.pack()
	frame.focus_set()

	root.mainloop()
