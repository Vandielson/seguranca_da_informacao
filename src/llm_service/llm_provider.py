"""Factory de provedores de LLM.

Agora suporta configuração em runtime (UI), sem depender do .env.
"""
from typing import Optional, Protocol, Dict

from llm_service.gemini_client import GeminiClient
from llm_service.mock_client import MockClient
from llm_service.ollama_client import OllamaClient
from settings import RuntimeLLMSettings


class LLMClient(Protocol):
    def generate_response(self, prompt: str, context: Optional[str] = None) -> Dict[str, object]:
        ...


def get_llm_client(settings: RuntimeLLMSettings) -> LLMClient:
    settings = settings.normalize()

    if settings.provider == "gemini":
        return GeminiClient()

    if settings.provider == "ollama":
        return OllamaClient(base_url=settings.ollama_url, model=settings.ollama_model)

    return MockClient()
