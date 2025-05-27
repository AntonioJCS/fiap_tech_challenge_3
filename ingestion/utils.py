import requests
import time


def parse_quantidade(quantidade_text):
    """
    Converte a quantidade de uma string para um valor float, removendo pontos e substituindo vírgulas por pontos.
    Se a string contiver '-', 'nd' ou '*', ou estiver vazia, retorna 0.0.

    Parâmetros:
    quantidade_text (str): A quantidade em formato de string (ex: "1.000,50" ou "-").

    Retorna:
    float: O valor numérico da quantidade ou 0.0 para entradas não numéricas.
    """
    if quantidade_text in ['-', 'nd', '*'] or not quantidade_text:
        return 0.0
    return float(quantidade_text.replace('.', '').replace(',', '.'))


def send_to_api(data, endpoint):
    """
    Envia uma lista de dados para um endpoint específico da API.

    Parâmetros:
    data (list): Lista de dicionários contendo os dados a serem enviados.
    endpoint (str): O nome do endpoint da API para o envio (ex: 'producao', 'importacao').

    Fluxo:
    - Itera sobre cada registro na lista `data`.
    - Envia uma requisição POST para a API com o registro em formato JSON.
    - Imprime uma mensagem de sucesso ou erro para cada envio, dependendo do código de status HTTP.
    - Aguarda 0,2 segundos entre cada envio para evitar sobrecarga no servidor.

    Exceções:
    - Em caso de falha de envio, imprime o código de status e a resposta de erro.
    """
    api_url = f'http://127.0.0.1:8000/{endpoint}/'
    headers = {'Content-Type': 'application/json'}

    for entry in data:
        response = requests.post(api_url, json=entry, headers=headers)
        if response.status_code in [200, 201]:
            print(f"Dados enviados com sucesso: {entry}")
        else:
            print(f"Erro ao enviar os dados: {response.status_code} - {response.text}")
        time.sleep(0.2)  # Delay de 0,2 segundos entre requisições
