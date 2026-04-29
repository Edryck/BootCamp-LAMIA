from sistema_biblioteca.src.dao import usuario_dao_pratica
from sistema_biblioteca.src.dao.usuario_dao_pratica import UsuariosDAO
from sistema_biblioteca.src.model.usuario_pratica import Usuario


def cadastrarUsuario(nome, senha):
    dao = UsuariosDAO()
    resultados = dao.buscarUsuario(nome)

    if resultados is None:
        sucesso = dao.inserirUsuario(nome, senha)
        if sucesso:
            return sucesso
    return False