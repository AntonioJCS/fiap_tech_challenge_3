from pydantic import BaseModel, Field

class ProducaoBase(BaseModel):
    """
    Produção de vinhos, sucos e derivados do Rio Grande do Sul.
    """
    categoria_produto: str = Field(..., description="Categoria do produto, por exemplo: vinho, suco de uva.")
    descricao_produto: str = Field(..., description="Descrição detalhada do produto.")
    quantidade: float = Field(..., description="Quantidade produzida em litros.")
    ano: int = Field(..., description="Ano da produção.")

class ProducaoCreate(ProducaoBase):
    pass

class Producao(ProducaoBase):
    id: int = Field(..., description="Identificador único da produção.")

    class Config:
        orm_mode = True
