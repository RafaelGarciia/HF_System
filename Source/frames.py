from curses import window
import tkinter as tk
from tkinter import Scrollbar, ttk
from window import Window

class Main_frame():
    def __init__(self) -> None:
        ...

    def __call__(self, window:Window) -> None:
        self.window = window
        self.root = window.root
        self.translate = window.translate

        # Frame Config
        self.main_frame = tk.Frame(self.root)
        self.main_frame.bind('<Button>', lambda event: self.report_label.place_forget())

        self.window.clear_frame()
        self.window.active_frame = self.main_frame
        self.window.active_frame.place(x=0, y=0)


        self.report_label = tk.Label(self.main_frame, text="", justify='center')

class Frame_Companie():
    def __init__(self) -> None:
        ...

    def __call__(self, window:Window) -> None:
        self.window = window
        self.root = window.root
        self.translate = window.translate

        # Frame Config
        main_frame = tk.Frame(self.root)
        main_frame.bind('<Button>', lambda event: self.report_label.place_forget())

        self.window.clear_frame()
        self.window.active_frame = main_frame
        self.window.active_frame.place(x=0, y=0)


        # Name Label
        tk.Label(main_frame,
            text = self.translate.get_translate(['word.companie']),
            justify = 'center'
        ).place(relx=0, y=7, relwidth=0.12)

        # Name Entry
        self.entry_name = tk.Entry(main_frame, justify='left')
        self.entry_name.place(relx=0.12, y=8, relwidth=0.6)

        # Companie ListBox-object
        self.list_companie = tk.Listbox(main_frame)
        self.list_companie.bind('<Double-Button>', self.select_companie)        

        # Scrollbar set
        scrollbar = tk.Scrollbar(main_frame, orient='vertical')
        scrollbar.configure(command=self.list_companie.yview)
        scrollbar.place(relx=0.97, rely=0.5, relwidth=0.03, relheight=0.5)

        # Companie ListBox config
        self.load_list_box()
        self.list_companie.configure(yscrollcommand=scrollbar.set)
        self.list_companie.place(relx=0, rely=0.5, relwidth=1, relheight=0.5)

        # Report Label
        self.report_label = tk.Label(main_frame, text="", justify='center')

        # Save Button
        button_save = tk.Button(main_frame,
            text    = self.translate.get_translate(['word.save']),
            command = self.save_companie,
            width   = 5
        )
        button_save.place(relx=0.73, y=5, width=60)

        # Delete Button
        button_delete =tk.Button(main_frame,
            text    = self.translate.get_translate(['word.delete']),
            command = self.delete_companie,
            width   = 5
        )
        button_delete.place(relx=0.87, y=5, width=60)

    def select_companie(self, event):
        selected_item = self.list_companie.selection_get()
        self.entry_name.delete(0, 'end')
        self.entry_name.insert(0, selected_item)

    def load_list_box(self):
        self.list_companie.delete(0, 'end')

        connection, cursor = self.window.connect_db()
        query = cursor.execute(
            """SELECT name FROM companies ORDER BY name ASC;"""
        ).fetchall()
        connection.close()

        # Insert ListBox
        for item in query:
            self.list_companie.insert('end', item[0])

    def save_companie(self):
        connection, cursor = self.window.connect_db()
        companie_list = cursor.execute("SELECT * FROM companies").fetchall()

        name = self.entry_name.get().upper()
        
        # Checks if the name is empty
        if name in (None, '', ' '):
            self.update_report_label(
                self.translate.get_translate(
                    ['error.name-empty']
            )   )
 
            connection.close()
            return
        
        # Check if the company is not registered
        exist = False
        for item in companie_list:
            if item == name:
                exist = True
        
        # In case there is
        if exist:
            self.update_report_label(
                self.translate.get_translate(
                    ['error.companie-already-registered']
            )   )
            
            connection.close()
            return
        
        # In case there is no
        else:
            try:
                cursor.execute(f"INSERT INTO companies VALUES ('{name}')")
                connection.commit()
                connection.close()

                self.update_report_label(
                    self.translate.get_translate(
                        ['report.companie-success-registered']
                )   )

                self.entry_name.delete(0, 'end')
                self.load_list_box()
                return
            
            except Exception as error:
                print(error)
        
    def delete_companie(self):
        connection, cursor = self.window.connect_db()
        companie_list = cursor.execute("SELECT * FROM companies").fetchall()

        name = self.entry_name.get().upper()

        if name in (None, '', ' '):
            try: name = self.list_companie.selection_get()
            except:
                self.update_report_label(
                    self.translate.get_translate(['error.name-empty'])
                )
        elif name not in companie_list:
            self.update_report_label(
                self.translate.get_translate(['error.Company-not-found'])
            )
        else:
            try:
                cursor.execute(f"DELETE FROM companies WHERE name = '{name}'")
                connection.commit()
                connection.close()

                self.update_report_label(
                    self.translate.get_translate(
                        ['report.companie-success-deleted']
                )   )

                self.entry_name.delete(0, 'end')
                self.load_list_box()
                return

            except Exception as error:
                print(error)

    def update_report_label(self, msg):
        self.report_label.configure(text = msg)
        self.report_label.place(relx=0.5, rely=0.90, relwidth=0.45)


class Frame_employee(Main_frame):
    def __call__(self, window:Window) -> None:
        super.__call__(window)

        tk.Label(self.main_frame,
            text = self.translate.get_translate(['word.companie'])
        ).place(x=5, y=50)

        self.cb_companie = ttk.Combobox(self.main_frame, width=23)
        self.cb_companie.place(relx=0.14, y=50)

        button_save = tk.Button(self.main_frame,
            text=self.translate.get_translate(['word.save']),
            command=apply,
            width=5
        )
        button_save.place(relx=0.37, y=80)

        scrollbar = tk.Scrollbar(self.main_frame, orient='vertical')
        scrollbar.place(relx=0.97, rely=0.01, relwidth=0.03, relheight=0.97)


        self.tw_employees = ttk.Treeview(self.main_frame,
            height=18, columns=('name', 'companie'), show='headings'
        )
        self.tw_employees.heading(  'name'  , text=self.translate.get_translate([  'word.name'  ]))
        self.tw_employees.heading('companie', text=self.translate.get_translate(['word.companie']))

        self.tw_employees.column(  'name'  , width=100)
        self.tw_employees.column('companie', width= 1 )

        self.tw_employees.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.tw_employees.yview)

        scrollbar.place(relx=0.97, rely=0.01, relwidth=0.03, relheight=0.97)
        self.tw_employees.place(relx=0.48, rely=0.01, relwidth=0.49, relheight=0.90)


    def load_combobox_companie(self):
        connection, cursor = self.window.connect_db()
        query = cursor.execute(
            """SELECT name FROM companies ORDER BY name ASC;"""
        ).fetchall()
        connection.close()

        self.cb_companie['values'] = query

    def load_tree_view(self):
        
        