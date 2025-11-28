"""Cliente para integração com Google Gemini API."""
import google.generativeai as genai
from config import GEMINI_API_KEY
from typing import Optional, Dict


class GeminiClient:
    """Cliente para interagir com a API do Gemini."""
    
    def __init__(self):
        if not GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY não configurada no .env")
        
        genai.configure(api_key=GEMINI_API_KEY)
        # Usa gemini-2.0-flash (modelo disponível e rápido)
        # Se não funcionar, tenta gemini-2.5-flash
        try:
            self.model = genai.GenerativeModel('gemini-2.0-flash')
        except Exception:
            # Fallback para gemini-2.5-flash
            self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_response(self, prompt: str, context: Optional[str] = None) -> Dict[str, any]:
        """
        Gera resposta do Gemini.
        
        Args:
            prompt: Prompt do usuário
            context: Contexto adicional (opcional, para RAG)
        
        Returns:
            Dict com:
                - response: resposta do modelo
                - usage: informações de uso (tokens, etc.)
        """
        try:
            # Monta o prompt completo com contexto (se houver)
            full_prompt = prompt
            if context:
                full_prompt = f"Contexto:\n{context}\n\nPergunta: {prompt}"
            
            # Gera resposta
            response = self.model.generate_content(full_prompt)
            
            return {
                "response": response.text,
                "usage": {
                    "prompt_tokens": len(full_prompt.split()),
                    "response_tokens": len(response.text.split()) if response.text else 0
                },
                "success": True
            }
        except Exception as e:
            return {
                "response": None,
                "error": str(e),
                "success": False
            }

