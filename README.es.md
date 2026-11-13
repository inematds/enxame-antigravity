# Ficha del Enjambre — /swarm de Google Antigravity sin caos

[![Ficha del Enjambre](guia/assets/banner-es.jpg)](https://inematds.github.io/enxame-antigravity/guia/es/)

**🇧🇷 [Português](README.md) · 🇺🇸 [English](README.en.md) · 🇪🇸 [Español](README.es.md)**

## Qué es

¿Todavía le pides todo a un solo agente? El `/swarm` de Google Antigravity (app y CLI, en vista previa para Google AI Pro y Ultra) divide una tarea entre varios agentes con nombre, que trabajan al mismo tiempo, y asigna un verificador para revisar y probar. Solo funciona bien si las partes no se pisan entre sí. La **Ficha del Enjambre** es una hoja breve que escribes antes de introducir `/swarm`: quién es responsable de cada cosa, qué no toca cada agente, cuándo está listo, quién verifica y cuándo parar. Este kit incluye la plantilla, un verificador que puntúa de 0 a 8 y prepara el texto para pegar, y una ayuda que indica si el caso realmente requiere un enjambre. Solo necesitas Python 3.

> **Importante:** este kit **no ha probado /swarm**. Antigravity no está instalado en la máquina donde se creó. Todo lo relacionado con `/swarm` proviene de la [documentación oficial](https://antigravity.google/docs/swarm). Las «salidas reales» de este repositorio son de `checar.py`, que solo lee el Markdown de la ficha.

## 📖 Guía de uso

Guía completa (landing + paso a paso): **https://inematds.github.io/enxame-antigravity/guia/es/**

🎬 Vídeo: pronto en la guía.

## El proceso, de principio a fin

Quién hace qué: 🧠 tú · ⚙️ script de este kit · 🤖 `/swarm` en Antigravity

| # | Paso | Comando | Quién |
|---|---|---|---|
| 1 | Ver si el caso requiere un enjambre (o un subagente, `/boost`, `/teamwork`) | `python3 escolher.py` (preguntas) o `python3 escolher.py --divide-limpo sim` | 🧠 + ⚙️ |
| 2 | Copiar la plantilla y completar: tarea, cómo verificar, partes, verificador, límites | `cp modelos/FICHA.md minha-ficha.md` | 🧠 |
| 3 | Revisar la ficha: 8 elementos, puntuación de 0–8, con el motivo y cómo corregirlo | `python3 checar.py minha-ficha.md` | ⚙️ |
| 4 | Corregir los ✘ y volver a revisar hasta obtener una puntuación de 7 u 8 | `python3 checar.py minha-ficha.md` | 🧠 |
| 5 | Generar el texto listo para pegar (PT; `--en` genera el esqueleto en inglés). Solo se genera con una puntuación ≥ 7; por debajo, muestra qué corregir y termina con código 1 | `python3 checar.py minha-ficha.md --prompt` | ⚙️ |
| 6 | En Antigravity, pegar la línea completa (ya empieza con `/swarm`). Si no reconoce el comando pegado, escribir `/swarm`, Tab y pegar el resto | `/swarm …` | 🧠 |
| 7 | El coordinador divide la tarea, crea los workers con el brief de cada uno y el `@verifier` | — | 🤖 |
| 8 | Seguir el tablero y responder a las solicitudes de aprobación | app: panel Swarm (Board, Members, Graph) · CLI: `/swarm board`, Alt+S, Alt+J | 🧠 |
| 9 | El verificador lee los diffs y ejecuta el comando; el coordinador informa del resultado | — | 🤖 |
| 10 | Ejecutar por tu cuenta el comando de «Cómo verificar» y pedir al coordinador que retire a quienes hayan terminado | el comando de tu ficha | 🧠 |

Mantenimiento del kit (cuando cambie `checar.py` o un ejemplo):

```bash
python3 -m unittest -v
for d in calculadora-roi landing-page investigacao-lenta testes-por-pacote; do
  python3 checar.py exemplos/$d/ficha.md --prompt    > exemplos/$d/prompt.txt
  python3 checar.py exemplos/$d/ficha.md --prompt --en > exemplos/$d/prompt.en.txt
done
```

## Qué contiene

| Archivo | Para qué sirve |
|---|---|
| `modelos/FICHA.md` | Plantilla de la ficha (Markdown sencillo, en PT) |
| `checar.py` | Revisa 8 elementos, puntúa de 0 a 8; `--prompt` (solo con puntuación ≥ 7), `--en`, `--json`; termina con código 0 si la puntuación es ≥ 7 |
| `escolher.py` | Subagente, `/boost`, `/swarm` o `/teamwork`, según la tabla oficial; con flags o preguntas |
| `exemplos/` | 4 fichas con puntuación 8 (calculadora de ROI con 4 entradas, landing page, investigación lenta, pruebas por paquete), una ficha deficiente, los `prompt.txt` generados y `saidas.txt` |
| `CUIDADOS.md` (en portugués) | Cuota, vista previa, worker sin cuota, la retirada es permanente, relato de bloqueo de cuenta |
| `tests/` | `python3 -m unittest -v` |

## Los 8 elementos de `checar.py`

1. La tarea está escrita.
2. «Cómo verificar» incluye un comando entre acentos graves.
3. Al menos 2 partes (con una sola, usa un agente o un subagente).
4. Cada parte tiene una persona responsable (archivos y carpetas entre acentos graves, o una pregunta para una investigación).
5. Las responsabilidades no se superponen: mismo archivo, carpeta que contiene el archivo de otra parte, patrón glob simple (con `*`, como `src/*.js`).
6. Cada parte incluye «no tocar» y «listo cuando».
7. El verificador incluye «ejecuta»; avisa si falta una proporción adecuada (1 por cada 2–4 partes) o si el modelo no es distinto del de los workers.
8. Límites de cuota y de parada, y ninguna frase que pida un bucle sin supervisión (la negación, «nada de bucles», sí cuenta).

Salida real (de `checar.py`, no de `/swarm`) en el ejemplo deficiente:

```text
✘ 5. Donos não se sobrepõem — colisão: @design `site/` × @textos `site/index.html`
   → como corrigir: Dê cada arquivo a uma peça só. Se duas precisam do mesmo arquivo, quebre o arquivo em partes, junte as duas peças numa só, ou peça cópias de trabalho (working copy) para cada worker.
Nota: 2/8 — ainda não: corrija os ✘ antes do /swarm
```

Todas las salidas: [`exemplos/saidas.txt`](exemplos/saidas.txt) (en portugués).

**Sobre `--en`:** solo el esqueleto del texto («Give each piece its own worker», «Add 1 verifier…») sale en inglés; lo que escribiste en la ficha se mantiene tal como está.

## Fuentes

- Documentación oficial de `/swarm`: https://antigravity.google/docs/swarm
- Comandos (`/boost`, `/teamwork` y otros): https://antigravity.google/docs/slash-commands
- `/teamwork`: https://antigravity.google/docs/teamwork

Kit abierto y gratuito de [INEMA.CLUB](https://inema.club). Licencia MIT.