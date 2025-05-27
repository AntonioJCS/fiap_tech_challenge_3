import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


def preprocessar_dados(df: pd.DataFrame, target_col: str = "QTD_UNIDADE_FARMACOTECNICA"):
    df = df.copy()
    df["DATA"] = pd.to_datetime(df["ANO_VENDA"].astype(str) + "-" + df["MES_VENDA"].astype(str))
    df.set_index("DATA", inplace=True)
    df = df[[target_col]].dropna()
    scaler = MinMaxScaler()
    df_scaled = scaler.fit_transform(df)
    return df, df_scaled, scaler


def criar_sequencias(data: np.ndarray, seq_length: int):
    X, y = [], []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length])
    return np.array(X), np.array(y)


def construir_modelo(seq_length: int):
    model = Sequential([
        LSTM(50, activation='relu', return_sequences=True, input_shape=(seq_length, 1)),
        Dropout(0.2),
        LSTM(50, activation='relu'),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mse')
    return model


def treinar_modelo(model, X_train, y_train, X_test, y_test):
    callbacks = [
        EarlyStopping(patience=10, restore_best_weights=True),
        ModelCheckpoint("models/modelo_lstm.keras", save_best_only=True)
    ]
    history = model.fit(
        X_train, y_train,
        epochs=50,
        batch_size=8,
        validation_data=(X_test, y_test),
        callbacks=callbacks,
        verbose=1
    )
    return history


def prever(model, X_test, scaler, y_test=None, plot: bool = False):
    y_pred = model.predict(X_test)
    y_pred_inv = scaler.inverse_transform(y_pred)

    if y_test is not None:
        y_test_inv = scaler.inverse_transform(y_test.reshape(-1, 1))
        if plot:
            plt.figure(figsize=(10, 5))
            plt.plot(y_test_inv, label='Real')
            plt.plot(y_pred_inv, label='Previsto')
            plt.legend()
            plt.title('Previsão de Séries Temporais com LSTM')
            plt.show()

        df_resultado = pd.DataFrame({
            "REAL": y_test_inv.flatten(),
            "PREVISTO": y_pred_inv.flatten()
        })
        return df_resultado

    return y_pred_inv
