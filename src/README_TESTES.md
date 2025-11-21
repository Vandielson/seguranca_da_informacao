# 🧪 Guia Rápido de Testes

## Como Executar os Testes

### Opção 1: Usando pytest diretamente

```powershell
cd "D:\PERIODO 7\Seguranca\seguranca_da_informacao\src"
pytest
```

### Opção 2: Usando o script auxiliar

```powershell
cd "D:\PERIODO 7\Seguranca\seguranca_da_informacao\src"
python run_tests.py
```

### Opção 3: Dentro do Docker

```powershell
cd "D:\PERIODO 7\Seguranca\seguranca_da_informacao"
docker compose exec app pytest
```

## Testes Disponíveis

### Testes Unitários

1. **test_input_sanitizer.py** - Testa sanitização de entrada
   - Sanitização de strings vazias
   - Detecção de PII (emails, etc.)
   - Normalização de texto

2. **test_firewall.py** - Testa firewall LLM
   - Detecção de prompt injection
   - Detecção de jailbreak
   - Verificação de tamanho de prompt

3. **test_rbac.py** - Testa RBAC adaptativo
   - Cálculo de risk score
   - Diferentes papéis de usuário
   - Horários e frequência de requisições

4. **test_output_sanitizer.py** - Testa sanitização de saída
   - Remoção de PII
   - Detecção de conteúdo proibido

5. **test_compliance.py** - Testa mapeamento de conformidade
   - Mapeamento de controles para normas
   - Geração de logs de auditoria

### Testes Funcionais

6. **test_api.py** - Testa endpoints da API
   - Endpoint raiz (`/`)
   - Endpoint de chat (`/chat`)
   - Validação de entrada
   - Bloqueio pelo firewall

## Executar Testes Específicos

```powershell
# Apenas testes do firewall
pytest tests/test_firewall.py

# Apenas um teste específico
pytest tests/test_firewall.py::TestLLMFirewall::test_check_normal_prompt

# Com mais verbosidade
pytest -v

# Mostrar prints (se houver)
pytest -s
```

## Estrutura dos Testes

Cada arquivo de teste segue o padrão:

```python
import pytest
from modulo.arquivo import Classe

class TestClasse:
    def setup_method(self):
        # Configuração antes de cada teste
        self.objeto = Classe()
    
    def test_metodo_especifico(self):
        # Teste específico
        resultado = self.objeto.metodo()
        assert resultado == esperado
```

## Notas Importantes

- Alguns testes podem falhar se a API do Gemini não estiver configurada
- Testes que dependem de serviços externos podem ser mockados
- Execute `pytest -v` para ver detalhes de cada teste

