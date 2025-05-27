import requests
from bs4 import BeautifulSoup
from utils import parse_quantidade, send_to_api

# Dicionário para mapear os tipos de processamento e suas subopções
TIPOS_PROCESSAMENTO = {
    "Viníferas": "subopt_01",
    "Americanas e Híbridas": "subopt_02",
    "Uvas de mesa": "subopt_03",
    "Sem classificação": "subopt_04"
}


def scrape_processamento(ano):
    """
    Realiza o scraping dos dados de processamento de uvas para viníferas, americanas e híbridas, uvas de mesa
    e cultivos sem classificação para um determinado ano, extraindo e estruturando as informações em uma lista de dicionários.

    Parâmetros:
    ano (int): O ano para o qual os dados de processamento devem ser coletados.

    Retorna:
    list: Uma lista de dicionários contendo informações sobre a categoria de cultivo, tipo de processamento,
          descrição do cultivo, quantidade e o ano de processamento. Exemplo:
          [
              {
                  "categoria_cultivo": "Uvas Viníferas",
                  "tipo_processamento": "Viníferas",
                  "descricao_cultivo": "Uvas para vinho tinto",
                  "quantidade": 5000,
                  "ano": 2023
              },
              ...
          ]

    Fluxo:
    - Itera sobre os tipos de processamento definidos em `TIPOS_PROCESSAMENTO`, enviando uma requisição para cada subopção correspondente ao tipo.
    - Verifica se a resposta HTTP foi bem-sucedida. Em caso de erro, imprime uma mensagem de erro e passa para o próximo tipo de processamento.
    - Analisa o conteúdo HTML da página e procura pela tabela que contém os dados de processamento.
    - Para cada linha da tabela:
        - Define a categoria de cultivo principal, caso a linha represente uma categoria.
        - Extrai a descrição do cultivo e a quantidade se a linha representa um subitem.
        - Adiciona as informações estruturadas em um dicionário dentro da lista `data`.

    Dependências:
    - parse_quantidade (function): Função auxiliar para converter textos de quantidade em formato numérico.

    Exceções:
    - Caso ocorra erro de conexão ou o layout da página seja alterado, a função pode retornar dados incompletos ou vazios.
    """

    base_url = 'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&subopcao={subopcao}&opcao=opt_03'
    data = []

    # Iterar pelos diferentes tipos de processamento
    for tipo_processamento, subopcao in TIPOS_PROCESSAMENTO.items():
        url = base_url.format(ano=ano, subopcao=subopcao)
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Erro ao acessar a página para o ano {ano}, tipo {tipo_processamento}: {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', class_='tb_base tb_dados')

        if not table:
            print(f"Nenhuma tabela encontrada para o tipo {tipo_processamento} no ano {ano}")
            continue

        current_category = None

        # Iterar pelas linhas da tabela
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
                        "categoria_cultivo": current_category,
                        "tipo_processamento": tipo_processamento,
                        "descricao_cultivo": descricao,
                        "quantidade": quantidade,
                        "ano": ano
                    })
    return data
