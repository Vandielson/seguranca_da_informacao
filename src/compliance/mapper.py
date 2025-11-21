"""Mapper de Conformidade - Mapeia controles para normas."""
from typing import Dict, List
from datetime import datetime


class ComplianceMapper:
    """Mapeia controles técnicos para requisitos de conformidade."""
    
    def __init__(self):
        # Mapeamento de controles para normas
        self.control_mappings = {
            "input_sanitization": {
                "eu_ai_act": ["Article 9", "Article 10"],
                "owasp": ["LLM01", "LLM02"],
                "iso": ["ISO/IEC 27001:2022 A.9.4"],
                "enisa": ["ENISA AI Security Guidelines"]
            },
            "firewall_llm": {
                "eu_ai_act": ["Article 15"],
                "owasp": ["LLM03", "LLM04"],
                "iso": ["ISO/IEC 27001:2022 A.12.6"],
                "enisa": ["ENISA AI Security Guidelines"]
            },
            "rbac_adaptive": {
                "eu_ai_act": ["Article 9"],
                "owasp": ["LLM05"],
                "iso": ["ISO/IEC 27001:2022 A.9.2"],
                "enisa": ["ENISA AI Security Guidelines"]
            },
            "output_sanitization": {
                "eu_ai_act": ["Article 10"],
                "owasp": ["LLM06"],
                "iso": ["ISO/IEC 27001:2022 A.9.4"],
                "enisa": ["ENISA AI Security Guidelines"]
            }
        }
    
    def map_controls(self, controls_applied: List[str]) -> Dict[str, any]:
        """
        Mapeia controles aplicados para requisitos de conformidade.
        
        Args:
            controls_applied: Lista de controles aplicados
        
        Returns:
            Dict com mapeamento de conformidade
        """
        compliance_evidence = {
            "timestamp": datetime.now().isoformat(),
            "controls_applied": controls_applied,
            "compliance_mapping": {},
            "standards_covered": set()
        }
        
        # Mapeia cada controle
        for control in controls_applied:
            if control in self.control_mappings:
                compliance_evidence["compliance_mapping"][control] = self.control_mappings[control]
                
                # Adiciona padrões cobertos
                for standard in self.control_mappings[control].keys():
                    compliance_evidence["standards_covered"].add(standard)
        
        # Converte set para list para serialização JSON
        compliance_evidence["standards_covered"] = list(compliance_evidence["standards_covered"])
        
        return compliance_evidence
    
    def generate_audit_log(self, request_data: Dict, response_data: Dict) -> Dict[str, any]:
        """
        Gera log de auditoria estruturado.
        
        Args:
            request_data: Dados da requisição
            response_data: Dados da resposta
        
        Returns:
            Log de auditoria estruturado
        """
        return {
            "timestamp": datetime.now().isoformat(),
            "request_id": request_data.get("request_id"),
            "user_id": request_data.get("user_id"),
            "user_role": request_data.get("user_role"),
            "prompt": request_data.get("prompt"),
            "controls_applied": request_data.get("controls_applied", []),
            "risk_score": request_data.get("risk_score"),
            "firewall_result": request_data.get("firewall_result"),
            "response_length": len(response_data.get("response", "")),
            "compliance_evidence": self.map_controls(request_data.get("controls_applied", []))
        }

