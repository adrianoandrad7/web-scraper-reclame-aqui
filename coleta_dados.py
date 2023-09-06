import requests
from bs4 import BeautifulSoup
import time
import funcoes

base_url = "https://www.reclameaqui.com.br/empresa/sulamerica-saude/lista-reclamacoes/?busca=idoso&pagina={}"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

inicio = time.time()

lote_reclamacao = []

try:
    id_reclamacao = 0
    num_pag = 1

    while True:
        
        urls_reclamacao = [] 
        url_completa = base_url.format(num_pag)
        print(f"Processando página {num_pag}: {url_completa}")

        response = requests.get(url_completa, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        if num_pag == 1:
            pag_max = funcoes.coleta_pag_max(soup)

        print('Salvando os links de cada reclamação em uma lista...')
        funcoes.coleta_link(soup, urls_reclamacao)
        
        for url in urls_reclamacao:
            print(url)

        print('Salvando as reclamações de cada link em uma lista...')
        funcoes.coleta_reclamacao(urls_reclamacao, lote_reclamacao, id_reclamacao, num_pag)

        print('Salvando as reclamações coletadas no CSV...')
        funcoes.salva_csv(lote_reclamacao)

        id_reclamacao += len(lote_reclamacao)

        num_pag += 1
        print(num_pag)

        if num_pag > pag_max:
            break

except requests.exceptions.RequestException as e:
    print("Erro na solicitação HTTP:", e)

fim = time.time()
tempo_execucao = fim - inicio
horas, restante = divmod(tempo_execucao, 3600)
minutos, segundos = divmod(restante, 60)
print(f"Tempo de execução do programa: {int(horas)} horas, {int(minutos)} minutos, {int(segundos)} segundos")
print('Fim de processamento - todas as reclamações foram salvas no CSV')
 



