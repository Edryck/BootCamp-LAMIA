from sistema_biblioteca.src.controller import livro_controller_pratica, usuario_controller_pratica
from sistema_biblioteca.src.model.usuario_pratica import Usuario


class Bibliotecario (Usuario):
    def __init__(self):
        super()

    def cadastrarLivro(self, titulo, autor, isbn):
        sucesso = livro_controller_pratica.cadastrarLivro(titulo, autor, isbn, disponivel = True)
        if sucesso:
            return True
        return False

    def deletarLivro(self, isbn):
        sucesso = livro_controller_pratica.deletarLivro(isbn)
        if sucesso:
            return True
        return False

    def alterarLivro(self, titulo, autor, isbn):
        sucesso = livro_controller_pratica.editarLivro(titulo, autor, isbn)
        if sucesso:
            return True
        return False

    def alterarUsuario(self, nome, senha, idUsuario):
        sucesso = usuario_controller_pratica.editarUsuario(nome, senha, idUsuario)
        if sucesso:
            return True
        return False

    def deletarUsuario(self, idUsuario):
        sucesso = usuario_controller_pratica.deletarUsuario(idUsuario)
        if sucesso:
            return True
        return False