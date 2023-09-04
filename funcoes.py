from bs4 import BeautifulSoup
import requests
import os
import csv

url_base = "https://www.reclameaqui.com.br"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

def coleta_link(soup, urls_reclamacao):
    
    for link in soup.find_all('div', class_='sc-1pe7b5t-0 iQGzPh'):
        url_completa = url_base + link.find('a')['href']
        urls_reclamacao.append(url_completa)
        print(url_completa)
    
    return urls_reclamacao 

def coleta_reclamacao(urls_reclamacao, lote_reclamacao):

    cont = 0
    for url in urls_reclamacao:
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            
            soup = BeautifulSoup(response.text, 'html.parser')
            titulo = soup.find('h1', class_='lzlu7c-3 eisBFu').text
            conteudo = soup.find('p', class_='lzlu7c-17 cNqaUv').text
            status = ''
            div_pai_status = soup.findAll('div', class_='lzlu7c-18 cEqucS')
        
            if div_pai_status:
                for div in div_pai_status:
                    status_span = div.find('span')
                    if status_span:
                        status = status_span.text.strip()
                    else:
                        print("Elemento span não encontrado.")
            else:
                print("Elemento div para o status não encontrado.")

            cont += 1
            reclamacao = {'id': cont, 'titulo': titulo, 'conteudo' : conteudo, 'status' : status}
            lote_reclamacao.append(reclamacao)
            
        else:
            print("A solicitação falhou com o código de status:", response.status_code)
       
    return lote_reclamacao

def salva_csv(lote_reclamacao):
     
    diretorio_data = "data"
    diretorio_reclame_aqui = "reclame_aqui"
    arquivo_csv = 'dados.csv'
    caminho_arquivo = os.path.join(diretorio_data, diretorio_reclame_aqui, arquivo_csv)
    os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

    with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:    
        campos = ["id", "titulo", "conteudo", "status"]
        writer = csv.DictWriter(arquivo_csv, fieldnames=campos)
        writer.writeheader()

        for reclamacao in lote_reclamacao:
            writer.writerow(reclamacao)
        
       
