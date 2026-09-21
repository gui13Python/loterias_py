"""
Aposta Certa — Gerador de jogos (Lotofácil e Mega-Sena) em Flask.

Permite gerar jogos automaticamente com filtros estatísticos, ou o usuário
pode escolher manualmente parte (ou todas) as dezenas de cada jogo.
"""

import random
from flask import Flask, render_template, request

app = Flask(__name__, static_folder="public", static_url_path="")

CFG = {
    "lotofacil": {"total": 25, "pick": 15, "nome": "Lotofácil"},
    "megasena": {"total": 60, "pick": 6, "nome": "Mega-Sena"},
}

MOLDURA_LOTOFACIL = {1, 2, 3, 4, 5, 6, 10, 11, 15, 16, 20, 21, 22, 23, 24, 25}

MAX_TENTATIVAS = 20000


def eh_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def validar_lotofacil(jogo):
    pares = sum(1 for x in jogo if x % 2 == 0)
    if pares not in (7, 8):
        return False
    primos = sum(1 for x in jogo if eh_primo(x))
    if primos not in (5, 6):
        return False
    moldura = sum(1 for x in jogo if x in MOLDURA_LOTOFACIL)
    if moldura not in (9, 10):
        return False
    soma = sum(jogo)
    if not (180 <= soma <= 220):
        return False
    return True


def validar_megasena(jogo):
    pares = sum(1 for x in jogo if x % 2 == 0)
    if pares not in (2, 3, 4):
        return False
    soma = sum(jogo)
    if not (130 <= soma <= 240):
        return False
    ordenado = sorted(jogo)
    for i in range(len(ordenado) - 2):
        if ordenado[i + 1] == ordenado[i] + 1 and ordenado[i + 2] == ordenado[i] + 2:
            return False
    return True


VALIDADORES = {"lotofacil": validar_lotofacil, "megasena": validar_megasena}


def estatisticas(game, jogo):
    """Retorna as métricas do jogo para exibição, independente de ele passar nos filtros."""
    pares = sum(1 for x in jogo if x % 2 == 0)
    soma = sum(jogo)
    stats = [
        {"label": "Pares / Ímpares", "valor": f"{pares}P / {len(jogo) - pares}I"},
        {"label": "Soma das dezenas", "valor": soma},
    ]
    if game == "lotofacil":
        primos = sum(1 for x in jogo if eh_primo(x))
        moldura = sum(1 for x in jogo if x in MOLDURA_LOTOFACIL)
        stats.append({"label": "Números primos", "valor": primos})
        stats.append({"label": "Na moldura", "valor": moldura})
    return stats


def gerar_jogo(game, fixas):
    """
    Gera um jogo para `game` ('lotofacil' ou 'megasena').
    `fixas` é a lista de dezenas que o usuário escolheu manualmente (pode ser vazia).

    Se o usuário já escolheu todas as dezenas do jogo, devolve o jogo manual
    direto (sem sorteio), só calculando se ele bate com os filtros.
    Caso contrário, completa o restante por sorteio até achar uma combinação
    que passe nos filtros estatísticos.
    """
    cfg = CFG[game]
    total, pick = cfg["total"], cfg["pick"]
    fixas = sorted(set(fixas))

    if len(fixas) == pick:
        jogo = fixas
        passou = VALIDADORES[game](jogo)
        return jogo, 0, passou

    universo = list(range(1, total + 1))
    fixas_set = set(fixas)
    disponiveis = [n for n in universo if n not in fixas_set]
    faltam = pick - len(fixas)

    candidato = None
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        variaveis = random.sample(disponiveis, faltam)
        candidato = sorted(fixas_set | set(variaveis))
        if VALIDADORES[game](candidato):
            return candidato, tentativa, True

    # Não achou nada dentro dos filtros com essas fixas (raro, mas possível)
    return candidato, MAX_TENTATIVAS, False


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        game = request.form.get("game", "lotofacil")
    else:
        game = request.args.get("game", "lotofacil")
    if game not in CFG:
        game = "lotofacil"

    fixas_selecionadas = []
    resultado = None
    erro = None

    if request.method == "POST":
        brutas = request.form.getlist("fixa")
        try:
            fixas_selecionadas = sorted({int(x) for x in brutas})
        except ValueError:
            fixas_selecionadas = []

        pick = CFG[game]["pick"]
        if len(fixas_selecionadas) > pick:
            erro = f"Você escolheu {len(fixas_selecionadas)} dezenas, mas o {CFG[game]['nome']} só permite {pick}."
        else:
            jogo, tentativas, passou = gerar_jogo(game, fixas_selecionadas)
            resultado = {
                "jogo": jogo,
                "jogo_fmt": [f"{n:02d}" for n in jogo],
                "tentativas": tentativas,
                "passou": passou,
                "manual_completo": len(fixas_selecionadas) == pick,
                "stats": estatisticas(game, jogo),
            }

    return render_template(
        "index.html",
        cfg=CFG,
        game=game,
        total=CFG[game]["total"],
        pick=CFG[game]["pick"],
        fixas_selecionadas=fixas_selecionadas,
        resultado=resultado,
        erro=erro,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
