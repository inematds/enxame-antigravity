#!/usr/bin/env python3
"""escolher.py — subagente, /boost, /swarm ou /teamwork? Responde pela tabela oficial do Google Antigravity
(https://antigravity.google/docs/swarm, seção "Choose between Swarm, Teamwork, Boost, and subagents").

Uso com flags (sem perguntas):
  python3 escolher.py --divide-limpo sim          # tarefa ampla que se divide limpo -> /swarm
  python3 escolher.py --dificil                   # problema difícil, não amplo     -> /boost
  python3 escolher.py --dias                      # vários marcos, horas a dias      -> /teamwork
  python3 escolher.py --lateral                   # tarefa lateral e focada          -> subagente
Sem flags, faz as perguntas no terminal. --json devolve o resultado em JSON.
Só biblioteca padrão; não chama nenhuma API.
"""
import argparse
import json
import sys

FONTE = "tabela oficial: https://antigravity.google/docs/swarm"

OPCOES = {
    "teamwork": {
        "usar": "/teamwork <objetivo>",
        "porque": "Projeto de vários marcos que leva horas a dias (migração do repositório inteiro, simulação, "
                  "pesquisa longa). Começa com uma entrevista, trabalha numa pasta própria e passa por auditores a cada marco.",
        "plano": "planos pagos",
        "horizonte": "horas a dias",
    },
    "subagente": {
        "usar": "subagente (delegação automática ou menção @subagent)",
        "porque": "Tarefa lateral e focada (pesquisar no código, conferir no navegador, rodar os testes) enquanto "
                  "você segue na conversa principal. O agente que pediu confere a resposta.",
        "plano": "todos os planos",
        "horizonte": "segundos a minutos",
    },
    "boost": {
        "usar": "/boost <tarefa>",
        "porque": "O problema é difícil, não amplo (bug cabeludo, condição de corrida, algoritmo, refatoração acoplada): "
                  "vários agentes tentam, desafiam e corrigem a mesma solução em rodadas.",
        "plano": "planos pagos",
        "horizonte": "segundos a horas",
    },
    "swarm": {
        "usar": "/swarm <tarefa>",
        "porque": "Tarefa ampla que se divide limpo em arquivos, pacotes ou perguntas independentes: workers com nome "
                  "trabalham ao mesmo tempo e um @verifier revisa os diffs e roda os testes, tudo num quadro único.",
        "plano": "Google AI Pro e Google AI Ultra (em prévia; gasta cota muito mais rápido que uma conversa)",
        "horizonte": "minutos a horas",
        "depois": "Antes de digitar, escreva a Ficha do Enxame: cp modelos/FICHA.md minha-ficha.md && "
                  "python3 checar.py minha-ficha.md",
    },
    "agente": {
        "usar": "o agente padrão, numa conversa normal",
        "porque": "Não é amplo, não é difícil, não é lateral nem de vários dias: para o dia a dia, a documentação manda "
                  "pedir direto ao agente padrão. Um enxame aqui só gastaria cota.",
        "plano": "todos os planos",
        "horizonte": "—",
    },
}


def decidir(divide_limpo=False, dificil=False, dias=False, lateral=False):
    """Devolve a chave de OPCOES. Ordem: vários dias > lateral > divide limpo > difícil > agente padrão."""
    if dias:
        return "teamwork"
    if lateral:
        return "subagente"
    if divide_limpo:
        return "swarm"
    if dificil:
        return "boost"
    return "agente"


def sim_nao(txt):
    t = (txt or "").strip().lower()
    if t in ("s", "sim", "y", "yes", "si", "sí"):
        return True
    if t in ("n", "nao", "não", "no", ""):
        return False
    raise ValueError(f"responda sim ou não (veio: {txt!r})")


PERGUNTAS = [
    ("dias", "O trabalho tem vários marcos e leva horas a dias (migração inteira, pesquisa longa)? [s/N] "),
    ("lateral", "É uma tarefa lateral e focada (pesquisar no código, rodar os testes, checar no navegador)? [s/N] "),
    ("divide_limpo", "Divide limpo em arquivos, pacotes ou perguntas que não se tocam? [s/N] "),
    ("dificil", "O problema é difícil mais do que amplo (bug cabeludo, condição de corrida, algoritmo)? [s/N] "),
]


def perguntar(entrada=input):
    resp = {}
    for chave, texto in PERGUNTAS:
        while True:
            try:
                resp[chave] = sim_nao(entrada(texto))
                break
            except EOFError:
                resp[chave] = False
                break
            except ValueError as e:
                print(e)
        if resp[chave] and chave in ("dias", "lateral"):
            break  # já decidiu
    return resp


def explicar(chave, extra=None):
    o = OPCOES[chave]
    linhas = [f"Use: {o['usar']}", f"Por quê: {o['porque']}", f"Plano exigido: {o['plano']} · horizonte típico: "
              f"{o['horizonte']} ({FONTE})"]
    if extra:
        linhas.append(f"Atenção: {extra}")
    if o.get("depois"):
        linhas.append(f"Próximo passo: {o['depois']}")
    return "\n".join(linhas)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Qual ferramenta do Antigravity usar: subagente, /boost, /swarm ou /teamwork.")
    ap.add_argument("--divide-limpo", choices=["sim", "nao", "não"], help="a tarefa se divide limpo em partes independentes?")
    ap.add_argument("--dificil", action="store_true", help="problema difícil (bug, corrida, algoritmo), não amplo")
    ap.add_argument("--dias", action="store_true", help="vários marcos, horas a dias")
    ap.add_argument("--lateral", action="store_true", help="tarefa lateral e focada")
    ap.add_argument("--perguntar", action="store_true", help="faz as perguntas mesmo fora de um terminal (lê da entrada)")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    a = ap.parse_args(argv)

    usou_flag = a.divide_limpo is not None or a.dificil or a.dias or a.lateral
    if usou_flag:
        r = {"divide_limpo": a.divide_limpo == "sim", "dificil": a.dificil, "dias": a.dias, "lateral": a.lateral}
    elif a.perguntar or sys.stdin.isatty():
        r = perguntar()
    else:
        print("sem flags e sem terminal: use --divide-limpo sim|nao, --dificil, --dias ou --lateral", file=sys.stderr)
        return 2
    r = {k: r.get(k, False) for k in ("divide_limpo", "dificil", "dias", "lateral")}
    chave = decidir(**r)
    extra = None
    if chave == "swarm" and r["dificil"]:
        extra = "se uma das peças for difícil de verdade, rode /boost só nela antes ou depois do enxame."
    if a.json:
        print(json.dumps({"escolha": chave, **OPCOES[chave], "respostas": r, "atencao": extra, "fonte": FONTE},
                         ensure_ascii=False, indent=2))
    else:
        print(explicar(chave, extra))
    return 0


if __name__ == "__main__":
    sys.exit(main())
