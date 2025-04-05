from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Cultivo(Base):
    """
    Banco de dados de uva, vinho e derivados.

    Dados de cultivo de uvas no Rio Grande do Sul, incluindo informações sobre
    a categoria de cultivo, tipo de processamento, descrição e quantidade anual.
    """
    __tablename__ = "cultivos"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único do cultivo.")
    categoria_cultivo = Column(String, index=True, comment="Categoria do cultivo, por exemplo: uvas viníferas.")
    descricao_cultivo = Column(String, index=True, comment="Descrição detalhada do tipo de cultivo.")
    tipo_processamento = Column(String, index=True, comment="Tipo de processamento do cultivo, ex: vinificação.")
    quantidade = Column(Float, comment="Quantidade cultivada em toneladas.")
    ano = Column(Integer, comment="Ano do cultivo.")
