import requests
import funcoes
from bs4 import BeautifulSoup

urls_reclamacao = [] # salva 10 a cada pagina
url = "https://www.reclameaqui.com.br/empresa/sao-cristovao-planos-de-saude/lista-reclamacoes/?busca=idoso&pagina=1"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    funcoes.coleta_link(soup, urls_reclamacao)
    funcoes.coleta_reclamacao(urls_reclamacao)
        
else:
    print("A solicitação falhou com o código de status:", response.status_code)


