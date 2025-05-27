from sqlalchemy.orm import Session
from datetime import datetime
from models.historico import HistoricoCarga


def carga_ja_executada(session: Session, ano: int, mes: int) -> bool:
    return session.query(HistoricoCarga).filter_by(ano=ano, mes=mes).first() is not None


def registrar_carga(session: Session, ano: int, mes: int, quantidade: int):
    try:
        registro = HistoricoCarga(
            ano=ano,
            mes=mes,
            registros_inseridos=quantidade,
            data_execucao=datetime.now().isoformat()
        )
        session.add(registro)
        session.commit()
        print(f"Carga registrada no histórico: {ano}-{mes:02d}")
    except Exception as e:
        session.rollback()
        print(f"Erro ao registrar histórico da carga: {e}")
