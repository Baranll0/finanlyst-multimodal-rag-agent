from typing import Any, Dict, List
import pandas as pd
from agents.base_agent import BaseAgent
from core.llm_client import LLMClient

class FinancialAgent(BaseAgent):
    def __init__(self, llm_client: LLMClient):
        """
        Finansal analiz ajanı.
        
        Args:
            llm_client: LLM istemcisi
        """
        super().__init__(
            name="Finansal Analiz Uzmanı",
            description="Finansal verileri analiz eder, trendleri tespit eder ve öneriler sunar.",
            llm_client=llm_client
        )

    def _analyze_financial_data(self, data: pd.DataFrame) -> Dict[str, Any]:
        """
        Finansal verileri analiz eder.
        
        Args:
            data: Finansal veri çerçevesi
            
        Returns:
            Dict[str, Any]: Analiz sonuçları
        """
        analysis = {
            "summary": {},
            "trends": [],
            "recommendations": []
        }
        
        # Temel istatistikler
        if "price" in data.columns:
            analysis["summary"]["ortalama_fiyat"] = data["price"].mean()
            analysis["summary"]["en_yüksek_fiyat"] = data["price"].max()
            analysis["summary"]["en_düşük_fiyat"] = data["price"].min()
            
            # Trend analizi
            if len(data) > 1:
                price_change = data["price"].pct_change()
                if price_change.iloc[-1] > 0:
                    analysis["trends"].append("Fiyatlar yükseliş trendinde")
                else:
                    analysis["trends"].append("Fiyatlar düşüş trendinde")
        
        # Hacim analizi
        if "volume" in data.columns:
            analysis["summary"]["ortalama_hacim"] = data["volume"].mean()
            if data["volume"].iloc[-1] > data["volume"].mean():
                analysis["trends"].append("İşlem hacmi ortalamanın üzerinde")
        
        return analysis

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Finansal verileri işler ve analiz eder.
        
        Args:
            input_data: İşlenecek finansal veri
            
        Returns:
            Dict[str, Any]: Analiz sonuçları
        """
        # Girdiyi DataFrame'e dönüştür
        if isinstance(input_data, pd.DataFrame):
            data = input_data
        elif isinstance(input_data, dict):
            data = pd.DataFrame(input_data)
        else:
            raise ValueError("Girdi DataFrame veya dict olmalıdır")
        
        # Veriyi analiz et
        analysis = self._analyze_financial_data(data)
        
        # LLM'e analiz sonuçlarını gönder
        prompt = f"""Aşağıdaki finansal analiz sonuçlarını yorumla ve öneriler sun:

Özet:
{analysis['summary']}

Trendler:
{', '.join(analysis['trends'])}

Lütfen bu bilgileri kullanarak kısa bir değerlendirme yap ve 2-3 öneri sun."""

        # LLM'den yanıt al
        response = self.llm_client.generate(prompt)
        
        # Konuşma geçmişine ekle
        self._add_to_history("user", prompt)
        self._add_to_history("assistant", response)
        
        return {
            "analysis": analysis,
            "interpretation": response
        }
