#!python3
# Passa argumentos padrões
def saudacao (nome = 'Pessoa', idade = 20):
    print(f'Bom dia {nome}!\nVc nem parece ter {idade} anos!')
#  Função sem argumentos
# def saudação():
#   print('Boa tarde!')

def soma_e_multi(a, b, x):
    return a + b * x
# Executa a função só quando esse arquivo for o principal
if __name__ == '__main__':
    saudacao('Ana', idade =  30)