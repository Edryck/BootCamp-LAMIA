# Cria uma variável do tipo list
nums = [1, 2, 3]
print(type(nums))
# Adiciona valores na lista
nums.append(3)
nums.append(3)
nums.append(3)
print(len(nums)) # Imprime o tamanho da lista
# Imprime true se esse elemento está dentro da lista
print(2 in nums)
# Adiciona o 100 no indice 3
nums[3] = 100
nums.insert(0, -200) # Insere o -200 no indice 0

print(nums[6]) # Imprime o elemento do indice 6
print(nums[-1]) # Imprime o último elemento
print(nums[-2]) # Imprime o penúltimo elemento
print(nums) # Imprime a lista