import tkinter as tk
from tkinter import ttk
from ttkbootstrap.widgets import Frame, Label, Entry, Button
import sql
from ttkbootstrap.constants import *


class Fornecedor(Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Título
        Label(self, text='Fornecedores', font=('Arial', 15), anchor='center', justify="center").grid(row=0, column=0, columnspan=2)#pack(fill='x')


        # Campos de entrada
        form_frame = Frame(self)    # frame do formulário de cadastro
        form_frame.grid(row=1, column=0) #pack(side='left', expand=True)

        Label(form_frame, text='Nome:').grid(
            row=0, column=0, padx=10, pady=5, sticky=E
        )
        self.var_name = tk.StringVar()
        self.entry_name = Entry(form_frame, textvariable= self.var_name ,width=40)
        self.entry_name.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text='Endereço:').grid(
            row=1, column=0, padx=10, pady=5, sticky=E
        )
        self.var_address = tk.StringVar()
        self.entry_address = Entry(form_frame, textvariable= self.var_address ,width=40)
        self.entry_address.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text='NFE:').grid(
            row=2, column=0, padx=10, pady=5, sticky=E
        )
        self.var_nfe = tk.StringVar()
        self.entry_nfe = Entry(form_frame, textvariable=self.var_nfe, width=40)
        self.entry_nfe.grid(row=2, column=1, padx=5, pady=5)

        #

        # Frame da tabela
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.grid(row=1, column=1, rowspan=2)    #pack(side='right', expand=True)

        # Scroll bar vertical
        scrollbar = ttk.Scrollbar(self.tree_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        # Tabela para a visualização
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=('id', 'nome'),
            show='headings',
            height=15,
            yscrollcommand=scrollbar.set,
        )
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.column('id', width=0, stretch=False)  # Oculta ID
        self.tree.column('nome', width=135)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)
        self.tree.bind('<Double-1>', self.select_item)


        # Botões de ação
        botoes_frame = Frame(self)
        botoes_frame.grid(row=2, column=0)   #pack(side='right')

        self.button_1 = Button(
            botoes_frame,
            text='',
            width=10,
            bootstyle='danger',
            state='disable',
            #command=self.excluir_item,
        )
        self.button_1.grid(row=0, column=0, padx=10)

        self.button_2 = Button(
            botoes_frame,
            text='',
            width=10,
            bootstyle='primary',
            state='disable',
            #command=self.editar_item,
        )
        self.button_2.grid(row=0, column=1, padx=10)

        self.button_3 = Button(
            botoes_frame,
            text='Adicionar',
            width=10,
            bootstyle='success',
            state='active',
            command=self.add_item,
        )
        self.button_3.grid(row=0, column=2, padx=10)


        # Label de mensagens temporárias
        self.msg_label = ttk.Label(self, text='', foreground='red')
        self.msg_label.grid(row=3, column=0, columnspan=2) #pack(pady=5)

        self.load_tree()


    def load_tree(self):
        self.clear_tree()
        for _id, _nome, _endereço, _nfe in sql.get_all('fornecedor'):
            self.tree.insert('', 'end', values=(_id, _nome, _endereço, _nfe))

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def add_item(self):
        name = self.var_name.get().strip().capitalize()
        address = self.var_address.get().strip().capitalize()
        nfe = self.var_nfe.get().strip().capitalize()

        if not name:
            self.show_alert('Insira um nome para o fornecedor.')
            return

        forn_list = [item[1] for item in sql.get_all('fornecedor')] 

        if name in forn_list:
            self.show_alert(f'Fornecedor {name} já cadastrado.')     
        else:
            try:
                sql.insert('fornecedor', [(name, address, nfe)])
                self.show_alert(f"{name} cadastrado com sucesso.", 'green')
                self.var_name.set('')
                self.var_address.set('')
                self.var_nfe.set('')
            except Exception as e:
                self.show_alert(f'Erro: {e}')
        self.load_tree()
        
    
    def show_alert(self, text: str, color: str = 'red', time: int = 3000):
        self.msg_label.configure(text=text, foreground=color)
        self.after(time, lambda: self.msg_label.configure(text=''))

    def select_item(self, event):
        item_id = self.tree.focus() # Pega o ID do item selecionado
        item = self.tree.item(item_id)  # Pega os dados do item
        values = item['values']  # Lista com os valores da linha
        
        self.entry_name.config(state='readonly')
        self.entry_address.config(state='readonly')
        self.entry_nfe.config(state='readonly')

        self.button_3_mode('cls')
        self.button_2_mode('edit', values)

        self.var_name.set(values[1])
        self.var_address.set(values[2])
        self.var_nfe.set(values[3])
    
    def clear_entrys(self):
        self.entry_name.config(state='normal')
        self.entry_address.config(state='normal')
        self.entry_nfe.config(state='normal')

        self.var_name.set('')
        self.var_address.set('')
        self.var_nfe.set('')

        self.button_1_mode('off')
        self.button_2_mode('off')
        self.button_3_mode('add')

    
    def edit_item(self, values):
        _id = values[0]
        def save_edit():
            name = self.var_name.get().strip().capitalize()
            address = self.var_address.get().strip().capitalize()
            nfe = self.var_nfe.get().strip().capitalize()

            if not name:
                self.show_alert('Insira um nome para o fornecedor.')
                return

            try: 
                sql.update('fornecedor', _id, [name, address, nfe])
                self.show_alert(f'Fornecedor {name} atualizado com sucesso', 'green')
                self.load_tree()
                self.clear_entrys()
            except Exception as e:
                self.show_alert(f"Erro ao atualizar: {e}")


        self.entry_name.config(state='normal')
        self.entry_address.config(state='normal')
        self.entry_nfe.config(state='normal')

        self.button_1_mode('cancel')
        self.button_2_mode('off')
        self.button_3_mode('save', save_edit)

    
    def button_1_mode(self, mode, command=None):
        match mode:
            case 'cancel': self.button_1.config(text='Cancelar', bootstyle='danger', state='active', command=self.clear_entrys)
            case 'off': self.button_1.config(text='', state='disable')

    def button_2_mode(self, mode, command=None):
        match mode:
            case 'edit': self.button_2.config(text='Editar', bootstyle='primary', state='active', command=lambda: self.edit_item(command))
            case 'off': self.button_2.config(text='', state='disable') 
    
    def button_3_mode(self, mode, command=None):
        match mode:
            case 'add': self.button_3.config(text='Adicionar', bootstyle='success', state='active',command=self.add_item)
            case 'cls': self.button_3.config(text='limpar', bootstyle='info', state='active', command=self.clear_entrys)
            case 'off': self.button_3.config(text='', state='disable')
            case 'save': self.button_3.config(text='Salvar', bootstyle='success', state='active',command=command)
    


