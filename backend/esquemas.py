# Validadores de dados (Pydantic)

from pydantic import BaseModel, Field


# Esquema para receber os dados de criação do agendamento (Input)
class AgendamentoCriar(BaseModel):
    nome_paciente: str = Field(..., description="Nome do paciente")
    data: str = Field(
        ..., description="Data da consulta no formato YYYY-MM-DD"
    )
    horario: str = Field(
        ..., description="Horário da consulta no formato HH:MM"
    )


# Esquema para retorno completo dos dados salvos (Output)
class AgendamentoResposta(AgendamentoCriar):
    id: int

    class Config:
        from_attributes = True