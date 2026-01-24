import sqlite3

class Database:
    def __init__(self):
        self.conexao = sqlite3.connect('dados//biblioteca_pratica.db')
        self.criarTabela()
    
    def criarTabela(self):
        c = self.conexao.cursor()

        c.execute("""create table if not exists usuarios (idUsuario integer primary key autoincrement,nome varchar(50), senha varchar(50) not null)""")
        c.execute("""create table if not exists livros (idLivro integer primary key autoincrement, titulo varchar(50), autor varchar(50), isbn varchar(50), disponivel boolean)""")

        self.conexao.commit()
        c.close()