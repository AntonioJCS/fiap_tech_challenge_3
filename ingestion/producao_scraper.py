import requests
from bs4 import BeautifulSoup
from utils import parse_quantidade, send_to_api


def scrape_producao(ano):
    """
    Realiza o scraping dos dados de produção de vinhos e derivados para um determinado ano,
    extraindo e estruturando as informações em uma lista de dicionários.

    Parâmetros:
    ano (int): O ano para o qual os dados de produção devem ser coletados.

    Retorna:
    list: Uma lista de dicionários contendo informações sobre a categoria do produto,
          descrição do produto, quantidade produzida e o ano de produção. Exemplo:
          [
              {
                  "categoria_produto": "Vinhos",
                  "descricao_produto": "Vinho Tinto",
                  "quantidade": 15000,
                  "ano": 2023
              },
              ...
          ]

    Fluxo:
    - Envia uma solicitação GET para a URL da Embrapa com o ano especificado.
    - Verifica se a resposta foi bem-sucedida; em caso de erro, imprime uma mensagem e retorna uma lista vazia.
    - Analisa o conteúdo HTML da resposta para localizar a tabela com dados de produção.
    - Itera sobre as linhas da tabela:
        - Se a linha representa uma nova categoria de produto, atualiza a categoria atual.
        - Se a linha representa um subitem, extrai a descrição do produto e a quantidade, e adiciona aos dados.

    Dependências:
    - parse_quantidade (function): Função auxiliar para converter texto de quantidade em formato numérico.

    Exceções:
    - Caso ocorra erro de conexão ou o layout da página seja alterado, a função pode retornar dados incompletos ou vazios.
    """

    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02'
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao acessar a página para o ano {ano}: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='tb_base tb_dados')

    data = []
    current_category = None

    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        if len(columns) == 2:
            categoria = columns[0].get_text(strip=True)
            quantidade_text = columns[1].get_text(strip=True)
            quantidade = parse_quantidade(quantidade_text)

            if "tb_item" in columns[0]['class']:
                current_category = categoria
            elif "tb_subitem" in columns[0]['class']:
                descricao = categoria
                data.append({
                    "categoria_produto": current_category,
                    "descricao_produto": descricao,
                    "quantidade": quantidade,
                    "ano": ano
                })

    return data
