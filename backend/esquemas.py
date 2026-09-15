# Modelo da tabela de agendamentos no banco

from sqlalchemy import Column, Integer, String
from backend.banco_dados import BaseModel


# Definindo a tabela 'agendamentos' que será criada no banco de dados
class AgendamentoModelo(BaseModel):
    __tablename__ = "agendamentos"

    id = Column(Integer, primary_key=True, index=True)
    nome_paciente = Column(String, nullable=False)
    data = Column(String, nullable=False)  # Formato YYYY-MM-DD
    horario = Column(String, nullable=False)  # Formato HH:MM