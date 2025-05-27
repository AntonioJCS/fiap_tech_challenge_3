import pandas as pd
from storage.db import SessionLocal
from storage.models import VendaManipulado
from ml.modelo_lstm import preprocessar_dados, criar_sequencias, construir_modelo, treinar_modelo

# Cria sessão
session = SessionLocal()

try:
    # Consulta dados do banco
    query = session.query(VendaManipulado.ano_venda, VendaManipulado.mes_venda, VendaManipulado.qtd_unidade_farmacotecnica)
    df = pd.read_sql(query.statement, session.bind)

    # Prepara os dados
    df, df_scaled, scaler = preprocessar_dados(df, target_col="QTD_UNIDADE_FARMACOTECNICA")
    X, y = criar_sequencias(df_scaled, seq_length=3)

    # Divide treino/teste
    test_size = int(len(X) * 0.2)
    X_train, X_test = X[:-test_size], X[-test_size:]
    y_train, y_test = y[:-test_size], y[-test_size:]

    # Treina modelo
    model = construir_modelo(seq_length=3)
    treinar_modelo(model, X_train, y_train, X_test, y_test)

finally:
    session.close()
