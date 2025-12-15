from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid
from datetime import datetime
import os

from sanitization.input_sanitizer import InputSanitizer
from sanitization.output_sanitizer import OutputSanitizer
from firewall_llm.firewall import LLMFirewall
from rbac_adaptativo.rbac import AdaptiveRBAC
from llm_service.llm_provider import get_llm_client
from compliance.mapper import ComplianceMapper
from settings import RuntimeLLMSettings

app = FastAPI(
    title="Pipeline de Segurança para LLMs",
    description="PoC para aplicar controles (Firewall, RAG, RBAC) em APIs de LLM."
)

static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

input_sanitizer = InputSanitizer()
output_sanitizer = OutputSanitizer()
firewall = LLMFirewall()
rbac = AdaptiveRBAC()
compliance_mapper = ComplianceMapper()

runtime_llm_settings = RuntimeLLMSettings()
_llm_client = None


def _reset_llm_client() -> None:
    global _llm_client
    _llm_client = None


def get_client():
    global _llm_client
    if _llm_client is None:
        _llm_client = get_llm_client(runtime_llm_settings)
    return _llm_client


class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = None
    user_role: str = "user"


class ChatResponse(BaseModel):
    response: str
    request_id: str
    controls_applied: list
    risk_score: Optional[float] = None
    compliance_evidence: Optional[dict] = None


class ProviderSettingsRequest(BaseModel):
    provider: str = "mock"  # mock | ollama | gemini
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"


@app.get("/")
def root():
    return {"status": "API de Segurança de LLM está no ar!"}


@app.get("/chat", response_class=HTMLResponse)
def web_ui():
    static_file = os.path.join(static_dir, "index.html")
    if os.path.exists(static_file):
        return FileResponse(static_file)
    return HTMLResponse("<h1>UI não encontrada. Verifique a pasta /static.</h1>")


@app.get("/api/provider")
def get_provider_settings() -> Dict[str, Any]:
    s = runtime_llm_settings.normalize()
    return {
        "provider": s.provider,
        "ollama_url": s.ollama_url,
        "ollama_model": s.ollama_model,
    }


@app.post("/api/provider")
def set_provider_settings(req: ProviderSettingsRequest) -> Dict[str, Any]:
    runtime_llm_settings.provider = req.provider
    runtime_llm_settings.ollama_url = req.ollama_url
    runtime_llm_settings.ollama_model = req.ollama_model
    runtime_llm_settings.normalize()

    _reset_llm_client()

    return {
        "ok": True,
        "provider": runtime_llm_settings.provider,
        "ollama_url": runtime_llm_settings.ollama_url,
        "ollama_model": runtime_llm_settings.ollama_model,
    }


# --- Botão de teste (valida conexão/modelo do Ollama) ---
@app.post("/api/provider/test")
def test_provider_settings() -> Dict[str, Any]:
    s = runtime_llm_settings.normalize()

    if s.provider != "ollama":
        return {
            "ok": False,
            "provider": s.provider,
            "message": "Selecione 'ollama' como provedor para executar o teste de conexão/modelo.",
        }

    # cria cliente no estado atual (sem mexer no client global)
    client = get_llm_client(s)

    # prompt curtíssimo só para validar pipeline
    resp = client.generate_response("Responda apenas: OK")

    if resp.get("success"):
        return {
            "ok": True,
            "provider": "ollama",
            "ollama_url": s.ollama_url,
            "ollama_model": s.ollama_model,
            "message": "Conexão com Ollama OK.",
            "sample_response": resp.get("response"),
        }

    return {
        "ok": False,
        "provider": "ollama",
        "ollama_url": s.ollama_url,
        "ollama_model": s.ollama_model,
        "message": "Falha ao conectar/gerar via Ollama.",
        "error": resp.get("error"),
    }


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    request_id = str(uuid.uuid4())
    timestamp = datetime.utcnow().isoformat()

    controls_applied = []

    try:
        fw_result = firewall.check(req.message)
        controls_applied.append({"control": "firewall", "result": fw_result})

        if not fw_result["allowed"]:
            return ChatResponse(
                response="Bloqueado pelo Firewall: Prompt malicioso detectado.",
                request_id=request_id,
                controls_applied=controls_applied,
                risk_score=fw_result.get("risk_score", 0),
                compliance_evidence={
                    "timestamp": timestamp,
                    "control": "firewall",
                    "status": "blocked",
                    "detected_patterns": fw_result.get("detected_patterns", []),
                    "risk_score": fw_result.get("risk_score", 0),
                },
            )

        sanitized_input = input_sanitizer.sanitize(req.message)
        controls_applied.append({"control": "input_sanitizer", "result": sanitized_input})

        normalized_input = sanitized_input.get("sanitized_text", req.message)

        rbac_result = rbac.evaluate_access(
            user_id=req.user_id or "anon",
            role=req.user_role,
            prompt=normalized_input
        )
        controls_applied.append({"control": "rbac", "result": rbac_result})

        if not rbac_result["allowed"]:
            return ChatResponse(
                response="Acesso negado pelo RBAC Adaptativo.",
                request_id=request_id,
                controls_applied=controls_applied,
                risk_score=rbac_result.get("risk_score", 0),
                compliance_evidence={
                    "timestamp": timestamp,
                    "control": "rbac",
                    "status": "denied",
                    "role": req.user_role,
                    "risk_score": rbac_result.get("risk_score", 0),
                },
            )

        llm_response = get_client().generate_response(normalized_input)
        controls_applied.append({
            "control": "llm_provider",
            "result": {"success": llm_response.get("success"), "provider": llm_response.get("provider")}
        })

        if not llm_response.get("success"):
            raise HTTPException(
                status_code=502,
                detail={
                    "error": "Erro no provedor de LLM",
                    "details": llm_response.get("error"),
                    "provider": llm_response.get("provider"),
                },
            )

        sanitized_output = output_sanitizer.sanitize(llm_response.get("response") or "")
        controls_applied.append({"control": "output_sanitizer", "result": sanitized_output})

        final_output = sanitized_output.get("sanitized_text", llm_response.get("response") or "")

        compliance_evidence = compliance_mapper.map_controls(controls_applied)

        return ChatResponse(
            response=final_output,
            request_id=request_id,
            controls_applied=controls_applied,
            risk_score=rbac_result.get("risk_score"),
            compliance_evidence=compliance_evidence
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"error": "Erro interno do servidor", "details": str(e)}
        )
