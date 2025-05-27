import pandas as pd

def prepare_data(df: pd.DataFrame, target_column: str):
    # Agrupar por ano e somar a quantidade
    df = df.groupby("ano", as_index=False)[target_column].sum()

    # Ordenar por ano
    df = df.sort_values("ano")

    # Normalizar a coluna de quantidade (opcional)
    df[target_column] = df[target_column].astype(float)

    return df
