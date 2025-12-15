"""Configurações do ambiente."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Provedor de LLM (evita dependência obrigatória do Gemini)
# Valores típicos: mock | ollama | gemini
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")

# Configurações do Ollama (se LLM_PROVIDER=ollama)
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.1")

# Configurações da aplicação
APP_ENV = os.getenv("APP_ENV", "dev")
APP_PORT = int(os.getenv("APP_PORT", "8000"))

# Configurações do ChromaDB
CHROMA_HOST = os.getenv("CHROMA_HOST", "localhost")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8001"))

# Configurações de segurança
MAX_PROMPT_LENGTH = int(os.getenv("MAX_PROMPT_LENGTH", "5000"))
RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))  # segundos
