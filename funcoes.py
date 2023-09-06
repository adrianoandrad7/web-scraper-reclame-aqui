from bs4 import BeautifulSoup
import requests
import os
import csv

url_base = "https://www.reclameaqui.com.br"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}

def coleta_link(soup, urls_reclamacao):
    
    div_pai = soup.find_all('div', class_='sc-1pe7b5t-0 iQGzPh')
    
    if div_pai:
        for link in div_pai:
            a_element = link.find('a', href=True)
            if a_element:
                url_completa = url_base + a_element['href']
                if url_completa not in urls_reclamacao:
                    urls_reclamacao.append(url_completa)
                    print("Coletando link da reclamação número:", len(urls_reclamacao))
                else:
                    print("Url ja se encontra na lista ")
            else:
                print("Não encontrou elemento a")
    else:
        print('Não encontrou div pai')
        
    return urls_reclamacao 

def coleta_reclamacao(urls_reclamacao, lote_reclamacao, id, num_pag):
    cont = id
    for url in urls_reclamacao:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            print("Coletando reclamação número:", cont, "da página:", num_pag)
            
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

            cont += 1
            reclamacao = {'id': cont, 'titulo': titulo, 'conteudo': conteudo, 'status': status}
            lote_reclamacao.append(reclamacao)
            
        except requests.exceptions.RequestException as e:
            print("Solicitação falhou para a URL:", url, "com erro:", e)
       
    return lote_reclamacao

def salva_csv(lote_reclamacao):
    
    if not lote_reclamacao:
        print("Nenhuma reclamação para salvar no CSV.")
        return
     
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
    

def coleta_pag_max(soup):
    div_pai = soup.find('div', class_='sc-1sm4sxr-3 fGiCjJ')
    
    if not div_pai:
        print('Não encontrou div pai')
        return None

    ul = div_pai.find('ul')
    if not ul:
        print('Não encontrou o elemento ul')
        return None

    li_elements = ul.find_all('li')
    if not li_elements:
        print('Não encontrou os elementos li')
        return None

    oitavo_item = li_elements[7].text
    pag_max = int(oitavo_item)
    print(f'Número máximo de páginas encontrado: {pag_max}')
    return pag_max
