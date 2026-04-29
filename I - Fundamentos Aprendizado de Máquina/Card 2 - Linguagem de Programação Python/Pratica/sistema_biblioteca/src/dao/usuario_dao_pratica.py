from sistema_biblioteca.src.dao.database_pratica import Database

class UsuariosDAO(object):
    def __init__(self, idUsuario = 0, nome = "", senha = ""):
        self.idUsuario = idUsuario
        self.nome = nome
        self.senha = senha

    # Inserir usuário
    def inserirUsuario(self, nome, senha):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "insert into usuarios (nome, senha) values (?, ?)"
            c.execute(sql, (nome, senha,))

            database.conexao.commit()
            c.close()
            return True
        except Exception as e:
            print(f"Ocorreu um erro na inserção: {e}")
            return False

    # Atualizar usuário
    def atualizarUsuario(self, nome, senha, idUsuario):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "update usuarios set nome = ?, senha = ? where idUsuario = ?"
            c.execute(sql, (nome, senha, idUsuario,))

            database.conexao.commit()
            c.close()
            return True
        except Exception as e:
            print(f"Ocorreu um erro na alteração: {e}")
            return False

    # Deletar usuário
    def deletarUsuario(self, idUsuario):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "delete from usuarios where idUsuario = ?"
            c.execute(sql, (idUsuario,))

            database.conexao.commit()
            c.close()
            return "Usuário excluído com sucesso!"
        except Exception as e:
            return f"Ocorreu um erro ao excluir: {e}"

    # Buscar usuário
    def buscarUsuario(self, termo):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "select * from usuarios where idUsuario = ? or nome = ?"
            c.execute(sql, (termo, termo,))
            linha = c.fetchone()

            c.close()
            if linha:
                self.idUsuario = linha[0]
                self.nome = linha[1]
                self.senha = linha[2]
                return linha
            else:
                return None
        except Exception as e:
            print(f"Ocorreu um erro na busca: {e}")
            return None

    def listarUsuarios(self):
        database = Database()
        try:
            c = database.conexao.cursor()

            sql = "select * from usuarios"
            c.execute(sql)

            usuarios = c.fetchall()

            c.close()
            if usuarios is None:
                return None
            else:
                return usuarios
        except Exception as e:
            print(f"Ocorreu um erro ao listar os usuarios: {e}")
            return None