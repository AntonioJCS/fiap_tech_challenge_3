from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(
    prefix="/processamento",
    tags=["Processamento"]
)

@router.get("/", response_model=list[schemas.Cultivo], description="Retorna uma lista de processamentos de vinhos e derivados no Rio Grande do Sul.")
def get_processamentos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    return crud.get_processamentos(db=db, skip=skip, limit=limit)

@router.get("/ano/{ano}", response_model=list[schemas.Cultivo], description="Retorna uma lista de processamentos filtrados pelo ano especificado.")
def get_processamento_por_ano(ano: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    processamentos = crud.get_processamento_by_ano(db=db, ano=ano, skip=skip, limit=limit)
    if not processamentos:
        raise HTTPException(status_code=404, detail="Nenhum processamento encontrado para este ano")
    return processamentos

@router.post("/", response_model=schemas.Cultivo, description="Cria um novo registro de processamento.")
def create_processamento(cultivo: schemas.CultivoCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    return crud.create_processamento(db=db, cultivo=cultivo)

@router.put("/{cultivo_id}", response_model=schemas.Cultivo, description="Atualiza um registro de processamento existente com novos dados.")
def update_processamento(cultivo_id: int, cultivo: schemas.CultivoCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    db_processamento = crud.get_processamento(db=db, cultivo_id=cultivo_id)
    if db_processamento is None:
        raise HTTPException(status_code=404, detail="Processamento não encontrado")
    return crud.update_processamento(db=db, cultivo_id=cultivo_id, cultivo=cultivo)

@router.delete("/{cultivo_id}", description="Deleta um registro de processamento pelo ID especificado.")
def delete_processamento(cultivo_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    db_processamento = crud.get_processamento(db=db, cultivo_id=cultivo_id)
    if db_processamento is None:
        raise HTTPException(status_code=404, detail="Processamento não encontrado")
    crud.delete_processamento(db=db, cultivo_id=cultivo_id)
    return {"message": "Processamento deletado com sucesso"}
