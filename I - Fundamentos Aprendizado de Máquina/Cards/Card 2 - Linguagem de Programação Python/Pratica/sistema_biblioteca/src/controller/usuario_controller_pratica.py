from sistema_biblioteca.src.dao.livro_dao_pratica import LivroDAO
from sistema_biblioteca.src.dao.usuario_dao_pratica import UsuariosDAO

def pesquisarUsuario(termo):
    dao = UsuariosDAO()

    if termo == "":
        return None
    else:
        livro = dao.buscarUsuario(termo)
        if livro is None:
            return None
        return livro

def editarUsuario(nome, senha, idUsuario):
    dao = UsuariosDAO()

    # Verifica se os dados foram preenchidos
    if nome == "" or senha == "":
        return False
    sucesso = dao.atualizarUsuario(nome, senha, idUsuario)
    # Verifica se foi atualizado
    if sucesso:
        return True
    return False

# Lista todos os usuarios do banco de dados
def listarUsuarios():
    dao = UsuariosDAO()
    usuarios = dao.listarUsuarios()

    if usuarios is not None:
        return usuarios
    return None

def deletarUsuario(idUsuario):
    dao = UsuariosDAO()

    sucesso = dao.deletarUsuario(idUsuario)
    # Verifica se foi preenchido
    if idUsuario == "":
        return False
    elif sucesso:
        return True
    return False

def emprestarLivro(isbn):
    dao = LivroDAO()

    livro = dao.buscarLivro(isbn)

    if isbn == "":
        return False
    # Se o livro estiver estiver disponivel
    elif livro[4] == 1:
        sucesso = dao.emprestarLivro(livro[0])
        if sucesso:
            return True
    return False

def devolverLivro(isbn):
    dao = LivroDAO()

    livro = dao.buscarLivro(isbn)

    if isbn == "":
        return False
    # Se o livro estiver estiver indisponivel
    elif livro[4] == 0:
        sucesso = dao.devolverLivro(livro[0])
        if sucesso:
            return True
    return False