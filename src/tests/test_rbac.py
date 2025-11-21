"""Testes unitários para AdaptiveRBAC."""
import pytest
from rbac_adaptativo.rbac import AdaptiveRBAC


class TestAdaptiveRBAC:
    """Testes para RBAC adaptativo."""
    
    def setup_method(self):
        """Configuração antes de cada teste."""
        self.rbac = AdaptiveRBAC()
    
    def test_calculate_risk_score_basic(self):
        """Testa cálculo básico de risk score."""
        result = self.rbac.calculate_risk_score(
            user_role="user",
            prompt="Teste",
            user_id="user1"
        )
        assert result["risk_score"] >= 0
        assert result["risk_score"] <= 100
        assert result["risk_level"] in ["low", "medium", "high", "critical"]
        assert result["action"] in ["allow", "step_up", "block"]

