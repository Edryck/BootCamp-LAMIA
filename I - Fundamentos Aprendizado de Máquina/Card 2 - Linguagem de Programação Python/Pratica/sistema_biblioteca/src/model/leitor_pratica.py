from sistema_biblioteca.src.controller import usuario_controller_pratica
from sistema_biblioteca.src.model.usuario_pratica import Usuario

class Leitor (Usuario):
    def __init__(self):
        super()

    def emprestarLivro(self, isbn):
        sucesso = usuario_controller_pratica.emprestarLivro(isbn)
        if sucesso:
            return True
        return False

    def devolverLivro(self, isbn):
        sucesso = usuario_controller_pratica.devolverLivro(isbn)
        if sucesso:
            return True
        return False