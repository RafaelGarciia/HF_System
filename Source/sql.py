import sqlite3 as sql
from os import system

def connect() -> list[sql.Connection, sql.Cursor]:
    connection = sql.connect('bank.db')
    cursor = connection.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS employees (name, company)")
    cursor.execute("CREATE TABLE IF NOT EXISTS companies (name)")

    return connection, cursor