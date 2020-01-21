import tkinter as tk
from tkinter import ttk, filedialog
import os, threading

root = tk.Tk()

class myGUI():

    outputPath = tk.StringVar()
    inputPath = tk.StringVar()
    wmarkPath = tk.StringVar()
    filenamePath = tk.StringVar()
    positionSelection = tk.StringVar()
    positionSelection.set('lower_right')
    rbuttonInitSelection = tk.IntVar()
    rbuttonInitSelection.set(1)
    alphaValue = tk.StringVar()
    scaleValue = tk.StringVar()

    positions = [
        "Upper Left","Upper Center","Upper Right",
        "Middle Left","Middle Center","Middle Right",
        "Lower Left","Lower Center","Lower Right"
    ]

    rbutton_selections = [ # Title, Value
        ("Bulk Photos (Select Input/Output Folders)", 1),
        ("Individual Image (Select Single Image)", 2)
    ]

    def __init__(self, master):
        # Create Master
        self.master = master

        # Define Window Attributes
        self.master.minsize(width=550, height=300)
        self.master.maxsize(width=550, height=300)
        self.master.title("Watermarker")
        self.master.geometry("550x300")

        # Apply a Style
        self.master.style = ttk.Style()
        self.master.style.theme_use("xpnative")

        # Create all of our widgets
        self.create_watermark_options()
        self.create_image_options()
        self.create_bulk_options()
        self.create_single_options()
        self.create_radio_buttons()
        self.create_footer()

        # Go ahead and disable the non-selected label frame
        self.disable_widget(self.singleframe.winfo_children())

    def create_watermark_options(self):
        self.scaleframe = ttk.LabelFrame(self.master, text="Watermark Options")
        self.scaleframe.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.label = ttk.Label(self.scaleframe, text="Watermark Transparency:")
        self.label.grid(row=0, column=0)

        self.alpha = ttk.Scale(self.scaleframe, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_label_alpha)
        self.alpha.set(80)
        self.alpha.grid(row=1, column=0)

        self.label = ttk.Label(self.scaleframe, textvariable=self.alphaValue)
        self.label.grid(row=2, column=0)

        self.label = ttk.Label(self.scaleframe, text="Watermark Scale:")
        self.label.grid(row=0, column=1)

        self.scale = ttk.Scale(self.scaleframe, from_=20, to=80, orient=tk.HORIZONTAL, comman=self.set_label_scale)
        self.scale.set(80)
        self.scale.grid(row=1, column=1)

        self.label = ttk.Label(self.scaleframe, textvariable=self.scaleValue)
        self.label.grid(row=2, column=1)

    def create_image_options(self):
        self.imageframe = ttk.LabelFrame(self.master, text="Image Options")
        self.imageframe.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.label = ttk.Label(self.imageframe, text="Position of Watermark:")
        self.label.grid(row=0, column=0)

        self.position = ttk.Combobox(self.imageframe, state="readonly", values=self.positions)
        self.position.set("Lower Right")
        self.position.grid(row=1, column=0)
        self.position.bind('<<ComboboxSelected>>', self.on_select_pos)

        self.label = ttk.Label(self.imageframe, text="Watermark Image:")
        self.label.grid(row=0, column=1)

        self.output = ttk.Button(self.imageframe, text="Browse...", command=lambda: self.search_for_file_path("wmark"))
        self.output.grid(row=1, column=1)

    def create_bulk_options(self):
        self.bulkframe = ttk.LabelFrame(self.master, text="Bulk Photos")
        self.bulkframe.grid(row=5, column=0, padx=10, sticky="nsew")

        self.label = ttk.Label(self.bulkframe, text="Input Path:")
        self.label.pack()

        self.input = ttk.Button(self.bulkframe, text="Browse...", command=lambda: self.search_for_dir_path("input"))
        self.input.pack()

        self.label = ttk.Label(self.bulkframe, text="Output Path:")
        self.label.pack()

        self.output = ttk.Button(self.bulkframe, text="Browse...", command=lambda: self.search_for_dir_path("output"))
        self.output.pack()

    def create_single_options(self):
        self.singleframe = ttk.LabelFrame(self.master, text="Single Photo")
        self.singleframe.grid(row=5, column=1, padx=10, sticky="nsew")

        self.label = ttk.Label(self.singleframe, text="Input Image:")
        self.label.pack()

        self.input = ttk.Button(self.singleframe, text="Browse...", command=lambda: self.search_for_file_path("input"))
        self.input.pack()

        self.label = ttk.Label(self.singleframe, text="Output Image Filename:")
        self.label.pack()

        self.output = ttk.Button(self.singleframe, text="Save...", command=self.save_file_path)
        self.output.pack()

    def create_radio_buttons(self):
        self.radiobuttons = []

        for title, value in self.rbutton_selections:
            radio = ttk.Radiobutton(self.master, text=title, variable=self.rbuttonInitSelection, command=self.show_choice, value=value)
            radio.grid(row=2+value, column=0, columnspan=2)
            self.radiobuttons.append(radio)

    def create_footer(self):
        self.progress = ttk.Progressbar(self.master, orient="horizontal", length=200, mode="determinate")
        self.progress.grid(row=6, column=0, pady=10)

        self.bytes = 0
        self.maxbytes = 0

        self.close_button = ttk.Button(self.master, text="OK", command=self.run)
        self.close_button.grid(row=6, column=1, rowspan=2, padx=50, pady=10, sticky='w')

        self.close_button = ttk.Button(self.master, text="Cancel", command=self.master.quit)
        self.close_button.grid(row=6, column=1, padx=50, pady=10, sticky='e')

    def search_for_dir_path(self, method):
        print("Searching for directory...")

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

    def search_for_file_path(self, method):
        print("Searching for a file...")

        currdir = os.path.expanduser('~')
        titleStr = ''
        if method == "input":
            titleStr = 'Please select an input image'
        elif method == "wmark":
            titleStr = 'Please select a watermark image'
        tempdir = tk.filedialog.askopenfilename(parent=root, initialdir=currdir, title=titleStr, filetypes=(("jpg files","*.jpg *.jpeg"),("png files","*.png")))
        if len(tempdir) > 0:
            print ("You chose: %s" % tempdir)

        if method == "wmark":
            self.wmarkPath.set(tempdir)
        elif method == "input":
            self.inputPath.set(tempdir)
        elif method == "output":
            self.outputPath.set(tempdir)

    def save_file_path(self):
        print("Saving file...")

        currdir = os.path.expanduser('~')
        titleStr = 'Please name your new image file'
        tempdir = tk.filedialog.asksaveasfilename(parent=root, initialdir=currdir, title=titleStr, defaultextension=".png", filetypes=(("png files","*.png"),("jpg files","*.jpg *.jpeg")))
        if len(tempdir) > 0:
            print ("You chose: %s" % tempdir)

        self.filenamePath.set(tempdir)

    def disable_widget(self, children):
        for child in children:
            child.configure(state='disabled')

    def enable_widget(self, children):
        for child in children:
            child.configure(state='normal')

    def run(self):
        #Stuff for progress bar
        self.progress["value"] = 0
        self.maxbytes = 5000
        self.progress["maximum"] = 5000

        _wmark = self.wmarkPath.get()
        _input = self.inputPath.get()
        _output = self.outputPath.get()
        _filename = self.filenamePath.get()
        _position = self.positionSelection.get().replace(" ", "_").lower()
        _alpha = self.alpha.get() / 100
        _scale = self.scale.get()

        command = "python ../../src/watermark.py"

        # Append the input file
        if len(_input) == 0:
            print('----------------------------')
            print("ERROR: Please Select an Input File/Directory")
            return
        else:
            command += " -i "
            command += _input

        # Append the output file
        if self.rbuttonInitSelection.get() == 1:
            command += " -o "
            command += _output
            command += " -b 1"
        elif self.rbuttonInitSelection.get() == 2:
            command += " -f "
            command += _filename
            command += " -b 0"
        
        # Append the watermark file
        if len(_wmark) == 0:
            print('----------------------------')
            print("ERROR: Please Select a Watermark Image")
            return
        else:
            command += " -w "
            command += _wmark

        # Append the alpha and scale values
        command = command + " -p " + _position + " -a " + str(_alpha) + " -s " + str(int(_scale))

        # Update Progress Bar
        self.read_bytes()

        # Run the command in the system
        print("Running script...")
        print(command)
        os.system(command)

    def read_bytes(self):
        '''simulate reading 500 bytes; update progress bar'''
        self.bytes += 500
        self.progress["value"] = self.bytes
        #if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            #self.after(100, self.read_bytes)

    def show_choice(self):
        choice = self.rbuttonInitSelection.get()

        print("You selected radio button #", choice)

        if choice == 1:
            self.disable_widget(self.singleframe.winfo_children())
            self.enable_widget(self.bulkframe.winfo_children())
        elif choice == 2:
            self.disable_widget(self.bulkframe.winfo_children())
            self.enable_widget(self.singleframe.winfo_children())

    def on_select_pos(self, event=None):
        print('----------------------------')

        if event: # <-- this works only with bind because `command=` doesn't send event
            print("event.widget:", event.widget.get())
            self.positionSelection.set(self.position.get())

    def set_label_alpha(self, val):
        self.alphaValue.set("{} %".format(int(float(val))))

    def set_label_scale(self, val):
        self.scaleValue.set("{} %".format(int(float(val))))

my_gui = myGUI(root)
root.mainloop()

# _wmark = my_gui.wmarkPath.get()
# _input = my_gui.inputPath.get()
# _output = my_gui.outputPath.get()
# _position = my_gui.positionSelection.get().replace(" ", "_").lower()
# _alpha = my_gui.alpha.get() / 100
# _scale = my_gui.scale.get()

# print("python ../../src/watermark.py -i " + _input + " -o " + _output + " -w " + _wmark + " -p " + _position
#                                          + " -a " + str(_alpha) + " -s " + str(_scale))

# os.system("python ../../src/watermark.py -i " + _input + " -o " + _output + " -w " + _wmark + " -p " + _position
#                                          + " -a " + str(_alpha) + " -s " + str(_scale))