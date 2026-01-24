from tkinter import *
from tkinter import messagebox
from sistema_biblioteca.src.controller import criar_usuario_pratica

class CadPrincipal:
    # Estrutura da tela de cadastro
    def __init__(self, master):
        self.root = master
        self.root.title("Sistema de Biblioteca - Cadastro")
        self.root.geometry("500x350")

        # Formulário de Login
        self.formulario = LabelFrame(self.root, text="Cadastro")
        self.formulario.pack(ipadx=20, expand=True)

        self.mensagem = Label(
            self.formulario,
            text="Cadastro",
            font=("Arial", 15, "bold")
        )
        self.mensagem.pack(pady=20)

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

        self.conteiner2 = Frame(self.formulario)
        self.conteiner2.pack(padx=20)

        # Campo de adicionar a senha do usuário
        self.senhaLabel = Label(self.conteiner2)
        self.senhaLabel["text"] = "Senha: "
        self.senhaLabel["width"] = 7
        self.senhaLabel.pack(pady=10, side="left")

        self.campoSenha = Entry(self.conteiner2)
        self.campoSenha["width"] = 30
        self.campoSenha["show"] = "*"
        self.campoSenha.pack(pady=10, side="left")

        # Botão de cadastrar
        self.botaoCadastro = Button(self.formulario)
        self.botaoCadastro["text"] = "Cadastrar"
        self.botaoCadastro["font"] = ("Calibri", "8")
        self.botaoCadastro["width"] = 12
        self.botaoCadastro["command"] = self.cadUsuario
        self.botaoCadastro.pack()

        # Botão de voltar
        self.botaoSair = Button(self.formulario)
        self.botaoSair["text"] = "Sair"
        self.botaoSair["font"] = ("Calibri", "8")
        self.botaoSair["width"] = 12
        self.botaoSair["command"] = self.voltar
        self.botaoSair.pack()

    # Volta para a tela de login
    def voltar(self):
        from sistema_biblioteca.src.view import login_pratica
        self.formulario.destroy()
        login_pratica.Application(self.root)

    def cadUsuario(self):
        usuario = self.campoUsuario.get()
        senha = self.campoSenha.get()
        if usuario == "" or senha == "":
            messagebox.showerror("Erro", "Informe os campos")
        else:
            sucesso = criar_usuario_pratica.cadastrarUsuario(usuario, senha)
            if sucesso:
                messagebox.showinfo("Sucesso!", " Usuário cadastrado com sucesso!")
                self.voltar()
            else:
                messagebox.showerror("Erro", "Não foi possível cadastrar o usuário")