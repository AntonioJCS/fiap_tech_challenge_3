from sqlalchemy.orm import Session
from app.models.importacao import Importacao
from app.schemas.importacao import ImportacaoCreate

def get_importacoes(db: Session, skip: int = 0, limit: int = 10):
    """
    Retorna uma lista de importações, com opção de limitar o número de registros.

    Args:
        db (Session): Sessão de banco de dados.
        skip (int): Número de registros para pular, padrão é 0.
        limit (int): Número máximo de registros a retornar, padrão é 10.

    Returns:
        list: Lista de objetos Importacao.
    """
    return db.query(Importacao).offset(skip).limit(limit).all()

def get_importacao_by_ano(db: Session, ano: int, skip: int = 0, limit: int = 10):
    """
    Retorna uma lista de importações filtradas pelo ano especificado.

    Args:
        db (Session): Sessão de banco de dados.
        ano (int): Ano para filtrar os registros.
        skip (int): Número de registros para pular, padrão é 0.
        limit (int): Número máximo de registros a retornar, padrão é 10.

    Returns:
        list: Lista de objetos Importacao filtrados pelo ano.
    """
    return db.query(Importacao).filter(Importacao.ano == ano).offset(skip).limit(limit).all()

def get_importacao(db: Session, importacao_id: int):
    """
    Retorna uma importação específica pelo ID.

    Args:
        db (Session): Sessão de banco de dados.
        importacao_id (int): ID da importação a ser recuperada.

    Returns:
        Importacao: Objeto Importacao ou None se não encontrado.
    """
    return db.query(Importacao).filter(Importacao.id == importacao_id).first()

def create_importacao(db: Session, importacao: ImportacaoCreate):
    """
    Cria uma nova importação no banco de dados.

    Args:
        db (Session): Sessão de banco de dados.
        importacao (ImportacaoCreate): Dados da nova importação.

    Returns:
        Importacao: Objeto Importacao recém-criado.
    """
    db_importacao = Importacao(
        categoria=importacao.categoria,
        pais_origem=importacao.pais_origem,
        quantidade=importacao.quantidade,
        valor=importacao.valor,
        ano=importacao.ano
    )
    db.add(db_importacao)
    db.commit()
    db.refresh(db_importacao)
    return db_importacao

def update_importacao(db: Session, importacao_id: int, importacao: ImportacaoCreate):
    """
    Atualiza uma importação existente com novos dados.

    Args:
        db (Session): Sessão de banco de dados.
        importacao_id (int): ID da importação a ser atualizada.
        importacao (ImportacaoCreate): Dados atualizados da importação.

    Returns:
        Importacao: Objeto Importacao atualizado ou None se não encontrado.
    """
    db_importacao = db.query(Importacao).filter(Importacao.id == importacao_id).first()
    if db_importacao:
        db_importacao.categoria = importacao.categoria
        db_importacao.pais_origem = importacao.pais_origem
        db_importacao.quantidade = importacao.quantidade
        db_importacao.valor = importacao.valor
        db_importacao.ano = importacao.ano
        db.commit()
        db.refresh(db_importacao)
    return db_importacao

def delete_importacao(db: Session, importacao_id: int):
    """
    Deleta uma importação do banco de dados pelo ID.

    Args:
        db (Session): Sessão de banco de dados.
        importacao_id (int): ID da importação a ser deletada.

    Returns:
        None
    """
    db_importacao = db.query(Importacao).filter(Importacao.id == importacao_id).first()
    if db_importacao:
        db.delete(db_importacao)
        db.commit()
