"""Provedor de LLM determinístico (sem rede)."""
from typing import Optional, Dict


class MockClient:
    def __init__(self, fixed_response: str = "OK (mock): resposta gerada sem provedor externo."):
        self.fixed_response = fixed_response

    def generate_response(self, prompt: str, context: Optional[str] = None) -> Dict[str, object]:
        full_prompt = prompt if not context else f"Contexto:\n{context}\n\nPergunta:\n{prompt}"
        text = self.fixed_response
        return {
            "response": text,
            "usage": {"prompt_tokens": len(full_prompt.split()), "response_tokens": len(text.split())},
            "success": True,
            "provider": "mock",
        }
