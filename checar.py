#!/usr/bin/env python3
"""checar.py — confere uma Ficha do Enxame antes do /swarm do Google Antigravity.

Uso:
  python3 checar.py ficha.md            # 8 itens, nota 0–8, como corrigir
  python3 checar.py ficha.md --prompt   # texto pronto para o /swarm (PT), só com nota 7 ou mais
  python3 checar.py ficha.md --prompt --en   # o esqueleto do texto em inglês
  python3 checar.py ficha.md --json     # resultado em JSON

Código de saída: 0 se a nota for 7 ou mais; 1 se for menor; 2 se o arquivo não abrir.
Só biblioteca padrão. O script lê o Markdown; ele não chama o Antigravity nem nenhuma API.
"""
import argparse
import fnmatch
import json
import math
import re
import sys
import unicodedata

NOTA_MINIMA = 7


# ---------- leitura do Markdown ----------

def norm(txt):
    """minúsculas e sem acento, para comparar títulos e chaves."""
    t = unicodedata.normalize("NFKD", txt.strip().lower())
    return "".join(c for c in t if not unicodedata.combining(c))


def preenchido(txt):
    """texto com conteúdo de verdade (não vazio, não marcador <...>, não reticências)."""
    t = re.sub(r"<[^>]*>", "", txt or "").strip(" .…-*\t\n")
    return len(t) >= 3


def ler_ficha(texto):
    """Devolve {'tarefa', 'verificar', 'pecas': [...], 'verificador', 'limites', 'modelo_workers', 'linhas'}."""
    ficha = {"tarefa": "", "verificar": "", "pecas": [], "verificador": None,
             "limites": None, "modelo_workers": "", "linhas": texto.splitlines()}
    secao = None
    peca = None
    em_bloco = False
    for linha in texto.splitlines():
        s = linha.strip()
        if s.startswith("```"):
            em_bloco = not em_bloco
            if secao == "verificar":
                ficha["verificar"] += linha + "\n"
            continue
        if not em_bloco:
            m = re.match(r"^(#{1,3})\s+(.*)$", s)
            if m:
                nivel, titulo = len(m.group(1)), m.group(2).strip()
                t = norm(titulo)
                if nivel == 3 and secao in ("pecas", "peca") and titulo.startswith("@"):
                    peca = {"nome": titulo.split()[0], "campos": {}}
                    ficha["pecas"].append(peca)
                    secao = "peca"
                    continue
                peca = None
                if t.startswith("tarefa"):
                    secao = "tarefa"
                elif t.startswith("como verificar"):
                    secao = "verificar"
                elif t.startswith("pecas"):
                    secao = "pecas"
                elif t.startswith("verificador"):
                    secao = "verificador"
                    ficha["verificador"] = {}
                elif t.startswith("limites"):
                    secao = "limites"
                    ficha["limites"] = []
                elif t.startswith("modelo dos workers"):
                    secao = "modelo"
                else:
                    secao = None
                continue
        if secao == "tarefa":
            ficha["tarefa"] += linha + "\n"
        elif secao == "verificar":
            ficha["verificar"] += linha + "\n"
        elif secao == "modelo":
            ficha["modelo_workers"] += re.sub(r"^\s*[-*]\s*", "", linha) + " "
        elif secao in ("peca", "verificador"):
            m = re.match(r"^\s*[-*]\s*([^:]+):\s*(.*)$", linha)
            if m:
                chave = norm(m.group(1))
                destino = peca["campos"] if secao == "peca" else ficha["verificador"]
                destino[chave] = m.group(2).strip()
        elif secao == "limites":
            m = re.match(r"^\s*[-*]\s*(.+)$", linha)
            if m:
                txt = m.group(1).strip()
                kv = re.match(r"^([^:]{1,40}):\s*(.*)$", txt)
                # linha de modelo ("cota: <quanto aceita gastar>") não conta como limite
                if preenchido(kv.group(2) if kv else txt):
                    ficha["limites"].append(txt)
    ficha["tarefa"] = ficha["tarefa"].strip()
    ficha["verificar"] = ficha["verificar"].strip()
    ficha["modelo_workers"] = ficha["modelo_workers"].strip()
    return ficha


