from bs4 import BeautifulSoup
import requests

url_base = "https://www.reclameaqui.com.br"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

def coleta_link(soup, urls_reclamacao):
    
    for link in soup.find_all('div', class_='sc-1pe7b5t-0 iQGzPh'):
        url_completa = url_base + link.find('a')['href']
        urls_reclamacao.append(url_completa)
    
    return urls_reclamacao 

def coleta_reclamacao(urls_reclamacao):
    
    cont = 0
    for url in urls_reclamacao:
        
        response = requests.get(url, headers=headers)
        print(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        cont += 1
        
        titulo = soup.find('h1', class_='lzlu7c-3 eisBFu').text
        conteudo = soup.find('p', class_='lzlu7c-17 cNqaUv').text
        ##status = soup.find('span', class_='sc-1a60wwz-1 kwzooO').text
        
        print("Processamento da mensagem", cont)
        print("Título:", titulo)
        print("Conteúdo:", conteudo)
        ##print("Status:", status)
        print("-" * 90)    
    
    