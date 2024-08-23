# Importing the Tkinter module.
import tkinter as tk
from tkinter  import ttk

# Importing the Custom Functions module.
import funcs as fnc


# Exception class.
# Used when you hear an error when loading the Json configuration file.
class LoadConfigError(Exception):
    def __init__(self, message, errors):            
        # Call the base class constructor with the parameters it needs.
        super().__init__(message)
            
        self.errors = errors



# V Main Code V

#-# Main window
window      = tk.Tk()
# Window sise
win_width   = 500
win_height  = 300

def update_window():
    global window, active_translation, win_width, win_height

    window.title(active_translation['window_title'])
    window.geometry(f"{win_width}x{win_height}")
    window.resizable(False, False)

def top_bar():
    global window, active_translation
    global set_locale_en, set_locale_pt_br
    global frame_welcome, frame_new_sicknote

    def cascademenu_sys(root:tk.Menu) -> tk.Menu:
        # Creating a cascade menu with system options
        topbar_sys_cascade_menu = tk.Menu (root, tearoff=False)
        # |   Home   | Go to home page
        # | Language | Cascade menu to set the localization system
        # |----------|
        # |   Exit   | Exit button

        topbar_sys_cascade_menu.add_command   (   #-# Home button
            label   = active_translation['topbar_sys_home.button'],
            command = frame_welcome
        )
        topbar_sys_cascade_menu.add_cascade   (   #-# Language cascade menu
            label   = active_translation['topbar_sys_lang.cascmenu'],
            menu    = lang_submenu (root)
        )
        topbar_sys_cascade_menu.add_separator ()  #-# Separator
        topbar_sys_cascade_menu.add_command   (   #-# Exit button
            label   = active_translation['topbar_sys_exit.button'],
            command = window.quit
        )

        return topbar_sys_cascade_menu

    def lang_submenu(root:tk.Menu) -> tk.Menu:
        # Create a menu with locations
        topbar_lang_menu = tk.Menu (root, tearoff=False)
        # |  en   | Set the localization in English
        # | pt_br | Set the localization in Brazilian_Portuguese
        
        topbar_lang_menu.add_command ( #-# English locate button
            label   = 'en',
            command = set_locale_en
        )
        topbar_lang_menu.add_cascade ( #-# Brazilian_Portuguese button
            label   = 'pt_br',
            command = set_locale_pt_br
        )
    
        return topbar_lang_menu

    def menu_sicknote(root:tk.Menu) -> tk.Menu:
        # Creating a cascade menu with release of sick notes
        topbar_sick_notes_menu = tk.Menu(root, tearoff=False)
        # | New |
        
        topbar_sick_notes_menu.add_command(     #-# New sick note button
            label   = active_translation['topbar_sicknote_new.button'],
            command = frame_new_sicknote
        )

        return topbar_sick_notes_menu

    # Creating the top menubar
    top_bar = tk.Menu(window)

    # Applying all cascade menus to the top menubar
    top_bar.add_cascade(    #-# System cascade menu
        label = active_translation['topbar_sys.topmenu'],
        menu  = cascademenu_sys(top_bar)
    )
    top_bar.add_cascade(    #-# Sick notes cascade menu
        label = active_translation['topbar_sicknote.topmenu'],
        menu  = menu_sicknote(top_bar)
    )

    # Applying the menubar to the window
    window.config(menu=top_bar)


#-# Load and Save Json Config.
config_file = 'config.json'
app_version = '1.0.0'

def load_config() -> None:
    global app_version, translation_matrix, locale, config_file
    global save_config, update_translation

    # Try to open the file, if can't, call the function to create the json file.
    try: fnc.read_json(config_file)
    except FileNotFoundError:
        save_config()

    # After creating or opening the file, values ​​are assigned to its variables.
    file = fnc.read_json(config_file)
    if file['version'] == app_version:
        locale = file['locale']
        update_translation()
    else: # If the file version is not compatible with the application version
        raise LoadConfigError('The version of the config file is not compatible with the application')

