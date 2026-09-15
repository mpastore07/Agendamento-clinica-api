// Script para a página de agendamento

const URL_BASE = "http://127.0.0.1:8000";

// Seleção de elementos da página
const campoData = document.getElementById("campo-data");
const btnBuscar = document.getElementById("btn-buscar");
const secaoHorarios = document.getElementById("secao-horarios");
const gradeHorarios = document.getElementById("grade-horarios");
const secaoConfirmacao = document.getElementById("secao-confirmacao");
const campoNome = document.getElementById("campo-nome");
const btnConfirmar = document.getElementById("btn-confirmar");
const mensagemStatus = document.getElementById("mensagem-status");
const listaAgendamentos = document.getElementById("lista-agendamentos");

let horarioSelecionado = null;

// Carrega a lista de agendamentos salvos ao abrir a página
document.addEventListener("DOMContentLoaded", carregarAgendamentos);

// 1. Buscar Horários Disponíveis
btnBuscar.addEventListener("click", async () => {
    const data = campoData.value;
    if (!data) {
        exibirMensagem("Por favor, selecione uma data.", "red");
        return;
    }

    exibirMensagem("Consultando disponibilidade...", "black");
    secaoHorarios.classList.add("escondido");
    secaoConfirmacao.classList.add("escondido");
    horarioSelecionado = null;

    try {
        const resposta = await fetch(`${URL_BASE}/available?date=${data}`);
        const horarios = await resposta.json();

        if (horarios.length === 0) {
            exibirMensagem("Sem horários disponíveis para esta data (Final de semana, Feriado ou Agenda lotada).", "orange");
            return;
        }

        exibirMensagem("", "black");
        montarGradeDeHorarios(horarios);
        secaoHorarios.classList.remove("escondido");

    } catch (erro) {
        exibirMensagem("Erro ao conectar com o servidor.", "red");
    }
});

// Renderiza os botões de horário na tela
function montarGradeDeHorarios(horarios) {
    gradeHorarios.innerHTML = "";
    horarios.forEach(horario => {
        const botao = document.createElement("button");
        botao.classList.add("botao-horario");
        botao.textContent = horario;
        botao.addEventListener("click", () => {
            document.querySelectorAll(".botao-horario").forEach(b => b.classList.remove("selecionado"));
            botao.classList.add("selecionado");
            horarioSelecionado = horario;
            secaoConfirmacao.classList.remove("escondido");
        });
        gradeHorarios.appendChild(botao);
    });
}

// 2. Salvar Agendamento
btnConfirmar.addEventListener("click", async () => {
    const nome = campoNome.value.trim();
    const data = campoData.value;

    if (!nome || !horarioSelecionado || !data) {
        exibirMensagem("Preencha todos os campos para agendar.", "red");
        return;
    }

    const dadosEnvio = {
        nome_paciente: nome,
        data: data,
        horario: horarioSelecionado
    };

    try {
        const resposta = await fetch(`${URL_BASE}/appointments`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dadosEnvio)
        });

        if (resposta.ok) {
            exibirMensagem("Agendamento realizado com sucesso!", "green");
            campoNome.value = "";
            secaoHorarios.classList.add("escondido");
            secaoConfirmacao.classList.add("escondido");
            carregarAgendamentos();
        } else {
            const erro = await resposta.json();
            exibirMensagem(`Erro: ${erro.detail}`, "red");
        }
    } catch (erro) {
        exibirMensagem("Erro ao salvar agendamento.", "red");
    }
});

// 3. Listar Agendamentos
async function carregarAgendamentos() {
    try {
        const resposta = await fetch(`${URL_BASE}/appointments`);
        const agendamentos = await resposta.json();

        listaAgendamentos.innerHTML = "";
        agendamentos.forEach(item => {
            const li = document.createElement("li");
            li.textContent = `${item.data} às ${item.horario} - Paciente: ${item.nome_paciente}`;
            listaAgendamentos.appendChild(li);
        });
    } catch (erro) {
        console.error("Erro ao carregar lista de agendamentos:", erro);
    }
}

function exibirMensagem(texto, cor) {
    mensagemStatus.textContent = texto;
    mensagemStatus.style.color = cor;
}