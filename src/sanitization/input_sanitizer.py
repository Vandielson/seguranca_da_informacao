"""Sanitização de entrada - Remove/mascara PII e normaliza formatos."""
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from typing import Dict, List, Optional


class InputSanitizer:
    """Sanitiza entrada removendo/mascarando PII."""
    
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
    
    def sanitize(self, text: str) -> Dict[str, any]:
        """
        Sanitiza o texto de entrada.
        
        Returns:
            Dict com:
                - sanitized_text: texto sanitizado
                - detected_entities: lista de entidades detectadas
                - has_pii: boolean indicando se PII foi encontrado
        """
        if not text:
            return {
                "sanitized_text": "",
                "detected_entities": [],
                "has_pii": False
            }
        
        # Detecta PII - tenta português primeiro, fallback para inglês
        try:
            results = self.analyzer.analyze(text=text, language="pt")
        except ValueError:
            # Se português não estiver disponível, usa inglês
            results = self.analyzer.analyze(text=text, language="en")
        
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
            "has_pii": len(detected_entities) > 0
        }
    
    def normalize(self, text: str) -> str:
        """Normaliza formato do texto (encoding, quebras de linha, etc.)."""
        if not text:
            return ""
        
        # Remove caracteres de controle
        normalized = text.encode('utf-8', errors='ignore').decode('utf-8')
        
        # Normaliza quebras de linha
        normalized = normalized.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove espaços múltiplos
        normalized = ' '.join(normalized.split())
        
        return normalized.strip()

