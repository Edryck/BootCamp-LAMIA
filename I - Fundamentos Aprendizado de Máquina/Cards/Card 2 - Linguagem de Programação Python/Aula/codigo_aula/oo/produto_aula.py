#!python3
# Classes
class Produto:
    # pass para criar uma classe vazia, o self seria o separa o queria da classe
    def _init__(self, nome, preco=1.99, desc=0):
        self.nome = nome # O self falar sobre o nome do obj da classe, e o outro nome é do construtor
        self.__preco = preco # para privar a o atributo
        self.desc = desc

    @property
    def preco(self): # Meio que um getter para pegar variaveis privadas
        return self.__preco
    
    @property.setter # Um setter para mudar o valor de uma variavel privada
    def preco(self, novo_preco):
        if novo_preco > 0:
            self.__preco = novo_preco

    @property 
    def preco_final(self):
        return (1 - self.desc) * self.__preco

p1 = Produto('Caneta', 10, 0.1)
p2 = Produto('Caderno', 14, 0.5)

p1.preco = 70.99
p2.preco = 17.99

print(p1.nome, p1.preco, p1.desc, p1.preco_final)
print(p2.nome, p2.preco, p2.desc, p2.preco_final)