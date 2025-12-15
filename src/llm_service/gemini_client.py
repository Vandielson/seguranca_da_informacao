"""Cliente opcional para integração com Google Gemini API.

Este módulo é "tolerante": se a dependência ou a API key não estiverem disponíveis,
ele não deve derrubar a aplicação na importação. O erro aparece apenas quando
o provedor Gemini é realmente usado.
"""
from typing import Optional, Dict

from config import GEMINI_API_KEY


class GeminiClient:
    """Cliente para interagir com a API do Gemini."""

    def __init__(self):
        self._configured = False
        self._model = None

    def _ensure_ready(self) -> None:
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não configurada no .env")

        try:
            import google.generativeai as genai  # type: ignore
        except Exception as e:
            raise ImportError(
                "Dependência google-generativeai não disponível. "
                "Instale 'google-generativeai' ou use LLM_PROVIDER=mock/ollama."
            ) from e

        if not self._configured:
            genai.configure(api_key=GEMINI_API_KEY)
            try:
                self._model = genai.GenerativeModel("gemini-2.0-flash")
            except Exception:
                self._model = genai.GenerativeModel("gemini-2.5-flash")
            self._configured = True

    def generate_response(self, prompt: str, context: Optional[str] = None) -> Dict[str, object]:
        try:
            self._ensure_ready()

            full_prompt = prompt
            if context:
                full_prompt = f"Contexto:\n{context}\n\nPergunta:\n{prompt}"

            response = self._model.generate_content(full_prompt)

            text = getattr(response, "text", None)

            return {
                "response": text,
                "usage": {
                    "prompt_tokens": len(full_prompt.split()),
                    "response_tokens": len(text.split()) if text else 0,
                },
                "success": True,
                "provider": "gemini",
            }
        except Exception as e:
            return {"response": None, "error": str(e), "success": False, "provider": "gemini"}
