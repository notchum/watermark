

import numpy as np
import cv2, os, argparse
from imutils import paths

import tkinter as tk
from tkinter import ttk, filedialog
import os, threading

# Init Tkinter
root = tk.Tk()
root.minsize(width=550, height=300)
root.maxsize(width=550, height=300)
root.title("Watermarker")
root.geometry("550x300")
root.style = ttk.Style()
root.style.theme_use("xpnative")

outputPath = tk.StringVar()
inputPath = tk.StringVar()
wmarkPath = tk.StringVar()

class WatermarkApp():

    def __init__(self, *args, **kwargs):
        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("StartPage")

    def showFrame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

class ImageViewer():

    def __init__(self, master, image):
        # Create Master
        self.master = master

    def resizeImage(self):
        pass

    def showImage(self):
        pass

class Commands():

    def __init__(self, master):
        # Create Master
        self.master = master

    def saveImage(self):
        pass

class Frame1():

    def __init__(self, master):
        # Create Master
        self.master = master

class MainWindow():

    def __init__(self, master):
        # Create Master
        self.master = master

        # Create ImageViewer
        self.image_viewer = ImageViewer(master)

        # Create WatermarkViewer
        self.wm_viewer = WatermarkViewer(master)

        # Create Commands
        self.commads = Commands(master)

    # Frame 1
    def searchPath(self):
        print("Searching for path...")

        currdir = os.path.expanduser('~')
        titleStr = ''
        if method == "input":
            titleStr = 'Please select an input directory'
        elif method == "output":
            titleStr = 'Please select an output directory'
        tempdir = tk.filedialog.askdirectory(parent=root, initialdir=currdir, title=titleStr)
        if len(tempdir) > 0:
            print ("You chose: %s" % tempdir)

        if method == "input":
            self.inputPath.set(tempdir)
        elif method == "output":
            self.outputPath.set(tempdir)
        elif method == "wmark":
            self.wmarkPath.set(tempdir)

    def disableWidget(self, children):
        for child in children:
            child.configure(state='disabled')

    def enableWidget(self, children):
        for child in children:
            child.configure(state='normal')

class ProgressBar():

    def __init__(self, master):
        # Create Master
        self.master = master

class ImageCropper():

    def __init__(self, master):
        # Create Master
        self.master = master

class Button(ttk.Button):

    def __init__(self, *args, **kwargs):
        ttk.Button.__init__(self, *args, **kwargs)
        self['bg'] = 'red'

class WatermarkViewer():

    def __init__(self, master):
        # Create Master
        self.master = master






















def main():
    app = WatermarkApp()
    app.mainloop()

# Main
if __name__ == "__main__":
    main()