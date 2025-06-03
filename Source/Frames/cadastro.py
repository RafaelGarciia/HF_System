import tkinter as tk
from tkinter import END, ttk
from ttkbootstrap.widgets import Frame, Label, Entry, Button
import sql


class FrameCadastroMaterial(Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=20)

        Label(self, text="Matéria-Prima", font=("Arial", 18)).pack(pady=(0, 10))

        # Campo de entrada
        self.nome_var = tk.StringVar()
        entry_frame = Frame(self)
        entry_frame.pack(fill="x", pady=10)

        Entry(entry_frame,textvariable=self.nome_var).pack(side="left", fill="x", expand=True, padx=(0, 10))
        Button(entry_frame, text="Adicionar", command=self.adicionar_item).pack(side="left")

        # Tabela
        self.tree = ttk.Treeview(self, columns=("nome",), show="headings", height=10)
        #self.tree.heading("nome", text="Matéria-Prima")
        self.tree.pack(fill="both", expand=True, pady=10)
        self.tree_clear()
        
        conn, cursor = sql.connect()
        cursor.execute('SELECT * FROM material')
        results = cursor.fetchall()
        conn.close()
        del conn, cursor

        for item in results:
            self.tree.insert("", "end", values=(item,))


    def tree_clear(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def adicionar_item(self):
        nome = self.nome_var.get().strip()
        if nome:
            sql.insert('material', [nome])
            self.nome_var.set("")