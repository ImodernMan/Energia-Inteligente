# Relatório de testes automatizados — Energia Inteligente

- Data/hora: 2026-11-15T12:57:18-03:00
- Ambiente: Energia-Inteligente
- Execução: API Spring Boot por HTTP local; roteiro Python padrão
- Porta: 18081
- Banco: test-data/automated-test.db (SQLite descartável)
- NVIDIA_API_KEY: removida do ambiente do processo; nenhum pedido externo enviado
- Banco original (energia-inteligente.db): não utilizado; execução usou apenas test-data/automated-test.db.

## Resumo

- Aprovados: **14**
- Reprovados: **0**
- Erros de execução: **0**
- Total: **14**

## Resultado por caso

| Caso | Resultado | Esperado | Observado |
|---|---|---|---|
| API-001 Saúde GET /api/teste | PASS | HTTP 200 | HTTP 200 |
| SIM-001 Criar simulação | PASS | HTTP 2xx e ID | criada simulação ID 1 |
| SIM-002 Listar simulações | PASS | simulação criada encontrada | simulação encontrada |
| DB-001 Persistência após reiniciar API | PASS | registro permanece | registro preservado após reinício |
| USR-001 Criar usuário | PASS | HTTP 2xx e ID | criado usuário ID 1 |
| USR-002 Listar usuários | PASS | usuário encontrado | usuário encontrado |
| USR-003 Atualizar usuário | PASS | campos atualizados | nome e e-mail atualizados |
| USR-004 Excluir usuário | PASS | usuário removido | usuário removido e ausência confirmada |
| VAL-001 JSON malformado | PASS | HTTP 400 | HTTP 400 |
| VAL-002 Simulação sem campos obrigatórios | PASS | HTTP 400/422 | HTTP 400 |
| VAL-003 Usuário sem nome/e-mail | PASS | HTTP 400/422 | HTTP 400 |
| VAL-004 Valores negativos na simulação | PASS | HTTP 400/422 | HTTP 400 |
| ERR-001 Análise de simulação inexistente | PASS | HTTP 404 | HTTP 404 |
| AI-001 Sem chave NVIDIA | PASS | HTTP 424/503 controlado; sem tráfego externo | HTTP 503 sem chave, sem chamada externa |

## Correções implementadas e aprovadas

- VAL-003 — Usuário: adicionados @NotBlank, @Email e @Valid; cadastro sem nome/e-mail agora retorna HTTP 400.
- VAL-004 — Simulação: adicionados @PositiveOrZero, @NotBlank e @Valid; valores negativos ou localização vazia agora retornam HTTP 400.
- ERR-001 — Simulação inexistente: RuntimeException genérica substituída por ResponseStatusException com HTTP 404.
- AI-001 — Chave NVIDIA ausente: erro mapeado para HTTP 503; nenhuma chamada externa é feita sem a credencial.

## Melhorias futuras fora do escopo destes 14 casos

- Validar se o usuário existe antes de executar PUT, retornando 404 quando o ID não existir.
- Tratar timeout, respostas 4xx/5xx e corpo inesperado do provedor NVIDIA; acrescentar testes unitários com RestClient mockado.

## Evidências

- Banco de testes: test-data/automated-test.db
- Log do servidor: tests/backend-test.log
- A suíte reinicia a API para verificar persistência.

## Limitações

- A chamada real à NVIDIA não foi testada; nenhum segredo foi usado.
- Uma API hospedada não foi testada porque ainda não temos URL confirmada.
- Códigos HTTP 400/422, 404 e 424/503 são critérios de qualidade esperados nesta suíte.
