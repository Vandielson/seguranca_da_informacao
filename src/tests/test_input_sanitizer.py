"""Testes unitários para InputSanitizer."""
import pytest
from sanitization.input_sanitizer import InputSanitizer


class TestInputSanitizer:
    """Testes para sanitização de entrada."""
    
    def setup_method(self):
        """Configuração antes de cada teste."""
        self.sanitizer = InputSanitizer()
    
    def test_sanitize_basic(self):
        """Testa sanitização básica de texto."""
        text = "Olá, como você está?"
        result = self.sanitizer.sanitize(text)
        assert len(result["sanitized_text"]) > 0
        assert "sanitized_text" in result
        assert "has_pii" in result

