from tkinter import *
from tkinter import messagebox, ttk

from sistema_biblioteca.src.controller import livro_controller_pratica, usuario_controller_pratica
from sistema_biblioteca.src.model.bibliotecario_pratica import Bibliotecario

class TelaAdmin:
    def __init__(self, master):
        self.root = master
        self.root.title("Sistema de Biblioteca - Administrador", )
        self.root.geometry("445x550")

        self.borda = LabelFrame(self.root)
        self.borda["background"] = "#e9e9e9"
        self.borda.pack(ipady=3, ipadx=3, expand=True, fill="y")
        self.conteinerPrincipal = Frame(self.borda)
        self.conteinerPrincipal.pack(pady=20, padx=20, expand=True, fill="both")

        # Barra de rolagem da tela inteira
        scrollbar = ttk.Scrollbar(self.conteinerPrincipal, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.mensagem = Label(self.conteinerPrincipal)
        self.mensagem["text"] = "Bem-vindo à Biblioteca"
        self.mensagem["font"] = ("Arial", 15, "bold")
        self.mensagem.pack(pady=5)

        Button(self.conteinerPrincipal, text="Sair", command=self.sair).pack()

        self.conteinerConsulta = LabelFrame(self.conteinerPrincipal)
        self.conteinerConsulta["text"] = "Pesquisar Livro"
        self.conteinerConsulta.pack(padx=10, pady=10, expand=True, fill="x")

        self.consultarLivro = Entry(self.conteinerConsulta)
        self.consultarLivro["width"] = 30
        self.consultarLivro.pack(pady=20, side="left", expand=True, fill="x")

        self.buscar = Button(self.conteinerConsulta)
        self.buscar["command"] = self.buscarLivro
        self.buscar["text"] = "Buscar Livro"
        self.buscar.pack(pady=20, padx=5, side="right")

        self.abas = ttk.Notebook(self.conteinerPrincipal)
        self.abas.pack(fill="both", expand=True)

        # O conteiner principal de cada aba
        self.abaLivros = Frame(self.abas)
        self.abaUsuarios = Frame(self.abas)

        # Adição das abas
        self.abas.add(self.abaLivros, text="Gerenciar Livros")
        self.abas.add(self.abaUsuarios, text="Gerenciar Usuários")

        self.conteinerCadastro = LabelFrame(self.abaLivros)
        self.conteinerCadastro["text"] = "Adicionar/Remover/Editar Livro"
        self.conteinerCadastro.pack(padx=10, pady=10, expand=True, fill="x")

        # Função para criar os campos de input
        def criarCampo(frame, texto):
            conteiner = Frame(frame)
            conteiner.pack(pady=2)
            Label(conteiner, text=texto, width=15, anchor="e").pack(side="left")
            entry = Entry(conteiner, width=30)
            entry.pack(side="left")
            return entry

        self.tituloLivro = criarCampo(self.conteinerCadastro, "Título do Livro:")
        self.autorLivro = criarCampo(self.conteinerCadastro, "Autor do Livro:")
        self.isbnLivro = criarCampo(self.conteinerCadastro, "ISBN:")

        self.opcoes = Frame(self.conteinerCadastro)
        self.opcoes.pack()

        Button(self.opcoes, text="Cadastrar Livro", command=self.cadastrarLivro).pack(pady=10, side="left",)
        Button(self.opcoes, text="Editar Livro", command=self.editarLivro).pack(pady=10, side="left", )
        Button(self.opcoes, text="Deletar Livro", command=self.deletarLivro).pack(pady=10, side="left",)

        Label(self.conteinerCadastro, text=f"OBS: Para deletar o livro coloque o ISBN dele e clica deletar,\npara alterar adicione o ISBN e altere os dados titulo e autor.").pack()

        # Lista dos livros do banco de dados
        self.conteinerLista = LabelFrame(self.abaLivros)
        self.conteinerLista["text"] = "Acervo da Biblioteca"
        self.conteinerLista.pack(pady=10, padx=10, expand=True, fill="x")

        # Botão para atualizar a lista
        Button(self.conteinerLista, text="Atualizar Lista", command=self.carregarLista).pack(anchor="e")

        # Lista de livros
        colunas = ("ID", "Título", "Autor", "ISBN")
        self.tree = ttk.Treeview(self.conteinerLista)
        self.tree["columns"] = colunas
        self.tree["show"] = "headings"

        self.tree.heading("ID", text="ID")
        self.tree.heading("Título", text="Título")
        self.tree.heading("Autor", text="Autor")
        self.tree.heading("ISBN", text="ISBN")

        self.tree.column("ID", width=25, anchor="center")
        self.tree.column("Título", width=150)
        self.tree.column("Autor", width=100)
        self.tree.column("ISBN", width=75)

        # Barra de rolagem da lista
        scrollbar0 = ttk.Scrollbar(self.conteinerLista)
        scrollbar0["orient"] = "vertical"
        scrollbar0["command"] = self.tree.yview
        self.tree.configure(yscroll=scrollbar0.set)
        scrollbar0.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Carrega a lista quando abre a tela
        self.carregarLista()

        self.conteinerGerenciarUsuarios = LabelFrame(self.abaUsuarios)
        self.conteinerGerenciarUsuarios["text"] = "Atualizar/Deletar Usuários"
        self.conteinerGerenciarUsuarios.pack(pady=10, padx=10, expand=True, fill="x")

        self.idUsuario = criarCampo(self.conteinerGerenciarUsuarios, "Id:")
        self.nomeUsuario = criarCampo(self.conteinerGerenciarUsuarios, "Nome do Usuário:")
        self.senhaUsuario = criarCampo(self.conteinerGerenciarUsuarios, "Senha de Usuário:")

        self.opcoes1 = Frame(self.conteinerGerenciarUsuarios)
        self.opcoes1.pack()

        Button(self.opcoes1, text="Atualizar Usuário", command=self.atualizarUsuario).pack(pady=10, side="left", )
        Button(self.opcoes1, text="Deletar Usuário", command=self.deletarUsuario).pack(pady=10, side="left", )

        # Lista dos usuário do banco de dados
        self.conteinerUsuario = LabelFrame(self.abaUsuarios)
        self.conteinerUsuario["text"] = "Usuários da Biblioteca"
        self.conteinerUsuario.pack(pady=10, padx=10, expand=True, fill="x")

        # Botão para atualizar a lista
        Button(self.conteinerUsuario, text="Atualizar Lista", command=self.carregarListaUsuarios).pack(anchor="e")

        # Lista de livros
        colunasLU = ("IDUsuario", "NomeUsuario", "SenhaUsuario")
        self.treeU = ttk.Treeview(self.conteinerUsuario)
        self.treeU["columns"] = colunasLU
        self.treeU["show"] = "headings"

        self.treeU.heading("IDUsuario", text="ID")
        self.treeU.heading("NomeUsuario", text="Nome do Usuário")
        self.treeU.heading("SenhaUsuario", text="Senha do Usuário")

        self.treeU.column("IDUsuario", width=25, anchor="center")
        self.treeU.column("NomeUsuario", width=150)
        self.treeU.column("SenhaUsuario", width=100)

        # Barra de rolagem da lista
        scrollbar1 = ttk.Scrollbar(self.conteinerUsuario)
        scrollbar1["orient"] = "vertical"
        scrollbar1["command"] = self.treeU.yview
        self.tree.configure(yscroll=scrollbar1.set)
        scrollbar1.pack(side="right", fill="y")
        self.treeU.pack(fill="both", expand=True)

        self.carregarListaUsuarios()

    def buscarLivro(self):
        token = self.consultarLivro.get()
        # Chama o controller
        livro = livro_controller_pratica.pesquisarLivro(token)

        if livro is None:
            messagebox.showwarning("Atenção", "Livro não encontrado.")
        else:
            # Mostra os dados encontrados
            messagebox.showinfo("Livro Encontrado", f"ID: {livro[0]}\nTítulo: {livro[1]}\nAutor: {livro[2]}\nISBN: {livro[3]}\nDisponível: {livro[4]}")

    def cadastrarLivro(self):
        bibliotecario = Bibliotecario()

        titulo = self.tituloLivro.get()
        autor = self.autorLivro.get()
        isbn = self.isbnLivro.get()

        sucesso = bibliotecario.cadastrarLivro(titulo, autor, isbn)

        if sucesso:
            messagebox.showinfo("Livro cadastrado!", "Cadastro realizado com sucesso!")
            # Limpa campos de input
            self.tituloLivro.delete(0, END)
            self.autorLivro.delete(0, END)
            self.isbnLivro.delete(0, END)
            # Atualiza a lista de livros
            self.carregarLista()
        else:
            messagebox.showerror("Erro", "Não foi possível realizar o cadastro!")

    def editarLivro(self):
        bibliotecario = Bibliotecario()

        titulo = self.tituloLivro.get()
        autor = self.autorLivro.get()
        isbn = self.isbnLivro.get()

        sucesso = bibliotecario.alterarLivro(titulo, autor, isbn)
        if sucesso:
            messagebox.showinfo("Livro Alterado!", "Os dados do livro foram alterados com sucesso!")
            # Limpa campos de input
            self.tituloLivro.delete(0, END)
            self.autorLivro.delete(0, END)
            self.isbnLivro.delete(0, END)
            # Atualiza a lista de livros
            self.carregarLista()
        else:
            messagebox.showerror("Erro", "Não foi possível realizar a alteração!")

    def deletarLivro(self):
        bibliotecario = Bibliotecario()

        isbn = self.isbnLivro.get()

        sucesso = bibliotecario.deletarLivro(isbn)
        if sucesso:
            messagebox.showinfo("Livro deletado!", "O livro deletado com sucesso!")
            self.isbnLivro.delete(0, END)
            self.carregarLista()
        else:
            messagebox.showerror("Erro", "Não foi possível deletar esse livro!")

    def carregarLista(self):
        # Limpa a lista
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Busca os dados recentes
        livros = livro_controller_pratica.listarLivros()

        if livros:
            for livro in livros:
                # Insere na tabela
                self.tree.insert("", "end", values=(livro[0], livro[1], livro[2], livro[3]))

    def atualizarUsuario(self):
        bibliotecario = Bibliotecario()

        nome = self.nomeUsuario.get()
        senha = self.senhaUsuario.get()

        sucesso = bibliotecario.alterarUsuario(nome, senha)
        if sucesso:
            messagebox.showinfo("Dados atualizados!", f"Os dados do usuário {nome} foram atualizados com sucesso!")
            self.nomeUsuario.delete(0, END)
            self.senhaUsuario.delete(0, END)
            self.carregarListaUsuarios()
        else:
            messagebox.showerror("Erro", "Não foi possível atualizar os dados deste usuário!")

    def deletarUsuario(self):
        bibliotecario = Bibliotecario()

        id = self.idUsuario.get()

        sucesso = bibliotecario.deletarUsuario(id)
        if sucesso:
            messagebox.showinfo("Usuário excluído!", f"O usuário foi apagado com sucesso!")
            self.idUsuario.delete(0, END)
            self.carregarListaUsuarios()
        else:
            messagebox.showerror("Erro", "Não foi possível excluir este usuário!")

    def carregarListaUsuarios(self):
        for usuario in self.treeU.get_children():
            self.treeU.delete(usuario)

        usuarios = usuario_controller_pratica.listarUsuarios()

        if usuarios is not None:
            for usuario in usuarios:
                self.treeU.insert("", "end", values=(usuario[0], usuario[1], usuario[2]))

    def sair(self):
        from sistema_biblioteca.src.view import login_pratica
        self.borda.destroy()
        login_pratica.Application(self.root)