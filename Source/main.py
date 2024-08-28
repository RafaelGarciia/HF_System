# Importing the Tkinter module.
import tkinter as tk
from tkinter  import ttk

# Importing the Custom Functions module.
import funcs as fnc

# Importing the sqlite module.
import sqlite3 as sql

from exception_module import LoadConfigError


translation_matrix = {
    "pt_br":{
        "window_title"                  : 'Sistema HF'  ,
    
        "generic_companie"              : 'Empresa'     ,
        "generic_employees"             : 'Funcionarios',
        "generic_date"                  : 'Data'        ,
        "generic_sicknotes"             : 'Atestados'   ,
        "generic_new"                   : 'Novo'        ,
        "generic_list"                  : 'Listar'      ,
        "generic_save"                  : 'Salvar'      ,
        "generic_name"                  : 'Nome'        ,
    

        "topbar_sys.topmenu"            : 'Sistema'     ,
        "topbar_sys_home.button"        : 'Home'        ,
        "topbar_sys_lang.cascmenu"      : 'Idioma'      ,
        "topbar_sys_exit.button"        : 'Sair'        ,

        "frame_welcome.msg"             : 'Bem vindo'   ,

        "frame_companies_alreadyregistered.error" : 'Empresa já cadastrada',
        "frame_companies_succeusregistered.report": 'Empresa cadastrado com sucesso',
        "frame_companies_name-empty.error"        : 'O nome não pode ficar vazio',

        "frame_employees_alreadyregistered.error" : 'Funcionário já cadastrado',
        "frame_employees_succeusregistered.report": 'Funcionário cadastrado com sucesso',
        "frame_employees_companieempty.error"     : 'A empresa não pode ficar vazia',
        "frame_employees_nameempty.error"         : 'O nome não pode ficar vazio',

        "frame_employees_Employeename.label"      : 'Nome do Funcionario',
    },

    "en":{
        "window.title"              : 'System HF'   ,

        "word.companie"             : 'Companie'    ,
        "word.employees"            : 'Employees'   ,
        "word.date"                 : 'Date'        ,
        "word.sicknotes"            : 'Sick Notes'  ,
        "word.new"                  : 'New'         ,
        "word.list"                 : 'List'        ,
        "word.save"                 : 'Save'        ,
        "word.name"                 : 'Name'        ,
        "word.system"               : 'System'      ,
        "word.home"                 : 'Home'        ,
        "word.language"             : 'Language'    ,
        "word.exit"                 : 'Exit'        ,

        "error.name-empty"                  : 'The name cannot be empty'    ,
        "error.companie-empty"              : 'The companie cannot be empty',
        "error.companie-already-registered" : 'Companie already registered',
        "error.employee-already-registered" : 'Employee already registered',
        
        
        "report.companie-success-registered"    : 'Companie successfully registered',
        "report.employee-success-registered"    : 'Employee successfully registered',

        "label.employee-name"       : 'Employee Name',
        "msg.welcome"               : 'Welcome',
    }
}


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
    global frame_welcome, frame_sicknote_new, frame_employee_new_view, frame_companie

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
            label   = active_translation['generic_new'],
            command = frame_sicknote_new
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
        label = active_translation['generic_sicknotes'],
        menu  = menu_sicknote(top_bar)
    )
    top_bar.add_command(    #-# employee Frame
        label   = active_translation['generic_employees'],
        command = frame_companie
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


#-# Connect the database sql
sql_file = 'database.db'

def connect():
    global sql_file

    connection = sql.connect(sql_file)
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS employees (id, name, companie)")
    cursor.execute("CREATE TABLE IF NOT EXISTS companies (id, name)")

    return connection, cursor


#-# Translation
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

def frame_sicknote_new():
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
        text    = active_translation['generic_date'],
        font    = ("Tahoma", 10),
        relief  = 'flat',
        bg      = fnc.rgb_to_hex(112, 128, 144)
    ).place(x=5, y=5)

    #-# Date entry
    entry_date = tk.Entry(top_frame, width=11, justify='center')
    entry_date.place(x=45, y=5)
    entry_date.insert(0, fnc.get_today())

    employees = []
    connection, cursor = connect()
    query = cursor.execute("""
        SELECT name FROM employees ORDER BY name ASC;
    """).fetchall()
    connection.close()

    for item in query:
        employees.append(f"{item[0]}")

    cb_employee = ttk.Combobox(active_frame, width=50)
    cb_employee['values'] = employees
    cb_employee.place(x=5, y=50)


    active_frame.place(x=0, y=0)

