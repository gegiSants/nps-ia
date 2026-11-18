# Exemplos (antes → depois)

Comentários fictícios de NPS, para ilustrar a saída. A `resposta_sugerida` é o texto
que um CSM poderia revisar e enviar — não é enviada automaticamente.

### 1. Detrator — instabilidade

**Entrada:** nota **2** · "O sistema fica fora do ar toda semana e atrapalha meu fechamento mensal."

```json
{
  "categoria": "detrator",
  "tema": "produto",
  "sentimento": "negativo",
  "motivo": "instabilidade do sistema no fechamento",
  "resposta_sugerida": "Sentimos muito pela instabilidade que atrapalhou seu fechamento. Já levamos o caso ao time técnico e gostaríamos de entender melhor o impacto — podemos te chamar para uma conversa esta semana?"
}
```

### 2. Promotor — suporte

**Entrada:** nota **10** · "O suporte resolveu meu problema de certificado em minutos, muito atenciosos."

```json
{
  "categoria": "promotor",
  "tema": "suporte",
  "sentimento": "positivo",
  "motivo": "suporte rápido na emissão do certificado",
  "resposta_sugerida": "Que ótimo saber que o suporte te atendeu com rapidez! Obrigada por compartilhar — seguimos à disposição sempre que precisar."
}
```

### 3. Neutro — comercial

**Entrada:** nota **5** · "O comercial sumiu depois que fechei o contrato."

```json
{
  "categoria": "detrator",
  "tema": "atendimento_comercial",
  "sentimento": "negativo",
  "motivo": "falta de acompanhamento do comercial pós-venda",
  "resposta_sugerida": "Pedimos desculpas pela falta de acompanhamento após a contratação. Vamos te direcionar a um ponto de contato fixo no CS para garantir que isso não se repita — pode ser?"
}
```
