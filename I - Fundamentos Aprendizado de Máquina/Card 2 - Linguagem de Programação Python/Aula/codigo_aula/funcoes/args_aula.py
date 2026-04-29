# Passa varios argumentos dentro dessa função
def soma(*nums):
    total = 0
    for n in nums:
        total += n
    return total
# Para argumentos nomeados, normalmente para dicionários
def resultado_final(**kwargs):
    status = 'aprovado (a)' if kwargs['nota'] >= 7 else 'reprovado(a)'
    return f'{kwargs["nome"]} foi {status}'