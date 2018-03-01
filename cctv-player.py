import sys
import os
import Tkinter
import vlc

# Config vars
window_title = ""
max_vids_x = 3
sources = {}

# Check for config file
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
cnffilepath = os.path.join(dirname, "cctv-player.conf")
try:
	cnffile = open(cnffilepath, 'r')
	for line in cnffile:
		data = line.strip('\n').strip('\r')
		if '#' not in data:
			if '=' in data:
				variable, value = data.split('=', 1)
				variable = variable.strip(' ')
				value = value.lstrip(' ')
				if variable == 'window_title':
					window_title = value
				elif variable == 'max_vids_x':
					max_vids_x = value
				elif variable[:6] == 'source':
					variable, sourcenum = variable.split('-', 1)
					sources[int(sourcenum)] = value
				else:
					print("Unknown config option: "+variable+"\n")
	cnffile.close()
except:
	print "No config file found. ["+cnffilepath+"]\n"

# Startup config window
cnf_root = Tkinter.Tk()
cnf_root.title('Config')
cnf_root.protocol("WM_DELETE_WINDOW", sys.exit)
cnf_root.columnconfigure(1, weight=1)

cnf_sources_labels = {}
cnf_sources_addresses = {}
cnf_sources_entries = {}
cnf_sources_counter = 0

# Add source field
def cnf_add_source(src=''):
	global cnf_sources_counter
	global cnf_sources_counter
	global cnf_sources_addresses
	global cnf_sources_entries
	global cnf_sources_labels
	global cnf_ok
	
	cnf_sources_counter += 1
	cnf_sources_labels[cnf_sources_counter] = Tkinter.Label(cnf_root, text='Source '+str(cnf_sources_counter))
	cnf_sources_addresses[cnf_sources_counter] = Tkinter.StringVar()
	cnf_sources_addresses[cnf_sources_counter].set(src)
	cnf_sources_entries[cnf_sources_counter] = Tkinter.Entry(cnf_root, textvariable=cnf_sources_addresses[cnf_sources_counter])
	cnf_sources_labels[cnf_sources_counter].grid(row=(2+cnf_sources_counter), column=0)
	cnf_sources_entries[cnf_sources_counter].grid(row=(2+cnf_sources_counter), column=1, sticky=(Tkinter.E, Tkinter.W))
	# Move the OK button
	cnf_ok.pack_forget()
	cnf_ok.grid(row=(3+cnf_sources_counter), column=0)

# Window title
cnf_window_title = Tkinter.StringVar()
cnf_window_title.set(window_title)
cnf_label_title = Tkinter.Label(cnf_root, text='Window Title:')
cnf_label_title.grid(row=0, column=0)
cnf_title = Tkinter.Entry(cnf_root, textvariable=cnf_window_title)
cnf_title.grid(row=0, column=1, sticky=Tkinter.W)

# Max videos per row
cnf_mvx = Tkinter.StringVar()
cnf_mvx.set(max_vids_x)
cnf_label_max_vids_x = Tkinter.Label(cnf_root, text='Max Videos per row:')
cnf_label_max_vids_x.grid(row=1, column=0)
cnf_max_vids_x = Tkinter.OptionMenu(cnf_root, cnf_mvx, 1, 2, 3, 4, 5)
cnf_max_vids_x.grid(row=1, column=1, sticky=Tkinter.W)

# Add source button
cnf_label_sources = Tkinter.Label(cnf_root, text='Soures:')
cnf_label_add_source = Tkinter.Button(cnf_root, text='ADD SOURCE', command=cnf_add_source)
cnf_label_sources.grid(row=2, column=0)
cnf_label_add_source.grid(row=2, column=1, sticky=Tkinter.W)

# OK button
cnf_ok = Tkinter.Button(cnf_root, text="OK", command=cnf_root.destroy)
cnf_ok.grid(row=(3+cnf_sources_counter), column=0)

# Add sources already defined in config
for s in sources.values():
	cnf_add_source(s)

cnf_root.mainloop()

# Update config vars
window_title = cnf_window_title.get()
max_vids_x = int(cnf_mvx.get())
sources = {}
for (k,s) in cnf_sources_addresses.items():
	sources[k] = s.get()

