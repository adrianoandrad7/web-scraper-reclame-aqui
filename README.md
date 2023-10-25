# Web Scraper para Coleta de Reclamações no Site Reclame Aqui

Este é um projeto Python que realiza a raspagem de reclamações no site do Reclame Aqui. Ele coleta informações sobre reclamações, no nosso contexto reclmações sobre idosos nos em planos de súde.

## Pré-requisitos

Antes de usar este projeto, certifique-se de ter o Python instalado no seu sistema. Você pode instalar as bibliotecas necessárias usando o `pip`:

## Instalação de Dependências

Você pode instalar as bibliotecas necessárias usando o `pip` e o arquivo `requirements.txt` onde contém todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

| Biblioteca        | Versão   | Documentação                                  |
|-------------------|----------|-----------------------------------------------|
| beautifulsoup4    | 4.12.2   | [Documentação do BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) |
| requests          | 2.31.0   | [Documentação do requests](https://docs.python-requests.org/en/latest/)          |
selenium | 4.1.0 | [Documentação do Selenium](https://www.selenium.dev/documentation/) |

## Como usar

Antes de executar o projeto, siga as etapas abaixo para configurar a URL de pesquisa específica da empresa cujas reclamações deseja obter:

1. Vá para o site Reclame Aqui (https://www.reclameaqui.com.br).

2. Pesquise a empresa da qual deseja coletar reclamações utilizando a barra de pesquisa do site.

3. Na página da empresa, vá para a aba "Reclamações".

4. Se desejar, adicione tags específicas para a pesquisa de reclamações na empresa.

5. Após realizar a pesquisa, copie a URL do navegador.

## Configurando a URL de Pesquisa

Agora, substitua a URL na variável `base_url` no arquivo `main.py` pela URL que você copiou após a pesquisa. Lembre-se de remover o número da página. Isso permitirá que o web scraper colete todas as reclamações da sua pesquisa, incluindo todas as páginas.

Exemplo:
```python
base_url = "https://www.reclameaqui.com.br/empresa/sulamerica-saude/lista-reclamacoes/?busca=idoso&pagina="
```

## Execute o cod

Clone o repositório:

```bash
 git clone https://github.com/adrianoandrad7/Raspagem-ReclameAqui.git
```

Execute o código Python:

```bash
python main.py
```

## Personalização

Você pode personalizar este projeto ajustando as configurações no arquivo main.py:

* `base_url`: URL base para a pesquisa de reclamações.
* `headers`: Cabeçalhos HTTP para a solicitação.
* `coleta_link`: Função para coletar links de reclamações.
* `coleta_reclamacao`: Função para coletar informações detalhadas de reclamações.
* `salva_csv`: Função para salvar os dados coletados em um arquivo CSV.
* `coleta_pag_max`: Função para coletar o número máximo de páginas.
* `processar_paginas`: Principal função reponsável por processar as páginas, coletar e salvar as reclamações em um arquivo csv.
