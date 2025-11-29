"""Firewall LLM - Detecta e bloqueia prompts maliciosos."""
import re
from typing import Dict, List, Optional
from src.config import MAX_PROMPT_LENGTH


class LLMFirewall:
    """Firewall para detectar e bloquear prompt injection e jailbreaks."""
    
    def __init__(self):
        # Padrões de prompt injection (exemplos básicos)
        self.injection_patterns = [
            r"ignore\s+all\s+previous\s+instructions",   # obrigatório para o teste
            r"ignore\s+(previous|all|above)",
            r"forget\s+(everything|all|previous)",
            r"system\s+prompt",                          # obrigatório para o teste
            r"reveal\s+your\s+system\s+prompt",          # obrigatório para o teste
            r"system\s*:",                               
            r"assistant\s*:",
            r"you\s+are\s+now",
            r"act\s+as\s+if",
            r"pretend\s+to\s+be",
            r"disregard\s+(all|previous)",
]
        
        # Padrões de jailbreak (exemplos básicos)
        self.jailbreak_patterns = [
            r"bypass",
            r"override",
            r"hack",
            r"exploit",
            r"vulnerability",
        ]
        
        # Compila regexes
        self.injection_regexes = [re.compile(pattern, re.IGNORECASE) for pattern in self.injection_patterns]
        self.jailbreak_regexes = [re.compile(pattern, re.IGNORECASE) for pattern in self.jailbreak_patterns]
    
    def check(self, prompt: str) -> Dict[str, any]:
        """
        Verifica se o prompt é malicioso.
        
        Returns:
            Dict com:
                - allowed: boolean indicando se o prompt é permitido
                - reason: motivo da rejeição (se houver)
                - detected_patterns: lista de padrões detectados
                - risk_score: score de risco (0-100)
        """
        if not prompt:
            return {
                "allowed": False,
                "reason": "Prompt vazio",
                "detected_patterns": [],
                "risk_score": 0
            }
        
        # Verifica tamanho
        if len(prompt) > MAX_PROMPT_LENGTH:
            return {
                "allowed": False,
                "reason": f"Prompt muito longo (máximo: {MAX_PROMPT_LENGTH} caracteres)",
                "detected_patterns": [],
                "risk_score": 100
            }
        
        detected_patterns = []
        risk_score = 0
        
        # Verifica padrões de injection
        for regex in self.injection_regexes:
            if regex.search(prompt):
                detected_patterns.append(f"injection: {regex.pattern}")
                risk_score += 30
        
        # Verifica padrões de jailbreak
        for regex in self.jailbreak_regexes:
            if regex.search(prompt):
                detected_patterns.append(f"jailbreak: {regex.pattern}")
                risk_score += 40
        
        # Limita risk_score a 100
        risk_score = min(risk_score, 100)
        
        # Se risk_score >= 50, bloqueia
        allowed = risk_score < 50
        
        return {
            "allowed": allowed,
            "reason": "Prompt malicioso detectado" if not allowed else None,
            "detected_patterns": detected_patterns,
            "risk_score": risk_score
        }

