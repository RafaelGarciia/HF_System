import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Entry, Button
from Frames.cadastro import FrameCadastroMaterial
from sql import sql

DATA_PATH = 'data_base.db'


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()

        # Verificando o banco de dados
        sql.execute_script('sql\\mk_database.sql')


        self.title('Janela principal')
        self.geometry('800x600')
        self.style = Style("flatly")
        
        # Menu Superior
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Tab do Sistema
        tab_sys = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Sistema', menu=tab_sys)
        # V---Menu---V
        tab_sys.add_command(label="Home", command=lambda: self.show_frame(HomePage))
        tab_sys.add_separator()
        tab_sys.add_command(label='Sair', command=self.quit)

        # Tab de Cadastros
        tab_cad = tk.Menu(menubar, tearoff=False)
        menubar.add_cascade(label='Cadastros', menu=tab_cad)
        # V---Menu---V
        tab_cad.add_command(label="Material", command=lambda: self.show_frame(FrameCadastroMaterial))
        
        # Container para as paginas
        self.container = Frame(self)
        self.container.pack(fill='both', expand=True)

        self.show_frame(HomePage)

    
    def show_frame(self, frame) -> None:
        self.container.pack_forget()
        self.container.pack(fill='both', expand=True)
        page: Frame = frame(self.container)
        page.grid(row=0, column=0, sticky='nsew')



class HomePage(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Página Inicial", font=("Arial", 20)).pack(pady=20)



class Page2(Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Esta é a Página 2", font=("Arial", 20)).pack(pady=20)



if __name__ == '__main__':
    app = App()
    app.mainloop()