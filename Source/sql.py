import sqlite3 as sqlite

path_db = 'data_base.db'


def connect() -> tuple[sqlite.Connection, sqlite.Cursor]:
    conn = sqlite.connect(path_db)
    cursor = conn.cursor()

    return conn, cursor


def execute(sql_script, values=''):
    conn, cursor = connect()
    cursor.execute(sql_script, values)
    conn.commit()
    cursor.close()
    conn.close()
    del conn, cursor


def select(sql_script):
    conn, cursor = connect()
    cursor.execute(sql_script)
    values = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    del conn, cursor
    return values


def execute_script(path_script):
    with open(path_script, 'r', encoding='utf-8') as file:
        script_sql = file.read()

    conn, cursor = connect()
    cursor.executescript(script_sql)
    conn.commit()
    cursor.close()
    conn.close()
    del conn, cursor


def insert(table: str, dados: list[str]):
    """
    Insere dados em uma tabela.

    :param table: str - Nome da tabela no banco
    :param dados: list of tuples - Lista de tuplas com os valores a serem inseridos
    """

    # Obtem as colunas da tabela
    colunas = get_columns(table)

    if not colunas:
        raise ValueError('Nenhuma coluna encontrada para inserção.')

    # Monta o SQL dinamicamente
    colunas_str = ', '.join(colunas)
    placeholders = ', '.join(['?'] * len(colunas))
    sql = f'INSERT INTO {table} ({colunas_str}) VALUES ({placeholders})'

    execute(sql, dados)


def get_columns(table: str):

    columns_info = select(
        f'PRAGMA table_info({table})'
    )    # Obtem as colunas da tabela

    # Mantém colunas que NÃO são AUTOINCREMENT e que exigem valor
    columns = [
        col[1] for col in columns_info if not col[5] or col[4] is not None
    ]
    return columns


def get_all(table: str):

    columns = get_columns(table)
    results = select(f'SELECT * FROM {table} ORDER BY {columns[0]} ASC')
    return results


def delete(table: str, id_: int):
    execute(f'DELETE FROM {table} WHERE id = ?', (id_,))


def update(table: str, id, new_values: list):
    _columns = ', '.join([f'{col} = ?' for col in get_columns(table)])
    try:
        execute(f'UPDATE {table} SET {_columns} WHERE id = {id}', new_values)
    except Exception as e:
        ...
