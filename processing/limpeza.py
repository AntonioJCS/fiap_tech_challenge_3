import pandas as pd

def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """
    Limpa e padroniza os dados brutos extraídos do CSV da ANVISA
    para o formato compatível com o modelo ORM VendaManipulado.

    Args:
        df (pd.DataFrame): Dados brutos lidos do CSV.

    Returns:
        pd.DataFrame: Dados limpos e padronizados.
    """

    # Renomear colunas para snake_case
    df = df.rename(columns={
        "ANO_VENDA": "ano_venda",
        "MES_VENDA": "mes_venda",
        "UF_VENDA": "uf_venda",
        "MUNICIPIO_VENDA": "municipio_venda",
        "DCB": "dcb",
        "PRINCIPIO_ATIVO": "principio_ativo",
        "QTD_ATIVO_POR_UNID_FARMACOTEC": "qtd_ativo_por_unid_farmacotec",
        "UNIDADE_MEDIDA_PRINCIPIO_ATIVO": "unidade_medida_principio_ativo",
        "QTD_UNIDADE_FARMACOTECNICA": "qtd_unidade_farmacotecnica",
        "TIPO_UNIDADE_FARMACOTECNICA": "tipo_unidade_farmacotecnica",
        "CONSELHO_PRESCRITOR": "conselho_prescritor",
        "UF_CONSELHO_PRESCRITOR": "uf_conselho_prescritor",
        "TIPO_RECEITUARIO": "tipo_receituario",
        "CID10": "cid10",
        "SEXO": "sexo",
        "IDADE": "idade",
        "UNIDADE_IDADE": "unidade_idade"
    })

    # Tratamento de tipos numéricos
    df["ano_venda"] = pd.to_numeric(df["ano_venda"], errors="coerce").astype("Int64")
    df["mes_venda"] = pd.to_numeric(df["mes_venda"], errors="coerce").astype("Int64")
    df["qtd_ativo_por_unid_farmacotec"] = (
        df["qtd_ativo_por_unid_farmacotec"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )
    df["qtd_unidade_farmacotecnica"] = (
        df["qtd_unidade_farmacotecnica"]
        .astype(str)
        .str.replace(",", ".")
        .astype(float)
    )
    df["idade"] = pd.to_numeric(df["idade"], errors="coerce").astype("Int64")
    df["sexo"] = pd.to_numeric(df["sexo"], errors="coerce").astype("Int64")
    df["unidade_idade"] = pd.to_numeric(df["unidade_idade"], errors="coerce").astype("Int64")

    # Limpa espaços em branco
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].str.strip()

    return df
