# nps-ia — classificação e resposta de NPS com LLM

Projeto prático de **prompt engineering**: lê um comentário de pesquisa NPS e, com um prompt
bem desenhado, devolve **dados estruturados** (tema, sentimento, motivo) e uma **resposta
sugerida** para o time de Customer Success — com uma **avaliação de acurácia** para comparar
versões do prompt.

> Feito ao concluir o curso *Prompt Engineering: projetando e automatizando interações com LLMs*,
> aplicando a técnica a um problema real de CS (NPS), não a um exemplo genérico.

## O problema

Uma pesquisa de NPS gera muito texto livre. Ler, categorizar e responder cada comentário à mão
não escala. A ideia aqui é transformar o comentário em **dado acionável** e adiantar uma resposta,
mantendo a pessoa no controle (o CSM revisa antes de enviar).

## O que faz

Para cada comentário (nota + texto), o modelo retorna:

```json
{
  "categoria": "promotor | neutro | detrator",   // vem da nota (regra do NPS, não do LLM)
  "tema": "suporte | produto | preço | prazo | usabilidade | atendimento_comercial | outro",
  "sentimento": "positivo | neutro | negativo",
  "motivo": "frase curta com a razão central",
  "resposta_sugerida": "2 a 4 frases, tom de CS, em pt-BR"
}
```

A engenharia do prompt (papel, enums fechados, saída só-JSON, few-shot, guardrails, temperature 0)
está documentada em **[`prompt.md`](prompt.md)**. Exemplos de saída em **[`data/exemplos.md`](data/exemplos.md)**.

## Como a qualidade é medida

Nada de "achismo": há um gabarito de 18 comentários rotulados à mão em
[`data/teste.json`](data/teste.json), e [`src/avaliar.py`](src/avaliar.py) roda o classificador
em cima dele e calcula a **acurácia de tema e de sentimento**. É assim que se compara uma versão
do prompt com a próxima.

## Resultados

Rodando contra o gabarito (`openai/gpt-oss-120b` via Groq, `temperature=0`):

| Métrica | Acurácia |
|---|---|
| Tema | **100%** (18/18) |
| Sentimento | **100%** (18/18) |

O número alto é esperado: são 18 casos rotulados à mão e sem ambiguidade, feitos para **demonstrar o método**. O valor do projeto não é o "100%" em si — é ter uma régua **reprodutível** para comparar versões do prompt. Num conjunto maior e com dados reais a acurácia cai, e é aí que essa avaliação passa a valer: ela mostra *onde* o prompt erra (qual tema, qual nota) para a próxima iteração.

## Como rodar

```bash
pip install -r requirements.txt
cp .env.example .env            # e cole sua GROQ_API_KEY (grátis em https://console.groq.com)
export $(grep -v '^#' .env | xargs)

python src/avaliar.py           # roda a avaliação e mostra a acurácia
python src/classificar.py       # classifica um comentário de exemplo
```

Sem instalar nada, dá para rodar o self-check da lógica (não chama a API):

```bash
python src/test_avaliar.py      # ok: 3 checagens passaram
```

> O LLM é acessado por uma API **compatível com OpenAI** (Groq por padrão — grátis e rápido).
> Trocar de provedor (OpenAI, etc.) é só mudar `LLM_BASE_URL` e `GROQ_MODEL` no `.env`.

## Estrutura

```
nps-ia/
├── prompt.md              # o prompt e as técnicas, explicados
├── src/
│   ├── classificar.py     # o prompt + chamada ao LLM + guardrails
│   ├── avaliar.py         # acurácia contra o gabarito
│   └── test_avaliar.py    # self-check sem API
└── data/
    ├── teste.json         # 18 comentários rotulados (gabarito)
    └── exemplos.md        # saídas de exemplo (antes → depois)
```

## Limitações e próximos passos

- Dataset pequeno (18 casos) — serve para demonstrar o método; um uso real pediria mais e dados próprios.
- Os comentários são **fictícios**, para não expor dados de clientes.
- Próximos: dataset maior, um 2º prompt como *LLM-as-judge* para avaliar a `resposta_sugerida`,
  e plugar o mesmo prompt num fluxo n8n para rodar automaticamente a cada nova resposta.
