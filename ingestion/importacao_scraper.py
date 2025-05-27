import requests
from bs4 import BeautifulSoup
from utils import parse_quantidade, send_to_api

# Dicionário para mapear os tipos de importação e suas subopções
TIPOS_IMPORTACAO = {
    "Vinhos de mesa": "subopt_01",
    "Espumantes": "subopt_02",
    "Uvas frescas": "subopt_03",
    "Uvas passas": "subopt_04",
    "Suco de uva": "subopt_05",
}


def scrape_importacao(ano):
    """
    Realiza o scraping dos dados de importação de vinhos, espumantes, uvas frescas, uvas passas e suco de uva
    para um determinado ano, extraindo e estruturando as informações em uma lista de dicionários.

    Parâmetros:
    ano (int): O ano para o qual os dados de importação devem ser coletados.

    Retorna:
    list: Uma lista de dicionários contendo informações sobre a categoria do produto,
          país de origem, quantidade importada, valor e o ano de importação. Exemplo:
          [
              {
                  "categoria": "Vinhos de mesa",
                  "pais_origem": "Chile",
                  "quantidade": 2000,
                  "valor": 100000,
                  "ano": 2023
              },
              ...
          ]

    Fluxo:
    - Itera sobre os tipos de importação definidos em `TIPOS_IMPORTACAO`, enviando uma requisição para cada subopção correspondente ao tipo.
    - Verifica se a resposta HTTP foi bem-sucedida. Em caso de erro, imprime uma mensagem de erro e passa para o próximo tipo de importação.
    - Analisa o conteúdo HTML da página e procura pela tabela que contém os dados de importação.
    - Para cada linha da tabela:
        - Extrai o país de origem, quantidade importada e valor.
        - Adiciona as informações estruturadas em um dicionário dentro da lista `data`.

    Dependências:
    - parse_quantidade (function): Função auxiliar para converter textos de quantidade e valor em formato numérico.

    Exceções:
    - Caso ocorra erro de conexão ou o layout da página seja alterado, a função pode retornar dados incompletos ou vazios.
    """

    base_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&subopcao={subopcao}&opcao=opt_05'
    data = []

    # Iterar pelos diferentes tipos de importação
    for tipo_importacao, subopcao in TIPOS_IMPORTACAO.items():
        url = base_url.format(ano=ano, subopcao=subopcao)
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Erro ao acessar a página para o ano {ano}, tipo {tipo_importacao}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='tb_base tb_dados')

        if not table:
            print(f"Nenhuma tabela encontrada para o tipo {tipo_importacao} no ano {ano}")
            continue

        for row in table.find('tbody').find_all('tr'):
            columns = row.find_all('td')
            if len(columns) == 3:
                pais_origem = columns[0].get_text(strip=True)
                quantidade_text = columns[1].get_text(strip=True)
                quantidade = parse_quantidade(quantidade_text)

                valor_text = columns[2].get_text(strip=True)
                valor = parse_quantidade(valor_text)

                data.append({
                    "categoria": tipo_importacao,
                    "pais_origem": pais_origem,
                    "quantidade": quantidade,
                    "valor": valor,
                    "ano": ano
                })
    return data
