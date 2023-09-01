import requests

from bs4 import BeautifulSoup

# url = "https://www.reclameaqui.com.br/empresa/amil/lista-reclamacoes/?busca=idoso&pagina=1"
url = "https://www.reclameaqui.com.br/empresa/sao-cristovao-planos-de-saude/lista-reclamacoes/?busca=idoso&pagina=1"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    
    # Criar um objeto BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontre todos os elementos com a classe 'sc-1pe7b5t-0'
    elementos = soup.find_all('div', class_='sc-1pe7b5t-0')

    for elemento in elementos:
        
        # Extrair o título (h4) dentro do elemento
        titulo = elemento.find('h4', class_='sc-1pe7b5t-1 jAlTVn').text

        # Extrair o texto do parágrafo (p) dentro do elemento
        conteudo = elemento.find('p', class_='sc-1pe7b5t-2 jmCUqY').text
        
        #Extrair status
        status_element = soup.find('span', class_='sc-1pe7b5t-4 bfzjDQ')
        status_text = status_element.find(text=True, recursive=False)

        # Imprimir os resultados
        print("Título:", titulo)
        print("Conteúdo:", conteudo)
        print("Status:", status_text)
        print("-" * 90)     
else:
    print("A solicitação falhou com o código de status:", response.status_code)


