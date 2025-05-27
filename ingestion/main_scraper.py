import argparse
from producao_scraper import scrape_producao
from processamento_scraper import scrape_processamento
from comercializacao_scraper import scrape_comercializacao
from importacao_scraper import scrape_importacao
from exportacao_scraper import scrape_exportacao
from utils import send_to_api

def run_scraper(entidade, ano_inicial, ano_final):
    """
    Executa o scraper para a entidade de viticultura especificada, coletando dados de acordo
    com o intervalo de anos fornecido e enviando-os para uma API.

    Parâmetros:
    entidade (str): A entidade para qual os dados serão coletados. Opções: 'producao', 'processamento',
                    'comercializacao', 'importacao', 'exportacao'.
    ano_inicial (int): O ano inicial para iniciar a coleta de dados.
    ano_final (int): O ano final para a coleta de dados.

    Fluxo:
    - Itera sobre o intervalo de anos especificado.
    - Para cada ano, realiza o scraping dos dados para a entidade escolhida.
    - Envia os dados coletados para a API usando `send_to_api`.
    - Se a entidade fornecida não for reconhecida, imprime uma mensagem de erro.

    Dependências:
    - scrape_producao, scrape_processamento, scrape_comercializacao, scrape_importacao, scrape_exportacao:
      Funções de scraping para cada entidade.
    - send_to_api (function): Função para enviar os dados coletados para uma API.

    Exceções:
    - Não realiza tratamento de exceções explícito; qualquer erro de rede ou scraping será exibido durante a execução.

    Exemplos:
    >>> run_scraper('producao', 2010, 2015)
    Scrapando dados para o ano 2010
    Scrapando dados para o ano 2011
    ...
    """
    for ano in range(ano_inicial, ano_final + 1):
        print(f"Scrapando dados para o ano {ano}")
        if entidade == 'producao':
            dados = scrape_producao(ano)
            send_to_api(dados, 'producao')
        elif entidade == 'processamento':
            dados = scrape_processamento(ano)
            send_to_api(dados, 'processamento')
        elif entidade == 'comercializacao':
            dados = scrape_comercializacao(ano)
            send_to_api(dados, 'comercializacao')
        elif entidade == 'importacao':
            dados = scrape_importacao(ano)
            send_to_api(dados, 'importacao')
        elif entidade == 'exportacao':
            dados = scrape_exportacao(ano)
            send_to_api(dados, 'exportacao')
        else:
            print(f"Entidade {entidade} não reconhecida.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper para diferentes entidades de viticultura.')
    parser.add_argument('entidade', choices=['producao', 'processamento', 'comercializacao', 'importacao', 'exportacao'],
                        help='Escolha a entidade para scrapping: producao, processamento, comercializacao, importacao, exportacao')
    parser.add_argument('--ano_inicial', type=int, default=1970, help='Ano inicial para scraping (default: 1970)')
    parser.add_argument('--ano_final', type=int, default=2023, help='Ano final para scraping (default: 2023)')

    args = parser.parse_args()

    run_scraper(args.entidade, args.ano_inicial, args.ano_final)
