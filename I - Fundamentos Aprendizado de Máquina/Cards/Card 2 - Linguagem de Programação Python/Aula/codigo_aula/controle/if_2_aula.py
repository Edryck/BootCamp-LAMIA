#!python3

a = 'valor' # True
a = 0 # False
a = -0.00001 # True
a = '' # False
a = ' ' # True
a = [] # False
a = {} # False
# Operador If com operadors unários
if a:
    print('Existe!!!')
else:
    print('não existe ou zero ou vazio...')