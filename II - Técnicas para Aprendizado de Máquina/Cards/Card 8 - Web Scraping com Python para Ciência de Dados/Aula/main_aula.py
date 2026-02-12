from bs4 import BeautifulSoup
import requests
import time

print('Put some skill that you are not familiar with')
# Variável para  o input usada no filtro
unfamiliar_skill = input('>')
print(f'Filtering out {unfamiliar_skill}')

# Faz mais sentido criar uma função, assim ela será chamada em periodicamente
def find_jobs():
    # Para usar o get, iremos passar a URL do site que vamos realizar a extração
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=e').text
    # Criando uma instância do BS
    soup = BeautifulSoup(html_text, 'lxml')
    # Se utilizar o Inspencionar na página para localizar a parte que contém o conteúdo que queremos
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')
    for index, job in enumerate(jobs):
        # Agora selecionando as vagas com a data de publicação especifica
        # O texto dela vai estar dentro de um outro span
        published_date = job.find('span', class_='sim-posted').span.text 
        if 'few' in published_date:
            # Pegando agora o nome da empresa, na aula, a saída imprimindo apenas o texto, ele vem com alguns espaços
            # Então será utilizado o replace() para substituir os espaços por nada
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')
            # Pegando as skills que a vaga pede
            skills = job.find('span', class_='srp_skills').text.replace(' ', '')
            # O conteúdo onde está o link para mais informações da vaga
            more_info = job.header.h2.a['href']
            # Filtro
            if unfamiliar_skill not in skills:
                with open('posts/{index}_aula.txt', 'w') as f:
                    # Retirando o print com aspas triplas e substituindo pelas aspas duplas
                    # Vamos remover também os espaços em branco usando strip()
                    f.write(f"Company Name: {company_name.strip()} \n")
                    f.write(f"Required Skills: {skills.strip()} \n")
                    f.write(f"More Info: {more_info}")
                print(f'File saved: {index}.txt')

if __name__ == '__main__':
    while True:
        # Chama a função
        find_jobs()
        # Agora vem a parte de chamada periodica, vamos utilizar o sleep
        # Ele vai permitir que o programa espere por um determinado periodo de tempo
        # time.sleep(600)
        # ou
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)