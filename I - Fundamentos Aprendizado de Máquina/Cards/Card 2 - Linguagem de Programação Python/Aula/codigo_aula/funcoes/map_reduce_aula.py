from functools import reduce
# Função que cria outra função dentro dela, ela vai configurar quanto que vai ser somado, seria o delta
def somar_nota(delta):
    def calc(nota):
        return nota + delta
    return calc

notas = [6.4, 7.2, 5.4, 8.4]
# O map prepara a aplicação da função para cada nota, ele vai soma 1.5 ou 1.6 nas notas para cada nota da lista
notas_finais_1 = map(somar_nota(1.5), notas)
notas_finais_2 = map(somar_nota(1.6), notas)

print(notas_finais_1)
print(notas_finais_2)

def somar(a, b):
    return a + b

total = reduce(somar, notas, 0) # Acumula os valores, algo como a função de calcular média, soma inicia com 0 e para cada repetição ele vai adicionando as notas em soma, com o reduce isso economiza mais código
print(total)

# for i, nota in enumerate(notas):
#     notas[i] = nota + 1.5

# for i in range(len(notas)):
#     notas[i] = nota[i] + 1.5