def campo(peca, *nomes):
    for n in nomes:
        if n in peca["campos"]:
            return peca["campos"][n]
    return ""


def comando_de(txt):
    """primeiro comando escrito entre crases (`...`) ou em bloco ``` ```."""
    m = re.search(r"```[^\n]*\n(.*?)```", txt or "", re.S)
    if m and m.group(1).strip() and not m.group(1).strip().startswith("<"):
        return m.group(1).strip().splitlines()[0].strip()
    for c in re.findall(r"`([^`]+)`", txt or ""):
        if c.strip() and not c.strip().startswith("<"):
            return c.strip()
    return ""


def caminhos(txt):
    """caminhos do campo 'dono': tudo o que está entre crases. Texto sem crase é pergunta/assunto."""
    return [p.strip() for p in re.findall(r"`([^`]+)`", txt or "") if p.strip() and not p.strip().startswith("<")]


# ---------- sobreposição de donos (item 5) ----------

CURINGA = re.compile(r"[*?\[]")


def limpa(p):
    p = p.strip()
    while p.startswith("./"):
        p = p[2:]
    return p


def se_sobrepoe(a, b):
    """True se os dois donos podem cair no mesmo arquivo (igual, pasta que contém, glob simples)."""
    a, b = limpa(a), limpa(b)
    if a.rstrip("/") == b.rstrip("/"):
        return True
    ga, gb = bool(CURINGA.search(a)), bool(CURINGA.search(b))
    if not ga and not gb:
        pa, pb = a.rstrip("/") + "/", b.rstrip("/") + "/"
        return pb.startswith(pa) or pa.startswith(pb)  # pasta que contém o arquivo do outro
    if ga and not gb:
        return fnmatch.fnmatch(b, a) or fnmatch.fnmatch(b, a.rstrip("/") + "/*") or a.startswith(b.rstrip("/") + "/")
    if gb and not ga:
        return se_sobrepoe(b, a)
    # dois globs: prefixo literal compatível e final compatível
    if fnmatch.fnmatch(a, b) or fnmatch.fnmatch(b, a):
        return True
    pre_a, pre_b = CURINGA.split(a)[0], CURINGA.split(b)[0]
    if not (pre_a.startswith(pre_b) or pre_b.startswith(pre_a)):
        return False
    suf_a, suf_b = CURINGA.split(a)[-1], CURINGA.split(b)[-1]
    if suf_a and suf_b and not (suf_a.endswith(suf_b) or suf_b.endswith(suf_a)):
        return False
    return True


# ---------- laço sem supervisão (item 8) ----------

RISCO = re.compile(
    r"(sem supervis|unattended|overnight|toda (a )?noite|a noite (toda|inteira)|madrugada|headless|\bcron\b|"
    r"em la[cç]os?\b|\bin a loop\b|\bloops? (de|of) (enxames|swarms|sess)|dezenas de (sess|enxames|swarms|agentes)|"
    r"infinit|a cada \d+ ?(s|seg|min)\b|every \d+ ?(s|sec|min)\b|em massa|alto volume|high volume)",
    re.I)
NEGA = re.compile(
    r"(\bn[aã]o\b|\bnunca\b|\bnada de\b|\bjamais\b|\bevite\b|\bproibido\b|\bsem rodar\b|\bnem\b|"
    r"\bnever\b|\bdon'?t\b|\bdo not\b|\bavoid\b|\bno (background |unattended )?(loops?|cron|overnight)\b)", re.I)


def frases_de_laco(linhas):
    """linhas que pedem laço/execução sem supervisão e NÃO estão negadas."""
    ruins = []
    for linha in linhas:
        if RISCO.search(linha) and not NEGA.search(linha):
            ruins.append(linha.strip())
    return ruins


# ---------- os 8 itens ----------

def _curto(t, n=90):
    return t if len(t) <= n else t[:n].rstrip() + "…"


