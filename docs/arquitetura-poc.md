# Arquitetura do Sistema

Este diagrama representa o fluxo de requisições entre os componentes locais e os serviços em nuvem.

```mermaid
graph TB
    subgraph "Google Cloud"
        CTX -->|Prompt + Contexto| GEMINI(7. API Gemini 2.5)
        GEMINI -->|Resposta| RESP(8. Resposta Bruta)
    end

    subgraph "Ambiente Local/PoC (Docker)"
        U[Usuário] --> API[1. Endpoint FastAPI]
        API --> S_IN(2. Sanitização de Entrada)
        S_IN --> RBAC(3. RBAC Adaptativo)
        RBAC --> FW(4. LLM Firewall)
        FW --> RAG(5. RAG Privado)
        RAG --> DB[(ChromaDB)]
        RAG --> CTX(6. Montagem do Contexto)
        RESP --> S_OUT(9. Sanitização de Saída)
        S_OUT --> LOG(10. Mapper de Conformidade / Log)
        S_OUT --> U
    end
