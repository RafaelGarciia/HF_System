import tkinter as tk
from tkinter import END, ttk
from ttkbootstrap.widgets import Frame, Label, Entry, Button
import sql


class Material(Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

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

        Label(self, text='Empresa', font=('Arial', 18)).pack(
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
