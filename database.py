import sqlite3


def get_connection():
    conn = sqlite3.connect("biblioteca.db")
    conn.row_factory = sqlite3.Row
    return conn


def criar_tabela():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf TEXT,
            livro TEXT NOT NULL,
            data_emprestimo TEXT NOT NULL,
            data_devolucao TEXT NOT NULL,
            devolvido INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def listar_emprestimos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM emprestimos
        ORDER BY devolvido ASC,
                 id DESC
    """)

    dados = cursor.fetchall()
    conn.close()

    return dados


def adicionar_emprestimo(
        nome,
        cpf,
        livro,
        data_emprestimo,
        data_devolucao
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO emprestimos (
            nome,
            cpf,
            livro,
            data_emprestimo,
            data_devolucao
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        nome,
        cpf,
        livro,
        data_emprestimo,
        data_devolucao
    ))

    conn.commit()
    conn.close()


def marcar_devolvido(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE emprestimos
        SET devolvido = 1
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()


def desfazer_devolucao(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE emprestimos
        SET devolvido = 0
        WHERE id = ?
    """, (id,))

    conn.commit()
    conn.close()