import tkinter as tk
from tkinter import ttk

import sql
from ttkbootstrap.constants import *
from ttkbootstrap.widgets import Button, Entry, Frame, Label

from typing import Literal


class Base_Frame(Frame):

    table: str
    """  """

    stringvar_list: list[tk.StringVar]
    """  """

    frame_title: Label
    """ Frame Title\n\n  Titulo do frame"""

    entry_frame: Frame
    """Frame that groups all the Entries\n\n Frame que agrupa todas as Entradas"""

    list_view_frame: Frame
    """Frame containing the treeview\n\n Frame que contem a Treview"""

    list_view_tree: ttk.Treeview
    """  """

    buttons_frame: Frame
    """  """

    button_1: Button
    """  """

    button_2: Button
    """  """

    button_3: Button
    """  """

    warning_label: Label
    """  """

    # Inicio do Objeto base
    def __init__(self, parent, table):
        super().__init__(parent)

        self.table=table
        self.stringvar_list=[]

        # Titulo do frame
        self.frame_title = Label(self, text='', font=('Arial', 15), anchor='center', justify='center')
        self.frame_title.place(x=0, y=0, relwidth=1)
        
        # Frame que agrupa todas as entradas
        self.entry_frame = Frame(self)
        self.entry_frame.place(x=0, y=30, relwidth=0.68)

        # Label de mensagens temporárias
        self.warning_label = ttk.Label(self, text='', foreground='red', anchor='center', justify='center')
        self.warning_label.place(x=0, rely=0.83, relwidth=0.68)
        
        # Botões de ação
        self.buttons_frame = Frame(self)
        self.buttons_frame.place(x=0, rely=0.9, relwidth=1)

        self.button_1 = self.New_Button()
        self.button_1.grid(row=0, column=0, padx=15)

        self.button_2 = self.New_Button()
        self.button_2.grid(row=0, column=1, padx=15)

        self.button_3 = self.New_Button()
        self.button_3.grid(row=0, column=2, padx=15)

        self.button_mode(self.button_1, 'off')
        self.button_mode(self.button_2, 'off')
        self.button_mode(self.button_3, 'add')

        # Frame da tabela
        self.list_view_frame = ttk.Frame(self)
        self.list_view_frame.place(relx=0.68, y=30)

        # Scroll bar vertical
        scrollbar = ttk.Scrollbar(self.list_view_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y', padx=1, pady=1)

        # Tabela para a visualização
        self.list_view_tree = ttk.Treeview(self.list_view_frame, columns=('id',), show='headings', height=22, yscrollcommand=scrollbar.set)
        self.list_view_tree.heading('id', text='ID')
        self.list_view_tree.column('id', width=0, stretch=False)  # Oculta ID
        self.list_view_tree.pack(side='left', fill='both', expand=True, padx=1, pady=1)
        scrollbar.config(command=self.list_view_tree.yview)
        self.list_view_tree.bind('<Double-1>', self.select_item_in_list_view)
        self.list_view_tree.bind('<Delete>', lambda x: self.dell_item())

    # Get Funcs:
    def get_entrys(self) -> list[Entry]:            # Retorna uma lista com todas as Entrys do self.entry_frame
        return [widget for widget in self.entry_frame.winfo_children() if isinstance(widget, tk.Entry)]
    
    def get_selected_item(self) -> dict:            # Retorna um dicionario com as informações do item selecionado
        item_id = self.list_view_tree.focus()       # Pega o ID na tabela do item selecionado
        return self.list_view_tree.item(item_id)    # Pega os dados do item
    
    def get_stringvar(self) -> list[str]:           # Retorna uma lista com os valores ja formatados das StringVars
        return [var.get().strip().capitalize() for var in self.stringvar_list]

    # Clear Funcs:
    def clear_list_view(self):                      # Deleta todos os itens da self.list_view_tree
        for item in self.list_view_tree.get_children():
            self.list_view_tree.delete(item)

    def clear_entrys(self):                         # Desbloqueia as Entrys e limpa os valores das StringVars associadas
        # Normaliza as Entrys
        for widget in self.get_entrys(): widget.config(state='normal')
        # Seta as StringsVars como Vazias
        for var in self.stringvar_list: var.set('')

        self.button_mode(self.button_1, 'off')
        self.button_mode(self.button_2, 'off')
        self.button_mode(self.button_3, 'add')

    # Utils:
    def load_list_view(self):                       # Recarrega a self.list_view_tree com as informações do banco de dados
        self.clear_list_view()
        for _values in sql.get_all(self.table):
            self.list_view_tree.insert('', 'end', values=_values)
    
    def show_warning(self, text: str, color: str = 'red', time: int = 3000): # Mostra uma mensagem na janela
        self.warning_label.configure(text=text, foreground=color)
        self.after(time, lambda: self.warning_label.configure(text=''))

    def New_Button(self):                           # Preconfiguração da classe Button
        return Button(self.buttons_frame, text='', width=10, state='disable')

    # Base Actions:
    def add_item(self):                             # Rotina para adicionar um item ao banco de dados
        value_list = self.get_stringvar()

        if not value_list[0]:
            self.show_warning(f'o campo primeiro campo não pode estar vazio.')
            return
        
        cad_list = [_item[1] for _item in sql.get_all(self.table)]

        if value_list[0] in cad_list:
            self.show_warning('Item já cadastrado.')
        else:
            try:
                sql.insert(self.table, value_list)
                self.show_warning('Cadastrado com sucesso.', 'green')
                self.clear_entrys()
            except Exception as e:
                self.show_warning(f"Erro: {e}")
        self.load_list_view()

    def dell_item(self):                            # Rotina para deletar um item do banco de dados
        _id = self.get_selected_item()['values'][0]

        try:
            sql.delete(self.table, _id)
            self.show_warning('Deletado com sucesso.', 'green')
            self.clear_entrys()
        except Exception as e:
            self.show_warning(f'Erro ao deletar:\n{e}')
        self.load_list_view()

    def edit_item(self):                            # Rotina para iniciar uma edição de item
        for entry in self.get_entrys():
            entry.config(state='normal')
        
        self.button_mode(self.button_1, 'cancel')
        self.button_mode(self.button_2, 'off')
        self.button_mode(self.button_3, 'save')

    def save_edit(self):                            # Rotina para salvar e finalizar a edição do item
        _id = self.get_selected_item()['values'][0]
        value_list = self.get_stringvar()

        if not value_list[0]:
            self.show_warning(f'o campo primeiro campo não pode estar vazio.')
            return

        try:
            sql.update(self.table, _id, value_list)
            self.show_warning('Atualizado com sucesso.', 'green')
            self.clear_entrys()
        except Exception as e:
            self.show_warning(f'Erro ao atualizar:\n{e}')
        self.load_list_view()

    def select_item_in_list_view(self, event):      # Rotina para a seleção de um item na tabela
        _item = self.get_selected_item()
        item_values = _item['values']       # Lista com os valores da linha

        for widget in self.get_entrys():
            widget.config(state='readonly')
        
        for _index, _var in enumerate(self.stringvar_list):
            _var: tk.StringVar
            _var.set(item_values[_index+1])

        self.button_mode(self.button_1, 'dell')
        self.button_mode(self.button_2, 'edit')
        self.button_mode(self.button_3, 'clear')

    # Button Functions: 
    def button_mode(self, button: Button, mode: Literal['dell', 'edit', 'cancel', 'add', 'clear', 'save', 'off']='off'):
        match mode:
            case 'dell'     : button.config(text='Deletar', bootstyle='danger', state='active', command=self.dell_item)
            case 'edit'     : button.config(text='Editar',bootstyle='primary',state='active',command=self.edit_item)
            case 'cancel'   : button.config(text='Cancelar',bootstyle='danger',state='active',command=self.clear_entrys)
            case 'add'      : button.config(text='Adicionar',bootstyle='success',state='active',command=self.add_item)
            case 'clear'    : button.config(text='limpar',bootstyle='info',state='active',command=self.clear_entrys)
            case 'save'     : button.config(text='Salvar',bootstyle='success',state='active',command=self.save_edit)
            case 'off'      : button.config(text='', state='disable')


# Frame_pages: 
class Fornecedor(Base_Frame):
    def __init__(self, parent):
        super().__init__(parent, 'fornecedor')

        self.frame_title.configure(text='Fornecedor')

        Label(self.entry_frame, text='Nome:').grid(row=0, column=0, padx=10, pady=5, sticky=E)
        var_name = tk.StringVar(self.entry_frame)
        entry_name = Entry(self.entry_frame, name='nome', textvariable=var_name, width=40)
        entry_name.grid(row=0, column=1, padx=5, pady=5)

        Label(self.entry_frame, text='Endereço:').grid(row=1, column=0, padx=10, pady=5, sticky=E)
        var_address = tk.StringVar(self.entry_frame)
        entry_address = Entry(self.entry_frame, name='endereço',textvariable=var_address, width=40)
        entry_address.grid(row=1, column=1, padx=5, pady=5)
        
        Label(self.entry_frame, text='NFE:').grid(row=2, column=0, padx=10, pady=5, sticky=E)
        var_nfe = tk.StringVar(self.entry_frame)
        entry_nfe = Entry(self.entry_frame, name='nfe',textvariable=var_nfe, width=40)
        entry_nfe.grid(row=2, column=1, padx=5, pady=5)

        self.stringvar_list = [var_name, var_address, var_nfe]
        entry_name.bind('<Return>', lambda x: entry_address.focus_set())
        entry_address.bind('<Return>', lambda x: entry_nfe.focus_set())
        entry_nfe.bind('<Return>', lambda x: self.button_3.focus_set())
        self.button_3.bind('<Return>', lambda x: entry_name.focus_set() if var_name.get() == '' else self.button_3.invoke())

        self.list_view_tree.configure(columns=('id', 'nome'))
        self.list_view_tree.heading('id', text='ID')
        self.list_view_tree.heading('nome', text='Selecione')
        self.list_view_tree.column('id', width=0, stretch=False)  # Oculta ID
        self.list_view_tree.column('nome', width=135)

        self.load_list_view()

class Material(Base_Frame):
    def __init__(self, parent):
        super().__init__(parent, 'material')

        self.frame_title.configure(text='Materia Prima')

        Label(self.entry_frame, text='Nome:').grid(row=0, column=0, padx=10, pady=5, sticky=E)
        var_name = tk.StringVar(self.entry_frame)
        entry_name = Entry(self.entry_frame, name='nome', textvariable=var_name, width=40)
        entry_name.grid(row=0, column=1, padx=5, pady=5)

        self.stringvar_list = [var_name]
        entry_name.bind('<Return>', lambda x: self.button_3.focus_set())
        self.button_3.bind('<Return>', lambda x: entry_name.focus_set() if var_name.get() == '' else self.button_3.invoke())

        self.list_view_tree.configure(columns=('id', 'nome'))
        self.list_view_tree.heading('id', text='ID')
        self.list_view_tree.heading('nome', text='Selecione')
        self.list_view_tree.column('id', width=0, stretch=False)  # Oculta ID
        self.list_view_tree.column('nome', width=135)

        self.load_list_view()

class Empresa(Base_Frame):
    def __init__(self, parent):
        super().__init__(parent, 'empresa')

        self.frame_title.configure(text='Empresa')

        Label(self.entry_frame, text='Nome:').grid(row=0, column=0, padx=10, pady=5, sticky=E)
        var_name = tk.StringVar(self.entry_frame)
        entry_name = Entry(self.entry_frame, name='nome', textvariable=var_name, width=40)
        entry_name.grid(row=0, column=1, padx=5, pady=5)

        self.stringvar_list = [var_name]
        entry_name.bind('<Return>', lambda x: self.button_3.focus_set())
        self.button_3.bind('<Return>', lambda x: entry_name.focus_set() if var_name.get() == '' else self.button_3.invoke())

        self.list_view_tree.configure(columns=('id', 'nome'))
        self.list_view_tree.heading('id', text='ID')
        self.list_view_tree.heading('nome', text='Selecione')
        self.list_view_tree.column('id', width=0, stretch=False)  # Oculta ID
        self.list_view_tree.column('nome', width=135)

        self.load_list_view()

