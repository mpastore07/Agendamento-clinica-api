# Inicialização do servidor FastAPI.

from datetime import datetime
from typing import List
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.banco_dados import BaseModel, motor_banco, obter_banco
from backend.esquemas import AgendamentoCriar, AgendamentoResposta
from backend.modelos import AgendamentoModelo
from backend.servico_feriados import verificar_se_e_feriado

# Inicializa as tabelas no SQLite caso não existam
BaseModel.metadata.create_all(bind=motor_banco)

app = FastAPI(
    title="Sistema de Agendamento da Clínica",
    description="API REST para gerenciamento de horários e agendamentos.",
)

# Permite chamadas do Frontend via browser (evita erro de CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/available",
    response_model=List[str],
    summary="Listar horários disponíveis",
)
async def listar_horarios_disponiveis(
    date: str, banco: Session = Depends(obter_banco)
):
    """Verifica a data escolhida, consulta feriados, finais de semana e os horários já ocupados."""
    # 1. Validação do formato da data
    try:
        data_objeto = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD."
        )

    # 2. Regra de Negócio: Bloquear finais de semana (5 = Sábado, 6 = Domingo)
    if data_objeto.weekday() in [5, 6]:
        return []

    # 3. Regra de Negócio: Consumo da API pública e bloqueio em feriados
    e_feriado = await verificar_se_e_feriado(date)
    if e_feriado:
        return []

    # 4. Grade fixa de funcionamento: 08:00 às 18:00 (consultas de 1 hora de duração)
    horarios_totais = [
        "08:00",
        "09:00",
        "10:00",
        "11:00",
        "12:00",
        "13:00",
        "14:00",
        "15:00",
        "16:00",
        "17:00",
    ]

    # 5. Busca agendamentos já gravados no banco para esta data
    agendamentos_existentes = (
        banco.query(AgendamentoModelo)
        .filter(AgendamentoModelo.data == date)
        .all()
    )

    horarios_ocupados = [a.horario for a in agendamentos_existentes]

    # 6. Filtra apenas os horários livres
    horarios_livres = [
        h for h in horarios_totais if h not in horarios_ocupados
    ]

    return horarios_livres


@app.post(
    "/appointments",
    response_model=AgendamentoResposta,
    status_code=status.HTTP_201_CREATED,
    summary="Criar novo agendamento",
)
async def criar_agendamento(
    dados: AgendamentoCriar, banco: Session = Depends(obter_banco)
):
    """Valida novamente as regras de negócio e grava o agendamento no banco de dados."""
    # Validação do formato da data
    try:
        data_objeto = datetime.strptime(dados.data, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400, detail="Formato de data inválido. Use YYYY-MM-DD."
        )

    # Validação: Final de semana
    if data_objeto.weekday() in [5, 6]:
        raise HTTPException(
            status_code=400,
            detail="Não é possível agendar em finais de semana.",
        )

    # Validação: Feriado
    if await verificar_se_e_feriado(dados.data):
        raise HTTPException(
            status_code=400, detail="Não é possível agendar em feriados."
        )

    # Validação: Horário já ocupado
    conflito = (
        banco.query(AgendamentoModelo)
        .filter(
            AgendamentoModelo.data == dados.data,
            AgendamentoModelo.horario == dados.horario,
        )
        .first()
    )

    if conflito:
        raise HTTPException(
            status_code=400, detail="Este horário já está ocupado."
        )

    # Gravação no banco de dados
    novo_agendamento = AgendamentoModelo(
        nome_paciente=dados.nome_paciente,
        data=dados.data,
        horario=dados.horario,
    )

    banco.add(novo_agendamento)
    banco.commit()
    banco.refresh(novo_agendamento)

    return novo_agendamento


@app.get(
    "/appointments",
    response_model=List[AgendamentoResposta],
    summary="Listar todos os agendamentos",
)
def listar_todos_agendamentos(banco: Session = Depends(obter_banco)):
    """Retorna todos os agendamentos cadastrados."""
    return banco.query(AgendamentoModelo).all()