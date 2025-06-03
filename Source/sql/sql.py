import sqlite3 as sqlite

path_db = ''

def connect() -> tuple[sqlite.Connection, sqlite.Cursor]:
    conn = sqlite.connect(path_db)
    cursor = conn.cursor()

    return conn, cursor

def execute_script(path_script):
    with open(path_script, 'r', encoding='utf-8') as file:
        script_sql = file.read()
    
    conn, cursor = connect()
    cursor.executescript(script_sql)
    conn.commit()
    conn.close()

def insert(table:str, dados:list):
    """
    Insere dados em uma tabela sem precisar saber as colunas de antemão.
    
    :param table: str - Nome da tabela no banco
    :param dados: list of tuples - Lista de tuplas com os valores a serem inseridos
    """
    conn, cursor = connect()

    # Pegando as colunas da tabela
    cursor.execute(f'PRAGMA table_info({table})')
    colunas_info = cursor.fetchall()

    # Ignora colunas AUTOINCREMENT ou sem valor padrão obrigatório
    colunas = [col[1] for col in colunas_info if not col[5]]

    if not colunas:
        raise ValueError("Nenhuma coluna encontrada para inserção.")
    
    # Monta SQL dinâmico
    colunas_str = ", ".join(colunas)
    placeholders = ", ".join(["?"] * len(colunas))
    sql = f"INSERT INTO {table} ({colunas_str}) VALUES ({placeholders})"

    # Insere os dados
    cursor.executemany(sql, dados)

    conn.commit()
    conn.close()