class Material(Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=5)

        # Título
        Label(self, text='Matéria-Prima', font=('Arial', 18)).pack(
            pady=(0, 10)
        )

        # Campo de entrada
        self.nome_var = tk.StringVar()
        entry_frame = Frame(self)
        entry_frame.pack(fill='x', pady=10)

        Entry(entry_frame, textvariable=self.nome_var).pack(
            side='left', fill='x', expand=True, padx=(0, 10)
        )
        Button(
            entry_frame, text='Adicionar', command=self.adicionar_item
        ).pack(side='left')

        # Botões de ação
        botoes_frame = Frame(self)
        botoes_frame.pack(pady=10)

        Button(botoes_frame, text='Editar', command=self.editar_item).pack(
            side='left', padx=5
        )
        Button(botoes_frame, text='Excluir', command=self.excluir_item).pack(
            side='left', padx=5
        )

        # Frame da tabela
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill='both', expand=True)

        # Scroll bar vertical
        scrollbar = ttk.Scrollbar(self.tree_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        # Tabela para a visualização
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=('id', 'nome'),
            show='headings',
            height=10,
            yscrollcommand=scrollbar.set,
        )
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.column('id', width=0, stretch=False)  # Oculta ID
        self.tree.column('nome', width=200)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)

        # Label de mensagens temporárias
        self.msg_label = ttk.Label(self, text='', foreground='red')
        self.msg_label.pack(pady=5)

        self.load_tree()

    def load_tree(self):
        self.clear_tree()
        for id, material in sql.get_all('material'):
            self.tree.insert('', 'end', values=(id, material))

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def adicionar_item(self):
        nome = self.nome_var.get().strip().capitalize()
        if not nome:
            self.show_alert('Digite um nome para a matéria-prima.')
            return

        material_existente = [item[1] for item in sql.get_all('material')]

        if nome in material_existente:
            self.show_alert('Já cadastrado')
        else:
            try:
                sql.insert('material', [(nome,)])
                self.show_alert(f'"{nome}" inserido com sucesso.', 'green')
                self.nome_var.set('')  # Limpa campo
            except Exception as e:
                self.show_alert(f'Erro: {e}')
        self.load_tree()

    def show_alert(self, texto: str, cor='red', duração=3000):
        self.msg_label.configure(text=texto, foreground=cor)
        self.after(duração, lambda: self.msg_label.configure(text=''))

    def excluir_item(self):
        selecionado = self.tree.selection()
        if not selecionado:
            self.show_alert('Selecione um item para excluir.')
            return

        item = self.tree.item(selecionado)
        id_item = item['values'][0]  # id está na posição 0

        try:
            sql.delete('material', id_item)
            self.show_alert('Item excluído com sucesso.', 'green')
            self.load_tree()
        except Exception as e:
            self.show_alert(f'Erro ao excluir: {e}')

    def editar_item(self):
        selecionado = self.tree.selection()
        if not selecionado:
            self.show_alert('Selecione um item para editar.')
            return

        item = self.tree.item(selecionado)
        id_item = item['values'][0]
        nome_atual = item['values'][1]

        # Preenche o campo com o nome atual
        self.nome_var.set(nome_atual)

        # Altera o botão "Adicionar" para "Salvar"
        def salvar_edicao():
            novo_nome = self.nome_var.get().strip()
            if not novo_nome:
                self.show_alert('Digite um novo nome.')
                return

            try:
                sql.update('material', id_item, novo_nome)
                self.show_alert('Atualizado com sucesso!', 'green')
                self.nome_var.set('')
                self.load_tree()
                btn_salvar.destroy()
                btn_cancelar.destroy()
                btn_adicionar.pack(side='left')  # volta o botão de adicionar
            except Exception as e:
                self.show_alert(f'Erro ao atualizar: {e}')

        def cancelar_edicao():
            self.nome_var.set('')
            btn_salvar.destroy()
            btn_cancelar.destroy()
            btn_adicionar.pack(side='left')

        # Esconde o botão "Adicionar"
        btn_adicionar = self.children['!frame'].children['!button']
        btn_adicionar.pack_forget()

        # Adiciona botões "Salvar" e "Cancelar"
        btn_salvar = Button(
            self.children['!frame'], text='Salvar', command=salvar_edicao
        )
        btn_salvar.pack(side='left', padx=5)
        btn_cancelar = Button(
            self.children['!frame'], text='Cancelar', command=cancelar_edicao
        )
        btn_cancelar.pack(side='left')


