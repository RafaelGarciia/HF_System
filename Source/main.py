import sql
from Frames import cadastro
from window import Window

sql.execute(
    """
    CREATE TABLE IF NOT EXISTS material (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    );"""
)

sql.execute(
    """
    CREATE TABLE IF NOT EXISTS empresa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
    );"""
)

sql.execute(
    """
    CREATE TABLE IF NOT EXISTS fornecedor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    endereco TEXT,
    nfe TEXT
    );"""
)


app = Window('Janela', 500, 400)
app.config(
    menu=app.criar_menu(
        {
            'Sistema': {
                'Sair': app.quit,
            },
            'Cadastro': {
                'Material': lambda: app.show_frame(cadastro.Material),
                'Empresa': lambda: app.show_frame(cadastro.Empresa),
                'Fornecedor': lambda: app.show_frame(cadastro.Fornecedor),
            },
        }
    )
)
app.mainloop()
