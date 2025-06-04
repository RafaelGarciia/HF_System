from window import Window
from Frames import cadastro
import sql

sql.execute_script('sql_queries\\mk_database.sql')


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
