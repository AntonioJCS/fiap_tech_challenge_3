from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String

Base = declarative_base()

class VendaManipulado(Base):
    __tablename__ = "vendas_manipulados"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ano_venda = Column(Integer)
    mes_venda = Column(Integer)
    uf_venda = Column(String)
    municipio_venda = Column(String)
    dcb = Column(String)
    principio_ativo = Column(String)
    qtd_ativo_por_unid_farmacotec = Column(Float)
    unidade_medida_principio_ativo = Column(String)
    qtd_unidade_farmacotecnica = Column(Integer)
    tipo_unidade_farmacotecnica = Column(String)
    conselho_prescritor = Column(String)
    uf_conselho_prescritor = Column(String)
    tipo_receituario = Column(String)
    cid10 = Column(String)
    sexo = Column(String)
    idade = Column(Integer)
    unidade_idade = Column(String)