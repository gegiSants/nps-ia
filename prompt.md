# O prompt (e por que ele é assim)

O coração do projeto é o *system prompt* em [`src/classificar.py`](src/classificar.py).
Cada decisão abaixo é uma técnica de prompt engineering aplicada de propósito.

## Técnicas usadas

| Técnica | O que foi feito | Por quê |
|---|---|---|
| **Papel (role)** | "Você é um analista de Customer Success." | Dá contexto e tom às respostas sugeridas. |
| **Tarefa explícita** | Classificar comentário + sugerir resposta, a partir de nota e texto. | O modelo sabe exatamente o que entregar. |
| **Saída estruturada** | Pede **só JSON** com campos fixos + `response_format=json_object`. | Resposta vira dado, não texto solto — dá pra automatizar. |
| **Enums fechados** | `tema` e `sentimento` só aceitam valores de uma lista. | Evita rótulos inventados; deixa a classificação mensurável. |
| **Few-shot** | 2 exemplos (promotor e detrator) antes da pergunta. | Ancora o formato e o estilo da resposta. |
| **Guardrails** | Regras "não invente", "vazio → outro", "pt-BR". | Reduz alucinação e saída fora do escopo. |
| **Temperature 0** | Chamada determinística. | Classificação precisa ser estável e repetível. |
| **Separação de responsabilidades** | A `categoria` (promotor/neutro/detrator) é calculada pela **nota**, não pelo LLM. | O LLM só faz o que é difícil (ler o texto); a regra do NPS é código. |
| **Normalização pós-resposta** | `normalizar()` valida enums e aplica a regra. | O sistema não confia cegamente na saída do modelo. |

## Formato de saída

```json
{
  "tema": "suporte | produto | preço | prazo | usabilidade | atendimento_comercial | outro",
  "sentimento": "positivo | neutro | negativo",
  "motivo": "frase curta com a razão central",
  "resposta_sugerida": "2 a 4 frases, tom de CS, em pt-BR"
}
```

A **avaliação** ([`src/avaliar.py`](src/avaliar.py)) mede a acurácia de `tema` e `sentimento`
contra um gabarito rotulado à mão ([`data/teste.json`](data/teste.json)) — é assim que se
compara uma versão do prompt com a próxima, em vez de "achismo".
