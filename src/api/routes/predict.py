from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import pandas as pd
from services.previsao_service import fazer_previsao_com_lstm

router = APIRouter()

# Schema de entrada
class RegistroEntrada(BaseModel):
    ANO_VENDA: int
    MES_VENDA: int
    QTD_UNIDADE_FARMACOTECNICA: float

@router.post("/")
def prever_series(dados: List[RegistroEntrada]):
    df = pd.DataFrame([d.dict() for d in dados])
    resultado = fazer_previsao_com_lstm(df)
    return resultado.to_dict(orient="records")
