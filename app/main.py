from fastapi import FastAPI
from app.routers import auth, producao, processamento, comercializacao, importacao, exportacao, predict
from app.database import engine
from app.models import producao as producao_model
from app.models import processamento as processamento_model

# Criar as tabelas no banco de dados
producao_model.Base.metadata.create_all(bind=engine)
processamento_model.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluindo os routers
app.include_router(auth.router)
app.include_router(producao.router)
app.include_router(processamento.router)
app.include_router(comercializacao.router)
app.include_router(importacao.router)
app.include_router(exportacao.router)
app.include_router(predict.router, prefix="/predict", tags=["Previsões"])



@app.get("/")
def read_root():
    return {"message": "API Vitivinicultura"}


@app.on_event("startup")
def show_routes():
    print("\n📌 ROTAS REGISTRADAS:")
    for route in app.routes:
        print(f"{route.path} [{','.join(route.methods)}] → {route.name}")
