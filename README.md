# Segurança, Privacidade e Conformidade em Aplicações com LLMs

Repositório da disciplina de **Segurança da Informação** do curso de Bacharelado em Ciência da Computação (UFAPE), dedicado ao desenvolvimento de um **proof-of-concept (PoC)** de segurança para aplicações baseadas em **Large Language Models (LLMs)**.

O foco é projetar, implementar e avaliar um **pipeline de segurança** que combine:
- mitigação técnica de riscos (firewall LLM, sanitização, RAG),
- **controle de acesso adaptativo (RBAC dinâmico)**,
- e **evidências de conformidade regulatória** (AI Act, OWASP, ISO, ENISA),
de forma **end-to-end e reprodutível**.

---

## 1. Sobre a disciplina

- **Disciplina:** Segurança da Informação  
- **Curso:** Bacharelado em Ciência da Computação – UFAPE  
- **Tipo de atividade:** Projeto prático em grupo, com entregas incrementais:
  - Estado da arte e lacuna de pesquisa;
  - Arquitetura da solução e modelagem de ameaças;
  - Metodologia e planejamento de setup experimental;
  - Implementação do protótipo;
  - Execução de experimentos e análise de resultados.

Este repositório reúne os artefatos **teóricos e práticos** necessários para compreender, executar e reproduzir o estudo.

---

## 2. Visão geral do trabalho

### 2.1. Problema e contexto

Aplicações com LLMs vêm sendo usadas em contextos sensíveis (saúde, setor público, finanças) e, ao mesmo tempo, expostas a:

- **prompt injection** e *indirect prompt injection*  
- **insecure output handling**  
- **denial-of-wallet / DoS**  
- vazamento de dados sensíveis (PII, dados clínicos)  
- viés e comportamentos inesperados de saída  

Além disso, cresce a pressão por **conformidade regulatória** (ex.: EU AI Act, GDPR, normas de segurança) e por **evidências auditáveis** de que controles foram de fato aplicados.

### 2.2. Lacuna de pesquisa

A partir de três eixos principais:

- desafios de segurança e privacidade em LLMs (Rathod et al.),  
- RBAC adaptativo e detecção de anomalias em saúde (Yarram et al.),  
- guia prático de conformidade com o EU AI Act (Bunzel),  

identifica-se a lacuna:

> Falta um **framework avaliativo end-to-end, reprodutível e alinhado a normas**, que combine em uma mesma aplicação:
> - mitigação técnica de riscos (prompt injection, output handling, DoS),
> - **RBAC adaptativo** com detecção de anomalias,
> - **privacidade por design** (sanitização e RAG privado),
> - e **traçabilidade de conformidade** com evidências objetivas.

### 2.3. Objetivo geral

Projetar, implementar e avaliar um **middleware de segurança para uma aplicação com LLM**, capaz de:

- integrar múltiplas camadas de controle de segurança e privacidade;
- expor métricas comparáveis (segurança, desempenho, custo e conformidade);
- gerar artefatos reprodutíveis (código, scripts de setup, datasets sintéticos, relatórios).

---

## 3. Arquitetura de alto nível

A PoC é implementada como um **middleware de segurança** colocado entre os usuários internos e a API do LLM (Gemini). Toda requisição passa por uma sequência de camadas que combinam segurança, privacidade e conformidade, antes de chegar ao modelo.

### 3.1. Fluxo geral

```text
Usuário → API do Middleware → [Sanitização de entrada]
                              → [Firewall LLM]
                              → [RAG privado + ChromaDB]
                              → [RBAC adaptativo (risk score)]
                              → [Sanitização de saída]
                              → [Auditoria + Mapper de conformidade]
                              → LLM (Gemini API)
                              → Resposta ao usuário
```

Esse fluxo resume a visão do artigo: nenhum acesso ao LLM é feito sem passar por controles técnicos, e cada decisão é registrada de forma auditável.

### 3.2. Camadas principais

1. **Sanitização de entrada**  
   - Remoção ou mascaramento de PII (*Named Entity Recognition + redaction*).  
   - Normalização de formatos e codificação (Unicode, espaços, tokens suspeitos).  
   - Uso de regex e listas semânticas de bloqueio para termos e padrões de alto risco.

