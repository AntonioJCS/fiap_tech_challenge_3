from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.auth import get_current_user
from app.database import get_db

router = APIRouter(
    prefix="/exportacao",
    tags=["Exportação"]
)

@router.get("/", response_model=list[schemas.Exportacao], description="Retorna uma lista de exportações de vinhos e derivados no Rio Grande do Sul.")
def get_exportacoes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    return crud.get_exportacoes(db=db, skip=skip, limit=limit)

@router.get("/ano/{ano}", response_model=list[schemas.Exportacao], description="Retorna uma lista de exportações filtradas pelo ano especificado.")
def get_exportacao_por_ano(ano: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    exportacoes = crud.get_exportacao_by_ano(db=db, ano=ano, skip=skip, limit=limit)
    if not exportacoes:
        raise HTTPException(status_code=404, detail="Nenhuma exportação encontrada para este ano")
    return exportacoes

@router.post("/", response_model=schemas.Exportacao, description="Cria um novo registro de exportação.")
def create_exportacao(exportacao: schemas.ExportacaoCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    return crud.create_exportacao(db=db, exportacao=exportacao)

@router.put("/{exportacao_id}", response_model=schemas.Exportacao, description="Atualiza um registro de exportação existente com novos dados.")
def update_exportacao(exportacao_id: int, exportacao: schemas.ExportacaoCreate, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    db_exportacao = crud.get_exportacao(db=db, exportacao=exportacao_id)
    if db_exportacao is None:
        raise HTTPException(status_code=404, detail="Exportação não encontrada")
    return crud.update_exportacao(db=db, exportacao_id=exportacao_id, exportacao=exportacao)

@router.delete("/{exportacao_id}", description="Deleta um registro de exportação pelo ID especificado.")
def delete_exportacao(exportacao_id: int, db: Session = Depends(get_db), current_user: schemas.Usuario = Depends(get_current_user)):
    db_exportacao = crud.get_exportacao(db=db, exportacao_id=exportacao_id)
    if db_exportacao is None:
        raise HTTPException(status_code=404, detail="Exportação não encontrada")
    crud.delete_exportacao(db=db, exportacao_id=exportacao_id)
    return {"message": "Exportação deletada com sucesso"}
