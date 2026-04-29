from sistema_biblioteca.src.controller import livro_controller_pratica

class Usuario:
    def __init__(self, nome, senha):
        self.__nome = nome
        self.__senha = senha

    # Getters e Setters
    @property
    def nome(self):
        return self.__nome
    
    @nome.setter
    def nome(self, novo_nome):
        self.__nome = novo_nome

    @property
    def senha(self):
        return self.__senha
    
    @senha.setter
    def senha(self, nova_senha):
        self.__senha = nova_senha

    # Métodos, alguns vão estar com pass porque vai ser
    # implentado a lógica deles nas classes filhas (bibliotecário
    # e leitor), mas as funcionalidade disponiveis para os dois
    # serão implementadas aqui na classe pai.

    def pesquisarLivro(self, token):
        if token == "":
            return None
        else:
            livro = livro_controller_pratica
            if livro is None:
                return None
            else:
                return livro


    def emprestarLivro(self):
        pass

    def devolverLivro(self):
        pass

    def cadastrarLivro(self):
        pass

    def alterarLivro(self):
        pass

    def deletarLivro(self):
        pass

    def alterarUsuario(self):
        pass

    def deletarUsuario(self):
        pass