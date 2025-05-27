import requests
import pandas as pd
from io import StringIO

def scraper(ano: int, mes: int, cert_path=True) -> pd.DataFrame:
    """
    Faz download do CSV da ANVISA, converte em DataFrame e salva no SQLite.

    Args:
        ano (int): Ano (AAAA)
        mes (int): Mês (MM)
        cert_path (bool/str): Verificação de certificado
        salvar (bool): Se True, salva no banco

    Returns:
        pd.DataFrame: Dados extraídos ou DataFrame vazio em caso de erro
    """
    ano_str = str(ano).zfill(4)
    mes_str = str(mes).zfill(2)
    ano_mes_str = ano_str + mes_str

    url = f"https://dados.anvisa.gov.br/dados/SNGPC/Manipulados/EDA_Manipulados_{ano_mes_str}.csv"

    try:
        response = requests.get(url, verify=cert_path)
        response.raise_for_status()

        df = pd.read_csv(StringIO(response.text), sep=";", low_memory=False, dtype=str)

        return df

    except requests.exceptions.HTTPError as http_err:
        print(f"Erro HTTP: {http_err}")
    except requests.exceptions.SSLError as ssl_err:
        print(f"Erro de certificado SSL: {ssl_err}")
    except requests.exceptions.RequestException as err:
        print(f"Erro de requisição: {err}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return pd.DataFrame()
