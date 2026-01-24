from sistema_biblioteca.src.dao.usuario_dao_pratica import UsuariosDAO

def entrar(nome = "", senha = ""):
    usuario = UsuariosDAO()
    resultado = usuario.buscarUsuario(nome)

    # Verifica se retornou um usuário vazio
    if resultado is None:
        return False # Falha  o login
    return True