def frame_employee_new_view():
    global active_frame, active_translation, window, win_width
    global clear_frame, new_frame

    def apply():
        connection, cursor = connect()
        employees = cursor.execute("SELECT * FROM employees").fetchall()

        name = entry_name.get().upper()
        companie = cb_companie.get()
        cont_id = 1
        for item in employees:
            if item[0] == cont_id: cont_id += 1
            if item[1] == name:
                tk.Label(active_frame, text=active_translation["frame_employees_alreadyregistered.error"]).place(relx=0.05, rely=0.90)
                return

        if name not in (None, '', " "):
            if companie not in (None, '', " "):
                cursor.execute(f"INSERT INTO employees VALUES ({cont_id}, '{name}', '{companie}')")
                connection.commit()
                tk.Label(active_frame, text=active_translation['frame_employees_succeusregistered.report']).place(x=5, rely=0.90, relwidth=0.46)
                entry_name.delete(0, 'end')
                cb_companie.delete(0, 'end')
            else:
                tk.Label(active_frame, text=active_translation['frame_employees_companieempty.error']).place(x=5, rely=0.90, relwidth=0.46)
        else:
            tk.Label(active_frame, text=active_translation['frame_employees_nameempty.error']).place(x=5, rely=0.90, relwidth=0.46)

        connection.close()
        load_tree_view()

    def load_tree_view():
        connection, cursor = connect()
        tw_employees.delete(*tw_employees.get_children())

        query = cursor.execute(
            """SELECT name, companie FROM employees ORDER BY name ASC;"""
        ).fetchall()
        connection.close()

        for item in query:
            tw_employees.insert("", 'end', values=item)
        

    clear_frame()
    active_frame = new_frame()

    tk.Label(active_frame, text=active_translation['frame_employees_Employeename.label']).place(relx=0.125, y=0)

    entry_name = tk.Entry(active_frame, width=37, justify='left')
    entry_name.place(x=5, y=20)


    connection, cursor = connect()
    query = cursor.execute(
        """SELECT name FROM companies ORDER BY name ASC;"""
    ).fetchall()
    connection.close()

    companies = []
    for item in query:
        companies.append(item[0])


    tk.Label(active_frame, text=active_translation['generic_companie']).place(x=5, y=50)

    cb_companie = ttk.Combobox(active_frame, width=23)
    cb_companie['values'] = companies
    cb_companie.place(relx=0.14, y=50)

    button_save = tk.Button(active_frame, text=active_translation['generic_save'], command=apply, width=5)
    button_save.place(relx=0.37, y=80)

    scrollbar = tk.Scrollbar(active_frame, orient='vertical')

    tw_employees = ttk.Treeview(active_frame, height=18, yscrollcommand=scrollbar.set, columns=("name", 'companie'), show='headings')
    tw_employees.heading("name"    , text = active_translation['generic_name'    ])
    tw_employees.heading("companie", text = active_translation['generic_companie'])

    tw_employees.column("name"   , width = 100)
    tw_employees.column("companie", width = 1)

    tw_employees.configure(yscroll=scrollbar.set)

    scrollbar.place     (relx=0.97, rely=0.01, relwidth=0.03, relheight=0.97)
    tw_employees.place  (relx=0.48, rely=0.01, relwidth=0.49, relheight=0.90)
    

    load_tree_view()



    active_frame.place(x=0, y=0)

def frame_companie():
    global active_frame, active_translation, window, win_width
    global clear_frame, new_frame

    def apply():
        connection, cursor = connect()
        companies = cursor.execute("SELECT * FROM companies").fetchall()

        name = entry_name.get().upper()
        cont_id = 1
        for item in companies:
            if item[0] == cont_id: cont_id += 1
            if item[1] == name:
                tk.Label(active_frame, text=active_translation["frame_companies_alreadyregistered.error"]).place(relx=0.55, rely=0.90)
                return
        
        if name not in (None, '', " "):
            cursor.execute(f"INSERT INTO companies VALUES ({cont_id}, '{name}')")
            connection.commit()
            tk.Label(active_frame, text=active_translation['frame_employees_succeusregistered.report']).place(relx=0.55, rely=0.90, relwidth=0.46)
            entry_name.delete(0, 'end')
        else:
            tk.Label(active_frame, text=active_translation['generic_error.name-empty']).place(x=5, rely=0.90, relwidth=0.46)

        connection.close()
        load_list_box()

    def load_list_box():
        list_companie.delete(0, 'end')

        connection, cursor = connect()
        query = cursor.execute(
            """SELECT name FROM companies ORDER BY name ASC;"""
        ).fetchall()
        connection.close()

        # Config ListBox
        for item in query:
            list_companie.insert(tk.END, item[0])

    clear_frame()
    active_frame = new_frame()
    active_frame.place(x=0, y=0)

    # Name Label
    tk.Label(active_frame, text=active_translation['generic_companie'], justify='center').place(relx = 0.5, y=0, relwidth=0.5)
    
    # Entry Name
    entry_name = tk.Entry(active_frame, justify='left')
    entry_name.place(relx = 0.505, y=20, relwidth=0.48)

    # Instantiate object
    list_companie   = tk.Listbox  (active_frame)
    scrollbar       = tk.Scrollbar(active_frame, orient='vertical')

    # Query companies to list
    load_list_box()
    list_companie.configure(yscrollcommand = scrollbar.set)
    list_companie.place (relx=0, rely=0, relwidth=0.47, relheight=1)

    # Config ScrollBar
    scrollbar.configure(command = list_companie.yview)
    scrollbar.place(relx=0.47, rely=0, relwidth=0.03, relheight=1)

    # Save Button
    button_save = tk.Button(active_frame, text=active_translation['generic_save'], command=apply, width=5)
    button_save.place(relx=0.37, y=80)





load_config()
update_translation()

window.mainloop()


