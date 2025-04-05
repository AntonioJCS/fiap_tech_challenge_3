from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(
    prefix="/importacao",
    tags=["Importação"]
)

@router.get("/", response_model=list[schemas.Importacao], description="Retorna uma lista de importações de vinhos e derivados no Rio Grande do Sul.")
def get_importacoes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    return crud.get_importacoes(db=db, skip=skip, limit=limit)

@router.get("/ano/{ano}", response_model=list[schemas.Importacao], description="Retorna uma lista de importações filtradas pelo ano especificado.")
def get_importacao_por_ano(ano: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    importacoes = crud.get_importacao_by_ano(db=db, ano=ano, skip=skip, limit=limit)
    if not importacoes:
        raise HTTPException(status_code=404, detail="Nenhuma importação encontrada para este ano")
    return importacoes

@router.post("/", response_model=schemas.Importacao, description="Cria um novo registro de importação.")
def create_importacao(importacao: schemas.ImportacaoCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    return crud.create_importacao(db=db, importacao=importacao)

@router.put("/{importacao_id}", response_model=schemas.Importacao, description="Atualiza um registro de importação existente com novos dados.")
def update_importacao(importacao_id: int, importacao: schemas.ImportacaoCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    db_importacao = crud.get_importacao(db=db, importacao_id=importacao_id)
    if db_importacao is None:
        raise HTTPException(status_code=404, detail="Importação não encontrada")
    return crud.update_importacao(db=db, importacao_id=importacao_id, importacao=importacao)

@router.delete("/{importacao_id}", description="Deleta um registro de importação pelo ID especificado.")
def delete_importacao(importacao_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    db_importacao = crud.get_importacao(db=db, importacao_id=importacao_id)
    if db_importacao is None:
        raise HTTPException(status_code=404, detail="Importação não encontrada")
    crud.delete_importacao(db=db, importacao_id=importacao_id)
    return {"message": "Importação deletada com sucesso"}
