import tkinter as tk
from translate import Translate
import sqlite3 as sql
from os import system



class Window():
    def __init__(self) -> None:    
        self.root = tk.Tk()

        self.width  :int  = 500
        self.height :int  = 300

        self.translate = Translate()

        self.title  :str  = self.translate.get_translate("window.title")

        self.active_frame:tk.Frame | None = None

        self.root.resizable(False, False)
    
    def window_update(self) -> None:
        self.root.title(self.title)
        self.root.geometry(f"{self.width}x{self.height}")

    def mainloop(self) -> None:
        self.root.mainloop()

    def clear_frame(self) -> None:
        if self.active_frame == None: return
        else: self.active_frame.place_forget()

    def connect_db(self):
        system('mkdir database')
        connection = sql.connect('database\\bank.db')
        cursor = connection.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS employees (name, companie)")
        cursor.execute("CREATE TABLE IF NOT EXISTS companies (name)")

        return connection, cursor





