import json

def write_json(file:str, json_dict:dict) -> None:
    with open(file, 'w') as f:
        f.write(json.dumps(json_dict, indent=4, sort_keys=True))

def read_json(file:str) -> dict:
    with open(file, 'r') as f:
        return json.load(f)




# Import Tkinter
import tkinter as tk
from tkinter import ttk

# Import SQLite
import sqlite3 as sql


from datetime import date


def rgb(r,g, b):

    rgb=(r, g, b)
    return '#%02x%02x%02x' % rgb

translate = {
    "window_title"                  : '' ,
    
    "topbar_sys.topmenu"            : '' ,
    "topbar_sys_home.button"        : '' ,
    "topbar_sys_lang.cascmenu"      : '' ,
    "topbar_sys_exit.button"        : '' ,

    "topbar_sicknote.topmenu"       : '' ,
    "topbar_sicknote_new.button"    : '' ,

    "frame_welcome.msg"             : '' ,
    "frame_sicknote_new.date_label" : '' ,
}  

translate_matrix = {
    
    "pt_br":{
        "window_title"  : 'Sistema HF'              ,
    
        "topbar_sys.topmenu"        : 'Sistema'     ,
        "topbar_sys_home.button"    : 'Home'        ,
        "topbar_sys_lang.cascmenu"  : 'Idioma'      ,
        "topbar_sys_exit.button"    : 'Sair'        ,

        "topbar_sicknote.topmenu"    : 'Atestados'  ,
        "topbar_sicknote_new.button" : 'Novo'       ,

        "frame_welcome.msg" : 'Bem vindo'           ,

        "frame_sicknote_new.date_label" : 'Data'    ,
    },

    "en":{
        "window_title"  : 'System HF'               ,
    
        "topbar_sys.topmenu"        : 'System'      ,
        "topbar_sys_home.button"    : 'Home'        ,
        "topbar_sys_lang.cascmenu"  : 'Language'    ,
        "topbar_sys_exit.button"    : 'Exit'        ,

        "topbar_sicknote.topmenu"    : 'Sick Notes' ,
        "topbar_sicknote_new.button" : 'New'        ,

        "frame_welcome.msg" : 'Welcome'             ,

        "frame_sicknote_new.date_label" : 'Date'    ,
    }

}

class Application():
    def __init__(self) -> None:

        self.win_width :int = 500
        self.win_height:int = 300

        self.active_frame:tk.Frame = None

        self.window = tk.Tk()

        self.set_locale_en()
        self.start_window()
        self.start_top_bar()
        self.frame_welcome()

        self.window.mainloop()

    # Start Functions
    def start_window(self):
        self.window.title(translate['window_title'])
        self.window.geometry(f"{self.win_width}x{self.win_height}")
        self.window.resizable(False, False)

    def start_top_bar(self):
        def cascademenu_sys(root:tk.Menu) -> tk.Menu:
            # Creating a cascade menu with system options
            topbar_sys_cascade_menu = tk.Menu (root, tearoff=False)
            # |   Home   | Go to home page
            # | Language | Cascade menu to set the localization system
            # |----------|
            # |   Exit   | Exit button

            topbar_sys_cascade_menu.add_command   (   #-# Home button
                label   = translate['topbar_sys_home.button'],
                command = self.frame_welcome
            )
            topbar_sys_cascade_menu.add_cascade   (   #-# Language cascade menu
                label   = translate['topbar_sys_lang.cascmenu'],
                menu    = lang_submenu (root)
            )
            topbar_sys_cascade_menu.add_separator ()  #-# Separator
            topbar_sys_cascade_menu.add_command   (   #-# Exit button
                label   = translate['topbar_sys_exit.button'],
                command = self.window.quit
            )

            return topbar_sys_cascade_menu
        
        def lang_submenu(root:tk.Menu) -> tk.Menu:
            # Create a menu with locations
            topbar_lang_menu = tk.Menu (root, tearoff=False)
            # |  en   | Set the localization in English
            # | pt_br | Set the localization in Brazilian_Portuguese
            
            topbar_lang_menu.add_command ( #-# English locate button
                label   = 'en',
                command = self.set_locale_en
            )
            topbar_lang_menu.add_cascade ( #-# Brazilian_Portuguese button
                label   = 'pt_br',
                command = self.set_locale_pt_br
            )
        
            return topbar_lang_menu
        
        def menu_sicknote(root:tk.Menu) -> tk.Menu:
            # Creating a cascade menu with release of sick notes
            topbar_sick_notes_menu = tk.Menu(root, tearoff=False)
            # | New |
            
            topbar_sick_notes_menu.add_command(     #-# New sick note button
                label   = translate['topbar_sicknote_new.button'],
                command = self.frame_new_sick_note
            )

            return topbar_sick_notes_menu

        # Creating the top menubar
        top_bar = tk.Menu(self.window)

        # Applying all cascade menus to the top menubar
        top_bar.add_cascade(    #-# System cascade menu
            label = translate['topbar_sys.topmenu'],
            menu  = cascademenu_sys(top_bar)
        )
        top_bar.add_cascade(    #-# Sick notes cascade menu
            label = translate['topbar_sicknote.topmenu'],
            menu  = menu_sicknote(top_bar)
        )

        # Applying the menubar to the window
        self.window.config(menu=top_bar)

    # Gear Functions
    def set_locale_en(self):
        global translate_matrix, translate
        translate = translate_matrix['en']
        self.frame_welcome()
        self.start_top_bar()

    def set_locale_pt_br(self):
        global translate_matrix, translate
        translate = translate_matrix['pt_br']
        self.frame_welcome()
        self.start_top_bar()

    def clear_frame(self) -> None:
        if self.active_frame == None: return
        else: self.active_frame.place_forget()

    def new_frame(self) -> tk.Frame:
        return tk.Frame(self.window,
            width=self.win_width, height=self.win_height
        )

    

    # Frames Functions
    def frame_welcome(self) -> None:
        self.clear_frame()

        self.active_frame = self.new_frame()
        label_center_x = (self.win_width/2 ) - 70
        label_center_y = (self.win_height/2) - 25
        
        tk.Label(   #-# Central message of the frame
            self.active_frame,
            text = translate['frame_welcome.msg'],
            font = ("Tahoma", 25)
        ).place(x=label_center_x, y=label_center_y)
        
        self.active_frame.place(x=0, y=0)

    def frame_new_sick_note(self) -> None:
        self.clear_frame()
        self.active_frame = self.new_frame()

        pad_x = 5
        input_frame = tk.Frame(self.active_frame, width=self.win_width-(pad_x*2), height=30, relief='groove', bg=rgb(112,128,144))
        input_frame.place(x=pad_x, y=pad_x)

        tk.Label(input_frame,
            text   = translate['frame_sicknote_new.date_label'],
            font   = ("Tahoma", 10),
            relief = 'flat',
            bg=rgb(112,128,144)
        ).place(x=5, y=5)

        entry_date = tk.Entry(input_frame, width=11, justify='center')
        entry_date.place(x=45, y=5)

        if date.today().day < 10: day = f"0{date.today().day}"
        else: day = date.today().day

        if date.today().month < 10: month = f"0{date.today().month}"
        else: month = date.today().month

        entry_date.insert(0, f"{day}/{month}/{date.today().year}")







        self.active_frame.place(x=0, y=0)









Application()