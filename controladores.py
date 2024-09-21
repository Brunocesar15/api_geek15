from fastapi import APIRouter, status, HTTPException
from modelos import ProdutoModel
from servicos import ProdutoServico
from dtos import ProdutoDTO, AtualizarEstoqueDTO

# Objeto de rotas
roteador_produtos = APIRouter()

# Serviço de produtos
produto_servico = ProdutoServico()

@roteador_produtos.get("/{id}")
def obter_produto_por_id(id: int):
    return produto_servico.obter_produto_por_id(id=id)

@roteador_produtos.get("/")
def listar_produtos(nome: str | None = None, preco: float | None = None, categoria: str | None = None, franquia: str | None = None):
    return produto_servico.listar_produtos(nome=nome, preco=preco, categoria=categoria, franquia=franquia)

@roteador_produtos.post('/', 
    response_model=ProdutoModel, 
    status_code=status.HTTP_201_CREATED)
def adicionar_produto(produto: ProdutoDTO):
    novo_produto = ProdutoModel(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        quantidade_estoque=produto.quantidade_estoque,
        categoria=produto.categoria,
        franquia=produto.franquia
    )
    return produto_servico.salvar_produto(novo_produto)

@roteador_produtos.put('/{id}')
def atualizar_produto(id: int, produto: ProdutoDTO):
    produto_atualizado = ProdutoModel(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        quantidade_estoque=produto.quantidade_estoque,
        categoria=produto.categoria,
        franquia=produto.franquia
    )
    return produto_servico.atualizar_produto(produto=produto_atualizado, id=id)

@roteador_produtos.put("/estoque/{id}")
def atualizar_estoque(id: int, dados: AtualizarEstoqueDTO):
    try:
        produto_atualizado = produto_servico.atualizar_estoque(id=id, dados_estoque=dados)
        return produto_atualizado
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@roteador_produtos.delete('/{id}')
def deletar_produto(id: int):
    return produto_servico.deletar_produto(id=id)
