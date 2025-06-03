import sqlite3 as sqlite

path_db = 'data_base.db'


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


def insert(table: str, dados: list[tuple]):
    """
    Insere dados em uma tabela.

    :param table: str - Nome da tabela no banco
    :param dados: list of tuples - Lista de tuplas com os valores a serem inseridos
    """
    conn, cursor = connect()

    # Obtem as colunas da tabela
    cursor.execute(f'PRAGMA table_info({table})')
    colunas_info = cursor.fetchall()

    # Mantém colunas que NÃO são AUTOINCREMENT e que exigem valor
    colunas = [
        col[1] for col in colunas_info if not col[5] or col[4] is not None
    ]

    if not colunas:
        raise ValueError('Nenhuma coluna encontrada para inserção.')

    # Verifica os dados
    for i, item in enumerate(dados):
        if not isinstance(item, tuple):
            raise TypeError(
                f'Dado na posição {i} não é uma tupla. '
                "Se está inserindo uma única string, use vírgula: ('valor',)"
            )
        if len(item) != len(colunas):
            raise ValueError(
                f'Dado na posição {i} tem {len(item)} valores, mas a tabela espera {len(colunas)}.'
            )

    # Monta o SQL dinamicamente
    colunas_str = ', '.join(colunas)
    placeholders = ', '.join(['?'] * len(colunas))
    sql = f'INSERT INTO {table} ({colunas_str}) VALUES ({placeholders})'

    cursor.executemany(sql, dados)

    conn.commit()
    conn.close()


def get_all(table: str):
    conn, cursor = connect()
    cursor.execute('SELECT * FROM material')
    results = cursor.fetchall()
    conn.close()
    return results


def delete(table: str, id_: int):
    conn, cursor = connect()
    cursor.execute(f'DELETE FROM {table} WHERE id = ?', (id_,))
    conn.commit()
    conn.close()


def update(table: str, id_: int, nome: str):
    conn, cursor = connect()
    cursor.execute(f'UPDATE {table} SET nome = ? WHERE id = ?', (nome, id_))
    conn.commit()
    conn.close()
