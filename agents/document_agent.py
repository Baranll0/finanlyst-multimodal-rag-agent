from typing import Any, Dict, List
from agents.base_agent import BaseAgent
from core.llm_client import LLMClient
from rag.retriever import RAGRetriever
from rag.chunker import TextChunker
from utils.text_cleaner import TextCleaner

class DocumentAgent(BaseAgent):
    def __init__(
        self,
        llm_client: LLMClient,
        retriever: RAGRetriever,
        chunker: TextChunker,
        cleaner: TextCleaner
    ):
        """
        Belge işleme ajanı.
        
        Args:
            llm_client: LLM istemcisi
            retriever: RAG retriever
            chunker: Metin parçalayıcı
            cleaner: Metin temizleyici
        """
        super().__init__(
            name="Belge İşleme Uzmanı",
            description="Belgeleri işler, analiz eder ve özetler.",
            llm_client=llm_client
        )
        self.retriever = retriever
        self.chunker = chunker
        self.cleaner = cleaner

    def _process_document(self, text: str) -> Dict[str, Any]:
        """
        Belgeyi işler ve analiz eder.
        
        Args:
            text: İşlenecek metin
            
        Returns:
            Dict[str, Any]: İşleme sonuçları
        """
        # Metni temizle
        cleaned_text = self.cleaner.clean_text(text)
        
        # Metni parçalara ayır
        chunks = self.chunker.split_text(cleaned_text)
        
        # Parçaları vektör veritabanına ekle
        self.retriever.vector_store.add_texts(chunks)
        
        return {
            "chunk_count": len(chunks),
            "total_length": len(cleaned_text),
            "average_chunk_length": len(cleaned_text) / len(chunks) if chunks else 0
        }

    def _summarize_document(self, text: str) -> str:
        """
        Belgeyi özetler.
        
        Args:
            text: Özetlenecek metin
            
        Returns:
            str: Belge özeti
        """
        prompt = f"""Aşağıdaki metni ana noktaları, önemli detayları ve tüm kritik bilgileri içerecek şekilde ayrıntılı olarak özetle. Yanıtını sadece Türkçe ver. Gerekiyorsa çok uzun ve kapsamlı bir özet oluştur.

Metin:
{text}

Ayrıntılı özet:"""
        return self.llm_client.generate(prompt, max_tokens=1024)

    def process(self, input_data: Any) -> Dict[str, Any]:
        """
        Belgeyi işler ve analiz eder.
        
        Args:
            input_data: İşlenecek belge
            
        Returns:
            Dict[str, Any]: İşleme sonuçları
        """
        if not isinstance(input_data, str):
            raise ValueError("Girdi string olmalıdır")
        
        # Belgeyi işle
        processing_results = self._process_document(input_data)
        
        # Belgeyi özetle
        summary = self._summarize_document(input_data)
        
        # Konuşma geçmişine ekle
        self._add_to_history("user", "Belge işlendi ve özetlendi")
        self._add_to_history("assistant", summary)
        
        return {
            "processing_results": processing_results,
            "summary": summary
        }

    def query_document(self, question: str) -> Dict[str, Any]:
        """
        Belge hakkında soru sorar.
        
        Args:
            question: Soru
            
        Returns:
            Dict[str, Any]: Yanıt ve ilgili bilgiler
        """
        return self.retriever.query(question)
