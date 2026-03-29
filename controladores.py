from fastapi import APIRouter, status, HTTPException, File, UploadFile, Form
from modelos import ProdutoModel
from servicos import ProdutoServico
import os
import uuid

# Objeto de rotas
roteador_produtos = APIRouter()

# Serviço de produtos
produto_servico = ProdutoServico()

@roteador_produtos.post("", status_code=status.HTTP_201_CREATED)
async def adicionar_produto(
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade_estoque: int = Form(...),
    categoria: str = Form(...),
    imagem: UploadFile = File(...),
    destaque: bool = Form(False) 
):
    # Lógica de salvar imagem
    extensao = os.path.splitext(imagem.filename)[1]
    nome_arquivo = f"{uuid.uuid4()}{extensao}"
    caminho = os.path.join("static/uploads", nome_arquivo)
    
    with open(caminho, "wb") as buffer:
        buffer.write(await imagem.read())

    # Criar modelo para o banco
    novo_produto = ProdutoModel(
        nome=nome,
        descricao=descricao,
        preco=preco,
        quantidade_estoque=quantidade_estoque,
        categoria=categoria,
        imagem_url=f"/static/uploads/{nome_arquivo}",
        destaque=destaque
    )
    return produto_servico.salvar_produto(novo_produto)

@roteador_produtos.put("/{id}")
async def editar_produto(
    id: int,
    nome: str = Form(...),
    descricao: str = Form(...),
    preco: float = Form(...),
    quantidade_estoque: int = Form(...),
    categoria: str = Form(...),
    imagem: UploadFile = File(None), 
    destaque: bool = Form(False)
):
    # 1. Preparamos os dados básicos (Incluindo o destaque!)
    dados_atualizados = {
        "nome": nome,
        "descricao": descricao,
        "preco": preco,
        "quantidade_estoque": quantidade_estoque,
        "categoria": categoria,
        "destaque": destaque 
    }

    # 2. Lógica para nova imagem
    if imagem and imagem.filename:
        extensao = os.path.splitext(imagem.filename)[1]
        nome_arquivo = f"{uuid.uuid4()}{extensao}"
        caminho = os.path.join("static/uploads", nome_arquivo)
        
        with open(caminho, "wb") as buffer:
            buffer.write(await imagem.read())
        
        dados_atualizados["imagem_url"] = f"/static/uploads/{nome_arquivo}"

    # 3. Chama o serviço
    produto = produto_servico.atualizar_produto(id, dados_atualizados)
    
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    return produto

@roteador_produtos.get("/{id}")
def obter_produto_por_id(id: int):
    return produto_servico.obter_produto_por_id(id=id)

@roteador_produtos.get("/")
def listar_produtos(nome: str | None = None, preco: float | None = None, categoria: str | None = None):
    return produto_servico.listar_produtos(nome=nome, preco=preco, categoria=categoria)

@roteador_produtos.delete("/{id}")
def excluir_produto(id: int):
    sucesso = produto_servico.excluir_produto(id=id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return {"mensagem": "Produto removido com sucesso"}