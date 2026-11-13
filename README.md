# Ficha do Enxame — /swarm do Google Antigravity sem bagunça

[![Ficha do Enxame](guia/assets/banner.jpg)](https://inematds.github.io/enxame-antigravity/guia/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## O que é

Você ainda pede tudo para um agente só? O `/swarm` do Google Antigravity (app e CLI, em prévia para Google AI Pro e Ultra) divide uma tarefa entre vários agentes com nome, que trabalham ao mesmo tempo, e põe um verificador para revisar e testar. Ele só funciona bem se as partes não se atropelarem. A **Ficha do Enxame** é uma folha curta que você escreve antes de digitar `/swarm`: quem é dono de quê, o que cada um não toca, quando está pronto, quem verifica e quando parar. Este kit traz o modelo, um conferidor que dá nota de 0 a 8 e monta o texto para colar, e um ajudante que diz se o caso é mesmo de enxame. Precisa só de Python 3.

> **Importante:** este kit **não testou o /swarm**. O Antigravity não está instalado na máquina onde ele foi feito. Tudo sobre o `/swarm` vem da [documentação oficial](https://antigravity.google/docs/swarm). As "saídas reais" deste repositório são do `checar.py`, que só lê o Markdown da ficha.

## 📖 Guia de uso

Guia completo (landing + passo a passo): **https://inematds.github.io/enxame-antigravity/guia/**

🎬 Vídeo: em breve no guia.

## O processo, do início ao fim

Quem faz: 🧠 você · ⚙️ script deste kit · 🤖 o `/swarm` no Antigravity

| # | Passo | Comando | Quem |
|---|---|---|---|
| 1 | Ver se o caso é de enxame (ou de subagente, `/boost`, `/teamwork`) | `python3 escolher.py` (perguntas) ou `python3 escolher.py --divide-limpo sim` | 🧠 + ⚙️ |
| 2 | Copiar o modelo e preencher: tarefa, como verificar, peças, verificador, limites | `cp modelos/FICHA.md minha-ficha.md` | 🧠 |
| 3 | Conferir a ficha: 8 itens, nota 0–8, com o motivo e como corrigir | `python3 checar.py minha-ficha.md` | ⚙️ |
| 4 | Corrigir os ✘ e conferir de novo até nota 7 ou 8 | `python3 checar.py minha-ficha.md` | 🧠 |
| 5 | Gerar o texto pronto para colar (PT; `--en` monta o esqueleto em inglês). Só sai com nota ≥ 7; abaixo disso mostra o que corrigir e sai com código 1 | `python3 checar.py minha-ficha.md --prompt` | ⚙️ |
| 6 | No Antigravity, colar a linha inteira (ela já começa com `/swarm`). Se o comando colado não for reconhecido, digitar `/swarm`, Tab, e colar o resto | `/swarm …` | 🧠 |
| 7 | O coordenador divide, cria os workers com o brief de cada um e o `@verifier` | — | 🤖 |
| 8 | Acompanhar o quadro e responder aprovações | app: painel Swarm (Board, Members, Graph) · CLI: `/swarm board`, Alt+S, Alt+J | 🧠 |
| 9 | O verificador lê os diffs e roda o comando; o coordenador reporta | — | 🤖 |
| 10 | Rodar você mesmo o comando de "Como verificar" e pedir ao coordenador para remover quem terminou | o comando da sua ficha | 🧠 |

Manutenção do kit (quando mudar `checar.py` ou um exemplo):

```bash
python3 -m unittest -v
for d in calculadora-roi landing-page investigacao-lenta testes-por-pacote; do
  python3 checar.py exemplos/$d/ficha.md --prompt    > exemplos/$d/prompt.txt
  python3 checar.py exemplos/$d/ficha.md --prompt --en > exemplos/$d/prompt.en.txt
done
```

## O que tem aqui

| Arquivo | Para quê |
|---|---|
| `modelos/FICHA.md` | Modelo da ficha (Markdown simples, em PT) |
| `checar.py` | Confere 8 itens, nota 0–8; `--prompt` (só com nota ≥ 7), `--en`, `--json`; sai com 0 se a nota for ≥ 7 |
| `escolher.py` | Subagente, `/boost`, `/swarm` ou `/teamwork`, pela tabela oficial; flags ou perguntas |
| `exemplos/` | 4 fichas nota 8 (calculadora de ROI com 4 entradas, landing page, investigação lenta, testes por pacote), uma ficha ruim, os `prompt.txt` gerados e `saidas.txt` |
| `CUIDADOS.md` | Cota, prévia, worker sem cota, remover é permanente, relato de bloqueio de conta |
| `tests/` | `python3 -m unittest -v` |

## Os 8 itens do `checar.py`

1. Tarefa escrita.
2. "Como verificar" com um comando entre crases.
3. Pelo menos 2 peças (com uma só, use um agente só ou um subagente).
4. Toda peça tem dono (arquivos e pastas entre crases, ou uma pergunta, para investigação).
5. Donos não se sobrepõem: mesmo arquivo, pasta que contém arquivo de outro, glob simples (padrão com `*`, como `src/*.js`).
6. Toda peça tem "não mexe" e "pronto quando".
7. Verificador com "roda"; avisa se faltar proporção (1 para cada 2–4 peças) ou se o modelo não for diferente do dos workers.
8. Limites de cota e de parada, e nenhuma frase pedindo laço sem supervisão (a negação, "nada de laço", passa).

Saída real (do `checar.py`, não do `/swarm`) no exemplo ruim:

```text
✘ 5. Donos não se sobrepõem — colisão: @design `site/` × @textos `site/index.html`
   → como corrigir: Dê cada arquivo a uma peça só. Se duas precisam do mesmo arquivo, quebre o arquivo em partes, junte as duas peças numa só, ou peça cópias de trabalho (working copy) para cada worker.
Nota: 2/8 — ainda não: corrija os ✘ antes do /swarm
```

Todas as saídas: [`exemplos/saidas.txt`](exemplos/saidas.txt).

**Sobre o `--en`:** só o esqueleto do texto ("Give each piece its own worker", "Add 1 verifier…") sai em inglês; o que você escreveu na ficha vai como está.

## Fontes

- Documentação oficial do `/swarm`: https://antigravity.google/docs/swarm
- Comandos (`/boost`, `/teamwork` e outros): https://antigravity.google/docs/slash-commands
- `/teamwork`: https://antigravity.google/docs/teamwork

Kit aberto e grátis do [INEMA.CLUB](https://inema.club). Licença MIT.
