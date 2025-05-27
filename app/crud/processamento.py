from sqlalchemy.orm import Session
from app.models.processamento import Cultivo
from app.schemas.processamento import CultivoCreate

def get_processamentos(db: Session, skip: int = 0, limit: int = 10):
    """
    Retorna uma lista de cultivos processados, com opção de limitar o número de registros.

    Args:
        db (Session): Sessão de banco de dados.
        skip (int): Número de registros para pular, padrão é 0.
        limit (int): Número máximo de registros a retornar, padrão é 10.

    Returns:
        list: Lista de objetos Cultivo.
    """
    return db.query(Cultivo).offset(skip).limit(limit).all()

def get_processamento_by_ano(db: Session, ano: int, skip: int = 0, limit: int = 10):
    """
    Retorna uma lista de cultivos processados filtrados pelo ano especificado.

    Args:
        db (Session): Sessão de banco de dados.
        ano (int): Ano para filtrar os registros.
        skip (int): Número de registros para pular, padrão é 0.
        limit (int): Número máximo de registros a retornar, padrão é 10.

    Returns:
        list: Lista de objetos Cultivo filtrados pelo ano.
    """
    return db.query(Cultivo).filter(Cultivo.ano == ano).offset(skip).limit(limit).all()

def get_processamento(db: Session, cultivo_id: int):
    """
    Retorna um cultivo processado específico pelo ID.

    Args:
        db (Session): Sessão de banco de dados.
        cultivo_id (int): ID do cultivo processado a ser recuperado.

    Returns:
        Cultivo: Objeto Cultivo ou None se não encontrado.
    """
    return db.query(Cultivo).filter(Cultivo.id == cultivo_id).first()

def create_processamento(db: Session, cultivo: CultivoCreate):
    """
    Cria um novo registro de cultivo processado no banco de dados.

    Args:
        db (Session): Sessão de banco de dados.
        cultivo (CultivoCreate): Dados do novo cultivo processado.

    Returns:
        Cultivo: Objeto Cultivo recém-criado.
    """
    db_cultivo = Cultivo(
        categoria_cultivo=cultivo.categoria_cultivo,
        descricao_cultivo=cultivo.descricao_cultivo,
        tipo_processamento=cultivo.tipo_processamento,
        quantidade=cultivo.quantidade,
        ano=cultivo.ano
    )
    db.add(db_cultivo)
    db.commit()
    db.refresh(db_cultivo)
    return db_cultivo

def update_processamento(db: Session, cultivo_id: int, cultivo: CultivoCreate):
    """
    Atualiza um cultivo processado existente com novos dados.

    Args:
        db (Session): Sessão de banco de dados.
        cultivo_id (int): ID do cultivo processado a ser atualizado.
        cultivo (CultivoCreate): Dados atualizados do cultivo processado.

    Returns:
        Cultivo: Objeto Cultivo atualizado ou None se não encontrado.
    """
    db_cultivo = db.query(Cultivo).filter(Cultivo.id == cultivo_id).first()
    if db_cultivo:
        db_cultivo.categoria_cultivo = cultivo.categoria_cultivo
        db_cultivo.descricao_cultivo = cultivo.descricao_cultivo
        db_cultivo.quantidade = cultivo.quantidade
        db_cultivo.ano = cultivo.ano
        db_cultivo.tipo_processamento = cultivo.tipo_processamento
        db.commit()
        db.refresh(db_cultivo)
    return db_cultivo

def delete_processamento(db: Session, cultivo_id: int):
    """
    Deleta um cultivo processado do banco de dados pelo ID.

    Args:
        db (Session): Sessão de banco de dados.
        cultivo_id (int): ID do cultivo processado a ser deletado.

    Returns:
        None
    """
    db_cultivo = db.query(Cultivo).filter(Cultivo.id == cultivo_id).first()
    if db_cultivo:
        db.delete(db_cultivo)
        db.commit()
