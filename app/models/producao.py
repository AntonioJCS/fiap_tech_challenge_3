from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Producao(Base):
    """
    Banco de dados de uva, vinho e derivados.

    Dados de produção de vinhos e derivados no Rio Grande do Sul, incluindo informações sobre
    a categoria do produto, descrição e quantidade produzida anualmente.
    """
    __tablename__ = "producoes"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único da produção.")
    categoria_produto = Column(String, index=True, comment="Categoria do produto, por exemplo: vinho, suco de uva.")
    descricao_produto = Column(String, index=True, comment="Descrição detalhada do produto.")
    quantidade = Column(Float, comment="Quantidade produzida em litros ou unidades.")
    ano = Column(Integer, comment="Ano da produção.")
