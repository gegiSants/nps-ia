"""Classifica um comentário de NPS e sugere uma resposta, com saída JSON validada.

Usa um LLM via API compatível com OpenAI (Groq por padrão — chave grátis em
https://console.groq.com). Trocar de provedor é só mudar base_url/modelo.
"""
from __future__ import annotations

import json
import os

MODELO = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
BASE_URL = os.getenv("LLM_BASE_URL", "https://api.groq.com/openai/v1")

TEMAS = ["suporte", "produto", "preço", "prazo", "usabilidade", "atendimento_comercial", "outro"]
SENTIMENTOS = ["positivo", "neutro", "negativo"]

# O system prompt é o coração do projeto: papel, tarefa, enums fechados, saída
# só-JSON e regras (guardrails). Mantido aqui como fonte única; prompt.md explica.
SYSTEM_PROMPT = f"""Você é um analista de Customer Success. Sua tarefa é classificar um \
comentário de pesquisa NPS e sugerir uma resposta ao cliente.

Entrada: a nota (0 a 10) e o comentário do cliente.

Devolva SOMENTE um objeto JSON, sem texto antes ou depois, com exatamente estes campos:
- "tema": um de {TEMAS} — o assunto principal do comentário.
- "sentimento": um de {SENTIMENTOS} — o tom do comentário (pode divergir da nota).
- "motivo": frase curta (até 15 palavras) com a razão central, nas palavras do cliente.
- "resposta_sugerida": resposta curta (2 a 4 frases), em português do Brasil, tom cordial de CS,
  que reconhece o ponto e indica um próximo passo. Promotor: agradeça. Detrator: peça desculpas e ofereça contato.

Regras:
- Baseie-se apenas no que o comentário diz. Não invente fatos, números ou nomes.
- Comentário vazio ou genérico: infira o sentimento pela nota e use "tema": "outro".
- Escreva tudo em português do Brasil."""

# Few-shot: ancora o formato e o estilo da resposta (prompt engineering, não código).
FEWSHOTS = [
    (
        'Nota: 10\nComentário: "O suporte resolveu meu problema de certificado em minutos."',
        json.dumps({
            "tema": "suporte", "sentimento": "positivo",
            "motivo": "suporte rápido na emissão do certificado",
            "resposta_sugerida": "Que bom saber que o suporte te atendeu rápido! Obrigada pelo retorno — seguimos à disposição sempre que precisar.",
        }, ensure_ascii=False),
    ),
    (
        'Nota: 3\nComentário: "O sistema cai toda semana e atrapalha meu fechamento."',
        json.dumps({
            "tema": "produto", "sentimento": "negativo",
            "motivo": "instabilidade do sistema no fechamento",
            "resposta_sugerida": "Sentimos muito pela instabilidade que atrapalhou seu fechamento. Já encaminhamos o caso ao time técnico e queremos entender melhor — podemos te chamar para uma conversa?",
        }, ensure_ascii=False),
    ),
]


def categoria_por_nota(nota: int) -> str:
    """Regra do NPS (não é trabalho do LLM): 0-6 detrator, 7-8 neutro, 9-10 promotor."""
    if nota >= 9:
        return "promotor"
    if nota >= 7:
        return "neutro"
    return "detrator"


def _entrada(nota: int, comentario: str) -> str:
    return f'Nota: {nota}\nComentário: "{(comentario or "").strip()}"'


def normalizar(nota: int, dados: dict) -> dict:
    """Guardrail: garante enums válidos e aplica a categoria pela nota (determinística)."""
    tema = dados.get("tema", "outro")
    if tema not in TEMAS:
        tema = "outro"
    sentimento = dados.get("sentimento", "neutro")
    if sentimento not in SENTIMENTOS:
        sentimento = "neutro"
    return {
        "categoria": categoria_por_nota(nota),
        "tema": tema,
        "sentimento": sentimento,
        "motivo": str(dados.get("motivo", "")).strip(),
        "resposta_sugerida": str(dados.get("resposta_sugerida", "")).strip(),
    }


def _cliente():
    from openai import OpenAI  # import preguiçoso: o self-check roda sem o pacote instalado

    chave = os.getenv("GROQ_API_KEY")
    if not chave:
        raise SystemExit("Defina GROQ_API_KEY (veja .env.example). Chave grátis: https://console.groq.com")
    return OpenAI(api_key=chave, base_url=BASE_URL)


def classificar(nota: int, comentario: str, cliente=None) -> dict:
    cliente = cliente or _cliente()
    mensagens: list[dict] = [{"role": "system", "content": SYSTEM_PROMPT}]
    for usuario, resposta in FEWSHOTS:
        mensagens.append({"role": "user", "content": usuario})
        mensagens.append({"role": "assistant", "content": resposta})
    mensagens.append({"role": "user", "content": _entrada(nota, comentario)})
    resp = cliente.chat.completions.create(
        model=MODELO,
        messages=mensagens,
        temperature=0,  # classificação precisa ser estável
        response_format={"type": "json_object"},
    )
    dados = json.loads(resp.choices[0].message.content)
    return normalizar(nota, dados)


if __name__ == "__main__":  # teste rápido manual: python src/classificar.py
    from pprint import pprint
    pprint(classificar(2, "Demora demais pra responder os chamados de suporte."))