def checar(texto):
    f = ler_ficha(texto)
    pecas = f["pecas"]
    itens = []

    def item(n, titulo, ok, motivo, corrigir, avisos=None):
        itens.append({"n": n, "titulo": titulo, "ok": bool(ok), "motivo": motivo,
                      "corrigir": "" if ok else corrigir, "avisos": avisos or []})

    # 1
    item(1, "Tarefa escrita", preenchido(f["tarefa"]),
         "tarefa: " + (_curto(f["tarefa"].splitlines()[0]) if preenchido(f["tarefa"]) else "vazia ou só marcador"),
         "Escreva em '# Tarefa' o que você quer pronto, em uma ou duas frases.")

    # 2
    cmd = comando_de(f["verificar"])
    item(2, "Como verificar tem um comando", bool(cmd),
         f"comando: {cmd}" if cmd else "nenhum comando entre crases em '## Como verificar'",
         "Em '## Como verificar', ponha o comando entre crases, ex.: `npm test` ou `python3 -m unittest`.")

    # 3
    item(3, "Pelo menos 2 peças", len(pecas) >= 2,
         f"{len(pecas)} peça(s): " + ", ".join(p["nome"] for p in pecas) if pecas else "nenhuma peça '### @nome'",
         "Com uma peça só, não precisa de enxame: use um agente só ou um subagente. "
         "Para usar /swarm, divida em '### @nome' (2 ou mais).")

    # 4
    sem_dono = [p["nome"] for p in pecas if not preenchido(campo(p, "dono"))]
    item(4, "Toda peça tem dono", pecas and not sem_dono,
         "todas têm dono" if pecas and not sem_dono else
         ("sem dono: " + ", ".join(sem_dono) if sem_dono else "não há peças"),
         "Em cada peça, escreva '- dono:' com os arquivos/pastas entre crases (`src/a.ts`) "
         "ou a pergunta que ela investiga.")

    # 5
    colisoes = []
    for i in range(len(pecas)):
        for j in range(i + 1, len(pecas)):
            for a in caminhos(campo(pecas[i], "dono")):
                for b in caminhos(campo(pecas[j], "dono")):
                    if se_sobrepoe(a, b):
                        colisoes.append(f"{pecas[i]['nome']} `{a}` × {pecas[j]['nome']} `{b}`")
    ok5 = len(pecas) >= 2 and not sem_dono and not colisoes
    item(5, "Donos não se sobrepõem", ok5,
         "nenhum arquivo com dois donos" if ok5 else
         ("colisão: " + "; ".join(colisoes[:4]) if colisoes else
          "precisa de 2 peças, todas com dono, para comparar"),
         "Dê cada arquivo a uma peça só. Se duas precisam do mesmo arquivo, quebre o arquivo em partes, "
         "junte as duas peças numa só, ou peça cópias de trabalho (working copy) para cada worker.")

    # 6
    faltam = []
    for p in pecas:
        if not preenchido(campo(p, "nao mexe", "nao mexe em")):
            faltam.append(f"{p['nome']} sem 'não mexe'")
        if not preenchido(campo(p, "pronto quando")):
            faltam.append(f"{p['nome']} sem 'pronto quando'")
    item(6, "Toda peça diz o que não mexe e quando está pronta", pecas and not faltam,
         "todas completas" if pecas and not faltam else ("; ".join(faltam) if faltam else "não há peças"),
         "Em cada peça, escreva '- não mexe:' (o que é dos outros) e '- pronto quando:' (o teste ou o sinal de fim).")

    # 7
    v = f["verificador"]
    avisos7 = []
    ok7 = v is not None and preenchido(v.get("roda", ""))
    if v is None:
        motivo7 = "sem seção '## Verificador'"
    elif not ok7:
        motivo7 = "verificador sem '- roda:' (o que ele roda e revisa)"
    else:
        try:
            qtd = int(re.findall(r"\d+", v.get("quantos", "1"))[0])
        except IndexError:
            qtd = 1
        precisa = max(1, math.ceil(len(pecas) / 4)) if pecas else 1
        motivo7 = f"{qtd} verificador(es) para {len(pecas)} peça(s); roda: {comando_de(v['roda']) or v['roda'][:60]}"
        if qtd < precisa:
            avisos7.append(f"a documentação fala em 1 verificador para cada 2 a 4 workers: "
                           f"com {len(pecas)} peças, use {precisa} ('- quantos: {precisa}')")
        mod = norm(v.get("modelo", ""))
        if not mod:
            avisos7.append("modelo do verificador não informado: escreva '- modelo: diferente dos workers'")
        elif "mesmo" in mod or "igual" in mod or (f["modelo_workers"] and mod == norm(f["modelo_workers"])):
            avisos7.append("verificador no mesmo modelo dos workers: outro modelo pega erros que o primeiro não vê")
    item(7, "Verificador definido", ok7, motivo7,
         "Acrescente '## Verificador' com '- roda:' (revisa os diffs e roda o comando de verificação), "
         "'- modelo: diferente dos workers' e, acima de 4 peças, '- quantos: 2'.", avisos7)

    # 8
    lim = f["limites"]
    avisos8 = []
    laco = frases_de_laco(f["linhas"])
    if lim is None:
        ok8, motivo8 = False, "sem seção '## Limites'"
    else:
        tudo = norm(" ".join(lim))
        tem_cota = bool(re.search(r"cota|quota|creditos|tokens", tudo))
        tem_parada = bool(re.search(r"\bpar(ar|e|ada|em)\b|\binterromp|\bencerr|\bstop\b", tudo))
        ok8 = tem_cota and tem_parada and not laco
        partes = []
        if not tem_cota:
            partes.append("falta limite de cota")
        if not tem_parada:
            partes.append("falta quando parar")
        if laco:
            partes.append("pede laço sem supervisão: " + laco[0][:80])
        motivo8 = "; ".join(partes) if partes else "cota e parada definidas; nenhum laço sem supervisão"
        if not re.search(r"remov|limp|retir|kill", tudo):
            avisos8.append("diga quando remover os workers (remover é permanente; ele entrega as mudanças antes)")
    item(8, "Limites de cota e de parada, sem laço sem supervisão", ok8, motivo8,
         "Em '## Limites', escreva quanto de cota aceita gastar e quando parar. Tire qualquer pedido de rodar "
         "em laço, à noite ou sem você olhando: laço de fundo sem supervisão em alto volume pode acionar o antiabuso.",
         avisos8)

    nota = sum(1 for i in itens if i["ok"])
    return {"nota": nota, "maximo": 8, "passa": nota >= NOTA_MINIMA, "itens": itens,
            "pecas": [p["nome"] for p in pecas], "ficha": f}


