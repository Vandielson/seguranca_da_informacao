from dataclasses import dataclass


@dataclass
class RuntimeLLMSettings:
    provider: str = "mock"  # mock | ollama | gemini
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3.1"

    def normalize(self) -> "RuntimeLLMSettings":
        self.provider = (self.provider or "mock").strip().lower()
        self.ollama_url = (self.ollama_url or "http://localhost:11434").strip()
        self.ollama_model = (self.ollama_model or "llama3.1").strip()
        return self
