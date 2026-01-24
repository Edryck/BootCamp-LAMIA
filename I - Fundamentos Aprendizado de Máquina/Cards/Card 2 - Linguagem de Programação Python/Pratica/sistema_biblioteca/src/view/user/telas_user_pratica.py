from tkinter import *
from tkinter import ttk, messagebox

from sistema_biblioteca.src.controller import livro_controller_pratica
from sistema_biblioteca.src.model.leitor_pratica import Leitor


class TelaUser:
    def __init__(self, master):
        self.root = master
        self.root.title("Sistema de Biblioteca - Usuário", )
        self.root.geometry("445x550")

        self.borda = LabelFrame(self.root)
        self.borda["background"] = "#e9e9e9"
        self.borda.pack(ipady=3, ipadx=3, expand=True, fill="y")

        self.conteinerPrincipal = Frame(self.borda)
        self.conteinerPrincipal.pack(pady=20, padx=20, expand=True, fill="both")

        scrollbar = ttk.Scrollbar(self.conteinerPrincipal)
        scrollbar["orient"] = "vertical"
        scrollbar.pack(side="right", fill="y")

        self.mensagem = Label(self.conteinerPrincipal)
        self.mensagem["text"] = "Bem vindo à Biblioteca"
        self.mensagem["font"] = ("Arial", 15, "bold")
        self.mensagem.pack(pady=10)

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

        self.conteinerEmpDev = LabelFrame(self.conteinerPrincipal)
        self.conteinerEmpDev["text"] = "Empréstimo/Devolução de Livros"
        self.conteinerEmpDev.pack(padx=10, pady=10, expand=True, fill="x")

        # Função para criar os campos de input
        def criarCampo(frame, texto):
            f = Frame(frame)
            f.pack(pady=2)
            Label(f, text=texto, width=15, anchor="e").pack(side="left")
            entry = Entry(f, width=30)
            entry.pack(side="left")
            return entry

        self.isbnLivro = criarCampo(self.conteinerEmpDev, "ISBN:")

        self.opcoes = Frame(self.conteinerEmpDev)
        self.opcoes.pack()

        # Botões de ação
        Button(self.opcoes, text="Pegar Livro", command=self.pegarLivro).pack(pady=10, side="left", )
        Button(self.opcoes, text="Devolver Livro", command=self.devolverLivro).pack(pady=10, side="left", )

        Label(self.conteinerEmpDev, text=f"OBS: Para reservar/devolver o livro coloque o ISBN\ndele e pressione Pegar/Devolver Livro.").pack()

        self.conteinerLista = LabelFrame(self.conteinerPrincipal)
        self.conteinerLista["text"] = "Acervo da Biblioteca"
        self.conteinerLista.pack(pady=10, padx=10, expand=True, fill="both")

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
        scrollbar = ttk.Scrollbar(self.conteinerLista)
        scrollbar["orient"] = "vertical"
        scrollbar["command"] = self.tree.yview
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(fill="both", expand=True)

        # Carrega a lista quando abre a tela
        self.carregarLista()

    def buscarLivro(self):
        token = self.consultarLivro.get()
        # Chama o controller
        livro = livro_controller_pratica.pesquisarLivro(token)

        if livro is None:
            messagebox.showwarning("Atenção", "Livro não encontrado.")
        else:
            # Mostra os dados encontrados
            messagebox.showinfo("Livro Encontrado",
                                f"ID: {livro[0]}\nTítulo: {livro[1]}\nAutor: {livro[2]}\nISBN: {livro[3]}\nDisponível: {livro[4]}")

    def pegarLivro(self):
        leitor = Leitor()
        isbn = self.isbnLivro.get()

        sucesso = leitor.emprestarLivro(isbn)
        if sucesso:
            messagebox.showinfo("Livro eemprestado", "O livro foi pego com sucesso!", )
            self.isbnLivro.delete(0, END)
        else:
            messagebox.showerror("Livro indisponível!", "Este livro não está disponível para empréstimo.")

    def devolverLivro(self):
        leitor = Leitor()
        isbn = self.isbnLivro.get()

        sucesso = leitor.devolverLivro(isbn)
        if sucesso:
            messagebox.showinfo("Livro devolvido", "O livro foi devolvido com sucesso!", )
            self.isbnLivro.delete(0, END)
        else:
            messagebox.showerror("Erro!", "Não foi possível devolver este livro.")

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

    def sair(self):
        from sistema_biblioteca.src.view import login_pratica
        self.borda.destroy()
        login_pratica.Application(self.root)