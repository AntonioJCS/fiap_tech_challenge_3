from pydantic import BaseModel, Field

class ImportacaoBase(BaseModel):
    """
    Importação de derivados de uva.
    """
    categoria: str = Field(..., description="Categoria do produto importado, por exemplo: suco de uva, vinho.")
    pais_origem: str = Field(..., description="País de origem do produto importado.")
    quantidade: int = Field(..., description="Quantidade do produto importado em unidades.")
    valor: float = Field(..., description="Valor total da importação em moeda local.")
    ano: int = Field(..., description="Ano da importação.")

class ImportacaoCreate(ImportacaoBase):
    pass

class Importacao(ImportacaoBase):
    id: int = Field(..., description="Identificador único da importação.")

    class Config:
        orm_mode = True