2. **Firewall LLM**  
   - Regras estáticas para bloquear prompts maliciosos e instruções claramente proibidas.  
   - Heurísticas semânticas para detectar *prompt injection*, *jailbreaks* e tentativas de burlar políticas.  
   - Mecanismos de **rate limiting** e controle de tamanho de *prompt* para mitigar *denial-of-wallet* e DoS lógico.

3. **RAG privado (repositório de conhecimento)**  
   - Conjunto de documentos institucionais neutros, previamente sanitizados, indexados em um banco vetorial (ex.: **ChromaDB**).  
   - Embeddings gerados com modelos de embedding do provedor (ex.: Gemini `text-embedding-004`).  
   - Metadados de confidencialidade e escopo que interagem com as regras de RBAC.

4. **RBAC adaptativo (risk-based access control)**  
   - Cálculo de um *risk score* por requisição, usando: papel do usuário, horário, contexto lógico, histórico de consultas e semântica do pedido.  
   - Ações possíveis:  
     - permitir a requisição,  
     - exigir autenticação reforçada (*step-up*),  
     - ou bloquear e registrar incidente.

5. **Sanitização de saída**  
   - Verificação da resposta do LLM para garantir que PII ou informações sensíveis não sejam reintroduzidas.  
   - Bloqueio de conteúdos proibidos por política institucional ou regulatória.  
   - Ajustes finais de formato e tom antes de retornar ao usuário.

6. **Auditoria e telemetria**  
   - Logs estruturados (idealmente em formato JSON) com: requisição, contexto, decisões tomadas, métricas de latência, custo e resultado final.  
   - Registros em modo *append-only*, pensados para uso em auditorias posteriores.

7. **Mapper de conformidade**  
   - Componente responsável por mapear cada controle técnico a requisitos de normas e boas práticas (AI Act, OWASP LLM Top 10, ISO/IEC 27001, ENISA AI Security).  
   - Geração de evidências exportáveis (relatórios, dashboards) a partir dos logs, permitindo demonstrar cobertura de requisitos.

---

## 4. Organização do repositório (estado atual)

Estrutura atual (resumida):

```text
.
├── apresentacaoequipe/      # Material de apresentação da equipe
├── apresentacoes/           # Apresentações das atividades da disciplina
├── docs/                    # Documentação adicional (artigo, texto da disciplina, etc.)
├── instrucoes_execucao/     # Guias passo a passo de execução e testes
├── outros_artefatos/        # PDFs, recursos auxiliares e materiais de apoio
├── src/                     # Código-fonte do protótipo (PoC)
├── .gitignore
├── README.md                # Este arquivo
├── docker-compose.yml       # Orquestração dos serviços em contêiner
├── setup.sh                 # Script de configuração inicial do ambiente (Linux)
├── EXECUTAR_TESTES.ps1      # Script PowerShell de execução de testes (Windows)
└── TESTAR_API.ps1           # Script PowerShell para testar a API (Windows)
```

Ideia geral:

- centralizar implementação e experimentos em `src/` + `docker-compose.yml` + scripts de setup e teste,
- manter apresentações e entregas da disciplina em `apresentacaoequipe/`, `apresentacoes/`, `docs/`, `instrucoes_execucao/` e `outros_artefatos/`.

Diretório de código-fonte (`src/`), em evolução incremental, concentra:

- ponto de entrada da aplicação (API do middleware),
- camadas de segurança (sanitização, firewall, RAG, RBAC adaptativo, auditoria),
- código de apoio a experimentos.

A organização fina em submódulos (por exemplo `firewall_llm/`, `sanitization/`, `rbac_adaptativo/`, `rag/`, `auditoria/`, `compliance_mapper/`) pode ser consolidada à medida que a implementação avança, seguindo o que foi discutido em sala.

---

## 5. Estrutura alternativa (possível encaminhamento futuro)

Caso o projeto evolua para um framework reutilizável ou base para TCC ou artigos futuros, uma estrutura mais modular pode ser adotada:

