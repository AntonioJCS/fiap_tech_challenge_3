import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from ml.modelo_lstm import preprocessar_dados, criar_sequencias, prever


def carregar_modelo_lstm(caminho_modelo: str = "artifacts/modelo_lstm.keras"):
    """Carrega um modelo LSTM salvo."""
    return load_model(caminho_modelo)


def fazer_previsao_com_lstm(df: pd.DataFrame, seq_length: int = 3, target_col: str = "QTD_UNIDADE_FARMACOTECNICA") -> pd.DataFrame:
    """
    Executa a pipeline de previsão usando o modelo LSTM salvo.
    Retorna um DataFrame com colunas ['REAL', 'PREVISTO'].
    """
    df, df_scaled, scaler = preprocessar_dados(df, target_col)
    X, y = criar_sequencias(df_scaled, seq_length)

    modelo = carregar_modelo_lstm()
    resultado = prever(modelo, X, scaler, y_test=y, plot=False)
    return resultado
