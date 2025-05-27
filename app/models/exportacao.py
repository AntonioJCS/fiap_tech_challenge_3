from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Exportacao(Base):
    """
    Banco de dados de uva, vinho e derivados.

    Exportação de vinhos e derivados no Rio Grande do Sul, incluindo informações
    sobre o destino, quantidade e valor das exportações anuais.
    """
    __tablename__ = "exportacoes"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único da exportação.")
    categoria = Column(String, index=True, comment="Categoria do produto exportado, por exemplo: vinho, suco de uva.")
    pais_destino = Column(String, index=True, comment="País de destino da exportação.")
    quantidade = Column(Integer, comment="Quantidade exportada em unidades ou litros.")
    valor = Column(Float, comment="Valor monetário da exportação em moeda local.")
    ano = Column(Integer, comment="Ano da exportação.")
