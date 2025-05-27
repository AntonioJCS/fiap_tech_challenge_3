"""
Responsável por armazenar os modelos de domínio da aplicação (ORM), representando as entidades do banco de dados.
Segue a convenção comum em aplicações FastAPI, separando modelos de dados (ORM) dos schemas da API (Pydantic).
"""

from sqlalchemy.ext.declarative import declarative_base
from .manipulados import VendaManipulado
from .historico import HistoricoCarga

Base = declarative_base()

__all__ = ["Base", "VendaManipulado", "HistoricoCarga"]

