from ingestion.scraping import scraper
from processing.limpeza import limpar_dados
from crud.manipulados import salvar_dataframe_com_orm
from crud.historico import carga_ja_executada, registrar_carga
from storage.db import criar_tabelas, SessionLocal
import time

def executar_pipeline(ano: int, mes: int):
    print(f"\nIniciando pipeline para {ano}-{mes:02d}...")

    # Cria sessão do banco
    session = SessionLocal()

    try:
        # Verifica se a carga já foi realizada
        if carga_ja_executada(session, ano, mes):
            print(f"Carga já realizada anteriormente para {ano}-{mes:02d}. Pulando.")
            return

        # Etapa 1 – Scraping
        df = scraper(ano, mes, cert_path="./certs/ca_bundle.pem")
        if df.empty:
            print("Nenhum dado retornado para esse mês.")
            return

        # Etapa 2 – Limpeza
        df_limpo = limpar_dados(df)

        # Etapa 3 – Inserção no banco e registro do histórico
        criar_tabelas()
        salvar_dataframe_com_orm(session, df_limpo)
        registrar_carga(session, ano, mes, len(df_limpo))

        print(f"Pipeline concluído com sucesso para {ano}-{mes:02d}.")

    finally:
        session.close()

if __name__ == "__main__":
    criar_tabelas()

    for ano in range(2014, 2023):
        for mes in range(1, 13):
            executar_pipeline(ano, mes)
            time.sleep(1)
