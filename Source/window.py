import tkinter as tk
from tkinter import font


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.width  :int  = 500
        self.height :int  = 300

        self.active_frame: tk.Frame = None

        self.defaultFont = font.nametofont('TkDefaultFont')
        self.defaultFont.configure(family='DejaVu Sans Mono')
        
        self.geometry(f'{self.width}x{self.height}')
        self.resizable(False, False)

    def clear_frame(self) -> None:
        if self.active_frame != None:
            self.active_frame.place_forget()
    
    def show_frame(self) -> None:
        if self.active_frame != None:
            self.active_frame.place(x=0, y=0)


