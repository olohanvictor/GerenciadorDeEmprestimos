import sqlite3

def criar_tabela():
    conn = sqlite3.connect("biblioteca.db")
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
    conn = sqlite3.connect("biblioteca.db")
    conn.row_factory = sqlite3.Row  # Permite acessar os dados como item["nome"]
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emprestimos ORDER BY devolvido ASC, id DESC")
    resultados = cursor.fetchall()
    conn.close()
    return resultados

def adicionar_emprestimo(nome, cpf, livro, data_emp, data_dev):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO emprestimos (nome, cpf, livro, data_emprestimo, data_devolucao, devolvido)
        VALUES (?, ?, ?, ?, ?, 0)
    """, (nome, cpf, livro, data_emp, data_dev))
    conn.commit()
    conn.close()

def atualizar_emprestimo(id_emprestimo, nome, cpf, livro, data_emp, data_dev):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE emprestimos 
        SET nome = ?, cpf = ?, livro = ?, data_emprestimo = ?, data_devolucao = ?
        WHERE id = ?
    """, (nome, cpf, livro, data_emp, data_dev, id_emprestimo))
    conn.commit()
    conn.close()

def marcar_devolvido(id_emprestimo):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE emprestimos SET devolvido = 1 WHERE id = ?", (id_emprestimo,))
    conn.commit()
    conn.close()

def desfazer_devolucao(id_emprestimo):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE emprestimos SET devolvido = 0 WHERE id = ?", (id_emprestimo,))
    conn.commit()
    conn.close()

def excluir_emprestimo(id_emprestimo):
    conn = sqlite3.connect("biblioteca.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM emprestimos WHERE id = ?", (id_emprestimo,))
    conn.commit()
    conn.close()