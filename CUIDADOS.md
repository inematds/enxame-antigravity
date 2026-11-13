# Cuidados antes de usar o /swarm

Base: documentação oficial do Google Antigravity (https://antigravity.google/docs/swarm), lida em 13/11/2026.
Este kit **não testou o /swarm**: o Antigravity não está instalado na máquina onde o kit foi feito. Os cuidados abaixo vêm da documentação e, onde está escrito "relato", de terceiros.

## O que a documentação oficial diz

1. **Cota.** Cada worker é um agente próprio, então um enxame gasta cota muito mais rápido que uma conversa. Pela nossa conta, três workers, um verificador e o monitor já são cinco agentes, não um.
2. **Prévia, só Pro e Ultra.** O `/swarm` está em prévia (preview) e só aparece nos planos Google AI Pro e Google AI Ultra, no app e na CLI. Pode mudar.
3. **Worker sem cota pausa e não volta sozinho.** Você vê o erro de cota uma vez; o membro fica parado até ter um post novo no quadro, alguém trocar o modelo dele ou você mandar mensagem. Ele não reinicia quando a cota renova.
4. **Remover é permanente.** Um worker removido (Killed) não volta; o coordenador cria outro. Remover também apaga a cópia de trabalho dele, por isso ele precisa entregar as mudanças antes.
5. **Quem espera não gasta.** Worker sem tarefa dorme no quadro sem usar tokens e acorda quando alguém o menciona. Você não precisa parar todos, mas pode pedir ao coordenador para remover quem já terminou.
6. **Verificador.** O coordenador costuma pôr 1 `@verifier` para cada 2 a 4 workers. Dá para pedir que ele rode em outro modelo ("run the verifier on a different model than the workers"), desde que seja um modelo que você pode escolher no seletor.

## Relato (não é fato nosso)

Um usuário relatou que a conta do Gemini/Antigravity foi **bloqueada em minutos** quando outro agente disparou dezenas de sessões sem supervisão, em segundos. Segundo o mesmo relato, a conta voltou depois de um recurso automático, em poucas horas.

A resposta citada no fórum do Google: uso automatizado é permitido e desconta da cota, mas **laços de fundo sem supervisão, em alto volume**, podem acionar a proteção antiabuso.

Não reproduzimos esse caso. Ele está aqui como alerta, não como medição.

## Recomendação

- **Comece pequeno:** 2 ou 3 peças e 1 verificador. Aumente só depois de ver como a cota se comporta na sua conta.
- **Acompanhe o quadro:** no app, painel Swarm (abas Board, Members e Graph); na CLI, `/swarm board` ou Alt+S.
- **Escreva os limites na ficha:** quanto de cota aceita gastar, quando parar, quando remover os workers. O `checar.py` reprova a ficha sem isso (item 8).
- **Nada de rodar enxames em laço noturno**, por agendamento ou disparados por outro agente sem você olhando. O `checar.py` reprova frases que pedem isso.
- **Peça uma prova:** `## Como verificar` com um comando. Sem comando, o verificador não tem o que rodar.
