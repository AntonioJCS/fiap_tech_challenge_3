import requests
from bs4 import BeautifulSoup
from utils import parse_quantidade, send_to_api

# Dicionário para mapear os tipos de processamento e suas subopções
TIPOS_EXPORTACAO = {
    "Vinhos de mesa": "subopt_01",
    "Espumantes": "subopt_02",
    "Uvas frescas": "subopt_03",
    "Suco de uva": "subopt_04"
}


def scrape_exportacao(ano):
    """
    Realiza o scraping dos dados de exportação de vinhos, espumantes, uvas frescas e suco de uva
    para um determinado ano, extraindo e estruturando as informações em uma lista de dicionários.

    Parâmetros:
    ano (int): O ano para o qual os dados de exportação devem ser coletados.

    Retorna:
    list: Uma lista de dicionários contendo informações sobre a categoria do produto,
          país de destino, quantidade exportada, valor e o ano de exportação. Exemplo:
          [
              {
                  "categoria": "Vinhos de mesa",
                  "pais_destino": "Argentina",
                  "quantidade": 1000,
                  "valor": 50000,
                  "ano": 2023
              },
              ...
          ]

    Fluxo:
    - Itera sobre os tipos de exportação definidos em `TIPOS_EXPORTACAO`, enviando uma requisição para cada subopção correspondente ao tipo.
    - Verifica se a resposta HTTP foi bem-sucedida. Em caso de erro, imprime uma mensagem de erro e passa para o próximo tipo.
    - Analisa o conteúdo HTML da página e procura pela tabela que contém os dados de exportação.
    - Para cada linha da tabela:
        - Extrai o país de destino, quantidade exportada e valor.
        - Adiciona as informações estruturadas em um dicionário dentro da lista `data`.

    Dependências:
    - parse_quantidade (function): Função auxiliar para converter textos de quantidade e valor em formato numérico.

    Exceções:
    - Caso ocorra erro de conexão ou o layout da página seja alterado, a função pode retornar dados incompletos ou vazios.
    """

    base_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&subopcao={subopcao}&opcao=opt_06'
    data = []

    # Iterar pelos diferentes tipos de processamento
    for tipo_exportacao, subopcao in TIPOS_EXPORTACAO.items():
        url = base_url.format(ano=ano, subopcao=subopcao)
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Erro ao acessar a página para o ano {ano}, tipo {tipo_exportacao}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='tb_base tb_dados')

        if not table:
            print(f"Nenhuma tabela encontrada para o tipo {tipo_exportacao} no ano {ano}")
            continue

        for row in table.find('tbody').find_all('tr'):
            columns = row.find_all('td')
            if len(columns) == 3:
                pais_origem = columns[0].get_text(strip=True)
                quantidade_text = columns[1].get_text(strip=True)
                quantidade = parse_quantidade(quantidade_text)

                valor_text = columns[1].get_text(strip=True)
                valor = parse_quantidade(valor_text)

                data.append({
                    "categoria": tipo_exportacao,
                    "pais_destino": pais_origem,
                    "quantidade": quantidade,
                    "valor": valor,
                    "ano": ano
                })
    return data
