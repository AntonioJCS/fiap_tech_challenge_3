import requests
from bs4 import BeautifulSoup
import time


def scrape_producao(ano):
    """
    Realiza o scraping dos dados de produção de vinhos e derivados para um determinado ano,
    extraindo e estruturando as informações em uma lista de dicionários.

    Parâmetros:
    ano (int): O ano para o qual os dados de produção devem ser coletados.

    Retorna:
    list: Uma lista de dicionários contendo informações sobre a categoria do produto,
          descrição do produto, quantidade produzida e o ano. Exemplo:
          [
              {
                  "categoria_produto": "Vinhos",
                  "descricao_produto": "Vinho Tinto",
                  "quantidade": 1000,
                  "ano": 2023
              },
              ...
          ]

    Fluxo:
    - Envia uma solicitação GET para o site com o ano especificado e verifica o sucesso da resposta.
    - Analisa o conteúdo HTML e localiza a tabela com os dados de produção.
    - Itera sobre as linhas da tabela para extrair:
        - A categoria principal, se a linha representa uma nova categoria.
        - A descrição do produto e a quantidade, caso a linha seja um subitem.
    - Adiciona os dados extraídos em um dicionário dentro da lista `data`.

    Exceções:
    - Retorna uma lista vazia e imprime uma mensagem em caso de erro de conexão.
    """

    url = f'http://vitibrasil.cnpuv.embrapa.br/index.php?ano={ano}&opcao=opt_02'

    response = requests.get(url)
    if response.status_code != 200:
        print(f"Erro ao acessar a página para o ano {ano}: {response.status_code}")
        return []

    # Parseando o conteúdo HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrando a tabela de interesse
    table = soup.find('table', class_='tb_base tb_dados')

    data = []
    current_category = None

    # Iterando pelas linhas da tabela
    for row in table.find('tbody').find_all('tr'):
        columns = row.find_all('td')
        if len(columns) == 2:
            # Limpando os dados
            categoria = columns[0].get_text(strip=True)
            quantidade_text = columns[1].get_text(strip=True)
            quantidade = parse_quantidade(quantidade_text)

            # Atualizando a categoria se for uma nova
            if "tb_item" in columns[0]['class']:
                current_category = categoria
            # Se for uma subcategoria, mantém a categoria corrente
            elif "tb_subitem" in columns[0]['class']:
                descricao = categoria
                data.append({
                    "categoria_produto": current_category,
                    "descricao_produto": descricao,
                    "quantidade": quantidade,
                    "ano": ano
                })

    return data


def parse_quantidade(quantidade_text):
    """
    Converte uma quantidade em formato de string para um valor numérico.

    Parâmetros:
    quantidade_text (str): A quantidade em formato de string (ex: "1.000,50").

    Retorna:
    float: O valor numérico da quantidade ou 0.0 se o valor for "-" ou vazio.
    """
    if quantidade_text == '-' or not quantidade_text:
        return 0.0
    return float(quantidade_text.replace('.', '').replace(',', '.'))


def send_to_api(data):
    """
    Envia uma lista de registros de produção para uma API REST.

    Parâmetros:
    data (list): Lista de dicionários contendo os dados de produção a serem enviados.

    Fluxo:
    - Itera sobre cada registro na lista `data`.
    - Envia uma solicitação POST para a API com o registro em formato JSON.
    - Imprime uma mensagem de sucesso ou erro, dependendo do código de status HTTP.
    - Aguarda 1 segundo entre cada envio para evitar sobrecarga no servidor.

    Exceções:
    - Em caso de falha de envio, imprime o código de status e a resposta de erro.
    """
    api_url = 'http://127.0.0.1:8000/producao/'  # Endpoint da API de Produção
    headers = {'Content-Type': 'application/json'}

    for entry in data:
        response = requests.post(api_url, json=entry, headers=headers)
        if response.status_code in [200, 201]:
            print(f"Dados enviados com sucesso: {entry}")
        else:
            print(f"Erro ao enviar os dados: {response.status_code} - {response.text}")
            print(entry)

        time.sleep(1)


if __name__ == '__main__':
    """
    Executa o scraping e envio de dados para os anos de 1970 a 2023.

    Fluxo:
    - Itera por cada ano no intervalo de 1970 a 2023.
    - Realiza o scraping dos dados de produção para o ano atual.
    - Se houver dados, envia os registros para a API; caso contrário, imprime uma mensagem informativa.
    """
    for ano in range(1970, 2024):
        print(f"Scrapando dados para o ano {ano}")
        producoes = scrape_producao(ano)

        if producoes:
            print(f"Enviando {len(producoes)} registros para o ano {ano}")
            send_to_api(producoes)
        else:
            print(f"Nenhuma produção encontrada para o ano {ano}")