# ---------- prompt pronto ----------

def _sem_crase(t):
    return re.sub(r"`([^`]+)`", r"\1", t or "").strip().rstrip(".")


def montar_prompt(res, en=False):
    """Texto de uma linha para colar no Antigravity. Só o esqueleto muda de idioma; o seu texto fica como está."""
    f = res["ficha"]
    tarefa = " ".join(_sem_crase(f["tarefa"]).split())
    cmd = comando_de(f["verificar"])
    pecas = []
    for p in f["pecas"]:
        dono, nao, pronto = (_sem_crase(campo(p, "dono")), _sem_crase(campo(p, "nao mexe", "nao mexe em")),
                             _sem_crase(campo(p, "pronto quando")))
        extra = " ".join(_sem_crase(v) for k, v in p["campos"].items()
                         if k not in ("dono", "nao mexe", "nao mexe em", "pronto quando"))
        pergunta = re.match(r"^\s*pergunta\s*:\s*(.*)$", dono, re.I)
        if en:
            dono_txt = f"investigates: {pergunta.group(1)}" if pergunta else f"owns {dono}"
            pecas.append(f"{p['nome']} {dono_txt}; must not touch {nao}; done when {pronto}"
                         + (f"; {extra}" if extra else ""))
        else:
            dono_txt = f"investiga: {pergunta.group(1)}" if pergunta else f"é dono de {dono}"
            pecas.append(f"{p['nome']} {dono_txt}; não mexe em {nao}; pronto quando {pronto}"
                         + (f"; {extra}" if extra else ""))
    v = f["verificador"] or {}
    try:
        qtd = int(re.findall(r"\d+", v.get("quantos", "1"))[0])
    except IndexError:
        qtd = 1
    roda = _sem_crase(v.get("roda", ""))
    mod = _sem_crase(v.get("modelo", ""))
    diferente = (not mod) or "diferente" in norm(mod) or "different" in norm(mod)
    lim = "; ".join(_sem_crase(x) for x in (f["limites"] or []))
    mw = _sem_crase(f["modelo_workers"])
    if en:
        s = f"/swarm {tarefa}. Give each piece its own worker. Pieces: " + " | ".join(pecas) + ". "
        s += (f"Add {qtd} verifier{'s' if qtd > 1 else ''} "
              + ("on a different model than the workers" if diferente else f"on {mod}")
              + f". Verifier: {roda}. ")
        if mw:
            s += f"Workers' model: {mw}. "
        if cmd:
            s += f"Verify with {cmd}. "
        if lim:
            s += f"Limits: {lim}."
    else:
        s = f"/swarm {tarefa}. Dê a cada peça o seu próprio worker. Peças: " + " | ".join(pecas) + ". "
        s += (f"Adicione {qtd} verificador{'es' if qtd > 1 else ''} "
              + ("num modelo diferente do dos workers" if diferente else f"no modelo {mod}")
              + f". Verificador: {roda}. ")
        if mw:
            s += f"Modelo dos workers: {mw}. "
        if cmd:
            s += f"Para verificar, rode {cmd}. "
        if lim:
            s += f"Limites: {lim}."
    return " ".join(s.split())


