from pydantic import BaseModel, Field

class ComercializacaoBase(BaseModel):
    """
    Banco de dados de uva, vinho e derivados

    Comercialização de vinhos e derivados no Rio Grande do Sul.
    """
    categoria_produto: str = Field(..., description="Categoria do produto, por exemplo: vinho, suco de uva.")
    descricao_produto: str = Field(..., description="Descrição detalhada do produto.")
    quantidade: float = Field(..., description="Quantidade comercializada em litros.")
    ano: int = Field(..., description="Ano da comercialização.")

class ComercializacaoCreate(ComercializacaoBase):
    pass

class Comercializacao(ComercializacaoBase):
    id: int = Field(..., description="Identificador único da comercialização.")

    class Config:
        orm_mode = True
