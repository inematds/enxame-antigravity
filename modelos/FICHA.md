# Tarefa
<o que você quer pronto, em uma ou duas frases>

## Como verificar
- comando: `<o comando que prova que deu certo, ex.: npm test>`

## Peças
<!-- Uma subseção por worker. Arquivos e pastas sempre entre crases. Dono pode ser uma pergunta (sem crases), para investigação. -->

### @primeira-peca
- dono: `<arquivo ou pasta que só esta peça edita>`
- não mexe: `<arquivos das outras peças>`
- pronto quando: <o teste ou o sinal de fim desta peça>

### @segunda-peca
- dono: `<outro arquivo ou pasta>`
- não mexe: `<arquivos das outras peças>`
- pronto quando: <o teste ou o sinal de fim desta peça>

## Verificador
- quantos: 1  <!-- 1 para cada 2 a 4 peças -->
- modelo: diferente dos workers
- roda: <o que ele revisa e roda, ex.: lê os diffs e roda `npm test`>

## Limites
- cota: <quanto aceita gastar; cada worker é um agente e gasta cota>
- parar: <quando parar, ex.: quando o comando passar ou depois de 2 rodadas de correção>
- limpar workers: remover os workers que acabaram, depois de entregarem as mudanças
- sem laço: nada de rodar /swarm em laço, à noite ou sem você olhando o quadro

## Modelo dos workers
- <opcional: o mesmo da conversa, ou outro que você escolhe no seletor de modelo>
