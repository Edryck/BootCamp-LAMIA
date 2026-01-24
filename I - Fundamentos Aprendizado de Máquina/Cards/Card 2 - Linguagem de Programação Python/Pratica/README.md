# Sistema de Biblioteca

---

Um sistema de biblioteca simples desenvolvido em Python. O sistema permite o login de usuário, reconhecendo se é um usuário normal ou o bibliotecário, conta com funcionalidades de adição, edição e exclusão de livros. Este projeto foi feito como um exemplo prático do básico da linguagem Python e aplicando o os pilares da Programação Orientada a Objetos.

---

### Funcionalidades

O sistema inclui as seguintes funcionalidades:
+ **Controle de Usuário:** Um sistema de login simples diferenciando o usuário comum (leitor) do administrador (bibliotecário).
+ **Cadastro de Livros:** Cadastro simples de livros na qual pede o as informações como título, autor, ISBN, ano de publicação e editora.
+ **Consulta de Livros:** Busca por livros através do título ou autor.
+ **Sistema de Empréstimos:** O usuário poder realizar um empréstimo e também a devolução do livro.
+ **Controle de Empréstimo:** Verificação básica para reconhecer quando o livro está livre ou se foi emprestado para alguém.
+ **Edição:** Atualiza os dados de um livro, caso seja necessário.
+ **Exclusão:** Remove um livro do acervo da biblioteca.

---

### Tecnologias Usadas

**Linguagem:** Python 3.13.0.  
**Arquitetura:** MVC (Model-View-Controller)  
**Interface:** Tkinter.  
**Banco de Dados:** SQLite.  
**Estrutura de Pastas:** 

````
sistema_biblioteca/
├─ main.py
├─ README.md
├─ requirements.txt
├─ dados/
│   └─ biblioteca.db 
└─ src/
    ├─ controller/
    ├─ dao/
    ├─ model/
    └─ view/ 
````  

**Pastas:**
+ **dados:** Onde ficará os arquivos salvos.
+ **src:** Onde vai ficar todo o código fonte.
+ **controller:** Aqui fica os controladores do sistema.
+ **dao:** Conexão com o banco de dados e o DAO.
+ **model:** Aqui fica os objetos/classes.
+ **view:** Aqui fica as interfaces.

**Arquivos:**
+ **main.py:** Ponto de partida.
+ **README.md:** Explicação do projeto.
+ **requirements.txt:** Lista de bibliotecas que serão utilizadas. (Não foi utilizada nenhuma biblioteca externa, foi utilizado as que são nativas do Python tanto para a interface gráfica quanto para o banco de dados)
+ **biblioteca.db:** O banco de dados do sistema.

---

### Como executar o projeto

**Pré-Requisitos:** Certifique de ter o Python 3.13 instalado no seu computador.  
**Clone o repositório:**  

````
git clone https://github.com/Edryck/Sistema-de-Biblioteca.git
````

**Execute o projeto:**  

Abra o terminal na pasta em que você clonou o repositório e digite o seguinte comando:
````
python main.py
````

**Acesso Inicial:** Quando rodar o sistema pela primeira vez, usa as credenciais do administrador padrão.
+ **Usuário:** *admin*.
+ **Senha:** *admin123*.
