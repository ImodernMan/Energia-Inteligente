# Relatório de testes automatizados — Energia Inteligente

- Data/hora: 2026-11-15T12:40:25-03:00
- Ambiente: cópia isolada Energia-Inteligente-lab-20261115
- Execução: API Spring Boot por HTTP local; roteiro Python padrão
- Porta: 18081
- Banco: test-data/automated-test.db (SQLite descartável)
- NVIDIA_API_KEY: removida do ambiente do processo; nenhum pedido externo enviado
- Segurança durante os testes: execução na cópia isolada; código de produção não foi alterado durante a rodada

## Resumo

- Aprovados: **10**
- Reprovados: **4**
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
| VAL-003 Usuário sem nome/e-mail | FAIL | HTTP 400/422 | esperado HTTP 400/422, recebido 200: {"id":1,"nome":null,"email":null} |
| VAL-004 Valores negativos na simulação | FAIL | HTTP 400/422 | esperado HTTP 400/422, recebido 200: {"id":2,"consumoMensal":-1.0,"areaDisponivel":-10.0,"investimento":-100.0,"localizacao":"DADOS NEGATIVOS TESTE","analiseIa":null} |
| ERR-001 Análise de simulação inexistente | FAIL | HTTP 404 | esperado HTTP 404, recebido 500: {"timestamp":"2026-11-15T15:40:25.620Z","status":500,"error":"Internal Server Error","path":"/api/simulacoes/987654321/analise"} |
| AI-001 Sem chave NVIDIA | FAIL | HTTP 424/503 controlado; sem tráfego externo | esperado HTTP 424/503 sem chave; recebido 500: {"timestamp":"2026-11-15T15:40:25.665Z","status":500,"error":"Internal Server Error","path":"/api/simulacoes/1/analise"} |

## Recomendações para falhas confirmadas

- Validação de entrada: adicionar spring-boot-starter-validation; criar DTOs com @NotBlank, @Email, @Positive ou @PositiveOrZero; usar @Valid nos endpoints. Não expor entidades JPA diretamente como DTOs.
- Recursos inexistentes: substituir RuntimeException genérica por ResponseStatusException com HttpStatus.NOT_FOUND (404), ou exceção de domínio mapeada num ControllerAdvice.
- Chave NVIDIA ausente: mapear configuração ausente para HTTP 503 (ou 424 conforme contrato), sem revelar detalhes internos ao cliente.
- Atualização de usuário: verificar a existência do ID antes do save; retornar 404 para ID inexistente se a intenção do endpoint PUT for atualizar apenas registros existentes.
- Integração externa: tratar timeout, erros 4xx/5xx e resposta vazia com mensagens controladas; testar o serviço com RestClient mockado, sem uma chave real.

## Evidências

- Banco de testes: test-data/automated-test.db
- Log do servidor: tests/backend-test.log
- A suíte reinicia a API para verificar persistência.

## Limitações

- A chamada real à NVIDIA não foi testada; nenhum segredo foi usado.
- Uma API hospedada não foi testada porque ainda não temos URL confirmada.
- Códigos HTTP 400/422, 404 e 424/503 são critérios de qualidade esperados nesta suíte.

## Plano de correção por arquivo

| Arquivo | Ajuste recomendado |
|---|---|
| src/main/java/com/energiainteligente/controller/UsuarioController.java | Receber um DTO validado; rejeitar nome vazio e e-mail ausente/inválido com @Valid e HTTP 400. |
| src/main/java/com/energiainteligente/controller/SimulacaoController.java | Receber DTO de simulação validado; impedir valores negativos e mapear ID inexistente para HTTP 404. |
| src/main/java/com/energiainteligente/model/Usuario.java e Simulacao.java (ou novos DTOs) | Definir regras de validação; preferir DTOs para entrada HTTP e manter entidades JPA separadas do contrato da API. |
| src/main/java/com/energiainteligente/service/InteligenciaArtificialService.java | Tratar ausência de NVIDIA_API_KEY como erro de configuração controlado, sem lançar RuntimeException genérica. |
| Novo ControllerAdvice (por exemplo, ApiExceptionHandler.java) | Centralizar mapeamento de erros de validação para 400, recurso inexistente para 404 e configuração externa indisponível para 503. |

### Ordem sugerida
1. Implementar DTOs e validação de usuário/simulação.
2. Corrigir o mapeamento de exceções para 404 e 503.
3. Acrescentar testes unitários para o serviço de IA usando mock, sem chave real e sem rede.
4. Executar novamente: python .\tests\test_api.py.
5. Só depois de aprovação, avaliar levar as correções para a branch de trabalho e abrir/atualizar o PR.
