"""Testes unitários para ComplianceMapper."""
import pytest
from compliance.mapper import ComplianceMapper


class TestComplianceMapper:
    """Testes para mapeamento de conformidade."""
    
    def setup_method(self):
        """Configuração antes de cada teste."""
        self.mapper = ComplianceMapper()
    
    def test_map_controls_basic(self):
        """Testa mapeamento básico de controles."""
        controls = ["input_sanitization", "firewall_llm"]
        result = self.mapper.map_controls(controls)
        assert len(result["compliance_mapping"]) > 0
        assert "standards_covered" in result

