# Tarefa
Melhorar a página inicial do site: visual mais limpo, textos mais claros e o formulário de contato funcionando.

## Como verificar
- comando: `npm test`

## Peças

### @visual
- dono: `site/estilo.css`
- não mexe: `site/index.html`, `site/contato.js`, `tests/`
- pronto quando: a página fica legível em 360 px de largura e o contraste do texto passa no teste de acessibilidade

### @textos
- dono: `site/index.html`
- não mexe: `site/estilo.css`, `site/contato.js`
- pronto quando: título, subtítulo e botões dizem em uma frase o que o site oferece, sem mudar os ids do formulário

### @formulario
- dono: `site/contato.js`, `tests/contato.test.js`
- não mexe: `site/index.html`, `site/estilo.css`
- pronto quando: o formulário valida nome e e-mail, mostra o erro ao lado do campo, e `npm test` passa

## Verificador
- quantos: 1
- modelo: diferente dos workers
- roda: lê os 3 diffs, confere que ninguém editou arquivo de outra peça e roda `npm test`

## Limites
- cota: só 3 workers e 1 verificador; se a cota acabar, parar e me avisar
- parar: quando `npm test` passar e o verificador aprovar, ou depois de 2 rodadas de correção
- limpar workers: remover os workers depois que entregarem as mudanças
- sem laço: nada de rodar /swarm em laço ou sem eu olhar o quadro
