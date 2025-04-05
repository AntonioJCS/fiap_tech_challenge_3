from sqlalchemy.orm import Session
from app.models.exportacao import Exportacao
from app.schemas.exportacao import ExportacaoCreate

def get_exportacoes(db: Session, skip: int = 0, limit: int = 10):
    """
    Retorna uma lista de exportações, com opção de limitar o número de registros.

    Args:
        db (Session): Sessão de banco de dados.
        skip (int): Número de registros para pular, padrão é 0.
        limit (int): Número máximo de registros a retornar, padrão é 10.

    Returns:
        list: Lista de objetos Exportacao.
    """
    return db.query(Exportacao).offset(skip).limit(limit).all()

def get_exportacao_by_ano(db: Session, ano: int, skip: int = 0, limit: int = 10):
    """
    Retorna uma lista de exportações filtradas pelo ano especificado.

    Args:
        db (Session): Sessão de banco de dados.
        ano (int): Ano para filtrar os registros.
        skip (int): Número de registros para pular, padrão é 0.
        limit (int): Número máximo de registros a retornar, padrão é 10.

    Returns:
        list: Lista de objetos Exportacao filtrados pelo ano.
    """
    return db.query(Exportacao).filter(Exportacao.ano == ano).offset(skip).limit(limit).all()

def get_exportacao(db: Session, exportacao_id: int):
    """
    Retorna uma exportação específica pelo ID.

    Args:
        db (Session): Sessão de banco de dados.
        exportacao_id (int): ID da exportação a ser recuperada.

    Returns:
        Exportacao: Objeto Exportacao ou None se não encontrado.
    """
    return db.query(Exportacao).filter(Exportacao.id == exportacao_id).first()

def create_exportacao(db: Session, exportacao: ExportacaoCreate):
    """
    Cria uma nova exportação no banco de dados.

    Args:
        db (Session): Sessão de banco de dados.
        exportacao (ExportacaoCreate): Dados da nova exportação.

    Returns:
        Exportacao: Objeto Exportacao recém-criado.
    """
    db_exportacao = Exportacao(
        categoria=exportacao.categoria,
        pais_destino=exportacao.pais_destino,
        quantidade=exportacao.quantidade,
        valor=exportacao.valor,
        ano=exportacao.ano
    )
    db.add(db_exportacao)
    db.commit()
    db.refresh(db_exportacao)
    return db_exportacao

def update_exportacao(db: Session, exportacao_id: int, exportacao: ExportacaoCreate):
    """
    Atualiza uma exportação existente com novos dados.

    Args:
        db (Session): Sessão de banco de dados.
        exportacao_id (int): ID da exportação a ser atualizada.
        exportacao (ExportacaoCreate): Dados atualizados da exportação.

    Returns:
        Exportacao: Objeto Exportacao atualizado ou None se não encontrado.
    """
    db_exportacao = db.query(Exportacao).filter(Exportacao.id == exportacao_id).first()
    if db_exportacao:
        db_exportacao.categoria = exportacao.categoria
        db_exportacao.pais_destino = exportacao.pais_destino
        db_exportacao.quantidade = exportacao.quantidade
        db_exportacao.valor = exportacao.valor
        db_exportacao.ano = exportacao.ano
        db.commit()
        db.refresh(db_exportacao)
    return db_exportacao

def delete_exportacao(db: Session, exportacao_id: int):
    """
    Deleta uma exportação do banco de dados pelo ID.

    Args:
        db (Session): Sessão de banco de dados.
        exportacao_id (int): ID da exportação a ser deletada.

    Returns:
        None
    """
    db_exportacao = db.query(Exportacao).filter(Exportacao.id == exportacao_id).first()
    if db_exportacao:
        db.delete(db_exportacao)
        db.commit()
