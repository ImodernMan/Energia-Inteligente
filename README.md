# Energia Inteligente

## ODS 7 — Energia Limpa e Acessível

O **Energia Inteligente** é um projeto acadêmico voltado a facilitar a avaliação de alternativas de geração de energia limpa para residências e microempresas. A proposta está alinhada ao **Objetivo de Desenvolvimento Sustentável 7 (ODS 7)**, que busca ampliar o acesso à energia limpa, confiável e sustentável.

## Sobre o projeto

O sistema busca ajudar o usuário a avaliar a viabilidade de uma alternativa energética a partir de informações como:

- Consumo mensal de energia;
- Área disponível para instalação;
- Valor disponível para investimento;
- Localização.

Com esses dados, o back-end recebe e armazena as simulações e pode realizar cálculos de viabilidade, apresentando estimativas que apoiem a tomada de decisão.

## Problema

Muitas residências e microempresas não possuem uma ferramenta acessível para organizar informações e avaliar se a implantação de uma 
fonte alternativa de energia pode ser viável para sua realidade

## Público-alvo

Usuários residenciais e microempresariais interessados em conhecer alternativas de energia limpa e avaliar cenários de investimento.

## Funcionalidades implementadas

- Cadastro de simulações com dados de consumo, área disponível, investimento e localização;
- Consulta das simulações cadastradas;
- Persistência dos dados em banco PostgreSQL na nuvem;
- Serviço de cálculo de viabilidade, com estimativas de economia e prazo de retorno do investimento;
- Aplicativo Flutter em desenvolvimento para consumir a API back-end.

> **Inteligência Artificial:** a integração com IA e a geração automatizada de recomendações fazem parte da evolução planejada do projeto. A disponibilidade dessa funcionalidade deve ser confirmada conforme a conclusão e integração do respectivo módulo.

## Arquitetura e tecnologias

O projeto está organizado em três partes principais:

1. **Aplicativo:** interface mobile desenvolvida com Flutter/Dart.
2. **Back-end:** API REST desenvolvida em Java com Spring Boot, responsável pelas regras de negócio e comunicação com o banco de dados.
3. **Banco de dados:** PostgreSQL hospedado no Supabase.

A comunicação entre o aplicativo e a API utiliza HTTP/REST e JSON.

### Tecnologias

| Tecnologia | Utilização |
|---|---|
| Java 17 | Linguagem do back-end |
| Spring Boot | Construção da API REST |
| Spring Data JPA | Persistência e acesso aos dados |
| PostgreSQL | Banco de dados relacional |
| Supabase | Hospedagem do banco de dados |
| Render | Hospedagem da API back-end |
| Flutter/Dart | Desenvolvimento do aplicativo |
| Git e GitHub | Versionamento e colaboração |

## API back-end

A API está hospedada no Render:

- **Endereço base:** https://energia-inteligente.onrender.com
- **Listar simulações:** GET https://energia-inteligente.onrender.com/api/simulacoes
- **Cadastrar simulação:** POST https://energia-inteligente.onrender.com/api/simulacoes

### Exemplo de cadastro

Envie uma requisição POST para `/api/simulacoes`, com o corpo JSON:

```json
{
  "consumoMensal": 350,
  "areaDisponivel": 40,
  "investimento": 20000,
  "localizacao": "Itaquaquecetuba-SP"
}
```

Os valores são apenas ilustrativos. A API utiliza as variáveis de ambiente `DB_URL`, `DB_USERNAME` e `DB_PASSWORD` para configurar a conexão com o PostgreSQL. Não armazene credenciais no repositório.

**Observação:** instâncias gratuitas do Render podem entrar em inatividade e levar alguns instantes para responder à primeira requisição após um período sem uso.

## Banco de dados

O banco utilizado no ambiente em nuvem é **PostgreSQL**, hospedado no **Supabase**. A aplicação Spring Boot acessa o banco por meio do Spring Data JPA e das configurações fornecidas por variáveis de ambiente.

## Arquitetura C4

### C4 Nível 1 — Contexto do sistema

![Diagrama C4 Nível 1](Energia%20Inteligente%20Sistema-2026-09-16-001915.png)

O diagrama apresenta o sistema e seus usuários externos. A representação da integração com Inteligência Artificial deve ser revisada para refletir o provedor e o estado atual do módulo.

### C4 Nível 2 — Contêineres

![Diagrama C4 Nível 2](Energia%20Inteligente-2026-09-16-001959.png)

O diagrama apresenta os principais contêineres da solução. **Atenção:** a versão atual da arquitetura utiliza Flutter/Dart no aplicativo, Java/Spring Boot na API e PostgreSQL no Supabase; referências antigas a SQLite ou a provedores anteriores de IA precisam ser atualizadas no diagrama.

## Modelo de dados

![Diagrama de Banco de Dados](https://github.com/user-attachments/assets/4ac6f4a1-176d-4ddf-a32e-f9f9774e1ae0)

O modelo conceitual apresenta entidades relacionadas a usuários, simulações, resultados de análise, endereços, recomendações, critérios de análise e fontes externas de dados. A implementação deve ser consultada no código do back-end para identificar quais entidades já estão efetivamente disponíveis.

## Como executar o back-end localmente

Pré-requisitos:

- JDK 17 ou compatível;
- Maven (ou o Maven Wrapper incluído no projeto);
- Acesso a uma instância PostgreSQL.

Configure as variáveis de ambiente necessárias antes de iniciar a aplicação:

- `DB_URL`: URL JDBC de conexão com o PostgreSQL;
- `DB_USERNAME`: usuário do banco;
- `DB_PASSWORD`: senha do banco.

Na pasta do back-end, execute:

```bash
./mvnw spring-boot:run
```

No Windows PowerShell:

```powershell
.\mvnw.cmd spring-boot:run
```

Por padrão, a aplicação utiliza a porta 8080, salvo configuração diferente pela variável `PORT`.

## Apresentação Final

Pitch Deck:https://canva.link/wtub2ektsjmz5ky

Apresentação final do Projeto Integrador.

Vídeo de apresentação e demonstração:
https://drive.google.com/file/d/1ZS5kAb5_YpI7dU6rVSmy_pLoQxwS9YdS/view?usp=drivesdk

Nesta apresentação são abordados o problema identificado com base no ODS 7, as decisões técnicas, a arquitetura utilizada, as tecnologias escolhidas, a demonstração do MVP, os desafios enfrentados durante o desenvolvimento e as possibilidades de evolução do projeto.

## Integrantes

1. Luiz Paulo Fernandes
2. Pamela Almeida dos Santos
3. Cauã Silva Rocha
4. Jhonatas Felipe Lopes Ribeiro
5. Diego Silva da Costa
6. Matheus Henrique Alves Soares
7. Pedro Henrique dos Santos de Carvalho

## Apresentação

**Vídeo de demonstração:** link a ser adicionado pelo grupo.

## 🎬 Vídeo da Apresentação

[Clique aqui para assistir ao vídeo completo](https://drive.google.com/file/d/1JR20FokNCJOMUhh_bHuURM3czFuxvB/view?usp=sharing)
