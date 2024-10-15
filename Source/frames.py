import tkinter as tk
from tkinter import Scrollbar, ttk
from Source.window import Window
from Source import sql

class Pattern_screen(tk.Frame):
    def __init__(self, root: Window):
        super().__init__(
            master=root,
            width=root.width,
            height=root.height,
            bg='lightgray',
        )
    

class Company_registration_screen(Pattern_screen):
    def __init__(self, root):
        super().__init__(root)
        input_frame = tk.Frame(self)
        input_frame.place(anchor="nw", relx=0.02, rely=0.03)
        tk.Label(input_frame, text='Empresa').pack(side='top')
        self.company_entry = tk.Entry(input_frame, justify="left", width=30)
        self.company_entry.pack(padx=5, pady=5, side="top")

        button_frame = tk.Frame(self)
        button_frame.place(anchor="nw", relx=0.45, rely=0.03)

        insert_icon = tk.PhotoImage(
            file='Source\\icons\\insert.png'
        ).subsample(4, 4)
        insert_button = tk.Button(
            button_frame,
            image=insert_icon,
            relief='flat',
            command=self.insert_company,
        )
        insert_button.image = insert_icon
        insert_button.pack(padx=2, pady=2, side='top')

        delete_icon = tk.PhotoImage(
            file='Source\\icons\\delete.png'
        ).subsample(4, 4)
        delete_button = tk.Button(
            button_frame,
            image=delete_icon,
            relief='flat',
            command= ... ,
        )
        delete_button.image = insert_icon
        delete_button.pack(padx=2, pady=2, side='top')

        list_frame = tk.Frame(self)
        self.listbox_company = tk.Listbox(list_frame)


        self.listbox_company.pack(
            anchor="center",
            expand=True,
            fill="both",
            padx=5,
            pady=5,
            side="bottom")
        list_frame.place(
            anchor="nw",
            relheight=0.75,
            relwidth=0.96,
            relx=0.02,
            rely=0.22)
        
        self.load_treeview()

    def load_treeview(self, event=None):
        
        # Table control variable
        self.id = None

        # Clean treeview
        self.listbox_company.delete(0, tk.END)

        # Request to the database
        connection, cursor = sql.connect()
        query = cursor.execute("""SELECT * FROM companies ORDER BY name ASC;""")
        for item in query:
            self.listbox_company.insert(tk.END, item[0])
        connection.close()

    def insert_company(self):

        company_name = self.company_entry.get()

        connection, cursor = sql.connect()
        query = cursor.execute("""SELECT * FROM companies ORDER BY name ASC;""")
        
        list_company = []
        for item in query:
            list_company.append(item[0])

        if company_name == "":
            print("Nome Vazio")
        elif company_name in list_company:
            print("A empresa ja existe.")
        else:
            cursor.execute("""INSERT INTO companies VALUES ('%s')"""% company_name)
            self.company_entry.delete(0, tk.END)

        self.load_treeview()

        connection.commit()
        connection.close()

