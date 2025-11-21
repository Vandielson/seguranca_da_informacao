"""RBAC Adaptativo - Calcula risk score e controla acesso."""
from typing import Dict, Optional
from datetime import datetime


class AdaptiveRBAC:
    """RBAC adaptativo com cálculo de risk score."""
    
    def __init__(self):
        # Limiares de risco
        self.LOW_RISK_THRESHOLD = 30
        self.MEDIUM_RISK_THRESHOLD = 60
        self.HIGH_RISK_THRESHOLD = 80
        
        # Histórico de requisições (simulado - em produção seria um banco)
        self.request_history = {}
    
    def calculate_risk_score(
        self,
        user_role: str,
        prompt: str,
        user_id: Optional[str] = None,
        timestamp: Optional[datetime] = None
    ) -> Dict[str, any]:
        """
        Calcula o risk score da requisição.
        
        Args:
            user_role: Papel do usuário (admin, user, guest)
            prompt: Texto do prompt
            user_id: ID do usuário (opcional)
            timestamp: Timestamp da requisição (opcional)
        
        Returns:
            Dict com:
                - risk_score: score de risco (0-100)
                - risk_level: nível de risco (low, medium, high, critical)
                - action: ação recomendada (allow, step_up, block)
                - factors: fatores que contribuíram para o score
        """
        if timestamp is None:
            timestamp = datetime.now()
        
        risk_score = 0
        factors = []
        
        # Fator 1: Papel do usuário
        role_scores = {
            "admin": 10,
            "user": 30,
            "guest": 50
        }
        role_score = role_scores.get(user_role.lower(), 50)
        risk_score += role_score
        factors.append(f"role_{user_role}: {role_score}")
        
        # Fator 2: Horário (requisições fora do horário comercial = maior risco)
        hour = timestamp.hour
        if hour < 8 or hour > 18:
            time_risk = 20
            risk_score += time_risk
            factors.append(f"off_hours: {time_risk}")
        
        # Fator 3: Tamanho do prompt (prompts muito longos = maior risco)
        prompt_length = len(prompt)
        if prompt_length > 1000:
            length_risk = min(20, (prompt_length - 1000) // 100)
            risk_score += length_risk
            factors.append(f"long_prompt: {length_risk}")
        
        # Fator 4: Histórico de requisições (muitas requisições recentes = maior risco)
        if user_id:
            recent_requests = self._count_recent_requests(user_id, timestamp)
            if recent_requests > 10:
                history_risk = min(20, (recent_requests - 10) * 2)
                risk_score += history_risk
                factors.append(f"high_frequency: {history_risk}")
        
        # Limita risk_score a 100
        risk_score = min(risk_score, 100)
        
        # Determina nível de risco
        if risk_score < self.LOW_RISK_THRESHOLD:
            risk_level = "low"
            action = "allow"
        elif risk_score < self.MEDIUM_RISK_THRESHOLD:
            risk_level = "medium"
            action = "allow"
        elif risk_score < self.HIGH_RISK_THRESHOLD:
            risk_level = "high"
            action = "step_up"
        else:
            risk_level = "critical"
            action = "block"
        
        # Registra requisição no histórico
        if user_id:
            self._record_request(user_id, timestamp)
        
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "action": action,
            "factors": factors
        }
    
    def _count_recent_requests(self, user_id: str, timestamp: datetime) -> int:
        """Conta requisições recentes do usuário (últimos 5 minutos)."""
        if user_id not in self.request_history:
            return 0
        
        recent_count = 0
        cutoff_time = timestamp.timestamp() - 300  # 5 minutos
        
        for req_time in self.request_history[user_id]:
            if req_time > cutoff_time:
                recent_count += 1
        
        return recent_count
    
    def _record_request(self, user_id: str, timestamp: datetime):
        """Registra uma requisição no histórico."""
        if user_id not in self.request_history:
            self.request_history[user_id] = []
        
        self.request_history[user_id].append(timestamp.timestamp())
        
        # Mantém apenas últimas 100 requisições
        if len(self.request_history[user_id]) > 100:
            self.request_history[user_id] = self.request_history[user_id][-100:]

