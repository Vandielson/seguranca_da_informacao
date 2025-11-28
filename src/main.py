from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
import os

# Importações dos módulos de segurança
from src.sanitization.input_sanitizer import InputSanitizer
from src.sanitization.output_sanitizer import OutputSanitizer
from src.firewall_llm.firewall import LLMFirewall
from src.rbac_adaptativo.rbac import AdaptiveRBAC
from src.llm_service.gemini_client import GeminiClient
from src.compliance.mapper import ComplianceMapper

app = FastAPI(
    title="Pipeline de Segurança para LLMs",
    description="PoC para aplicar controles (Firewall, RAG, RBAC) em APIs de LLM."
)

# Monta arquivos estáticos se a pasta existir
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Inicializa componentes
input_sanitizer = InputSanitizer()
output_sanitizer = OutputSanitizer()
firewall = LLMFirewall()
rbac = AdaptiveRBAC()
compliance_mapper = ComplianceMapper()

# GeminiClient será inicializado sob demanda (lazy) para evitar erros na inicialização
gemini_client = None

def get_gemini_client():
    """Obtém o cliente Gemini, inicializando-o se necessário."""
    global gemini_client
    if gemini_client is None:
        try:
            gemini_client = GeminiClient()
        except ValueError as e:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Erro de configuração",
                    "details": str(e),
                    "message": "GEMINI_API_KEY não configurada. Verifique o arquivo .env"
                }
            )
    return gemini_client


class ChatRequest(BaseModel):
    """Modelo de requisição para o endpoint /chat."""
    message: str
    user_id: Optional[str] = None
    user_role: str = "user"  # admin, user, guest


class ChatResponse(BaseModel):
    """Modelo de resposta do endpoint /chat."""
    response: str
    request_id: str
    controls_applied: list
    risk_score: Optional[float] = None
    compliance_evidence: Optional[dict] = None


@app.get("/")
def root():
    return {"status": "API de Segurança de LLM está no ar!"}

@app.get("/chat", response_class=HTMLResponse)
def web_ui():
    static_file = os.path.join(static_dir, "index.html")
    if os.path.exists(static_file):
        with open(static_file, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Interface web não encontrada.</h1>")


@app.get("/api/health")
def health_check():
    """Endpoint de health check para API."""
    return {"status": "API de Segurança de LLM está no ar!"}

@app.get("/api/config-check")
def config_check():
    """Endpoint para verificar configuração da API."""
    from config import GEMINI_API_KEY
    
    config_status = {
        "gemini_api_key_configured": bool(GEMINI_API_KEY),
        "gemini_api_key_length": len(GEMINI_API_KEY) if GEMINI_API_KEY else 0,
        "status": "ok" if GEMINI_API_KEY else "warning",
        "message": "Configuração OK" if GEMINI_API_KEY else "GEMINI_API_KEY não configurada. Crie um arquivo .env na raiz do projeto com: GEMINI_API_KEY=sua_chave_aqui"
    }
    
    return config_status


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal que processa mensagens através do pipeline de segurança.
    
    Pipeline:
    1. Sanitização de entrada
    2. RBAC adaptativo (cálculo de risk score)
    3. Firewall LLM
    4. Chamada ao LLM (Gemini)
    5. Sanitização de saída
    6. Auditoria e mapeamento de conformidade
    """
    request_id = str(uuid.uuid4())
    controls_applied = []
    request_data = {
        "request_id": request_id,
        "user_id": request.user_id,
        "user_role": request.user_role,
        "prompt": request.message,
        "timestamp": datetime.now()
    }
    
    try:
        # 1. Sanitização de entrada
        sanitization_result = input_sanitizer.sanitize(request.message)
        sanitized_input = sanitization_result["sanitized_text"]
        controls_applied.append("input_sanitization")
        
        # Normaliza o texto
        normalized_input = input_sanitizer.normalize(sanitized_input)
        
        # 2. RBAC Adaptativo - Calcula risk score
        rbac_result = rbac.calculate_risk_score(
            user_role=request.user_role,
            prompt=normalized_input,
            user_id=request.user_id,
            timestamp=datetime.now()
        )
        controls_applied.append("rbac_adaptive")
        request_data["risk_score"] = rbac_result["risk_score"]
        request_data["rbac_result"] = rbac_result
        
        # Se ação for "block", retorna erro
        if rbac_result["action"] == "block":
            raise HTTPException(
                status_code=403,
                detail={
                    "error": "Acesso bloqueado por alto risco",
                    "risk_score": rbac_result["risk_score"],
                    "risk_level": rbac_result["risk_level"]
                }
            )
        
        # Se ação for "step_up", adiciona aviso (em produção, exigiria MFA)
        if rbac_result["action"] == "step_up":
            # Por enquanto, apenas registra - em produção exigiria autenticação adicional
            pass
        
        # 3. Firewall LLM
        firewall_result = firewall.check(normalized_input)
        controls_applied.append("firewall_llm")
        request_data["firewall_result"] = firewall_result
        
        # Se firewall bloquear, retorna erro
        if not firewall_result["allowed"]:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Prompt bloqueado pelo firewall",
                    "reason": firewall_result["reason"],
                    "detected_patterns": firewall_result["detected_patterns"],
                    "risk_score": firewall_result["risk_score"]
                }
            )
        
        # 4. Chamada ao LLM (Gemini)
        llm_response = get_gemini_client().generate_response(normalized_input)
        
        if not llm_response["success"]:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Erro ao gerar resposta do LLM",
                    "details": llm_response.get("error", "Erro desconhecido")
                }
            )
        
        raw_response = llm_response["response"]
        
        # 5. Sanitização de saída
        output_sanitization_result = output_sanitizer.sanitize(raw_response)
        sanitized_output = output_sanitization_result["sanitized_text"]
        controls_applied.append("output_sanitization")
        
        # 6. Mapeamento de conformidade e auditoria
        compliance_evidence = compliance_mapper.map_controls(controls_applied)
        request_data["controls_applied"] = controls_applied
        
        # Gera log de auditoria
        audit_log = compliance_mapper.generate_audit_log(
            request_data=request_data,
            response_data={"response": sanitized_output}
        )
        
        # Em produção, salvaria o audit_log em banco de dados ou arquivo
        
        return ChatResponse(
            response=sanitized_output,
            request_id=request_id,
            controls_applied=controls_applied,
            risk_score=rbac_result["risk_score"],
            compliance_evidence=compliance_evidence
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro interno do servidor",
                "details": str(e)
            }
        )