# Main video player element class
class video_element:
	def __init__(self, address, root, fullscreen=False):
		self.root = root
		self.address = address
		self.video_x = vids_x
		self.video_y = vids_y
		# Outer frame
		self.frame = Tkinter.Frame(self.root)
		# Inner controls frame
		self.controlframe = Tkinter.Frame(self.frame)
		# Inner video frame
		self.vidframe = Tkinter.Frame(self.frame)
		# Canvas for video player
		self.canvas = Tkinter.Canvas(self.vidframe)
		self.canvas.pack(fill=Tkinter.BOTH, expand=Tkinter.YES)
		self.vidframe.rowconfigure(0, weight=1)
		self.vidframe.columnconfigure(0, weight=1)
		self.vidframe.grid(row=0, column=0, sticky=(Tkinter.E, Tkinter.W, Tkinter.N, Tkinter.S))
		self.frame.rowconfigure(0, weight=1)
		self.frame.columnconfigure(0, weight=1)
		if fullscreen == False:
			self.frame.grid(row=vids_y, column=vids_x, sticky=(Tkinter.E, Tkinter.W, Tkinter.N, Tkinter.S))
		else:
			self.frame.grid(row=0, column=0, sticky=(Tkinter.E, Tkinter.W, Tkinter.N, Tkinter.S))
		self.player = vlci.media_player_new()
		self.video = vlci.media_new(self.address)
		self.player.set_media(self.video)
		if os.name == "nt":
			self.player.set_hwnd(self.vidframe.winfo_id())
		else:
			self.player.set_xwindow(self.vidframe.winfo_id())
		# Control buttons
		if fullscreen == False:
			self.b_play = Tkinter.Button(self.controlframe, text="PLAY", command=self.play)
			self.b_play.pack(side=Tkinter.LEFT)
			self.b_stop = Tkinter.Button(self.controlframe, text="STOP", command=self.stop)
			self.b_stop.pack(side=Tkinter.LEFT)
			self.b_fullscreen = Tkinter.Button(self.controlframe, text="FULLSCREEN", command=self.fullscreen)
			self.b_fullscreen.pack(side=Tkinter.LEFT)
			self.controlframe.grid(row=1, column=0)
		else:
			self.b_play = Tkinter.Button(self.controlframe, text="PLAY", command=self.play)
			self.b_play.pack(side=Tkinter.LEFT)
			self.b_stop = Tkinter.Button(self.controlframe, text="STOP", command=self.stop)
			self.b_stop.pack(side=Tkinter.LEFT)
			self.b_close = Tkinter.Button(self.controlframe, text="CLOSE", command=self.close)
			self.b_close.pack(side=Tkinter.LEFT)
			self.controlframe.grid(row=1, column=0)
			self.root.protocol("WM_DELETE_WINDOW", self.close)
			self.play()

	def play(self):
		self.player.play()

	def stop(self):
		self.player.stop()

	def fullscreen(self):
		self.stop()
		self.fswin = Tkinter.Tk()
		self.fswin.title(self.root.title()+" "+str(self.video_x-1)+":"+str(self.video_y))
		self.fswin.rowconfigure(0, weight=1)
		self.fswin.columnconfigure(0, weight=1)
		self.fs_video_element = video_element(self.address, self.fswin, True)
		maximise_window(self.fswin)
		self.fswin.bind('<Configure>', self.resize_fs_window)
		self.fswin.mainloop()

	def close(self):
		self.stop()
		self.root.destroy()

	def resize_fs_window(self, event):
		self.fs_video_element.canvas.config(width=event.width, height=event.height)

# Handle window resize
def resize_window(event):
	for v in video_elements.values():
		v.canvas.config(width=event.width, height=event.height)

def maximise_window(root):
	try:
		root.winfo_toplevel().wm_state('zoomed')
	except:
		w = root.winfo_screenwidth()
		h = root.winfo_screenheight() - 60
		geom_string = "%dx%d+0+0" % (w,h)
		root.winfo_toplevel().wm_geometry(geom_string)

# Root window
root = Tkinter.Tk()
root.protocol("WM_DELETE_WINDOW", sys.exit)
# Maximise on startup
maximise_window(root)
root.title(window_title)
for i in range(10):
    root.rowconfigure(i, weight=1)
    root.columnconfigure(i, weight=1)

# Initialize variables
video_elements = {}
vids_x = 0
vids_y = 0

# VLC instance
#vlci = vlc.Instance('--no-xlib --file-caching=30000')
vlci = vlc.Instance()

# Set up each source
for (number, source) in sources.items():
	vids_x += 1
	if vids_x > max_vids_x:
		vids_y += 1
		vids_x = 1
	video_elements[number] = video_element(source, root)

# Set up handler for window size changes
root.bind('<Configure>', resize_window)

root.mainloop()
