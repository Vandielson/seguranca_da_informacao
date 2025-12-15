"""Firewall LLM - Detecta e bloqueia prompts maliciosos.

Objetivo prático:
- Bloquear ataques claros (prompt injection / jailbreak).
- Evitar falso-positivo: quando não há problema, deve seguir normalmente.
"""
import re
from typing import Dict, List, Tuple

from config import MAX_PROMPT_LENGTH


class LLMFirewall:
    """Firewall para detectar e bloquear prompt injection e jailbreaks."""

    def __init__(self):
        strong_injection: List[str] = [
            r"ignore\s+all\s+previous\s+instructions",
            r"reveal\s+your\s+system\s+prompt",
            r"system\s+prompt",
            r"forget\s+(everything|all|previous)",
            r"disregard\s+(all|previous)",
        ]

        weak_injection: List[str] = [
            r"ignore\s+(previous|all|above)",
            r"system\s*:",
            r"assistant\s*:",
            r"you\s+are\s+now",
            r"act\s+as\s+if",
            r"pretend\s+to\s+be",
        ]

        weak_jailbreak: List[str] = [
            r"bypass",
            r"override",
            r"hack",
            r"exploit",
            r"vulnerability",
        ]

        self.rules: List[Tuple[str, str, int]] = []
        self.rules += [("strong", p, 85) for p in strong_injection]
        self.rules += [("weak_injection", p, 20) for p in weak_injection]
        self.rules += [("weak_jailbreak", p, 15) for p in weak_jailbreak]

        self._compiled = [(kind, re.compile(pat, re.IGNORECASE), weight, pat) for kind, pat, weight in self.rules]

    def check(self, prompt: str) -> Dict[str, object]:
        if not prompt:
            return {"allowed": False, "reason": "Prompt vazio", "detected_patterns": [], "risk_score": 0}

        if len(prompt) > MAX_PROMPT_LENGTH:
            return {
                "allowed": False,
                "reason": f"Prompt excede o tamanho máximo ({MAX_PROMPT_LENGTH} caracteres)",
                "detected_patterns": [],
                "risk_score": 100,
            }

        detected_patterns: List[str] = []
        risk_score = 0
        strong_hits = 0
        weak_hits = 0

        for kind, rx, weight, pat_text in self._compiled:
            if rx.search(prompt):
                detected_patterns.append(pat_text)
                risk_score += weight
                if kind == "strong":
                    strong_hits += 1
                else:
                    weak_hits += 1

        risk_score = min(risk_score, 100)

        if strong_hits >= 1:
            return {
                "allowed": False,
                "reason": "Prompt injection/jailbreak forte detectado",
                "detected_patterns": detected_patterns,
                "risk_score": risk_score,
            }

        if weak_hits >= 3 and risk_score >= 50:
            return {
                "allowed": False,
                "reason": "Combinação de sinais fracos sugere prompt malicioso",
                "detected_patterns": detected_patterns,
                "risk_score": risk_score,
            }

        return {"allowed": True, "reason": None, "detected_patterns": detected_patterns, "risk_score": risk_score}