# ---------- saída ----------

def imprimir(res, nome):
    print(f"Ficha do Enxame: {nome}")
    for i in res["itens"]:
        print(f"{'✔' if i['ok'] else '✘'} {i['n']}. {i['titulo']} — {i['motivo']}")
        if not i["ok"]:
            print(f"   → como corrigir: {i['corrigir']}")
        for a in i["avisos"]:
            print(f"   ! aviso: {a}")
    veredito = "pronta para o /swarm" if res["passa"] else "ainda não: corrija os ✘ antes do /swarm"
    print(f"Nota: {res['nota']}/8 — {veredito}")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Confere uma Ficha do Enxame (nota 0–8) antes do /swarm.")
    ap.add_argument("ficha", help="arquivo .md da ficha")
    ap.add_argument("--prompt", action="store_true", help="imprime o texto pronto para colar no Antigravity")
    ap.add_argument("--en", action="store_true", help="com --prompt: esqueleto do texto em inglês")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    a = ap.parse_args(argv)
    try:
        with open(a.ficha, encoding="utf-8") as fh:
            texto = fh.read()
    except OSError as e:
        print(f"não consegui abrir {a.ficha}: {e}", file=sys.stderr)
        return 2
    res = checar(texto)
    if a.json:
        saida = {k: v for k, v in res.items() if k != "ficha"}
        saida["arquivo"] = a.ficha
        if a.prompt:
            saida["prompt"] = montar_prompt(res, en=a.en) if res["passa"] else None
        print(json.dumps(saida, ensure_ascii=False, indent=2))
    elif a.prompt:
        if not res["passa"]:
            # abaixo de 7 não monta o texto do /swarm: mostra o motivo e sai com 1
            print(f"Sem texto para o /swarm: a ficha tirou {res['nota']}/8 e precisa de {NOTA_MINIMA} ou mais.")
            for i in res["itens"]:
                if not i["ok"]:
                    print(f"✘ {i['n']}. {i['titulo']} — {i['motivo']}")
                    print(f"   → como corrigir: {i['corrigir']}")
            return 1
        print(montar_prompt(res, en=a.en))
    else:
        imprimir(res, a.ficha)
    return 0 if res["passa"] else 1


if __name__ == "__main__":
    sys.exit(main())
