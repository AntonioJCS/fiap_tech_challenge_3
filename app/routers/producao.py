from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(
    prefix="/producao",
    tags=["Produção"]
)

@router.get("/", response_model=list[schemas.Producao], description="Retorna uma lista de produções de vinhos e derivados no Rio Grande do Sul.")
def get_producoes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    return crud.get_producoes(db=db, skip=skip, limit=limit)

@router.get("/ano/{ano}", response_model=list[schemas.Producao], description="Retorna uma lista de produções filtradas pelo ano especificado.")
def get_producao_por_ano(ano: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    producoes = crud.get_producao_by_ano(db=db, ano=ano, skip=skip, limit=limit)
    if not producoes:
        raise HTTPException(status_code=404, detail="Nenhuma produção encontrada para este ano")
    return producoes

@router.post("/", response_model=schemas.Producao, description="Cria um novo registro de produção.")
def create_producao(producao: schemas.ProducaoCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    return crud.create_producao(db=db, producao=producao)

@router.put("/{producao_id}", response_model=schemas.Producao, description="Atualiza um registro de produção existente com novos dados.")
def update_producao(producao_id: int, producao: schemas.ProducaoCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    db_producao = crud.get_producao(db=db, producao_id=producao_id)
    if db_producao is None:
        raise HTTPException(status_code=404, detail="Produção não encontrada")
    return crud.update_producao(db=db, producao_id=producao_id, producao=producao)

@router.delete("/{producao_id}", description="Deleta um registro de produção pelo ID especificado.")
def delete_producao(producao_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    db_producao = crud.get_producao(db=db, producao_id=producao_id)
    if db_producao is None:
        raise HTTPException(status_code=404, detail="Produção não encontrada")
    crud.delete_producao(db=db, producao_id=producao_id)
    return {"message": "Produção deletada com sucesso"}
