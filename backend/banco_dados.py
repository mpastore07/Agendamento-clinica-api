# Configuração do banco de dados usando SQLite/SQLAlchemy

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Define o caminho do banco de dados SQLite na pasta do backend
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
CAMINHO_BANCO = os.path.join(DIRETORIO_ATUAL, "clinica.db")
URL_BANCO_DADOS = f"sqlite:///{CAMINHO_BANCO}"

# Cria o motor do banco de dados SQLite
motor_banco = create_engine(
    URL_BANCO_DADOS, connect_args={"check_same_thread": False}
)

# Cria a fábrica de sessões para manipular o banco
SessaoLocal = sessionmaker(autocommit=False, autoflush=False, bind=motor_banco)

# Classe base para a criação dos modelos relacionais
BaseModel = declarative_base()


# Função utilitária para obter a conexão com o banco a cada requisição
def obter_banco():
    banco = SessaoLocal()
    try:
        yield banco
    finally:
        banco.close()