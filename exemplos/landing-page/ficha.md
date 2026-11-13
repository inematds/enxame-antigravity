# Tarefa
Montar a landing page de um curso grátis em `site/`, com cabeçalho, benefícios, formulário de inscrição, depoimentos, perguntas frequentes e botões de chamada; cada seção num arquivo próprio e uma página que junta tudo.

## Como verificar
- comando: `python3 tests/checar_site.py site/`

## Peças

### @cabecalho
- dono: `site/partes/cabecalho.html`
- não mexe: `site/partes/beneficios.html`, `site/partes/formulario.html`, `site/partes/depoimentos.html`, `site/partes/faq.html`, `site/partes/botoes.html`, `site/index.html`, `site/estilo.css`
- pronto quando: título, uma frase de promessa e o menu com âncoras para as outras seções

### @beneficios
- dono: `site/partes/beneficios.html`
- não mexe: as outras partes, `site/index.html`, `site/estilo.css`
- pronto quando: 4 benefícios curtos, cada um com título e uma frase

### @formulario
- dono: `site/partes/formulario.html`, `site/form.js`
- não mexe: as outras partes, `site/index.html`, `site/estilo.css`
- pronto quando: campos nome e e-mail obrigatórios, e-mail validado em `site/form.js`, mensagem de obrigado sem enviar para nenhum servidor

### @depoimentos
- dono: `site/partes/depoimentos.html`
- não mexe: as outras partes, `site/index.html`, `site/estilo.css`
- pronto quando: 3 depoimentos marcados como exemplo (texto de demonstração, sem nome de pessoa real)

### @faq
- dono: `site/partes/faq.html`
- não mexe: as outras partes, `site/index.html`, `site/estilo.css`
- pronto quando: 5 perguntas em `<details>`, que abrem e fecham sem JavaScript

### @montagem
- dono: `site/index.html`, `site/estilo.css`, `site/partes/botoes.html`
- não mexe: `site/partes/cabecalho.html`, `site/partes/beneficios.html`, `site/partes/formulario.html`, `site/partes/depoimentos.html`, `site/partes/faq.html`, `site/form.js`
- pronto quando: `site/index.html` inclui as 6 partes na ordem, os botões levam ao formulário e a página não tem rolagem lateral em 360 px
- cópia de trabalho: sim, para montar sem atrapalhar as outras peças

## Verificador
- quantos: 2
- modelo: diferente dos workers
- roda: um revisa as partes de conteúdo e o outro a montagem; os dois rodam `python3 tests/checar_site.py site/` e devolvem os problemas para o dono da parte

## Limites
- cota: 6 workers e 2 verificadores no máximo; se algum ficar sem cota, parar e me avisar em vez de criar outro
- parar: quando o teste do site passar e os 2 verificadores aprovarem
- limpar workers: cada worker entrega as mudanças da cópia de trabalho antes de ser removido
- sem laço: nada de repetir o /swarm sozinho; eu acompanho pelo quadro
