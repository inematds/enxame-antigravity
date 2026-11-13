# Swarm Sheet — the Google Antigravity /swarm without the mess

[![Swarm Sheet](guia/assets/banner-en.jpg)](https://inematds.github.io/enxame-antigravity/guia/en/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## What it is

Do you still ask a single agent to do everything? Google Antigravity’s `/swarm` (app and CLI, in preview for Google AI Pro and Ultra) splits a task among several named agents who work at the same time, and adds a verifier to review and test their work. It works well only if the parts don’t get in each other’s way. The **Swarm Sheet** is a short worksheet you write before typing `/swarm`: who owns what, what each person must leave alone, when it’s done, who verifies, and when to stop. This kit includes the template, a checker that scores it from 0 to 8 and builds the text to paste, and a helper that tells you whether a swarm is the right choice. It only requires Python 3.

> **Important:** this kit **has not tested /swarm**. Antigravity is not installed on the machine where it was made. Everything about `/swarm` comes from the [official documentation](https://antigravity.google/docs/swarm). The “real outputs” in this repository are from `checar.py`, which only reads the sheet’s Markdown.

## 📖 User guide

Full guide (landing page + walkthrough): **https://inematds.github.io/enxame-antigravity/guia/en/**

🎬 Video: coming soon in the guide.

## The process, from start to finish

Who does what: 🧠 you · ⚙️ this kit’s script · 🤖 `/swarm` in Antigravity

| # | Step | Command | Who |
|---|---|---|---|
| 1 | Check whether this is a swarm case (or a subagent, `/boost`, `/teamwork`) | `python3 escolher.py` (questions) or `python3 escolher.py --divide-limpo sim` | 🧠 + ⚙️ |
| 2 | Copy the template and fill it in: task, how to verify, pieces, verifier, limits | `cp modelos/FICHA.md minha-ficha.md` | 🧠 |
| 3 | Check the sheet: 8 items, score 0–8, with reasons and fixes | `python3 checar.py minha-ficha.md` | ⚙️ |
| 4 | Fix the ✘ items and check again until the score is 7 or 8 | `python3 checar.py minha-ficha.md` | 🧠 |
| 5 | Generate the text ready to paste (PT; `--en` creates the outline in English). It only appears with a score ≥ 7; below that, it shows what to fix and exits with code 1 | `python3 checar.py minha-ficha.md --prompt` | ⚙️ |
| 6 | In Antigravity, paste the entire line (it already starts with `/swarm`). If the pasted command isn’t recognized, type `/swarm`, press Tab, and paste the rest | `/swarm …` | 🧠 |
| 7 | The coordinator splits the task, creates the workers with each one’s brief, and adds the `@verifier` | — | 🤖 |
| 8 | Follow the board and respond to approvals | app: Swarm panel (Board, Members, Graph) · CLI: `/swarm board`, Alt+S, Alt+J | 🧠 |
| 9 | The verifier reads the diffs and runs the command; the coordinator reports back | — | 🤖 |
| 10 | Run the “How to verify” command yourself and ask the coordinator to remove anyone who has finished | the command in your sheet | 🧠 |

Kit maintenance (when `checar.py` or an example changes):

```bash
python3 -m unittest -v
for d in calculadora-roi landing-page investigacao-lenta testes-por-pacote; do
  python3 checar.py exemplos/$d/ficha.md --prompt    > exemplos/$d/prompt.txt
  python3 checar.py exemplos/$d/ficha.md --prompt --en > exemplos/$d/prompt.en.txt
done
```

## What’s included

| File | Purpose |
|---|---|
| `modelos/FICHA.md` | Sheet template (plain Markdown, in PT) |
| `checar.py` | Checks 8 items, score 0–8; `--prompt` (only with a score ≥ 7), `--en`, `--json`; exits with 0 if the score is ≥ 7 |
| `escolher.py` | Subagent, `/boost`, `/swarm`, or `/teamwork`, based on the official table; flags or questions |
| `exemplos/` | 4 sheets scoring 8 (ROI calculator with 4 inputs, landing page, slow investigation, tests by package), one poor sheet, generated `prompt.txt` files, and `saidas.txt` |
| `CUIDADOS.md` (in Portuguese) | Quota, preview, worker without quota, removal is permanent, account-block report |
| `tests/` | `python3 -m unittest -v` |

## The 8 items checked by `checar.py`

1. Task written down.
2. “How to verify” with a command between backticks.
3. At least 2 pieces (with only one, use a single agent or a subagent).
4. Every piece has an owner (files and folders between backticks, or a question for an investigation).
5. Owners don’t overlap: same file, a folder containing another owner’s file, or a simple glob (pattern with `*`, such as `src/*.js`).
6. Every piece has “must not touch” and “done when” criteria.
7. Verifier with “runs”; warns if the ratio is missing (1 for every 2–4 pieces) or if the model differs from the workers’ model.
8. Quota and stopping limits, and no phrase asking for an unsupervised loop (a negation, “no loop,” passes).

Real output (from `checar.py`, not `/swarm`) for the poor example:

```text
✘ 5. Donos não se sobrepõem — colisão: @design `site/` × @textos `site/index.html`
   → como corrigir: Dê cada arquivo a uma peça só. Se duas precisam do mesmo arquivo, quebre o arquivo em partes, junte as duas peças numa só, ou peça cópias de trabalho (working copy) para cada worker.
Nota: 2/8 — ainda não: corrija os ✘ antes do /swarm
```

All outputs: [`exemplos/saidas.txt`](exemplos/saidas.txt) (in Portuguese).

**About `--en`:** only the text outline (“Give each piece its own worker”, “Add 1 verifier…”) is in English; what you wrote in the sheet stays as is.

## Sources

- Official `/swarm` documentation: https://antigravity.google/docs/swarm
- Commands (`/boost`, `/teamwork`, and others): https://antigravity.google/docs/slash-commands
- `/teamwork`: https://antigravity.google/docs/teamwork

Open and free kit from [INEMA.CLUB](https://inema.club). MIT License.