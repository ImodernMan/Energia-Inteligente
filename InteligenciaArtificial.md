# Inteligência Artificial — Energia-Inteligente

## 1. Objetivo da Inteligência Artificial

A Inteligência Artificial será um dos principais diferenciais do sistema Energia-Inteligente. Sua função será auxiliar usuários residenciais e de microempresas na análise de soluções de eficiência energética.

A IA receberá dados relacionados às consultas realizadas pelos usuários e poderá gerar análises personalizadas sobre investimento, economia e viabilidade de soluções energéticas.

## 2. API de Inteligência Artificial escolhida

A API escolhida para a integração inicial é a **Google Gemini API**, um serviço externo de Inteligência Artificial generativa.

A escolha considera a possibilidade de integração com o Back-end Java + Spring Boot por meio de requisições HTTP, além da disponibilidade de um nível gratuito para desenvolvimento e testes, respeitando os limites e condições da plataforma.

Documentação oficial: https://ai.google.dev/

## 3. Funcionamento da IA no sistema

O usuário informará os dados necessários para realizar uma consulta de eficiência energética. Essas informações serão encaminhadas ao Back-end, que ficará responsável por processar os dados e realizar a comunicação com a API de Inteligência Artificial.

A IA poderá auxiliar na interpretação dos dados e na geração de recomendações personalizadas, considerando informações como:

* Investimento estimado.
* Economia de energia.
* Viabilidade da solução.
* Características informadas pelo usuário.
* Estimativas de retorno financeiro.

## 4. Tecnologias utilizadas na integração

| Componente              | Tecnologia         |
| ----------------------- | ------------------ |
| Aplicativo móvel        | Dart + Flutter     |
| Back-end                | Java + Spring Boot |
| Comunicação             | REST HTTP / JSON   |
| Banco de dados          | SQLite             |
| Inteligência Artificial | Google Gemini API  |

## 5. Fluxo de comunicação

O fluxo planejado para a integração será:

1. O usuário informa os dados da consulta no aplicativo Flutter.
2. O aplicativo envia os dados para a API Back-end utilizando REST HTTP.
3. O Back-end processa os dados recebidos.
4. O Back-end envia uma solicitação para a Google Gemini API.
5. A API de IA retorna uma análise.
6. O Back-end organiza a resposta e envia o resultado para o aplicativo.

## 6. Responsabilidade do Back-end

A integração com a Inteligência Artificial será realizada pelo Back-end Java + Spring Boot.

O Back-end será responsável por:

* Receber e validar os dados enviados pelo aplicativo.
* Preparar as informações para a análise da IA.
* Realizar a comunicação com a API externa.
* Processar e organizar a resposta recebida.
* Retornar o resultado para o aplicativo móvel.

A chave de API deverá ser mantida no Back-end, evitando sua exposição no aplicativo Flutter.

## 7. Considerações sobre o MVP

A integração com a Inteligência Artificial será planejada inicialmente para atender às necessidades do MVP do Energia-Inteligente.

O objetivo é utilizar a IA como apoio à análise das consultas de eficiência energética, mantendo a possibilidade de evolução futura do sistema.

A implementação deverá considerar os limites de utilização da API, a segurança da chave de acesso e a validação das respostas geradas.

## 8. Status da implementação

**Status:** Planejamento arquitetural.

A integração com a Google Gemini API está definida como proposta para o sistema, mas sua implementação ainda será realizada nas próximas etapas do projeto.
