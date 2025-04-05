
from pydantic import BaseModel, Field
from typing import List

class LSTMInput(BaseModel):
    valores: List[float] = Field(..., example=[12500.0, 12700.0, 13100.0])

class LSTMResponse(BaseModel):
    prediction: float = Field(..., example=13350.5)
