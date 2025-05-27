from sqlalchemy.orm import Session
from app.models.comercializacao import Comercializacao
from app.schemas.comercializacao import ComercializacaoCreate

def get_comercializacoes(db: Session, skip: int = 0, limit: int = 10):
    """
    Retorna uma lista de comercializações, com a possibilidade de limitar o número de registros.

    Args:
        db (Session): Sessão de banco de dados.
        skip (int): Número de registros para pular, padrão é 0.
        limit (int): Número máximo de registros a retornar, padrão é 10.

    Returns:
        list: Lista de objetos Comercializacao.
    """
    return db.query(Comercializacao).offset(skip).limit(limit).all()

def get_comercializacao_by_ano(db: Session, ano: int, skip: int = 0, limit: int = 10):
    """
    Retorna uma lista de comercializações filtradas pelo ano especificado.

    Args:
        db (Session): Sessão de banco de dados.
        ano (int): Ano para filtrar os registros.
        skip (int): Número de registros para pular, padrão é 0.
        limit (int): Número máximo de registros a retornar, padrão é 10.

    Returns:
        list: Lista de objetos Comercializacao filtrados pelo ano.
    """
    return db.query(Comercializacao).filter(Comercializacao.ano == ano).offset(skip).limit(limit).all()

def get_comercializacao(db: Session, comercializacao_id: int):
    """
    Retorna uma comercialização específica pelo ID.

    Args:
        db (Session): Sessão de banco de dados.
        comercializacao_id (int): ID da comercialização a ser recuperada.

    Returns:
        Comercializacao: Objeto Comercializacao ou None se não encontrado.
    """
    return db.query(Comercializacao).filter(Comercializacao.id == comercializacao_id).first()

def create_comercializacao(db: Session, comercializacao: ComercializacaoCreate):
    """
    Cria uma nova comercialização no banco de dados.

    Args:
        db (Session): Sessão de banco de dados.
        comercializacao (ComercializacaoCreate): Dados da nova comercialização.

    Returns:
        Comercializacao: Objeto Comercializacao recém-criado.
    """
    db_comercializacao = Comercializacao(
        categoria_produto=comercializacao.categoria_produto,
        descricao_produto=comercializacao.descricao_produto,
        quantidade=comercializacao.quantidade,
        ano=comercializacao.ano
    )
    db.add(db_comercializacao)
    db.commit()
    db.refresh(db_comercializacao)
    return db_comercializacao

def update_comercializacao(db: Session, comercializacao_id: int, producao: ComercializacaoCreate):
    """
    Atualiza uma comercialização existente com novos dados.

    Args:
        db (Session): Sessão de banco de dados.
        comercializacao_id (int): ID da comercialização a ser atualizada.
        producao (ComercializacaoCreate): Dados atualizados da comercialização.

    Returns:
        Comercializacao: Objeto Comercializacao atualizado ou None se não encontrado.
    """
    db_comercializacao = db.query(Comercializacao).filter(Comercializacao.id == comercializacao_id).first()
    if db_comercializacao:
        db_comercializacao.categoria_produto = producao.categoria_produto
        db_comercializacao.descricao_produto = producao.descricao_produto
        db_comercializacao.quantidade = producao.quantidade
        db_comercializacao.ano = producao.ano
        db.commit()
        db.refresh(db_comercializacao)
    return db_comercializacao

def delete_comercializacao(db: Session, comercializacao_id: int):
    """
    Deleta uma comercialização do banco de dados pelo ID.

    Args:
        db (Session): Sessão de banco de dados.
        comercializacao_id (int): ID da comercialização a ser deletada.

    Returns:
        None
    """
    db_comercializacao = db.query(Comercializacao).filter(Comercializacao.id == comercializacao_id).first()
    if db_comercializacao:
        db.delete(db_comercializacao)
        db.commit()