def save_config() -> None:
    # Creates the json file if it does not exist.
    # If it exists, write it with updated information
    global app_version, locale, config_file

    json_config = {
        "version"   : app_version,
        "locale"    : locale
    }

    fnc.write_json(config_file, json_config)


#-# Translation
translation_matrix = {
    "pt_br":{
        "window_title"                  : 'Sistema HF'  ,
    
        "topbar_sys.topmenu"            : 'Sistema'     ,
        "topbar_sys_home.button"        : 'Home'        ,
        "topbar_sys_lang.cascmenu"      : 'Idioma'      ,
        "topbar_sys_exit.button"        : 'Sair'        ,

        "topbar_sicknote.topmenu"       : 'Atestados'   ,
        "topbar_sicknote_new.button"    : 'Novo'        ,

        "frame_welcome.msg"             : 'Bem vindo'   ,

        "frame_sicknote_new.date_label" : 'Data'        ,
    },

    "en":{
        "window_title"                  : 'System HF'   ,
    
        "topbar_sys.topmenu"            : 'System'      ,
        "topbar_sys_home.button"        : 'Home'        ,
        "topbar_sys_lang.cascmenu"      : 'Language'    ,
        "topbar_sys_exit.button"        : 'Exit'        ,

        "topbar_sicknote.topmenu"       : 'Sick Notes'  ,
        "topbar_sicknote_new.button"    : 'New'         ,

        "frame_welcome.msg"             : 'Welcome'     ,

        "frame_sicknote_new.date_label" : 'Date'        ,
    }
}
locale = 'en'
active_translation = {}

def set_locale_en():
    global locale, update_translation
    locale = 'en'
    update_translation()

def set_locale_pt_br():
    global locale, update_translation
    locale = 'pt_br'
    update_translation()

def update_translation():
    global active_translation, translation_matrix, locale
    global update_window, top_bar, clear_frame, frame_welcome
    global save_config


    active_translation = translation_matrix[locale]
    update_window()
    top_bar()
    clear_frame()
    frame_welcome()

    save_config()


#--# Frames
active_frame:tk.Frame = None

def clear_frame() -> None:
    global active_frame

    if active_frame == None: return
    else: active_frame.place_forget()

def new_frame() -> tk.Frame:
    global window, win_width, win_height
    return tk.Frame(window,
        width  = win_width,
        height = win_height
    )

def frame_welcome():
    global active_frame, active_translation, window
    global clear_frame, new_frame

    clear_frame()
    active_frame = new_frame()

    text_label = active_translation['frame_welcome.msg']
    label_center_x = (win_width/2 )-(len(text_label)*10)
    label_center_y = (win_height/2) - 25

    tk.Label(window,    #-# Central message of the frame.
        text = text_label, font = ("Tahoma", 25)
    ).place(x=label_center_x, y=label_center_y)

    active_frame.place(x=0, y=0)

def frame_new_sicknote():
    global active_frame, active_translation, window, win_width
    global clear_frame, new_frame

    clear_frame()
    active_frame = new_frame()

    pad_x = 5
    top_frame = tk.Frame(active_frame,
        width   = win_width - (2 * pad_x),
        height  = 30,
        relief  = 'groove',
        bg      = fnc.rgb_to_hex(112, 128, 144) 
    )
    top_frame.place(x=pad_x, y=pad_x)

    #-# Date label
    tk.Label(top_frame,
        text    = active_translation['frame_sicknote_new.date_label'],
        font    = ("Tahoma", 10),
        relief  = 'flat',
        bg      = fnc.rgb_to_hex(112, 128, 144)
    ).place(x=5, y=5)

    #-# Date entry
    entry_date = tk.Entry(top_frame, width=11, justify='center')
    entry_date.place(x=45, y=5)
    entry_date.insert(0, fnc.get_today())



    active_frame.place(x=0, y=0)






load_config()
update_translation()

window.mainloop()


