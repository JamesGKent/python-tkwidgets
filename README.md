# python-tkwidgets
A collection of widgets for python built on top of tkinter

## linkscrolledtext
a scrolled textbox with helper functions for adding "hyperlinks" that can trigger an action when clicked, and display a tooltip when the mouse is hovered over the link.

## scrolledframe
a scrolled frame with support for auto show/hide of scrollbars, and stretching the inner contents to fit the frame if its smaller.
simply use this widget as a normal frame to add widgets, then pack/grid/place as normal.  
To enable the stretching of the inner widgets use the correct options with grid or pack.  
to create with scrollbars:  
```
myframe = scrolledframe.ScrolledFrame(root, scrollbars='auto')  
```
valid options are: 'auto', 'both', 'x', 'y', None
where auto will show/hide the scrollbars as required and all other options are fixed.

## debuglogger
an interactive debugging/logging module that redirects any sydout or stderr output either to a log file or an on screen textbox for interactive use.  
example use:
```
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
  ```
