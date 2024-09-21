from sqlmodel import Field, SQLModel

class ProdutoModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    nome: str
    descricao: str
    preco: float
    quantidade_estoque: int
    categoria: str
    franquia: str | None
