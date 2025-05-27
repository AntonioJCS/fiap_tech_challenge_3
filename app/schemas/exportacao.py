from pydantic import BaseModel, Field

class ExportacaoBase(BaseModel):
    """
    Representa a exportação de derivados de uva, contendo informações sobre o destino, quantidade, valor e ano da exportação.
    """
    categoria: str = Field(..., description="Categoria do derivado de uva exportado (ex: vinho, suco, etc.)")
    pais_destino: str = Field(..., description="País para onde o derivado de uva foi exportado")
    quantidade: int = Field(..., description="Quantidade exportada, em unidades ou litros, dependendo da categoria")
    valor: float = Field(..., description="Valor total da exportação em dólares americanos")
    ano: int = Field(..., description="Ano em que a exportação foi realizada")

class ExportacaoCreate(ExportacaoBase):
    """
    Modelo para criação de uma nova exportação de derivados de uva.
    """
    pass

class Exportacao(ExportacaoBase):
    """
    Modelo que representa uma exportação já registrada, incluindo o ID da exportação.
    """
    id: int = Field(..., description="ID único da exportação registrada")

    class Config:
        orm_mode = True
