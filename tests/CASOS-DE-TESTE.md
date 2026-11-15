# Casos de teste automatizados — Energia Inteligente

## Objetivo
Testar os endpoints REST, operações CRUD, persistência SQLite e respostas de erro sem chave NVIDIA.

## Matriz de casos

| ID | Caso | Resultado esperado |
|---|---|---|
| API-001 | GET /api/teste | HTTP 200 e mensagem de funcionamento |
| SIM-001 | POST /api/simulacoes com dados válidos | HTTP 2xx, ID gerado e campos corretos |
| SIM-002 | GET /api/simulacoes | Registro criado aparece na lista |
| DB-001 | Reiniciar a API e consultar novamente | Registro continua gravado no SQLite |
| USR-001 | POST /api/usuarios com dados válidos | HTTP 2xx e ID gerado |
| USR-002 | GET /api/usuarios | Usuário aparece na lista |
| USR-003 | PUT /api/usuarios/{id} | Nome e e-mail atualizados |
| USR-004 | DELETE /api/usuarios/{id} | Usuário removido |
| VAL-001 | Enviar JSON malformado | HTTP 400 |
| VAL-002 | Criar simulação sem campos obrigatórios | HTTP 400 ou 422 |
| VAL-003 | Criar usuário sem nome e e-mail | HTTP 400 ou 422 |
| VAL-004 | Criar simulação com valores negativos | HTTP 400 ou 422 |
| ERR-001 | Solicitar análise de ID inexistente | HTTP 404 |
| AI-001 | Solicitar análise sem NVIDIA_API_KEY | HTTP 424 ou 503 controlado, sem chamada externa |

## Como executar

Na pasta de laboratório, abra PowerShell e rode:

    .\mvnw.cmd -B -DskipTests package
    python .\tests\test_api.py

O script:
- inicia o JAR na porta local 18081;
- remove NVIDIA_API_KEY apenas do ambiente do processo de teste;
- usa somente test-data/automated-test.db;
- reinicia a API para verificar persistência;
- encerra o servidor ao final;
- gera o relatório com aprovações, falhas e recomendações.

## Arquivos gerados
- tests/RELATORIO-TESTES.md — resultado e recomendações.
- tests/backend-test.log — log do servidor.
- test-data/automated-test.db — banco descartável da suíte.

Os critérios HTTP da matriz são expectativas de qualidade REST. Eles não significam que essas validações já existam no código atual.
