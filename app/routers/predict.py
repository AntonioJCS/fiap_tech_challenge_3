
from fastapi import APIRouter
from app.schemas.predict import LSTMInput, LSTMResponse
from tensorflow.keras.models import load_model
import numpy as np
import os

MODEL_PATH = "app/ml/models/lstm_model.h5"

router = APIRouter()

@router.post("/predict/lstm", response_model=LSTMResponse, summary="Previsão LSTM com entrada personalizada")
def post_lstm_prediction(data: LSTMInput):
    if not os.path.exists(MODEL_PATH):
        return {"prediction": -1.0}

    model = load_model(MODEL_PATH)
    values = np.array(data.valores).astype("float32").reshape((len(data.valores), 1))

    # Pega o último valor e usa como entrada para prever o próximo
    last_value = values[-1].reshape((1, 1, 1))
    prediction = model.predict(last_value, verbose=0)
    return {"prediction": prediction[0][0].item()}


@router.get("/predict/test", summary="Teste de funcionamento do router predict")
def test_router():
    return {"status": "ok"}
