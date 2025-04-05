
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from app.database import SessionLocal
from app.models.producao import Producao
from app.ml.preprocessing import prepare_data
import os

MODEL_PATH = "app/ml/models/lstm_model.h5"

def predict_lstm():
    # Verifica se o modelo existe
    if not os.path.exists(MODEL_PATH):
        return "Modelo LSTM não encontrado. Treine primeiro."

    # Carrega o modelo treinado
    model = load_model(MODEL_PATH)

    # Carrega os dados do banco
    with SessionLocal() as session:
        data = session.query(Producao).all()
        df = pd.DataFrame([d.__dict__ for d in data])

    if df.empty:
        return "Sem dados para previsão."

    # Prepara os dados
    df_prepared = prepare_data(df, target_column="quantidade")
    values = df_prepared["quantidade"].values.astype("float32")

    if len(values) < 1:
        return "Dados insuficientes para previsão."

    # Usar o último valor conhecido como entrada
    last_value = np.array([[values[-1]]]).reshape((1, 1, 1))

    # Realizar a previsão
    prediction = model.predict(last_value, verbose=0)

    return prediction[0][0].item()
