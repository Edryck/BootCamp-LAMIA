# Função de soma
def soma(a, b):
    return a + b
# Função de subtração
def sub(a, b):
    return a - b

somar = soma
print(somar(3, 4))
# Função que chama uma outra função e passa os argumentos op1 e op2 como argumentos para a função chamada no fn
def operacao_aritmetica(fn, op1, op2):
    return fn(op1, op2)

resultado = operacao_aritmetica(soma, 13, 48)
print(resultado)

resultado = operacao_aritmetica(sub, 13, 48)
print(resultado)
# Funções parciais, chama uma função dentro de outra função, se for uma aplicação grande, isso acho diminuir o tempo de processamento
def soma_parcial(a):
    def concluir_soma(b):
        return a + b
    return concluir_soma

resultado_final = soma_parcial(10)(12)
print(resultado_final)