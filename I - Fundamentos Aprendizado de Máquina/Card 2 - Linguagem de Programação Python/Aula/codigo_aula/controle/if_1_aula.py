#!python3

nota = float(input('Informe a nota do aluno: '))
# Operadores de controle - if
if nota >= 9: # Se
    print('Duas palavras: para bens! :P')
    print('Quadro de Honra')
elif nota >= 7: # Equivalente a else if em C
    print('Aprovado')
elif nota >= 5.5:
    print('Recuperação')
elif nota >= 3.5:
    print('Recuperação + Trabalho')
else: # Senão
    print('Reprovado')

print(nota)