from platform import system
import json
# from tkinter import Tk, Label, Button, Grid, grid_rowconfigure, Entry, IntVar, END, W, E, filedialog, Toplevel
from tkinter import *
from tkinter import Entry, filedialog


class PyDoc:

    def __init__(self, master):
        self.master = master
        master.title("Requests")

        self.label = Label(master, text="Text")
        self.filepath = ""

        self.lambda_button = Button(master, text="lambda", command=lambda: self.update("lambda"))
        self.open_button = Button(master, text="open", command=lambda: self.update("open"))
        self.viewing_session_button = Button(master, text="Viewing Session", command=lambda: self.update("Viewing Session"))
        # LAYOUT

        self.label.grid(row=0, column=0, sticky=W)
        self.viewing_session_button.grid(row=2, column=3)
        # self.entry.grid(row=1, column=0, columnspan=3, sticky=W+E)

        self.open_button.grid(row=1, column=2)

    def update(self, method):
        if method == "open":
            initialdir = "/" if (system() == "Linux") else "C:/"

            self.filepath = filedialog.askopenfilename(initialdir=initialdir, filetypes=(("jpeg files","*.jpg"),("all files","*.*")))
        elif method == "Viewing Session":
            with open('viewing_session.json', 'r') as file:
                data = json.load(file)
                Request_Window(Toplevel(self.master), data=data)
        else:
            pass


class Request_Window(Grid):

    def __init__(self, master, title="New Window", data={}):

        self.master = master
        master.title = title
        self.vcmd = master.register(self.validate)
        self.count = 0
        self.labels = {}
        self.entries = {}
        self.gen_window_from_json(data)

    def gen_window_from_json(self, raw_data, depth=0):
        for item in raw_data:
            self.count += 1
            if type(raw_data[item]) is dict:
                self.labels[item] = self.new_label(item, depth)
                self.gen_window_from_json(raw_data[item], depth + 1)

            else:
                self.labels[item] = self.new_label(item, depth)
                self.entries[item] = self.new_entry(raw_data[item], depth)

    def new_label(self, item="", depth=0):
        new_label = Label(self.master, text=item)
        new_label.grid(row=self.count, column=depth, sticky='W')
        return new_label

    def new_entry(self, item="", depth=0):
        new_entry = Entry(self.master, validate="key", validatecommand=(self.vcmd, '%P'))
        new_entry.grid(row=self.count, column=depth + 1, sticky='W')
        new_entry.insert(index=0, string=item)
        entered_text = new_entry.get()
        print(entered_text)
        # new_entry.insert(index=0, string="newdata")
        return new_entry

    def validate(self, new_text):
        if not new_text: # the field is being cleared
            self.data = 0
            return True

        try:
            self.data= new_text
            return True
        except ValueError:
            return False


root = Tk()
PyDoc = PyDoc(root)
root.mainloop()

