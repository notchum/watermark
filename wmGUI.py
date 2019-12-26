import tkinter as tk
from tkinter import ttk, filedialog
import os

class myGUI:

    outputPath = ''
    inputPath = ''
    wmarkPath = 'wmark.jpg'
    positionSelection = 'lower_right'

    def __init__(self, master):
        self.master = master
        self.alphaN = 80
        master.title("Watermarker")
        master.geometry("300x400")
        master.configure(background='#FBFBFB')

        self.label = tk.Label(master, text="Watermark Transparency:", bg='#FBFBFB', fg='black')
        self.label.pack()

        self.alpha = tk.Scale(master, bg='#FBFBFB', fg='black', from_=0, to=100, orient=tk.HORIZONTAL)
        self.alpha.set(80)
        self.alpha.pack()

        self.label = tk.Label(master, text="Watermark Scale:", bg='#FBFBFB', fg='black')
        self.label.pack()

        self.scale = tk.Scale(master, bg='#458BC6', fg='#FBFBFB', from_=20, to=80, orient=tk.HORIZONTAL)
        self.scale.set(80)
        self.scale.pack()

        self.label = tk.Label(master, text="Position of Watermark:", bg='#FBFBFB', fg='black')
        self.label.pack()

        self.position = ttk.Combobox(master, state="readonly", values=["Upper Left","Upper Center","Upper Right",
                                                                    "Middle Left","Middle Center","Middle Right",
                                                                    "Lower Left","Lower Center","Lower Right"])
        self.position.set("Lower Right")
        self.position.pack()
        self.position.bind('<<ComboboxSelected>>', self.on_select_pos)

        self.label = tk.Label(master, text="Input Path:", bg='#FBFBFB', fg='black')
        self.label.pack()

        self.input = tk.Button(master, text="Browse...", bg='#458BC6', fg='#FBFBFB', command=lambda: self.search_for_dir_path("input"))
        self.input.pack()

        self.label = tk.Label(master, text="Output Path:", bg='#FBFBFB', fg='black')
        self.label.pack()

        self.output = tk.Button(master, text="Browse...", bg='#458BC6', fg='#FBFBFB', command=lambda: self.search_for_dir_path("output"))
        self.output.pack()

        self.label = tk.Label(master, text="Watermark Image:", bg='#FBFBFB', fg='black')
        self.label.pack()

        self.output = tk.Button(master, text="Browse...", bg='#458BC6', fg='#FBFBFB', command=self.search_for_file_path)
        self.output.pack()

        self.close_button = tk.Button(master, bg='#458BC6', fg='#FBFBFB', text="Okay", command=master.quit)
        self.close_button.pack()

    def search_for_dir_path(self, method):
        currdir = os.getcwd()
        titleStr = ''
        if method is "input":
            titleStr = 'Please select an input directory'
        elif method is "output":
            titleStr = 'Please select an output directory'
        tempdir = tk.filedialog.askdirectory(parent=root, initialdir=currdir, title=titleStr)
        if len(tempdir) > 0:
            print ("You chose: %s" % tempdir)

        if method is "input":
            self.inputPath = tempdir
        elif method is "output":
            self.outputPath = tempdir
        elif method is "wmark":
            self.wmarkPath = tempdir

    def search_for_file_path(self):
        currdir = os.getcwd()
        tempdir = tk.filedialog.askopenfilename(parent=root, initialdir=currdir, title='Please select the watermark image')
        if len(tempdir) > 0:
            print ("You chose: %s" % tempdir)

        self.wmarkPath = tempdir

    def on_select_pos(self, event=None):
        print('----------------------------')

        if event: # <-- this works only with bind because `command=` doesn't send event
            print("event.widget:", event.widget.get())
            self.positionSelection = self.position.get()

root = tk.Tk()
my_gui = myGUI(root)
root.mainloop()

_wmark = my_gui.wmarkPath
_input = my_gui.inputPath
_output = my_gui.outputPath
_position = my_gui.positionSelection.replace(" ", "_").lower()
_alpha = my_gui.alpha.get() / 100
_scale = my_gui.scale.get()

print("/bin/python ../watermark.py -i " + _input + " -o " + _output + " -w " + _wmark + " -p " + _position
                                         + " -a " + str(_alpha) + " -s " + str(_scale))

os.system("/bin/python ../watermark.py -i " + _input + " -o " + _output + " -w " + _wmark + " -p " + _position
                                         + " -a " + str(_alpha) + " -s " + str(_scale))