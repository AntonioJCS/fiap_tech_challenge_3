from fastapi import FastAPI
from api.routes import health, predict

app = FastAPI(title="API de Previsão - Tech Challenge")

# Rotas principais
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(predict.router, prefix="/predict", tags=["Previsão"])


@app.get("/")
def read_root():
    return {"mensagem": "API de Previsão no ar!"}
