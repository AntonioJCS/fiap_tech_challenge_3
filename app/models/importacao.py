from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Importacao(Base):
    """
    Banco de dados de uva, vinho e derivados.

    Importação de vinhos e derivados para o Rio Grande do Sul, contendo informações
    sobre o país de origem, quantidade e valor das importações anuais.
    """
    __tablename__ = "importacoes"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único da importação.")
    categoria = Column(String, index=True, comment="Categoria do produto importado, por exemplo: vinho, suco de uva.")
    pais_origem = Column(String, index=True, comment="País de origem da importação.")
    quantidade = Column(Integer, comment="Quantidade importada em unidades ou litros.")
    valor = Column(Float, comment="Valor monetário da importação em moeda local.")
    ano = Column(Integer, comment="Ano da importação.")
