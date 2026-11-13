# CLAUDE.md — enxame-antigravity

Kit "Ficha do Enxame" + guia para o `/swarm` do Google Antigravity. Python 3, só biblioteca padrão.

- Testes: `python3 -m unittest -v` (todos passam antes de commitar).
- Mudou `checar.py` ou uma ficha de `exemplos/`: regenere `exemplos/*/prompt.txt`, `prompt.en.txt` e `exemplos/saidas.txt` (comandos no README, passo 7).
- **Regra dura:** nós não temos o Antigravity instalado e não testamos o `/swarm`. Nada no kit, README ou guia diz ou insinua o contrário. Fonte = documentação oficial (https://antigravity.google/docs/swarm). Relato de terceiro aparece como "relato", sem nome de criador, canal ou comunidade.
- Guia em `guia/` (PT) + `guia/en/` + `guia/es/`; tradução pelo `inema-traduz`. Commits como `inematds <inematds@gmail.com>`.

## Self-learning

Quando o Nei corrigir algo, ou você perceber um erro seu: antes de continuar, acrescente a lição como uma linha no TOPO de `## Lessons`.

## Lessons

- 13/11/2026: o modelo da ficha pede "nada de laço sem supervisão"; o detector do item 8 precisa aceitar a negação, senão reprova o próprio modelo (teste `test_negacao_do_laco_passa`).
