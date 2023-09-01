import csv
import os

# Suponha que 'dados' seja uma lista de dicionários, onde cada dicionário contém as informações.
# Por exemplo:
dados = [
    {"indice": 1, "titulo": "Título 1", "conteudo": "Conteúdo 1", "status": "Não respondida"},
    {"indice": 2, "titulo": "Título 2", "conteudo": "Conteúdo 2", "status": "Respondida"},
    # Adicione mais itens conforme necessário
]

# Diretório onde você deseja criar o arquivo CSV
diretorio_data = "data"
diretorio_coletadados = "coletadados"

# Nome do arquivo CSV
nome_arquivo = 'dados.csv'

# Construa o caminho completo para o arquivo CSV
caminho_arquivo = os.path.join(diretorio_data, diretorio_coletadados, nome_arquivo)

# Certifique-se de que o diretório de destino existe
os.makedirs(os.path.dirname(caminho_arquivo), exist_ok=True)

# Abra o arquivo CSV em modo de escrita com delimitador de vírgula
with open(caminho_arquivo, mode='w', newline='', encoding='utf-8') as arquivo_csv:
    # Defina a ordem das colunas
    campos = ["indice", "titulo", "conteudo", "status"]
    
    # Crie um objeto DictWriter usando a ordem das colunas e delimite por vírgula
    escritor_csv = csv.DictWriter(arquivo_csv, fieldnames=campos, delimiter=',')
    
    # Escreva os cabeçalhos
    escritor_csv.writeheader()

    # Escreva os dados
    for dado in dados:
        escritor_csv.writerow(dado)

print(f'Dados salvos com sucesso em {caminho_arquivo}')
