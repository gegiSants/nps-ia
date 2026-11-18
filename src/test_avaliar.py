"""Checagem rápida sem chamar a API: python src/test_avaliar.py"""
from avaliar import acuracia
from classificar import categoria_por_nota, normalizar


def test_acuracia():
    pred = [{"tema": "suporte"}, {"tema": "produto"}, {"tema": "preço"}]
    gold = [{"tema": "suporte"}, {"tema": "produto"}, {"tema": "prazo"}]
    assert acuracia(pred, gold, "tema") == 2 / 3
    assert acuracia([], [], "tema") == 0.0


def test_categoria_por_nota():
    assert categoria_por_nota(10) == "promotor"
    assert categoria_por_nota(8) == "neutro"
    assert categoria_por_nota(6) == "detrator"


def test_normalizar_guardrail():
    # tema/sentimento inválidos do LLM caem no padrão; categoria vem da nota
    saida = normalizar(2, {"tema": "inventado", "sentimento": "???", "motivo": " x "})
    assert saida["tema"] == "outro"
    assert saida["sentimento"] == "neutro"
    assert saida["categoria"] == "detrator"
    assert saida["motivo"] == "x"


if __name__ == "__main__":
    test_acuracia()
    test_categoria_por_nota()
    test_normalizar_guardrail()
    print("ok: 3 checagens passaram")
