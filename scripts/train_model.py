import pandas as pd
import numpy as np
from tensorflow.keras.models import save_model
from app.database import SessionLocal
from app.models.producao import Producao
from app.ml.preprocessing import prepare_data
from app.ml.models.lstm_model import build_lstm_model
import os

MODEL_PATH = "app/ml/models/lstm_model.h5"

def train_lstm_model():
    with SessionLocal() as session:
        data = session.query(Producao).all()
        df = pd.DataFrame([d.__dict__ for d in data])

    if df.empty:
        print("Sem dados para treinamento.")
        return

    df_prepared = prepare_data(df, target_column="quantidade")

    # Preparar os dados em formato de série temporal
    values = df_prepared["quantidade"].values.astype("float32")

    # Criar janelas de sequência
    X, y = [], []
    for i in range(len(values) - 1):
        X.append([values[i]])
        y.append(values[i + 1])

    X = np.array(X).reshape((len(X), 1, 1))
    y = np.array(y)

    # Criar e treinar o modelo
    model = build_lstm_model(input_shape=(1, 1))
    model.fit(X, y, epochs=50, verbose=1)

    # Salvar o modelo
    save_model(model, MODEL_PATH)
    print(f"Modelo salvo em {MODEL_PATH}")

if __name__ == "__main__":
    train_lstm_model()
