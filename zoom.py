from json import tool
import os
import tkinter as tk
import json
from tkinter import font
from tkinter import messagebox
from turtle import bgcolor

import yaml

tool_desc = "Zoom Scraper 1.0 identifies and collects the artifacts left behind by zoom on the host system."
tool_usage = "\n\nUsage - \n Click on Run tool to collect artifacts.\n Click on Results to view the collected artifacts"
tool_btn_desc = """
\n\nDescription -
* Results [User Data] => It shows information about the logged in users like name, company name, avatars, profile picture, etc.
* Results [Recordings] => It shows information about zoom meetings recorded host id, join time, meeting number, etc.
* Results [Chat time] => It shows timestamp information when the chats were exchanged.
* Results [Zoom Configurations] => It shows information about the zoom application configurations like installation path, version, working directory, background images, etc.
"""

result_file = "data.json"

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()

class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Zoom Forensics\n", font=('Helvetica bold', 15), bg="white")
        label.pack(side="top", fill="both", expand=False)
        text = tk.Text(self)
        text.config(border=0)
        text.config(font=('Helvetica', 12), wrap="word")
        text.pack(expand=True, fill='both')
        text.insert(tk.END, tool_desc)
        text.insert(tk.END, tool_usage)
        text.insert(tk.END, tool_btn_desc)

class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, text="Finished collecting artifacts. Results available.", font=('Helvetica bold', 15))
        label.config(border=0, background="White")
        label.pack(side="top", fill="both", expand=True) 


class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        if os.path.isfile(result_file):
            with open(result_file, 'r') as inside:
                json_val = json.load(inside)
                json_val ={"Recorded Meetings":json_val["Recorded Meetings"]}
                yaml_val = yaml.dump(json_val,indent=4)
                # dct = yaml.safe_load(yaml_val)
        else:
            yaml_val =""
        text = tk.Text(self)
        text.config(border=0)
        text.pack(expand=True, fill='both')
        if yaml_val:
            text.insert(tk.END, yaml_val)
        else:
            text.insert(tk.END, "No results available")

class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        if os.path.isfile(result_file):
            with open(result_file, 'r') as inside:
                json_val = json.load(inside)
                json_val ={"Chat time":json_val["chat_time"]}
                yaml_val = yaml.dump(json_val,indent=4)
                # dct = yaml.safe_load(yaml_val)
        else:
            yaml_val =""
        text = tk.Text(self)
        text.config(border=0)
        text.pack(expand=True, fill='both')
        if yaml_val:
            text.insert(tk.END, yaml_val)
        else:
            text.insert(tk.END, "No results available")

class Page5(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        if os.path.isfile(result_file):
            with open(result_file, 'r') as inside:
                json_val = json.load(inside)
                json_val ={"Zoom Config":json_val["config"]}
                yaml_val = yaml.dump(json_val,indent=4)
                # dct = yaml.safe_load(yaml_val)
        else:
            yaml_val =""
        text = tk.Text(self)
        text.config(border=0)
        text.pack(expand=True, fill='both')
        if yaml_val:
            text.insert(tk.END, yaml_val)
        else:
            text.insert(tk.END, "No results available")


class Page6(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)
        if os.path.isfile(result_file):
            with open(result_file, 'r') as inside:
                json_val = json.load(inside)
                json_val ={"Users":json_val["users"],"User Data":json_val["user_data"]}
                yaml_val = yaml.dump(json_val,indent=4)
                # dct = yaml.safe_load(yaml_val)
        else:
            yaml_val =""
        text = tk.Text(self)
        text.config(border=0)
        text.pack(expand=True, fill='both')
        if yaml_val:
            text.insert(tk.END, yaml_val)
        else:
            text.insert(tk.END, "No results available")


class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)
        p5 = Page5(self)
        p6 = Page6(self)

        buttonframe = tk.Frame(self)
        buttonframe.config(background="White")
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="About", command=p1.show)
        b2 = tk.Button(buttonframe, text="Run tool", command=p2.show)
        b3 = tk.Button(buttonframe, text="Results [Recordings]", command=p3.show)
        b4 = tk.Button(buttonframe, text="Results [Chat time]", command=p4.show)
        b5 = tk.Button(buttonframe, text="Results [Zoom Configurations]", command=p5.show)
        b6 = tk.Button(buttonframe, text="Results [User Data]", command=p6.show)

        b1.pack(side="left")
        b2.pack(side="left")
        b6.pack(side="left")
        b3.pack(side="left")
        b4.pack(side="left")
        b5.pack(side="left")


        p1.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Zoom Scraper 1.0")
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.minsize(500, 500)
    root.mainloop()