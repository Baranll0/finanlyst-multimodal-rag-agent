from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from core.llm_client import LLMClient

class BaseAgent(ABC):
    def __init__(
        self,
        name: str,
        description: str,
        llm_client: LLMClient,
        system_prompt: Optional[str] = None
    ):
        """
        Temel ajan sınıfı.
        
        Args:
            name: Ajanın adı
            description: Ajanın açıklaması
            llm_client: LLM istemcisi
            system_prompt: Sistem promptu
        """
        self.name = name
        self.description = description
        self.llm_client = llm_client
        self.system_prompt = system_prompt or self._get_default_system_prompt()
        self.conversation_history: List[Dict[str, str]] = []

    def _get_default_system_prompt(self) -> str:
        """
        Varsayılan sistem promptunu döndürür.
        
        Returns:
            str: Sistem promptu
        """
        return f"""Sen {self.name} adlı bir yapay zeka ajanısın.
Görevin: {self.description}

Yanıtlarını Türkçe olarak ver.
Yanıtlarını kısa ve öz tut.
Bilmediğin konularda tahmin etme, "Bu konuda yeterli bilgim yok" de."""

    def _add_to_history(self, role: str, content: str) -> None:
        """
        Konuşma geçmişine mesaj ekler.
        
        Args:
            role: Mesajın rolü (system, user, assistant)
            content: Mesaj içeriği
        """
        self.conversation_history.append({
            "role": role,
            "content": content
        })

    def _get_conversation_context(self) -> str:
        """
        Konuşma geçmişini formatlar.
        
        Returns:
            str: Formatlanmış konuşma geçmişi
        """
        context = []
        for message in self.conversation_history[-5:]:  # Son 5 mesajı al
            role = message["role"]
            content = message["content"]
            context.append(f"{role}: {content}")
        return "\n".join(context)

    @abstractmethod
    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Girdiyi işler ve yanıt üretir.
        
        Args:
            input_data: İşlenecek girdi
            
        Returns:
            Dict[str, Any]: İşleme sonucu
        """
        pass

    def reset(self) -> None:
        """Konuşma geçmişini sıfırlar."""
        self.conversation_history = []
        self._add_to_history("system", self.system_prompt) 