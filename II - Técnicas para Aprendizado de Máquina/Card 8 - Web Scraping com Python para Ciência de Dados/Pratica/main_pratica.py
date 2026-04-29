from bs4 import BeautifulSoup
import requests
import time
import csv

# URL do site e o nome que defini para o arquivo
site_url='https://animesonlinecc.to/episodio/'
csv_file = 'animes_pratica.csv'

# Carrega os dados do arquivo csv
def load_data(file_path):
    data={}
    # Abre o arquivo para leitura, o encoding é para a leitura correta de caractere com acentuação
    with open(file_path, 'r', encoding='utf-8') as f:
        r = csv.DictReader(f)
        for line in r:
            # Para cada linha, ele vai ler o nome que está em data e atribuir o ultimo episodio salvo e o link dele
            data[line['Nome']] = [line['Ultimo_Episodio'], line['Link']]
    return data

# Salvar os dados do arquivo csv
def save_data(file_path, data):
    # Vai abrir para escrita
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        # Escreve a o cabeçalho para o DictReader funcionar
        w.writerow(['Nome', 'Ultimo_Episodio', 'Link'])
        for name, info in data.items():
            # Escreve a linha, info[0] é o último episódio e o info[1] é  o link
            w.writerow([name, info[0], info[1]])

def find_new_episodes(site_url):
    # Tempo de espera para atualizar e ver se tem novos episodios
    wait_time = 60 * 60 # 1 hora

    while True:
        # Carrega os dados do arquivo
        my_animes = load_data(csv_file)
        # Para ver se houve alguma mudança, nesse caso seria se teve novos episodios lançados
        change = False
        print('\tÚltimos episódios lançados\n\n')

        # Pega o HTML do site como texto
        html = requests.get(site_url).text
        # Cria instância do BS4
        soup = BeautifulSoup(html, 'lxml')
        # No site a tag onde está os dados nome, episodio e link é do tipo article
        # Ele vai procura todos com essa tag
        animes = soup.find_all('article', class_='item se episodes')
        
        for anime in animes:
            # Aqui ele vai pegar os dados brutos (brutos por que vem assim: "<nome-do-anime> <episodio>")
            raw_data = anime.find('div', class_='eptitle').text
            # Agora vem a separação do nome com o episodio
            # Basicamente "Episodio 0" são 10 caracteres, contando com o espaço, porém, eventualmente pode haver 
            # "Episodio 10" que são 11 caracteres, os dados completo da primeira versão ficaria assim: "<nome> "
            # e a segunda versão assim: "<nome>"... Sim, eu adicionei o espaço para episodios de 0 a 9 e o resto sem espaço
            # ai entra o strip() para remover os espaços em branco. É bem provavel que isso não funcione para algo como
            # One Piece Episodio 100.
            anime_name = raw_data[1:-11].strip()
            # ... O do episodio seria o que sobra, e teria esses dois " Episodio 0" e "Episodio 10", se for maior que
            # 99 ele vai quebra o episodio e provavelmente tiraria o a letra 'E'
            anime_episodio = raw_data[-11:].strip()
            # Pega o link para o episódio
            anime_link = anime.find('a')['href']
            
            # Para verificar se o anime já está na lista
            if anime_name in my_animes:
                # Se estiver na lista, ele vai pegar o episodio e atualizar ele
                if my_animes[anime_name][0] != anime_episodio:
                    print(f"Atualizando: {anime_name} ({my_animes[anime_name][0]} -> {anime_episodio})")
                    my_animes[anime_name] = [anime_episodio, anime_link]
                    # Se atualizou o episodio... Então houve mudança
                    change = True
            # Se não está na lista, acredito que seja um anime novo, como pega só da primeira página
            # então pode ocorrer de pegar algo como: "<nome> Episodio 8"
            else:
                print(f"Novo anime encontrado: {anime_name}")
                my_animes[anime_name] = [anime_episodio, anime_link]
                # Novo na lista, então houve mudança
                change = True

        # Se houve mudança no arquivo, ele salva
        if change:
            save_data(csv_file, my_animes)
            print('\nArquivo atualizado')
        # Se não houve mudanças, não precisa salvar
        else:
            print('\nNada de novo')

        # Ele atualiza a cada uma hora
        print(f"Atualizando em {wait_time/60} minutos...\n")
        time.sleep(wait_time)


if __name__ == '__main__':
    find_new_episodes(site_url)