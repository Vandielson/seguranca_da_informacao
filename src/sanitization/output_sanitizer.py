"""Sanitização de saída - Filtra PII e conteúdo proibido."""
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from typing import Dict, List


class OutputSanitizer:
    """Sanitiza saída removendo PII e conteúdo proibido."""
    
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        # Lista de palavras/padrões proibidos (exemplo básico)
        self.forbidden_patterns = [
            "senha", "password", "token", "api_key", "secret"
        ]
    
    def sanitize(self, text: str) -> Dict[str, any]:
        """
        Sanitiza o texto de saída.
        
        Returns:
            Dict com:
                - sanitized_text: texto sanitizado
                - detected_entities: lista de entidades detectadas
                - has_pii: boolean indicando se PII foi encontrado
                - has_forbidden_content: boolean indicando conteúdo proibido
        """
        if not text:
            return {
                "sanitized_text": "",
                "detected_entities": [],
                "has_pii": False,
                "has_forbidden_content": False
            }
        
        # Detecta PII - tenta português primeiro, fallback para inglês
        try:
            results = self.analyzer.analyze(text=text, language="pt")
        except ValueError:
            # Se português não estiver disponível, usa inglês
            results = self.analyzer.analyze(text=text, language="en")
        
        # Verifica conteúdo proibido
        text_lower = text.lower()
        has_forbidden = any(pattern in text_lower for pattern in self.forbidden_patterns)
        
        # Anonimiza PII encontrado
        anonymized_result = self.anonymizer.anonymize(
            text=text,
            analyzer_results=results
        )
        
        detected_entities = [
            {
                "entity_type": r.entity_type,
                "start": r.start,
                "end": r.end,
                "score": r.score
            }
            for r in results
        ]
        
        return {
            "sanitized_text": anonymized_result.text,
            "detected_entities": detected_entities,
            "has_pii": len(detected_entities) > 0,
            "has_forbidden_content": has_forbidden
        }

