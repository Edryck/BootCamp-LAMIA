# Define dois tipos de variaveis com valores atribuídos
a = 3
b = 4.4
# Imprime a soma de a + b
print(a + b)
# Define dois tipos de variáveis
texto = 'Sua idade é... '
idade = 23
# Imprime o texto e a idade formatado
#print(texto + str(idade))
print(f'{texto} {idade}')
# Imprime 3 vezes o variável saudação
saudacao = 'bom dia '
print(3 * saudacao)
# Valores constantes
PI = 3.14
PI = 3.1415
# Pede ao usuário o raio
raio = float(input('Informe o raio da circ? '))
area = PI * pow(raio, 2) # Calcula a área
print(f'A área da circ é {area} m2.') # Imprime formado a área da circunferencia