class Empresa(Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        Label(self, text='Empresa', font=('Arial', 18)).pack(pady=(0, 10))

        # Campo de entrada
        self.nome_var = tk.StringVar()
        entry_frame = Frame(self)
        entry_frame.pack(fill='x', pady=10)

        Entry(entry_frame, textvariable=self.nome_var).pack(
            side='left', fill='x', expand=True, padx=(0, 10)
        )
        Button(
            entry_frame, text='Adicionar', command=self.adicionar_item
        ).pack(side='left')

        # Botões de ação
        botoes_frame = Frame(self)
        botoes_frame.pack(pady=10)

        Button(botoes_frame, text='Editar', command=self.editar_item).pack(
            side='left', padx=5
        )
        Button(botoes_frame, text='Excluir', command=self.excluir_item).pack(
            side='left', padx=5
        )

        # Frame da tabela
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(fill='both', expand=True)

        # Scroll bar vertical
        scrollbar = ttk.Scrollbar(self.tree_frame, orient='vertical')
        scrollbar.pack(side='right', fill='y')

        # Tabela com duas colunas: id (oculta) e nome
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=('id', 'nome'),
            show='headings',
            height=10,
            yscrollcommand=scrollbar.set,
        )
        self.tree.heading('id', text='ID')
        self.tree.heading('nome', text='Nome')
        self.tree.column('id', width=0, stretch=False)  # Oculta ID
        self.tree.column('nome', width=200)
        self.tree.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.tree.yview)

        # Label de mensagens temporárias
        self.msg_label = ttk.Label(self, text='', foreground='red')
        self.msg_label.pack(pady=5)

        self.load_tree()

    def load_tree(self):
        self.clear_tree()
        for id, empresa in sql.get_all('empresa'):
            self.tree.insert('', 'end', values=(id, empresa))

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def adicionar_item(self):
        nome = self.nome_var.get().strip().capitalize()
        if not nome:
            self.show_alert('Digite um nome para a empresa.')
            return

        empresa_existente = [item[1] for item in sql.get_all('empresa')]

        if nome in empresa_existente:
            self.show_alert('Já cadastrado')
        else:
            try:
                sql.insert('empresa', [(nome,)])
                self.show_alert(f'"{nome}" inserido com sucesso.', 'green')
                self.nome_var.set('')  # Limpa campo
            except Exception as e:
                self.show_alert(f'Erro: {e}')
        self.load_tree()

    def show_alert(self, texto: str, cor='red', duração=3000):
        self.msg_label.configure(text=texto, foreground=cor)
        self.after(duração, lambda: self.msg_label.configure(text=''))

    def excluir_item(self):
        selecionado = self.tree.selection()
        if not selecionado:
            self.show_alert('Selecione um item para excluir.')
            return

        item = self.tree.item(selecionado)
        id_item = item['values'][0]  # id está na posição 0

        try:
            sql.delete('empresa', id_item)
            self.show_alert('Item excluído com sucesso.', 'green')
            self.load_tree()
        except Exception as e:
            self.show_alert(f'Erro ao excluir: {e}')

    def editar_item(self):
        selecionado = self.tree.selection()
        if not selecionado:
            self.show_alert('Selecione um item para editar.')
            return

        item = self.tree.item(selecionado)
        id_item = item['values'][0]
        nome_atual = item['values'][1]

        # Preenche o campo com o nome atual
        self.nome_var.set(nome_atual)

        # Altera o botão "Adicionar" para "Salvar"
        def salvar_edicao():
            novo_nome = self.nome_var.get().strip()
            if not novo_nome:
                self.show_alert('Digite um novo nome.')
                return

            try:
                sql.update('empresa', id_item, novo_nome)
                self.show_alert('Atualizado com sucesso!', 'green')
                self.nome_var.set('')
                self.load_tree()
                btn_salvar.destroy()
                btn_cancelar.destroy()
                btn_adicionar.pack(side='left')  # volta o botão de adicionar
            except Exception as e:
                self.show_alert(f'Erro ao atualizar: {e}')

        def cancelar_edicao():
            self.nome_var.set('')
            btn_salvar.destroy()
            btn_cancelar.destroy()
            btn_adicionar.pack(side='left')

        # Esconde o botão "Adicionar"
        btn_adicionar = self.children['!frame'].children['!button']
        btn_adicionar.pack_forget()

        # Adiciona botões "Salvar" e "Cancelar"
        btn_salvar = Button(
            self.children['!frame'], text='Salvar', command=salvar_edicao
        )
        btn_salvar.pack(side='left', padx=5)
        btn_cancelar = Button(
            self.children['!frame'], text='Cancelar', command=cancelar_edicao
        )
        btn_cancelar.pack(side='left')
