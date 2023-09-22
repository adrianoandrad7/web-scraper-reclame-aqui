import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import requests
import time
import os
import csv

# Configurando o cabeçalho da requisição
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
}

def coleta_link(url_completa, urls_reclamacao):
    
     # Configuração do driver
    servico = Service(ChromeDriverManager().install())
    time.sleep(4)
    driver = webdriver.Chrome(service=servico)
    time.sleep(4)
    
    try:
       
        # Abre a página
        driver.get(url_completa)
        time.sleep(14)

        # Encontra os elementos de interesse
        div_pai = driver.find_elements(By.CSS_SELECTOR, 'div.sc-1pe7b5t-0.iQGzPh')

        if div_pai:
            for link in div_pai:
                a_element = link.find_element(By.TAG_NAME, 'a')
                if a_element:
                    url_completa = a_element.get_attribute('href')
                    time.sleep(2)
                    if url_completa not in urls_reclamacao:
                        print("Coletando link da reclamação número:", len(urls_reclamacao))
                        print('Url: ' + url_completa)
                        urls_reclamacao.append(url_completa)
                    else:
                        print("Url já se encontra na lista ")
                else:
                    print("Não encontrou elemento a")
        else:
            print('Não encontrou div pai')

    except Exception as e:
        print(f'Erro durante a coleta de links: {e}')

    finally:
        # Encerra o driver
        driver.quit()

    return urls_reclamacao

def coleta_reclamacao(urls_reclamacao, lote_reclamacao, id, num_pag):
    
    last_id = id  # Inicializa o last_id com o valor fornecido

    for i, url in enumerate(urls_reclamacao, start=id + 1):
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            print(f"Coletando reclamação número: {i} da página: {num_pag}")

            soup = BeautifulSoup(response.text, 'html.parser')
            titulo = soup.find('h1', class_='lzlu7c-3 eisBFu').text
            conteudo = soup.find('p', class_='lzlu7c-17 cNqaUv').text
            status = ''

            div_pai_status = soup.find_all('div', class_='lzlu7c-18 cEqucS')

            if div_pai_status:
                for div in div_pai_status:
                    status_span = div.find('span')
                    if status_span:
                        status = status_span.text.strip()
                    else:
                        print("Elemento span não encontrado.")
            else:
                print("Elemento div para o status não encontrado.")

            reclamacao = {'id': i, 'titulo': titulo, 'conteudo': conteudo, 'status': status}
            lote_reclamacao.append(reclamacao)
            last_id = i  # Atualiza o last_id com o último ID

        except requests.exceptions.RequestException as e:
            print(f"Solicitação falhou para a URL: {url} com erro: {e}")
            
    return lote_reclamacao, last_id  # Retorna também o último ID

def coleta_pag_max(url):
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Verifica se a solicitação foi bem-sucedida

        soup = BeautifulSoup(response.text, 'html.parser')

        div_pai = soup.find('div', class_='sc-1sm4sxr-3 fGiCjJ')
        ul = div_pai.find('ul') if div_pai else None
        li_elements = ul.find_all('li') if ul else []

        if not div_pai:
            print('Não encontrou div pai')
            return None

        if not ul:
            print('Não encontrou o elemento ul')
            return None

        if not li_elements or len(li_elements) < 8:
            print('Não encontrou os elementos li ou não há pelo menos 8 elementos')
            return None

        pag_max = int(li_elements[7].text)
        print('-' * 85)
        print(f'Número máximo de páginas encontrado: {pag_max}')
        print('-' * 85)
        return pag_max

    except requests.exceptions.RequestException as e:
        print(f'Erro na solicitação HTTP: {e}')
        return None

def salva_csv(lote_reclamacao):
    
    if not lote_reclamacao:
        print("Nenhuma reclamação para salvar no CSV.")
        return
    
    diretorio_data = "data"
    diretorio_reclame_aqui = "reclame_aqui"
    arquivo_csv = 'dados.csv'
    caminho_arquivo = os.path.join(diretorio_data, diretorio_reclame_aqui, arquivo_csv)

    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    modo_arquivo = 'a'

    with open(caminho_arquivo, mode=modo_arquivo, newline='', encoding='utf-8') as arquivo_csv:
        campos = ["id", "titulo", "conteudo", "status"]
        writer = csv.DictWriter(arquivo_csv, fieldnames=campos)

        if os.path.getsize(caminho_arquivo) == 0:
            writer.writeheader()  # Escreve o cabeçalho se o arquivo estiver vazio

        for reclamacao in lote_reclamacao:
            writer.writerow(reclamacao)

def processar_paginas(pag_max, url_base):

    id_reclamacao = 0
    
    for pagina_atual in range(1 , pag_max + 1):
        
        urls_reclamacao = []
        lote_reclamacao = []

        url_completa = url_base + f'{pagina_atual}'
        
        print('-' * 85)
        print('Página principal:', pagina_atual)
        print('Url processada:', url_completa)
        print('Coletando os links das reclamações...')
        
        urls_reclamacao = coleta_link(url_completa, urls_reclamacao)

        if(len(urls_reclamacao) == 0):
            print("Erro na coleta dos links.")
            break
        else:
            print("Total de links coletados:", len(urls_reclamacao))
        
        print('-' * 85)
        print('Coletando as reclamações...')
        
        lote_reclamacao, last_id = coleta_reclamacao(urls_reclamacao, lote_reclamacao, id_reclamacao, pagina_atual)
        id_reclamacao = last_id
        
        if(len(lote_reclamacao)) == 0:
            print("Erro na coleta das informações")
            break
        
        print('Salvando as reclamações coletadas no CSV...')
        salva_csv(lote_reclamacao)

        pagina_atual += 1

        if pagina_atual > pag_max:
            break