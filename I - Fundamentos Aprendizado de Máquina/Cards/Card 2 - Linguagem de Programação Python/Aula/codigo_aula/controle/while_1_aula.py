#!python3
# Estrutura de repetição While (enquanto)
total = 0
qtde = 0
nota = 0
# Enquanto nota diferente de -1 continua repetindo, -1 é para sair da repetição
while nota != -1:
    # Recebe as notas
    nota = float(input('Informe a nota ou para sair: '))
    if nota != -1:
        qtde += 1 # Quantidade de notas
        total += nota # Soma de todas as notas

print(f'A média da truma é {total / qtde}')