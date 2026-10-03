# Inteligência Artificial — Energia-Inteligente

## 1. Objetivo da Inteligência Artificial

A Inteligência Artificial é um dos principais diferenciais do sistema Energia-Inteligente. Sua função é auxiliar usuários residenciais e de microempresas na análise de soluções de eficiência energética.

A IA recebe os dados cadastrados em uma simulação e gera uma análise sobre a viabilidade do investimento, considerando informações fornecidas pelo usuário.

## 2. API de Inteligência Artificial escolhida

A integração do MVP utiliza a **API da NVIDIA**, com o modelo **NVIDIA Nemotron 3 Super 120B**.

O modelo é acessado pelo Back-end Java + Spring Boot por meio de requisições HTTP.

A escolha permite que o processamento da Inteligência Artificial seja realizado por um serviço externo, mantendo essa responsabilidade separada do aplicativo móvel.

A chave utilizada para autenticação é armazenada em uma variável de ambiente chamada:

`NVIDIA_API_KEY`

Dessa forma, a chave não precisa ser armazenada diretamente no código-fonte ou enviada ao repositório.

## 3. Funcionamento da IA no sistema

A análise de Inteligência Artificial utiliza uma simulação previamente cadastrada no sistema.

A simulação contém atualmente informações como:

- Consumo mensal de energia;
- Área disponível;
- Valor disponível para investimento;
- Localização.

O Back-end recupera esses dados e constrói um prompt que é enviado ao modelo Nemotron.

A IA recebe essas informações e produz uma análise textual simplificada sobre a possível viabilidade do investimento energético.

A resposta gerada é retornada pelo Back-end e também armazenada junto à simulação.

## 4. Tecnologias utilizadas na integração

| Componente | Tecnologia |
| --- | --- |
| Aplicativo móvel | Dart + Flutter |
| Back-end | Java + Spring Boot |
| Comunicação | REST HTTP / JSON |
| Banco de dados | SQLite |
| Inteligência Artificial | NVIDIA Nemotron 3 Super 120B |
| API externa | NVIDIA API |

## 5. Fluxo de comunicação

O fluxo implementado para a análise com Inteligência Artificial é:

1. Uma simulação é cadastrada no sistema.
2. O Back-end armazena a simulação no banco SQLite.
3. Uma requisição de análise é realizada utilizando o ID da simulação.
4. O Back-end recupera a simulação cadastrada.
5. O `InteligenciaArtificialService` prepara um prompt utilizando os dados da simulação.
6. O Back-end envia o prompt para a API da NVIDIA.
7. O modelo Nemotron processa os dados e gera uma análise.
8. O Back-end recebe e extrai o conteúdo da resposta.
9. A análise é armazenada no campo `analiseIa` da simulação.
10. A análise é retornada como resposta da API.

O endpoint implementado para solicitar uma análise é:

`POST /api/simulacoes/{id}/analise`

## 6. Responsabilidade do Back-end

A integração com a Inteligência Artificial é realizada pelo Back-end Java + Spring Boot.

O Back-end é responsável por:

- Recuperar os dados da simulação;
- Preparar o prompt enviado à IA;
- Realizar a comunicação HTTP com a API da NVIDIA;
- Autenticar a requisição utilizando a API Key;
- Receber e processar a resposta do modelo;
- Armazenar a análise gerada;
- Retornar o resultado da análise.

A chave da NVIDIA não é armazenada diretamente no código. O sistema utiliza a variável de ambiente `NVIDIA_API_KEY`.

## 7. Persistência da análise

A entidade `Simulacao` possui o atributo:

`analiseIa`

Esse atributo é utilizado para armazenar a resposta gerada pelo modelo de Inteligência Artificial.

Após a resposta do Nemotron, o Back-end associa a análise à simulação correspondente e utiliza o repositório para atualizar os dados no SQLite.

Dessa forma, a análise não existe apenas durante a requisição HTTP, permanecendo registrada no sistema.

## 8. Considerações sobre o MVP

A integração atual foi desenvolvida para atender ao escopo inicial do MVP.

A análise gerada pela IA possui caráter estimativo. Valores como geração de energia, economia financeira e tempo de retorno podem ser estimados pelo modelo a partir das informações fornecidas e não devem ser considerados cálculos técnicos definitivos.

Em versões futuras, o sistema poderá utilizar dados adicionais e fontes especializadas para fornecer cálculos energéticos mais precisos, utilizando a IA principalmente para interpretação e apresentação dos resultados.

## 9. Status da implementação

**Status: Integração funcional no Back-end.**

Atualmente, o sistema é capaz de:

- Cadastrar uma simulação;
- Recuperar uma simulação pelo ID;
- Enviar seus dados para o NVIDIA Nemotron;
- Receber uma análise gerada pela IA;
- Retornar a análise pela API;
- Armazenar a resposta no banco de dados SQLite.

A integração foi testada por meio do endpoint REST do Back-end.
