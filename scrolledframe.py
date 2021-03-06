try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    import ttk


__all__ = ['ScrolledFrame']

class ScrolledFrame:
    def __init__(self, master=None, *args, **kwargs):
        self._scrollbars = kwargs.pop('scrollbars', None)

        # a list of attributes that the outer frame should handle
        self.outer_attr = set(dir(tk.Widget))

        self.outer_frame = tk.Frame(master)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.vsb = ttk.Scrollbar(self.outer_frame, orient='vertical')
        self.hsb = ttk.Scrollbar(self.outer_frame, orient='horizontal')
        self.vsb.opts = {'column': 2, 'row': 1, 'sticky': 'nesw'}
        self.hsb.opts = {'column': 1, 'row': 2, 'sticky': 'nesw'}

        self.canvas = tk.Canvas(
            self.outer_frame, bd=0, highlightthickness=0,
            yscrollcommand=self.vsb.set,
            xscrollcommand=self.hsb.set)
        self.canvas.grid(column=1, row=1, sticky='nesw')

        self.vsb.config(command=self.canvas.yview)
        self.hsb.config(command=self.canvas.xview)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.canvas.bind('<Configure>', self._reconfigure)

        self.frame = tk.Frame(self.canvas)

        self.frame_id = self.canvas.create_window(
            0, 0, window=self.frame, anchor='nw')

        self.frame.bind('<Configure>', self._reconfigure)

        self.canvas.bind("<Enter>", self._bind_events)
        self.canvas.bind("<Leave>", self._unbind_events)

        self._showscrollbars()

        for attr in [
                'grid_columnconfigure',
                'grid_rowconfigure',
                'winfo_reqwidth',
                'winfo_reqheight',
                'configure']:
            self.outer_attr.discard(attr)

    def __getattr__(self, item):
        '''when an attribute is requested, provide from correct frame'''
        if item in self.outer_attr:
            # geometry attr. (eg pack, destroy, tkraise) passed to self.outer
            return getattr(self.outer_frame, item)
        else:
            # all other attributes (_w, children, etc) passed to self.inner
            return getattr(self.frame, item)

    def __repr__(self):
        return str(self.outer_frame)

    def _reconfigure(self, event=None):
        self.update_idletasks()
        f_reqsize = (self.frame.winfo_reqwidth(), self.frame.winfo_reqheight())
        c_size = (self.canvas.winfo_width(), self.canvas.winfo_height())
        f_width = max(f_reqsize[0], c_size[0])
        f_height = max(f_reqsize[1], c_size[1])

        # ensure scroll region clamped to canvas size if frame req is smaller
        self.canvas.config(scrollregion="0 0 %s %s" % (f_width, f_height))
        self.canvas.itemconfig(self.frame_id, width=f_width, height=f_height)

        if (self._scrollbars == 'auto'):
            self._showscrollbars()

    def _showscrollbars(self):
        if (self._scrollbars == 'both'):
            self.vsb.grid(**self.vsb.opts)
            self.hsb.grid(**self.hsb.opts)
        elif (self._scrollbars == 'x'):
            self.vsb.grid_remove()
            self.hsb.grid(**self.hsb.opts)
        elif (self._scrollbars == 'y'):
            self.vsb.grid(**self.vsb.opts)
            self.hsb.grid_remove()
        elif (self._scrollbars == 'auto'):
            f_reqsize = (
                self.frame.winfo_reqwidth(),
                self.frame.winfo_reqheight())
            # account for frame border
            padding = 2*int(str(self.outer_frame.cget('bd')))
            of_size = (
                self.outer_frame.winfo_width() - padding,
                self.outer_frame.winfo_height() - padding)
            c_size = (self.canvas.winfo_width(), self.canvas.winfo_height())
            vsbw = self.vsb.winfo_reqwidth()
            hsbh = self.hsb.winfo_reqheight()

            # if both smaller
            if (f_reqsize[1] <= of_size[1]) and (f_reqsize[0] <= of_size[0]):
                show_vert = False
                show_horz = False
            # if taller but narrower
            elif (f_reqsize[1] > of_size[1]) and (f_reqsize[0] <= of_size[0]):
                show_vert = True
                # if taller but narrower with scrollbar
                show_horz = (f_reqsize[0] > (of_size[0] - vsbw))
            # wider but shorter
            elif (f_reqsize[1] <= of_size[1]) and (f_reqsize[0] > of_size[0]):
                show_horz = True
                # if wider but shorter with scrollbar
                show_vert = (f_reqsize[1] > (of_size[1] - hsbh))
            else:  # both bigger
                show_vert = True
                show_horz = True

            if show_vert:
                self.canvas.configure(width=of_size[0] - vsbw)
                self.vsb.grid(**self.vsb.opts)
            else:
                self.vsb.grid_remove()
                self.canvas.configure(width=of_size[0])

            if show_horz:
                self.canvas.configure(height=of_size[1] - hsbh)
                self.hsb.grid(**self.hsb.opts)
            else:
                self.hsb.grid_remove()
                self.canvas.configure(height=of_size[1])

    def _bind_events(self, event=None):
        self.frame.bind_all("<Button-4>", self.onmousewheel)
        self.canvas.bind_all("<Button-4>", self.onmousewheel)
        self.frame.bind_all("<Button-5>", self.onmousewheel)
        self.canvas.bind_all("<Button-5>", self.onmousewheel)
        self.frame.bind_all("<MouseWheel>", self.onmousewheel)
        self.canvas.bind_all("<MouseWheel>", self.onmousewheel)

        self.frame.bind_all("<Prior>", self.onkeyscroll)  # pageup
        self.canvas.bind_all("<Next>", self.onkeyscroll)  # pagedown
        self.frame.bind_all("<Home>", self.onkeyscroll)
        self.canvas.bind_all("<End>", self.onkeyscroll)

    def _unbind_events(self, event=None):
        self.frame.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-4>")
        self.frame.unbind_all("<Button-5>")
        self.canvas.unbind_all("<Button-5>")
        self.frame.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<MouseWheel>")

        self.frame.unbind_all("<Prior>")  # pageup
        self.canvas.unbind_all("<Next>")  # pagedown
        self.frame.unbind_all("<Home>")
        self.canvas.unbind_all("<End>")

    def onmousewheel(self, event):
        """Linux uses event.num; Windows / Mac uses event.delta"""
        if event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        return 'break'

    def onkeyscroll(self, event):
        if event.keysym in ['Prior', 'Next', 'Home', 'End']:
            if (event.keysym == 'Prior'):
                self.canvas.yview('scroll', -1, 'pages')
            elif (event.keysym == 'Next'):
                self.canvas.yview('scroll', 1, 'pages')
            elif (event.keysym == 'Home'):
                self.canvas.yview('moveto', 0)
            elif (event.keysym == 'End'):
                self.canvas.yview('moveto', 1)
            return 'break'

    def resize(self):
        self._reconfigure()

    def get_reqwidth(self):
        f_reqwidth = self.frame.winfo_reqwidth()
        # account for frame border
        padding = 2*int(str(self.outer_frame.cget('bd')))
        vsb_width = self.vsb.winfo_width()
        # need vert scrollbar
        if (
                self.frame.winfo_reqheight() >
                (self.outer_frame.winfo_height() - padding)):
            return f_reqwidth + padding + vsb_width
        else:
            return f_reqwidth + padding
