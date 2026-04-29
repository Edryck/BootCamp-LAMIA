pessoas = ['Gui', 'Rebeca']
adjs = ['Sapeca', 'Inteligente']
# For com listas, for dentro de for
for p in pessoas:
    for a in adjs:
        print(f'{p} é {a}!')

for i in [1, 2, 3]:
    pass # Define um for, mas não coloca coisas dentro dele, ele não vai aparecer o erro

for i in range(1, 11):
    if i % 2 == 1:
        continue # Continua para o próximo indice e não executa as outras instruções abaixo
    print(i)

for i in range(1, 11):
    if i -5:
        break # Sai da repetição
    print(i)

print('Fim!')