from sqlalchemy.orm import Session
from app.models.producao import Producao
from app.schemas.producao import ProducaoCreate

def get_producoes(db: Session, skip: int = 0, limit: int = 10):
    """
    Retorna uma lista de produções, com opção de limitar o número de registros.

    Args:
        db (Session): Sessão de banco de dados.
        skip (int): Número de registros para pular, padrão é 0.
        limit (int): Número máximo de registros a retornar, padrão é 10.

    Returns:
        list: Lista de objetos Producao.
    """
    return db.query(Producao).offset(skip).limit(limit).all()

def get_producao_by_ano(db: Session, ano: int, skip: int = 0, limit: int = 10):
    """
    Retorna uma lista de produções filtradas pelo ano especificado.

    Args:
        db (Session): Sessão de banco de dados.
        ano (int): Ano para filtrar os registros.
        skip (int): Número de registros para pular, padrão é 0.
        limit (int): Número máximo de registros a retornar, padrão é 10.

    Returns:
        list: Lista de objetos Producao filtrados pelo ano.
    """
    return db.query(Producao).filter(Producao.ano == ano).offset(skip).limit(limit).all()

def get_producao(db: Session, producao_id: int):
    """
    Retorna uma produção específica pelo ID.

    Args:
        db (Session): Sessão de banco de dados.
        producao_id (int): ID da produção a ser recuperada.

    Returns:
        Producao: Objeto Producao ou None se não encontrado.
    """
    return db.query(Producao).filter(Producao.id == producao_id).first()

def create_producao(db: Session, producao: ProducaoCreate):
    """
    Cria um novo registro de produção no banco de dados.

    Args:
        db (Session): Sessão de banco de dados.
        producao (ProducaoCreate): Dados da nova produção.

    Returns:
        Producao: Objeto Producao recém-criado.
    """
    db_producao = Producao(
        categoria_produto=producao.categoria_produto,
        descricao_produto=producao.descricao_produto,
        quantidade=producao.quantidade,
        ano=producao.ano
    )
    db.add(db_producao)
    db.commit()
    db.refresh(db_producao)
    return db_producao

def update_producao(db: Session, producao_id: int, producao: ProducaoCreate):
    """
    Atualiza uma produção existente com novos dados.

    Args:
        db (Session): Sessão de banco de dados.
        producao_id (int): ID da produção a ser atualizada.
        producao (ProducaoCreate): Dados atualizados da produção.

    Returns:
        Producao: Objeto Producao atualizado ou None se não encontrado.
    """
    db_producao = db.query(Producao).filter(Producao.id == producao_id).first()
    if db_producao:
        db_producao.categoria_produto = producao.categoria_produto
        db_producao.descricao_produto = producao.descricao_produto
        db_producao.quantidade = producao.quantidade
        db_producao.ano = producao.ano
        db.commit()
        db.refresh(db_producao)
    return db_producao

def delete_producao(db: Session, producao_id: int):
    """
    Deleta uma produção do banco de dados pelo ID.

    Args:
        db (Session): Sessão de banco de dados.
        producao_id (int): ID da produção a ser deletada.

    Returns:
        None
    """
    db_producao = db.query(Producao).filter(Producao.id == producao_id).first()
    if db_producao:
        db.delete(db_producao)
        db.commit()
