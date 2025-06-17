from typing import Any, Dict, List, Optional
from agents.base_agent import BaseAgent
from agents.financial_agent import FinancialAgent
from agents.document_agent import DocumentAgent
from core.llm_client import LLMClient

class PlannerAgent(BaseAgent):
    def __init__(
        self,
        llm_client: LLMClient,
        financial_agent: FinancialAgent,
        document_agent: DocumentAgent
    ):
        """
        Planlayıcı ajan.
        
        Args:
            llm_client: LLM istemcisi
            financial_agent: Finansal analiz ajanı
            document_agent: Belge işleme ajanı
        """
        super().__init__(
            name="Görev Planlayıcı",
            description="Diğer ajanları koordine eder ve görevleri yönetir.",
            llm_client=llm_client
        )
        self.financial_agent = financial_agent
        self.document_agent = document_agent

    def _determine_task_type(self, input_data: Any) -> str:
        """
        Girdi tipine göre görev türünü belirler.
        
        Args:
            input_data: İşlenecek girdi
            
        Returns:
            str: Görev türü (financial, document, unknown)
        """
        if isinstance(input_data, (dict, list)) and any(
            key in str(input_data).lower()
            for key in ["price", "volume", "stock", "market", "financial"]
        ):
            return "financial"
        elif isinstance(input_data, str) and len(input_data) > 100:
            return "document"
        else:
            return "unknown"

    def _create_task_prompt(self, task_type: str, input_data: Any) -> str:
        """
        Görev tipine göre prompt oluşturur.
        
        Args:
            task_type: Görev türü
            input_data: İşlenecek girdi
            
        Returns:
            str: Görev promptu
        """
        if task_type == "financial":
            return f"""Finansal veri analizi yapılacak:
{input_data}

Lütfen veriyi analiz et ve öneriler sun."""
        
        elif task_type == "document":
            return f"""Belge işleme yapılacak:
{input_data[:200]}...

Lütfen belgeyi işle ve özetle."""
        
        else:
            return f"""Bilinmeyen görev türü:
{input_data}

Lütfen görevi analiz et ve uygun ajanı seç."""

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Girdiyi işler ve uygun ajanı seçer.
        
        Args:
            input_data: İşlenecek girdi
            
        Returns:
            Dict[str, Any]: İşleme sonuçları
        """
        # Görev türünü belirle
        task_type = self._determine_task_type(input_data)
        
        # Görev promptu oluştur
        task_prompt = self._create_task_prompt(task_type, input_data)
        
        # Konuşma geçmişine ekle
        self._add_to_history("user", task_prompt)
        
        # Görev türüne göre ajanı seç
        if task_type == "financial":
            result = self.financial_agent.process(input_data)
            agent_name = "Finansal Analiz Uzmanı"
        
        elif task_type == "document":
            result = self.document_agent.process(input_data)
            agent_name = "Belge İşleme Uzmanı"
        
        else:
            result = {
                "error": "Görev türü belirlenemedi",
                "input": str(input_data)
            }
            agent_name = "Bilinmeyen"
        
        # Sonucu konuşma geçmişine ekle
        self._add_to_history("assistant", f"{agent_name} görevi tamamladı")
        
        return {
            "task_type": task_type,
            "agent": agent_name,
            "result": result
        }

    def query(self, question: str) -> Dict[str, Any]:
        """
        Belge hakkında soru sorar.
        
        Args:
            question: Soru
            
        Returns:
            Dict[str, Any]: Yanıt ve ilgili bilgiler
        """
        return self.document_agent.query_document(question)
