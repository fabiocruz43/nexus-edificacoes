import sqlite3


def conectar():
    return sqlite3.connect("clientes.db")


def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            whatsapp TEXT NOT NULL,
            email TEXT,
            cidade TEXT,
            servico TEXT,
            mensagem TEXT,
            data TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def salvar_cliente(nome, whatsapp, email, cidade, servico, mensagem):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clientes
        (nome, whatsapp, email, cidade, servico, mensagem)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nome, whatsapp, email, cidade, servico, mensagem))

    conn.commit()
    conn.close()


def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, whatsapp, email, cidade, servico, mensagem, data
        FROM clientes
        ORDER BY id DESC
    """)

    clientes = cursor.fetchall()
    conn.close()
    return clientes