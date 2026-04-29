from tkinter import *
from tkinter import messagebox
from sistema_biblioteca.src.controller import autenticar_login_pratica
from sistema_biblioteca.src.view.user import telas_user_pratica
from sistema_biblioteca.src.view.admin import telas_admin_pratica

class Application:
    # Estrutura da tela de login
    def __init__(self, master):
        self.root = master
        self.root.title("Sistema de Biblioteca - Login")
        self.root.geometry("500x350")

        self.mensagem = Label(
            self.root,
            text="Sistema Biblioteca",
            font=("Arial", 15, "bold")
        )
        self.mensagem.pack(pady=20)

        # Formulário de Login
        self.formulario = LabelFrame(self.root)
        self.formulario["text"] = "Login"
        self.formulario.pack(ipadx=20, ipady=20, expand=True)

        # Campo de adicionar o nome do usuário
        self.conteiner1 = Frame(self.formulario)
        self.conteiner1.pack(padx=20)

        self.usuarioLabel = Label(self.conteiner1)
        self.usuarioLabel["text"] = "Usuário: "
        self.usuarioLabel["width"] = 7
        self.usuarioLabel.pack(pady=10, side="left")

        self.campoUsuario = Entry(self.conteiner1)
        self.campoUsuario["width"] = 30
        self.campoUsuario.pack(pady=10, side="left")

        # Campo de adicionar a senha do usuário
        self.conteiner2 = Frame(self.formulario)
        self.conteiner2.pack(padx=20)

        self.senhaLabel = Label(self.conteiner2)
        self.senhaLabel["text"] = "Senha: "
        self.senhaLabel["width"] = 7
        self.senhaLabel.pack(pady=10, side="left")

        self.campoSenha = Entry(self.conteiner2)
        self.campoSenha["width"] = 30
        self.campoSenha["show"] = "*"
        self.campoSenha.pack(pady=10, side="left")

        self.container3 = Frame(self.formulario)
        self.container3.pack()

        # Botão de entrar
        self.botaoEntrar = Button(self.container3)
        self.botaoEntrar["text"] = "Entrar"
        self.botaoEntrar["width"] = 12
        self.botaoEntrar["command"] = self.autenticar
        self.botaoEntrar.pack(side="left")

        # Botão de cadastrar
        self.botaoCadastro = Button(self.container3)
        self.botaoCadastro["text"] = "Cadastrar"
        self.botaoCadastro["width"] = 12
        self.botaoCadastro["command"] = self.telaCadastro
        self.botaoCadastro.pack(side="left")

        # Botão de sair
        self.botaoSair = Button(self.formulario)
        self.botaoSair["text"] = "Sair"
        self.botaoSair["width"] = 12
        self.botaoSair["command"] = self.root.quit
        self.botaoSair.pack()

    # Ir para tela de cadastro
    def telaCadastro(self):
        from sistema_biblioteca.src.view import cadastro_pratica
        self.formulario.destroy()
        self.mensagem.destroy()
        cadastro_pratica.CadPrincipal(self.root)

    # Autenticar login
    def autenticar(self):
        usuario = self.campoUsuario.get()
        senha = self.campoSenha.get()
        # Caso seja o administrador
        if usuario == "admin" and senha == "admin123":
            self.formulario.destroy()
            self.mensagem.destroy()
            telas_admin_pratica.TelaAdmin(self.root)
        # Caso seja o usuário comum (leitor)
        else:
            # Verifica se está cadastrado
            sucesso = autenticar_login_pratica.entrar(usuario, senha)
            # Se o que retornar não for none ou false
            if sucesso:
                self.formulario.destroy()
                self.mensagem.destroy()
                telas_user_pratica.TelaUser(self.root)
            else:
                messagebox.showerror(
                    "Erro",
                    "Usuário ou senha incorreta"
                )