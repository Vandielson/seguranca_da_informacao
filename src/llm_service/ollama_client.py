"""Provedor de LLM via Ollama (local/offline)."""
from typing import Optional, Dict
import httpx


class OllamaClient:
    def __init__(self, base_url: str, model: str):
        self.base_url = (base_url or "http://localhost:11434").rstrip("/")
        self.model = model or "llama3.1"

    def generate_response(self, prompt: str, context: Optional[str] = None) -> Dict[str, object]:
        full_prompt = prompt if not context else f"Contexto:\n{context}\n\nPergunta:\n{prompt}"

        try:
            url = f"{self.base_url}/api/generate"
            payload = {"model": self.model, "prompt": full_prompt, "stream": False}
            with httpx.Client(timeout=60.0) as client:
                r = client.post(url, json=payload)
                r.raise_for_status()
                data = r.json()

            text = data.get("response")
            return {
                "response": text,
                "usage": {
                    "prompt_tokens": len(full_prompt.split()),
                    "response_tokens": len(text.split()) if text else 0,
                },
                "success": True,
                "provider": "ollama",
                "model": self.model,
                "base_url": self.base_url,
            }
        except Exception as e:
            return {
                "response": None,
                "error": str(e),
                "success": False,
                "provider": "ollama",
                "model": self.model,
                "base_url": self.base_url,
            }
