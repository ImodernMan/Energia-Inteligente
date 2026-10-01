# Energia-Inteligente

## ODS 7 — Energia Limpa e Acessível

### Sobre o projeto

Nosso projeto tem como objetivo desenvolver um aplicativo mobile híbrido voltado para a análise da viabilidade de implantação de fontes alternativas de energia em residências e microempresas, contribuindo para o ODS 7 — Energia Limpa e Acessível.

### Problema

Muitas residências e microempresas não possuem uma ferramenta acessível que permita analisar a viabilidade da implantação de uma fonte alternativa de geração de energia, considerando fatores como consumo, localização, área disponível, investimento e expectativas de economia.

### Público-alvo

Usuários residenciais e microempresariais que desejam simular e analisar a viabilidade da implantação de uma fonte alternativa de geração de energia.

### Solução proposta

O sistema será um aplicativo mobile híbrido que permitirá ao usuário informar dados e expectativas relacionadas à implantação de uma fonte alternativa de energia. Essas informações serão utilizadas pelo sistema para realizar uma análise personalizada, com o auxílio de Inteligência Artificial, considerando os dados fornecidos pelo usuário e informações externas relevantes.

A solução terá como objetivo apresentar uma análise de viabilidade, estimativas e recomendações personalizadas para cada cenário.

### Inteligência Artificial

A Inteligência Artificial será um dos componentes centrais do sistema. A partir dos dados fornecidos pelo usuário e de informações complementares obtidas pelo sistema, a IA realizará uma análise personalizada de cada cenário.

A IA será responsável por interpretar as informações disponíveis, gerar uma classificação de viabilidade, apresentar uma justificativa para a análise e produzir recomendações para o usuário.

A arquitetura também permitirá futuras expansões, como a utilização de novas fontes de dados, diferentes tipos de energia e novos critérios de análise.

### Funcionalidades do MVP

1. Consulta de viabilidade de implantação;
2. Análise personalizada do cenário informado;
3. Geração de recomendações utilizando Inteligência Artificial;
4. Apresentação da justificativa da análise realizada pela IA.

### Principais Classes do Sistema

As principais classes do Energia Inteligente organizam o funcionamento do sistema. Usuario e Simulacao armazenam os dados, os Repositories cuidam do banco de dados, os Controllers fazem a comunicação com o aplicativo e o GeminiService integra a Inteligência Artificial para analisar as simulações e gerar recomendações.

### Tecnologias

- Java
- Spring Boot
- Banco de dados SQL
- Git
- GitHub
- Aplicativo mobile híbrido
- Inteligência Artificial

## Arquitetura

### C4 Nível 1 — Contexto do Sistema

![Diagrama C4 Nível 1](Energia%20Inteligente%20Sistema-2026-09-16-001915.png)

O diagrama de contexto apresenta uma visão geral do sistema Energia Inteligente, mostrando o usuário residencial ou microempresa como principal usuário da aplicação e a integração do sistema com a API externa de Inteligência Artificial Google Gemini API.

### C4 Nível 2 — Contêineres

![Diagrama C4 Nível 2](Energia%20Inteligente-2026-09-16-001959.png)

O diagrama de contêineres detalha os principais componentes do sistema Energia Inteligente: aplicativo mobile desenvolvido com Flutter/Dart, API back-end desenvolvida em Java/Spring Boot e banco de dados SQLite. O back-end realiza a comunicação com a API externa Google Gemini API para análise dos dados e geração de recomendações. A comunicação entre o aplicativo e o back-end ocorre por REST/HTTP utilizando JSON.

### Diagrama de Banco de Dados / Entidades

![Diagrama de Banco de Dados](a_clean_white_background_diagram_image_with_a_min.png -->)

O diagrama de banco de dados apresenta as principais entidades utilizadas pelo sistema Energia Inteligente e a forma como elas se relacionam. A entidade Usuário armazena os dados básicos de quem utiliza o sistema, podendo estar relacionada a um ou mais registros de Simulação.
A entidade Simulação armazena as informações utilizadas para realizar a análise de viabilidade, como tipo de energia, consumo mensal, área disponível, investimento estimado, economia estimada e o status da análise. Cada simulação também pode gerar um Resultado de IA, contendo a classificação de viabilidade, justificativa, recomendações e a data da análise.
O sistema também possui a entidade Endereço, responsável por armazenar os dados de localização do usuário, como logradouro, número, bairro, cidade, estado e CEP. Esse cadastro é opcional e pode ser utilizado para complementar as informações da simulação.
A entidade Recomendação representa as orientações geradas a partir da análise realizada pelo sistema. Essas recomendações possuem informações como título, descrição e prioridade, podendo utilizar Critérios de Análise para definir os parâmetros considerados durante a avaliação.
Por fim, a entidade Fonte de Dados Externa representa informações obtidas de fontes externas, como dados de clima, tarifas e incentivos. Essas informações podem ser utilizadas como apoio para melhorar a análise e gerar recomendações mais adequadas para cada cenário.


### Tecnologias e responsabilidades

- **Flutter/Dart:** desenvolvimento do aplicativo mobile e interface do usuário.
- **Java/Spring Boot:** desenvolvimento do back-end, regras de negócio e integração com a API de Inteligência Artificial.
- **SQLite:** armazenamento e persistência dos dados do sistema.
- **Google Gemini API:** análise dos dados e geração de recomendações utilizando Inteligência Artificial.
- **REST/HTTP + JSON:** comunicação entre o aplicativo mobile e a API back-end.

### Integrantes

1. Luiz Paulo Fernandes
2. Guilherme Alexandre Batista
3. Pamela Almeida dos Santos
4. Cauã Silva Rocha
5. Jhonatas Felipe Lopes Ribeiro
6. Diego Silva da Costa
7. Matheus Henrique Alves Soares
8. Pedro Henrique dos Santos de Carvalho