```text
.
├── README.md
├── docs/
│   ├── overview.md
│   ├── architecture.md
│   └── compliance_mapping.md
├── src/
│   ├── core/
│   │   ├── firewall_llm/
│   │   ├── sanitization/
│   │   ├── rbac_adaptativo/
│   │   ├── rag/
│   │   ├── auditoria/
│   │   └── compliance_mapper/
│   ├── api/
│   │   └── app/              # FastAPI / REST / gRPC
│   └── cli/
│       └── main.py           # Ferramenta de linha de comando para rodar cenários
├── infra/
│   ├── docker-compose.dev.yml
│   ├── docker-compose.prod.yml
│   ├── Dockerfile.app
│   ├── Dockerfile.chroma
│   └── k8s/                  # Manifests para Kubernetes (futuro)
├── scripts/
│   ├── bootstrap_dev.sh
│   ├── bootstrap_prod.sh
│   ├── seed_chroma.py
│   └── run_experiments.py
├── data/
│   ├── corpus_institucional/
│   ├── dados_sinteticos_saude/
│   └── ataques_prompts/
├── eval/
│   ├── configs/
│   └── notebooks/
└── examples/
    ├── healthcare_assistant/
    └── public_admin_assistant/
```

Essa organização facilita separar o núcleo de segurança (`src/core`) da camada de exposição (`src/api`) e da automação (`src/cli`), diferenciar configuração de desenvolvimento e produção em `infra/` e criar exemplos de referência por domínio na pasta `examples/`.

---

## 6. Requisitos para execução

### 6.1. Hardware mínimo

- Host ou VM com:
  - 4 vCPUs
  - 8–16 GB de RAM
  - pelo menos 40 GB de armazenamento
- Conexão estável à Internet (acesso à API do LLM)
- Opcional: GPU para experimentos mais pesados (não obrigatório na PoC inicial)

### 6.2. Software de base

- Sistema operacional:
  - Linux (por exemplo, Ubuntu Server) nativo ou em VM (VirtualBox, VMware, KVM)
  - Windows pode ser usado como host da VM ou via WSL2
- Ferramentas:
  - Docker Engine e Docker Compose
  - Git
  - Python 3.10 ou superior (para scripts locais, se necessário)

### 6.3. Contas externas e segredos

- Chave de API válida para o provedor de LLM (por exemplo, Gemini)
- Arquivo `.env` (não versionado) com, por exemplo:

```text
GEMINI_API_KEY=SEU_TOKEN_AQUI
APP_ENV=dev
APP_PORT=8000
CHROMA_HOST=chroma
CHROMA_PORT=8001
```

---

## 7. Setup do ambiente

### 7.1. Clonar o repositório

```bash
git clone https://github.com/Vandielson/seguranca_da_informacao.git
cd seguranca_da_informacao
```

### 7.2. Criar o `.env`

Crie o arquivo `.env` na raiz com as variáveis necessárias para:

- chave de API do LLM,
- parâmetros da aplicação (porta, flags de debug),
- configuração de banco vetorial (host, porta, etc.).

### 7.3. Executar o script de setup

Em ambientes Linux:

```bash
chmod +x setup.sh
./setup.sh
```

Em ambientes Windows, consulte os materiais em `instrucoes_execucao/` e os scripts PowerShell para auxiliar na configuração local.

### 7.4. Subir os contêineres

A orquestração dos serviços é feita via `docker-compose.yml`:

```bash
docker compose up -d
```

Isso deve subir:

- o contêiner da aplicação (middleware de segurança),
- o serviço de banco vetorial (se configurado),
- serviços auxiliares necessários para a PoC.

---

## 8. Scripts auxiliares (testes e diagnóstico)

Para facilitar testes rápidos, o repositório inclui scripts PowerShell, pensados para uso em ambientes Windows:

- `EXECUTAR_TESTES.ps1`  
  Script para executar o conjunto de testes automatizados definidos para o middleware (por exemplo, chamadas à API, cenários de ataque sintéticos e verificações de resposta).

- `TESTAR_API.ps1`  
  Script para fazer chamadas de teste à API do middleware, verificando se a aplicação está respondendo como esperado depois de subir os contêineres.

Os detalhes de uso desses scripts são documentados em `instrucoes_execucao/`. O conteúdo pode evoluir conforme novos testes são adicionados.

---

