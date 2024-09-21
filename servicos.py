from sqlmodel import Session, select
from sqlalchemy import update
from banco_dados import obter_engine
from modelos import ProdutoModel
from fastapi import status, HTTPException
from dtos import ProdutoDTO, AtualizarEstoqueDTO

class ProdutoServico:
    def __init__(self):
        self.engine = obter_engine()

    def obter_produto_por_id(self, id: int):
        with Session(self.engine) as sessao:
            consulta = select(ProdutoModel).where(ProdutoModel.id == id)
            return sessao.exec(consulta).one_or_none()
  
    def listar_produtos(self, nome: str | None = None, preco: float | None = None, categoria: str | None = None, franquia: str | None = None):
        with Session(self.engine) as sessao:
            if nome:
                consulta = select(ProdutoModel).where(ProdutoModel.nome == nome)
            elif preco:
                consulta = select(ProdutoModel).where(ProdutoModel.preco == preco)
            elif categoria:
                consulta = select(ProdutoModel).where(ProdutoModel.categoria == categoria)
            elif franquia:
                consulta = select(ProdutoModel).where(ProdutoModel.franquia == franquia)
            else:
                consulta = select(ProdutoModel)
            return sessao.exec(consulta).all()
  
    def salvar_produto(self, produto: ProdutoModel):
        with Session(self.engine) as sessao:
            sessao.add(produto)
            sessao.commit()
            sessao.refresh(produto)
            return produto

    def atualizar_estoque(self, id: int, dados_estoque: AtualizarEstoqueDTO):
        with Session(self.engine) as sessao:
            produto = self.obter_produto_por_id(id)
            if not produto:
                raise ValueError("Produto não encontrado")
            
            nova_quantidade = produto.quantidade_estoque + dados_estoque.quantidade
            if nova_quantidade < 0:
                raise ValueError("Não é possível vender mais do que o estoque disponível")

            produto.quantidade_estoque = nova_quantidade
            sessao.commit()
            sessao.refresh(produto)
            return produto

    def deletar_produto(self, id: int):
        with Session(self.engine) as sessao:
            produto = self.obter_produto_por_id(id)
            if produto.quantidade_estoque > 0:
                raise HTTPException(status_code=400, detail="Não é possível deletar produto com estoque")

            sessao.delete(produto)
            sessao.commit()
            return {"mensagem": "Produto deletado com sucesso"}
