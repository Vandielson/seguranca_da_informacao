"""Testes unitários para OutputSanitizer."""
import pytest
from sanitization.output_sanitizer import OutputSanitizer


class TestOutputSanitizer:
    """Testes para sanitização de saída."""
    
    def setup_method(self):
        """Configuração antes de cada teste."""
        self.sanitizer = OutputSanitizer()
    
    def test_sanitize_basic(self):
        """Testa sanitização básica de saída."""
        text = "A capital do Brasil é Brasília."
        result = self.sanitizer.sanitize(text)
        assert len(result["sanitized_text"]) > 0
        assert "has_forbidden_content" in result

