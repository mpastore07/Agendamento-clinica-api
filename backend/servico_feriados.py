# Integração com a API pública de feriados

import httpx

# URL oficial exigida no teste técnico
URL_API_FERIADOS = "https://date.nager.at/api/v3/PublicHolidays/2026/BR"


async def verificar_se_e_feriado(data_str: str) -> bool:
    """Consulta a API externa de feriados para validar se a data enviada é um feriado no Brasil no ano de 2026."""
    async with httpx.AsyncClient() as cliente:
        try:
            resposta = await cliente.get(URL_API_FERIADOS)
            if resposta.status_code == 200:
                feriados = resposta.json()
                # Verifica se a data informada consta na lista de feriados retornada
                for feriado in feriados:
                    if feriado.get("date") == data_str:
                        return True
            return False
        except Exception as e:
            print(f"Erro ao consultar a API de feriados: {e}")
            return False