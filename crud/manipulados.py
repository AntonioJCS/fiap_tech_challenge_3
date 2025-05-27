from sqlalchemy.orm import Session
import pandas as pd
from storage.models import VendaManipulado


def salvar_dataframe_com_orm(session: Session, df: pd.DataFrame):
    """Insere os dados do DataFrame usando ORM (VendaManipulado)."""
    try:
        registros = []
        for row in df.to_dict(orient="records"):
            safe_row = {
                k: (None if pd.isna(v) or isinstance(v, pd._libs.missing.NAType) else v)
                for k, v in row.items()
            }
            registros.append(VendaManipulado(**safe_row))

        session.bulk_save_objects(registros)
        session.commit()
        print(f"{len(registros)} registros salvos com sucesso via ORM.")
    except Exception as e:
        session.rollback()
        print(f"Erro ao salvar dados no banco via ORM: {e}")
