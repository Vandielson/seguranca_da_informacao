##  Como Acessar

1. **Inicie a aplicação** (Docker ou localmente):
   ```powershell
   # Com Docker
   docker compose up -d
   
   # Ou localmente
   cd src
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Acesse no navegador:**
   ```
   http://localhost:8000
   ```

##  Funcionalidades da Interface

### 1. **Chat Interativo**
   - Área de chat para conversar com o LLM
   - Mensagens do usuário aparecem à direita (roxo)
   - Respostas do assistente aparecem à esquerda (branco)
   - Suporte a Enter para enviar mensagens

### 2. **Seletor de Papel do Usuário**
   - 👤 **User** - Usuário padrão
   - 👑 **Admin** - Administrador
   - 🔓 **Guest** - Convidado
   
   O papel afeta o cálculo do risk score.

### 3. **Painel de Risk Score**
   - Círculo visual com o score (0-100)
   - Cores indicam o nível de risco:
     - 🟢 **Verde** - Risco Baixo (< 40)
     - 🟡 **Amarelo/Rosa** - Risco Médio (40-70)
     - 🔴 **Vermelho/Amarelo** - Risco Alto (> 70)

### 4. **Controles Aplicados**
   - Lista visual dos controles de segurança aplicados:
     - ✅ Sanitização de Entrada
     - ✅ RBAC Adaptativo
     - ✅ Firewall LLM
     - ✅ Sanitização de Saída

### 5. **Pipeline de Segurança Visual**
   - Animação mostrando cada etapa do pipeline:
     1. Sanitização de Entrada
     2. RBAC Adaptativo
     3. Firewall LLM
     4. Chamada ao LLM
     5. Sanitização de Saída
     6. Auditoria
   
   As etapas são destacadas em tempo real durante o processamento.

### 6. **Badges de Conformidade**
   - Mostra os padrões de conformidade atendidos:
     - EU AI Act
     - OWASP
     - ISO
     - ENISA

##  Como Usar

1. **Selecione seu papel** (User, Admin ou Guest)
2. **Digite uma mensagem** no campo de texto
3. **Pressione Enter** ou clique em "Enviar"
4. **Aguarde o processamento** - você verá a animação do pipeline
5. **Veja os resultados**:
   - Resposta do LLM no chat
   - Risk score atualizado
   - Controles aplicados
   - Badges de conformidade

##  Design Responsivo

A interface é totalmente responsiva e funciona bem em:
- 💻 Desktop
- 📱 Tablets
- 📱 Smartphones

##  Características Visuais

- **Gradientes modernos** (roxo/azul)
- **Animações suaves** (fade-in, hover effects)
- **Cards com sombras** para profundidade
- **Cores intuitivas** para indicadores de risco
- **Tipografia clara** e legível

##  Endpoints Disponíveis

- `GET /` - Interface web (HTML)
- `GET /api/health` - Health check da API (JSON)
- `POST /chat` - Endpoint de chat (JSON)
- `GET /docs` - Documentação Swagger do FastAPI
- `GET /redoc` - Documentação ReDoc do FastAPI

##  Solução de Problemas

### Interface não carrega
- Verifique se a aplicação está rodando
- Verifique se a porta 8000 está acessível
- Veja os logs: `docker compose logs` ou no terminal

### Erros ao enviar mensagens
- Verifique se o arquivo `.env` está configurado com `GEMINI_API_KEY`
- Veja os logs da aplicação para mais detalhes
- Verifique a conexão com a internet (necessária para API do Gemini)

### Estilos não aparecem
- Limpe o cache do navegador (Ctrl+F5)
- Verifique se o arquivo `static/index.html` existe

