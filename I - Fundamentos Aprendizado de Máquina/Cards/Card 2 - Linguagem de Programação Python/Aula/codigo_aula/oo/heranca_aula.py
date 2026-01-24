#!python3
# Heranças
class Carro: # Cria uma classe carro
    def _init__(self):
        self.__velocidade = 0 # Atributos da classe

    @property
    def velocidade(self):
        return self.__velocidade

    def acelerar(self): # Acelera
        self._velocidade += 5
        return self.__velocidade

    def frear(self): # Desacelera
        self._velocidade -= 5
        return self.__velocidade
    
class Uno (Carro): # Uma classe filha que herda o classe carro
    pass

class Ferrari(Carro): # Também é uma classe filha do carro
    def acelerar(self): # Mas sobrescreve uma das funções, usado como exemplo da aula, mas nçao faz sentido uma ferrari ser mais rápido que o Uno, imagina ainda se tiver com escada em cima
        super().acelerar()
        return super().acelerar()
    
c1 = Ferrari()
print(c1.acelerar())
print(c1.acelerar())
print(c1.acelerar())
print(c1.frear())
print(c1.frear())
print(c1.frear())