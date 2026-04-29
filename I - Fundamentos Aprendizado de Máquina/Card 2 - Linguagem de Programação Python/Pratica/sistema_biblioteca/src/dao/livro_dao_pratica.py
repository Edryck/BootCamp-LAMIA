from sistema_biblioteca.src.dao.database_pratica import Database

class LivroDAO(object):
    def __init__(self, titulo = "", autor = "", isbn = "", disponivel = True):
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponivel = disponivel

    # Inserir livro
    def inserirLivro(self, titulo, autor, isbn, disponivel):
        database = Database()
        try: 
            c = database.conexao.cursor()

            sql = "insert into livros (titulo, autor, isbn, disponivel) values (?, ?, ?, ?)"
            c.execute(sql, (titulo, autor, isbn, disponivel,))

            database.conexao.commit()
            c.close()

            return True
        except Exception as e:
            print(f"Ocorreu um erro ao inserir o livro: {e}")
            return False
        
    # Atualizar livro
    def atualizarLivro(self, titulo, autor, isbn):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "update livros set titulo = ?, autor = ? where isbn = ?"
            c.execute(sql, (titulo, autor, isbn,))

            database.conexao.commit()
            c.close()

            return True
        except Exception as e:
            print(f"Ocorreu um erro na alteração do livro: {e}")
            return False
    
    # Deletar livro
    def deletarLivro(self, isbn):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "delete from livros where isbn = ?"
            c.execute(sql, (isbn,))

            database.conexao.commit()
            c.close()

            return True
        except Exception as e:
            print(f"Ocorreu um erro ao excluir o livro: {e}")
            return False

            # Buscar livro
    def buscarLivro(self, termo):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "select * from livros where titulo = ? or autor = ? or isbn = ?"
            c.execute(sql, (termo, termo, termo,))

            linha = c.fetchone()

            if linha:
                self.idLivro = linha[0]
                self.titulo = linha[1]
                self.autor = linha[2]
                self.isbn = linha[3]
                self.disponivel = linha[4]
                c.close()
                return linha
            else:
                c.close()
                return None
        except Exception as e:
            print(f"Ocorreu um erro ao buscar o livro: {e}")
            return None

    def listarLivros(self):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "select * from livros"
            c.execute(sql)

            livros= c.fetchall()

            c.close()

            return livros
        except Exception as e:
            print(f"Ocorreu um erro ao listar os livros: {e}")
            return None

    def disponibilidadeLivro(self, isbn):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "select * from livros where isbn = ?"
            c.execute(sql, (isbn,))

            livro = c.fetchone()

            c.close()

            if livro:
                self.disponivel = livro[4]
                if livro[4]:
                    return True
            return False
        except Exception as e:
            print(f"Ocorreu um erro ao verificar a disponibilidade do livro: {e}")
            return False

    def emprestarLivro(self, idLivro):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "update livros set disponivel = 0 where idLivro = ?"
            c.execute(sql, (idLivro,))

            database.conexao.commit()
            c.close()

            return True
        except Exception as e:
            print(f"Ocorreu um erro no empréstimo do livro: {e}")
            return False

    def devolverLivro(self, idLivro):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "update livros set disponivel = 1 where idLivro = ?"
            c.execute(sql, (idLivro,))

            database.conexao.commit()
            c.close()

            return True
        except Exception as e:
            print(f"Ocorreu um erro na devolução do livro: {e}")
            return False