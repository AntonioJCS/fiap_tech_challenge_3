from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(
    prefix="/comercializacao",
    tags=["Comercialização"]
)



@router.get("/", response_model=list[schemas.Comercializacao], description="Retorna uma lista de comercializações de vinhos e derivados no Rio Grande do Sul.")
def get_comercializacoes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    return crud.get_comercializacoes(db=db, skip=skip, limit=limit)

@router.get("/ano/{ano}", response_model=list[schemas.Comercializacao], description="Retorna uma lista de comercializações filtradas pelo ano especificado.")
def get_comercializacao_por_ano(ano: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    comercializacoes = crud.get_comercializacao_by_ano(db=db, ano=ano, skip=skip, limit=limit)
    if not comercializacoes:
        raise HTTPException(status_code=404, detail="Nenhuma Comercializacao encontrada para este ano")
    return comercializacoes

@router.post("/", response_model=schemas.Comercializacao, description="Cria um novo registro de comercialização.")
def create_comercializacao(comercializacao: schemas.ComercializacaoCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    return crud.create_comercializacao(db=db, comercializacao=comercializacao)

@router.put("/{comercializacao_id}", response_model=schemas.Comercializacao, description="Atualiza um registro de comercialização existente com novos dados.")
def update_comercializacao(comercializacao_id: int, comercializacao: schemas.ComercializacaoCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    db_comercializacao = crud.get_comercializacao(db=db, comercializacao_id=comercializacao_id)
    if db_comercializacao is None:
        raise HTTPException(status_code=404, detail="Comercializacao não encontrada")
    return crud.update_comercializacao(db=db, comercializacao_id=comercializacao_id, comercializacao=comercializacao)

@router.delete("/{comercializacao_id}", description="Deleta um registro de comercialização pelo ID especificado.")
def delete_comercializacao(comercializacao_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    db_comercializacao = crud.get_comercializacao(db=db, comercializacao_id=comercializacao_id)
    if db_comercializacao is None:
        raise HTTPException(status_code=404, detail="Comercializacao não encontrada")
    crud.delete_comercializacao(db=db, comercializacao_id=comercializacao_id)
    return {"message": "Comercializacao deletada com sucesso"}
