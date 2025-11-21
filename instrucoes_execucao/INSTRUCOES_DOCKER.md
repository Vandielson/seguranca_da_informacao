#  Guia Rápido - Como Iniciar as Aplicações

Este guia mostra como iniciar a aplicação de segurança para LLMs no Windows.

##  Pré-requisitos

1. **Docker Desktop** instalado e rodando
   - Download: https://www.docker.com/products/docker-desktop/
   - Verifique se está rodando (ícone na bandeja do sistema)

2. **Chave de API do Google Gemini**
   - Obtenha em: https://makersuite.google.com/app/apikey

---

##  Configuração Inicial

### 1. Criar arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto (`seguranca_da_informacao/`) com:

```env
GEMINI_API_KEY=sua_chave_api_aqui
APP_ENV=dev
APP_PORT=8000
CHROMA_HOST=chroma
CHROMA_PORT=8001
```

**⚠️ IMPORTANTE:** Substitua `sua_chave_api_aqui` pela sua chave real!

### 2. Criar pastas necessárias

No PowerShell, execute:

```powershell
cd "D:\PERIODO 7\Seguranca\seguranca_da_informacao"
New-Item -ItemType Directory -Force -Path ".\data\corpus"
New-Item -ItemType Directory -Force -Path ".\data\db"
```

---

##  Opção 1: Executar com Docker (Recomendado)

### Passo 1: Construir e iniciar os containers

```powershell
cd "D:\PERIODO 7\Seguranca\seguranca_da_informacao"

# Construir a imagem
docker compose build

# Iniciar os containers
docker compose up -d
```

### Passo 2: Verificar se está funcionando

Abra o navegador e acesse: **http://localhost:8000**

Você deve ver:
```json
{"status": "API de Segurança de LLM está no ar!"}
```

### Passo 3: Ver logs (opcional)

```powershell
docker compose logs -f
```

---

##  Opção 2: Executar Localmente (Sem Docker)

### Passo 1: Instalar dependências

```powershell
cd "D:\PERIODO 7\Seguranca\seguranca_da_informacao\src"
pip install -r requirements.txt
```

### Passo 2: Iniciar a aplicação

```powershell
cd "D:\PERIODO 7\Seguranca\seguranca_da_informacao\src"
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

A aplicação estará disponível em: **http://localhost:8000**

---

##  Executar Testes

### Com Docker

```powershell
cd "D:\PERIODO 7\Seguranca\seguranca_da_informacao"
docker compose exec app pytest -v
```

### Localmente

```powershell
cd "D:\PERIODO 7\Seguranca\seguranca_da_informacao\src"
pytest -v
```

### Usando o script PowerShell

```powershell
cd "D:\PERIODO 7\Seguranca\seguranca_da_informacao"
.\EXECUTAR_TESTES.ps1
```

---

##  Testar a API

### 1. Health Check

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
```

### 2. Testar o endpoint `/chat`

```powershell
$body = @{
    message = "Qual é a capital do Brasil?"
    user_id = "user123"
    user_role = "user"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/chat" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
```

### 3. Usando curl (se tiver instalado)

```bash
curl -X POST "http://localhost:8000/chat" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Qual é a capital do Brasil?\", \"user_id\": \"user123\", \"user_role\": \"user\"}"
```

---

##  Pipeline de Segurança (Caminho Feliz)

Quando você faz uma requisição ao `/chat`, o sistema executa:

1. ✅ **Sanitização de entrada** → Remove/mascara PII
2. ✅ **RBAC Adaptativo** → Calcula risk score
3. ✅ **Firewall LLM** → Verifica se prompt é malicioso
4. ✅ **Chamada ao Gemini** → Gera resposta do LLM
5. ✅ **Sanitização de saída** → Remove PII da resposta
6. ✅ **Auditoria** → Gera log de conformidade

---

##  Comandos Úteis

### Docker

```powershell
# Ver status dos containers
docker compose ps

# Parar containers
docker compose down

# Reiniciar containers
docker compose restart

# Ver logs
docker compose logs -f

# Reconstruir do zero
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Testes

```powershell
# Executar todos os testes
pytest

# Executar teste específico
pytest tests/test_firewall.py -v

# Executar com cobertura
pytest --cov=. --cov-report=html
```

---

##  Solução de Problemas

### Erro: "docker compose" não é reconhecido
- Certifique-se de que o Docker Desktop está rodando
- Tente usar `docker-compose` (com hífen)

### Erro: Porta 8000 já está em uso
- Pare outros serviços na porta 8000
- Ou altere a porta no `docker-compose.yml`

### Erro: Arquivo .env não encontrado
- Certifique-se de que o arquivo `.env` está na raiz do projeto
- Verifique se o nome está correto (`.env` sem extensão)

### Erro: GEMINI_API_KEY não encontrada
- Verifique se a chave está no arquivo `.env`
- Certifique-se de que não há espaços extras na chave

---

##  Verificação Final

Se tudo estiver funcionando, você deve conseguir:

1. ✅ Acessar `http://localhost:8000` e ver a mensagem de status
2. ✅ Fazer requisições ao `/chat` e receber respostas
3. ✅ Executar os testes e ver todos passando
4. ✅ Ver os logs sem erros

---

##  Próximos Passos

Após a aplicação estar rodando:

- Explore a documentação em `docs/`
- Veja as apresentações em `apresentacoes/`
- Desenvolva novas funcionalidades em `src/`
- Execute experimentos de segurança

---



