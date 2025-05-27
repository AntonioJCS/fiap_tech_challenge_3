import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Caminho para o banco de dados SQLite
DB_PATH = os.path.join(os.path.dirname(__file__), "anvisa.db")

# Cria o engine e a sessão do SQLAlchemy
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(bind=engine)

def criar_tabelas():
    """Cria as tabelas no banco se ainda não existirem."""
    Base.metadata.create_all(engine)