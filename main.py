from bs4 import BeautifulSoup
import funcoes

# Configurando o cabeçalho da requisição
url_base = f'https://www.reclameaqui.com.br/empresa/unimed-bh/lista-reclamacoes/?busca=velhice&pagina='

#Buscando o número de páginas
#pag_max = funcoes.coleta_pag_max(url_base + f'{1}')

pag_max = 1; 

# Processando as páginas
funcoes.processar_paginas(pag_max,url_base)

print("Fim de processamento - todas as reclamações foram salvas no CSV")
    

