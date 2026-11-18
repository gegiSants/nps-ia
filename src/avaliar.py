"""Roda o classificador sobre data/teste.json e mede a acurácia contra o gabarito.

Uso: python src/avaliar.py
Precisa de GROQ_API_KEY no ambiente (ou num .env carregado pelo shell).
"""
from __future__ import annotations

import json
import pathlib

from classificar import classificar, _cliente

RAIZ = pathlib.Path(__file__).resolve().parent.parent
TESTE = RAIZ / "data" / "teste.json"


def acuracia(preditos: list[dict], gabarito: list[dict], campo: str) -> float:
    if not gabarito:
        return 0.0
    certos = sum(1 for p, g in zip(preditos, gabarito) if p[campo] == g[campo])
    return certos / len(gabarito)


def main() -> None:
    casos = json.loads(TESTE.read_text(encoding="utf-8"))
    cliente = _cliente()
    preditos = [classificar(c["nota"], c["comentario"], cliente) for c in casos]

    print(f"\n{'NOTA':<5}{'TEMA (previsto / gabarito)':<40}{'SENTIMENTO':<28}")
    print("-" * 73)
    for c, p in zip(casos, preditos):
        ok_t = "✓" if p["tema"] == c["tema"] else "✗"
        ok_s = "✓" if p["sentimento"] == c["sentimento"] else "✗"
        print(f"{c['nota']:<5}{ok_t} {p['tema']} / {c['tema']:<28}{ok_s} {p['sentimento']} / {c['sentimento']}")

    acc_tema = acuracia(preditos, casos, "tema")
    acc_sent = acuracia(preditos, casos, "sentimento")
    print("\n== Resultado ==")
    print(f"Acurácia de tema:       {acc_tema:.0%} ({len(casos)} casos)")
    print(f"Acurácia de sentimento: {acc_sent:.0%} ({len(casos)} casos)")
    # Linha pronta pra colar no README:
    print(f"\nPara o README: **Acurácia de tema: {acc_tema:.0%}** · **sentimento: {acc_sent:.0%}** (em {len(casos)} comentários)")


if __name__ == "__main__":
    main()
