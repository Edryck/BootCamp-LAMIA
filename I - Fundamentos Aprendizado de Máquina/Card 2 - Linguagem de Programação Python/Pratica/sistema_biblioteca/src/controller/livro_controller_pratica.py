from sistema_biblioteca.src.model.livro_pratica import Livro
from sistema_biblioteca.src.dao.livro_dao_pratica import LivroDAO

def validarLivro(titulo, autor, isbn, disponivel):
    novo_livro = Livro(titulo, autor, isbn, disponivel)
    dao = LivroDAO()
    livro = dao.buscarLivro(isbn)

    # Verifica se foi adicionado os dados do livro
    if len(novo_livro.titulo) == 0 or len(novo_livro.autor) == 0 or len(novo_livro.isbn) == 0:
        return False
    # Verifica se o titulo ou isbn já existe
    if livro is not None:
        if livro[1] == titulo or livro[3] == isbn:
            return False
    return True

def pesquisarLivro(token):
    dao = LivroDAO()

    if token == "":
        return None
    else:
        livro = dao.buscarLivro(token)
        if livro is None:
            return None
        else:
            return livro

def cadastrarLivro(titulo, autor, isbn, disponivel = True):
    dao = LivroDAO()
    sucesso = validarLivro(titulo, autor, isbn, disponivel)

    if sucesso:
        # Verifica se o livro foi cadastrado no banco de dados
        livro = dao.inserirLivro(titulo, autor, isbn, disponivel)
        if livro:
            return True
    return False

def editarLivro(titulo, autor, isbn):
    dao = LivroDAO()

    # Verifica se os dados foram preenchidos
    if titulo == "" or autor == "" or isbn == "":
        return False
    disponibilidade = dao.disponibilidadeLivro(isbn)
    # Só pode editar o livro se ele estiver com status de disponível = True ou 1
    if disponibilidade:
        sucesso = dao.atualizarLivro(titulo, autor, isbn)
        # Verifica se foi atualizado
        if not sucesso:
            return False
    return True

# Lista todos os livros do banco de dados, mas não pensei em nenhuma validação para colocar aqui
def listarLivros():
    dao = LivroDAO()
    livros = dao.listarLivros()

    return livros

def deletarLivro(isbn):
    dao = LivroDAO()

    sucesso = dao.deletarLivro(isbn)
    if isbn == "":
        return False
    elif sucesso:
        return True
    return False