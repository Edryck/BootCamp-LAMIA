#!python3
# Estrutura de repetição For
# Imprime números de 0 a 10
for i in range(10):
   print(i, end=' ') # O end='' é para colocar tudo mesma linha

print('')
# Imprime números de 1 a 10
for i in range(1, 11):
   print(i, end=' ')

print('')
# Imprime números de 1 a 100 com intervalos de 7
for i in range(1, 100, 7):
    print(i, end=' ')

print('')
# Imprime números de 20 a 0 com intervalos de 3
for i in range(20, 0, -3):
    print(i, end=' ')

print('')

nums = [2, 4, 6, 8]
# Imprime uma lista
for n in nums:
    print(n, end=' ')

print('')

texto = 'Python é muito massa!'
# Imprime uma string com espaços entre as letras
for letra in texto:
    print(letra, end= ' ')

print('')
# Imprime uma tupla
for n in {1, 2, 3, 4, 4, 4}:
    print(n, end=' ')

produto = {
    'nome': 'Caneta', 
    'preco': 8.80,
    'desc': 0.5
}
# Imprime um dictionary formatado
for atrib in produto:
    print(atrib, '==>',produto[atrib], end=' ')

print('')
# Imprime os items do dictionary
for atrib, valor in produto.items():
    print(atrib, '=>', valor, end=' ')

print('')
# Imprime os valores do dictionary
for valor in produto.values():
    print(valor, end=' ')

print('')
# Imprime as chaves do dictionary
for atrib in produto.keys():
    print(atrib, end=' ')