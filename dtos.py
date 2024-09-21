from pydantic import BaseModel

class ProdutoDTO(BaseModel):
    nome: str
    descricao: str 
    preco: float
    quantidade_estoque: int
    categoria: str
    franquia: str 

class AtualizarEstoqueDTO(BaseModel):
    quantidade: int
