from sqlmodel import SQLModel, create_engine

URL_BANCO_DADOS = 'sqlite:///produtos.db'

def obter_engine():
    return create_engine(URL_BANCO_DADOS)

def inicializar_banco(engine):
    SQLModel.metadata.create_all(engine)
