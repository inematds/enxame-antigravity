# Tarefa
Rodar o pytest no repositório, separar os testes que falham por pacote e consertar cada pacote sem apagar nenhum assert.

## Como verificar
- comando: `pytest -q`

## Peças

### @conserta-pagamentos
- dono: `pagamentos/`
- não mexe: `clientes/`, `relatorios/`, `tests/` de outros pacotes
- pronto quando: `pytest -q pagamentos` passa sem apagar nem afrouxar nenhum assert

### @conserta-clientes
- dono: `clientes/`
- não mexe: `pagamentos/`, `relatorios/`, `tests/` de outros pacotes
- pronto quando: `pytest -q clientes` passa sem apagar nem afrouxar nenhum assert

### @conserta-relatorios
- dono: `relatorios/`
- não mexe: `pagamentos/`, `clientes/`, `tests/` de outros pacotes
- pronto quando: `pytest -q relatorios` passa sem apagar nem afrouxar nenhum assert

## Verificador
- quantos: 1
- modelo: diferente dos workers
- roda: compara os diffs para achar assert apagado ou enfraquecido e roda de novo a suíte inteira com `pytest -q`

## Limites
- cota: um worker por pacote quebrado, no máximo 3; se a cota acabar, parar e me avisar
- parar: quando `pytest -q` passar inteiro ou depois de 2 rodadas sem melhora
- limpar workers: remover cada worker quando o pacote dele passar
- sem laço: nada de deixar o /swarm rodando em laço à noite
