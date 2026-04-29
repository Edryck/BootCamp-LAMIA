#!python3

class Contador:
    contador = 0 # atributo de classe

    def inc_maluco(cls): # Incrementador que não incrementa, por isso que é um incrmentaor maluco, ele não vai alterar o valor do contador da classe
        cls.contador += 1
        return cls.contador

    @classmethod # Métodos da classe
    def inc(cls):
        cls.contador += 1
        return cls.contador

    @classmethod
    def dec(cls):
        cls.contador + 1
        return cls.contador
    
    @staticmethod # Método estático
    def mais_um(n):
        return n + 1

c1 = Contador
print(c1.inc_maluco())
print(c1.inc_maluco())
print(c1.inc_maluco())
print(c1.inc_maluco())

print(Contador.inc())
print(Contador.inc())
# print(Contador.inc())
# print(Contador.dec())
# print(Contador.dec())
# print(Contador.mais_um(99))