from pydantic import BaseModel, Field

class CultivoBase(BaseModel):
    """
    Quantidade de uvas processadas no Rio Grande do Sul.
    """
    categoria_cultivo: str = Field(..., description="Categoria do cultivo, por exemplo: uva de mesa, uva para vinho.")
    tipo_processamento: str = Field(..., description="Tipo de processamento, como prensagem ou fermentação.")
    descricao_cultivo: str = Field(..., description="Descrição detalhada do cultivo e sua aplicação.")
    quantidade: float = Field(..., description="Quantidade processada em toneladas.")
    ano: int = Field(..., description="Ano do cultivo e processamento.")

class CultivoCreate(CultivoBase):
    pass

class Cultivo(CultivoBase):
    id: int = Field(..., description="Identificador único do cultivo.")

    class Config:
        orm_mode = True
