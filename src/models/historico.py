from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class HistoricoCarga(Base):
    __tablename__ = "historico_cargas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ano = Column(Integer)
    mes = Column(Integer)
    registros_inseridos = Column(Integer)
    data_execucao = Column(String)

