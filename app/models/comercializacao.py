from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Comercializacao(Base):
    """
    Banco de dados de uva, vinho e derivados.

    Comercialização de vinhos e derivados no Rio Grande do Sul.
    """
    __tablename__ = "comercializacoes"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único da comercialização.")
    categoria_produto = Column(String, index=True, comment="Categoria do produto, por exemplo: vinho, suco de uva.")
    descricao_produto = Column(String, index=True, comment="Descrição detalhada do produto.")
    quantidade = Column(Float, comment="Quantidade comercializada em litros.")
    ano = Column(Integer, comment="Ano da comercialização.")
