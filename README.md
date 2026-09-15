# 🩺 Sistema de Agendamento Inteligente para Clínica

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57.svg)

Aplicação Full Stack desenvolvida para automatizar e otimizar o fluxo de agendamento de consultas médicas de uma clínica. O sistema valida regras de negócio em tempo real, impedindo marcações fora do horário de expediente, em finais de semana, feriados nacionais ou em horários já ocupados.

---

## 🎯 Funcionalidades

- *Consulta de Horários Disponíveis:* Exibe a grade de horários livres (08:00 às 18:00) para uma data selecionada.
- *Validação de Dias Úteis:* Bloqueia automaticamente agendamentos aos sábados e domingos.
- *Integração com API Externa:* Consome a API [Nager.Date](https://date.nager.at/) para identificar feriados nacionais e impedir marcações nessas datas.
- *Persistência de Dados:* Salva e gerencia os agendamentos via banco de dados SQLite.
- *Prevenção de Conflitos:* Evita agendamentos duplicados no mesmo dia e horário.

---

## 🛠️ Tecnologias Utilizadas

### Backend
- *Python 3*
- *FastAPI* (Framework web de alta performance)
- *SQLAlchemy* (ORM para manipulação do banco de dados)
- *SQLite* (Banco de dados relacional leve)
- *HTTPX* (Cliente HTTP assíncrono para consumo da API externa)
- *Pydantic* (Validação e tipagem de dados)

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.10 ou superior instalado.
- Git instalado.

### Passo a Passo

1. *Clone o repositório:*
   ```bash
   git clone [https://github.com/seu-usuario/agendamento-clinica-api.git](https://github.com/seu-usuario/agendamento-clinica-api.git)
   cd agendamento-clinica-api
