from fastapi import FastAPI
from controladores import roteador_produtos
from banco_dados import inicializar_banco, obter_engine

# Criação do objeto FastAPI
app = FastAPI()

# Inicialização do banco de dados
inicializar_banco(obter_engine())

# Registro das rotas com o prefixo /api
app.include_router(roteador_produtos, prefix="/api")