## 9. Execução de experimentos (visão geral)

A PoC é pensada para testar diferentes cenários de segurança em cima da mesma aplicação:

1. **Baseline**  
   LLM com configuração mínima, quase sem controles.

2. **Baseline + Firewall LLM**

3. **Baseline + Firewall + RAG privado**

4. **Baseline + Firewall + RAG + RBAC adaptativo**

5. **Pipeline completo**  
   Todas as camadas ativas: sanitização de entrada e saída, firewall, RAG, RBAC, auditoria e mapper de conformidade.

Scripts específicos (por exemplo, `run_experiments.py`) podem ser adicionados em `src/` ou em um diretório `scripts/` no futuro para:

- orquestrar os cenários,
- disparar ataques ou prompts adversariais,
- salvar métricas em arquivos (CSV, JSON) para posterior análise.

### 9.1. Resultados parciais da Sprint II

Durante a sprint focada em **Execução da Implementação (Parte II)**, foram realizados testes controlados do middleware defensivo com quatro cenários de uso:

- **Prompt Seguro**  
- **Prompt Injection 1**  
- **Prompt Injection 2**  
- **Prompt Longo Demais**  

Para cada cenário foram coletadas métricas de:

- taxa de detecção,  
- número de falsos positivos,  
- latência média (ms),  
- throughput (requisições por segundo).  

#### 9.1.1. Síntese dos resultados

- **100% de detecção** em todos os cenários de teste.  
- Apenas **1 falso positivo**, observado no cenário *Prompt Seguro*.  
- **Latência média** entre aproximadamente **8,56 ms e 13,28 ms**.  
- **Throughput** entre aproximadamente **75 req/s e 117 req/s**.  

#### 9.1.2. Tabela consolidada

| Cenário              | Detecção | Falsos Positivos | Latência (ms) | Throughput (req/s) |
|----------------------|----------|------------------|----------------|---------------------|
| Prompt Seguro        | 100%     | 1                | 13.28          | 75.28              |
| Prompt Injection 1   | 100%     | 0                | 8.73           | 114.60             |
| Prompt Injection 2   | 100%     | 0                | 8.56           | 116.76             |
| Prompt Longo Demais  | 100%     | 0                | 8.97           | 111.46             |

#### 9.1.3. Interpretação

- O firewall LLM e as rotinas de sanitização estão conseguindo bloquear a totalidade dos ataques de *prompt injection* avaliados.  
- O impacto de desempenho é baixo, com latências compatíveis com uso interativo.  
- A ocorrência de um único falso positivo indica necessidade de ajuste fino dos limiares de detecção, mas já sugere boa calibragem inicial.  

O relatório detalhado dos testes se encontra em apresentações:

```text
apresentacoes/apresentação_atividade06.pdf
```

Esse documento descreve o procedimento dos testes e as métricas geradas a partir da PoC em execução.

---

## 10. Reprodutibilidade

Para que outra pessoa consiga reproduzir o estudo, basta:

1. Clonar o repositório e configurar o `.env`.  
2. Executar `setup.sh` para preparar o ambiente (ou seguir as instruções equivalentes em Windows).  
3. Subir os serviços com `docker compose up -d`.  
4. Popular o banco vetorial (se houver script de *seed*).  
5. Usar os scripts de teste (`EXECUTAR_TESTES.ps1`, `TESTAR_API.ps1` e futuros scripts Python) e analisar os resultados.  

A documentação em `docs/` e as apresentações em `apresentacoes/` ajudam a entender o racional por trás das escolhas de arquitetura e metodologia, e se conectam diretamente ao texto do artigo da disciplina.

---

## 11. Referências (nível de disciplina)

- Rathod et al. (2024). *Privacy and Security Challenges in Large Language Models.*  
- Yarram et al. (2024). *Privacy-Preserving Healthcare Data Security Using LLMs and Adaptive Access Control.*  
- Bunzel (2024). *Compliance Made Practical: Translating the EU AI Act into Implementable Security Actions.*  

---

## 12. Integrantes da equipe

- Leonardo Nunes  
- Antônio Marcos  
- Álvaro Gueiros  
- Lucas William  
- Mauro Vinícius  
- Vandielson Tenório  
