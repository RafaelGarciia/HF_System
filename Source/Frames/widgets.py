import tkinter as tk
from tkinter import ttk

import sql
import ttkbootstrap as ttkb

class CB_Entry(ttkb.Frame):
    def __init__(self, master, text, cb_values:list) -> None:
        super().__init__(master)
        
        self.label = ttkb.Label(self, text=text or 'Label:', width=10)
        self.label.grid(row=0, column=0, sticky='e')

        self.cb_var = tk.StringVar(self)
        self.combobox = ttkb.Combobox(self, width=8, values=cb_values)
        self.combobox.grid(row=0, column=1, sticky='e')
        

        self.entry_var = tk.StringVar(self)
        self.entry = ttkb.Entry(self, textvariable=self.entry_var, width=27)
        self.entry.grid(row=0, column=2, sticky='e')

        self.combobox.bind('<Return>', lambda x: self.entry.focus_set())


class Basic_Entry(ttkb.Frame):
    entry: ttkb.Entry
    var: tk.StringVar
    
    def __init__(self, master, text) -> None:
        super().__init__(master)
        
        #self._frame = ttkb.Frame(parent)
        self.label = ttkb.Label(self, text=text or 'Label:', width=10)
        self.label.grid(row=0, column=0, sticky='e')

        self.var = tk.StringVar(self)

        self.entry = ttkb.Entry(self, textvariable=self.var, width=40)
        self.entry.grid(row=0, column=1)

        self.pack(pady=1)