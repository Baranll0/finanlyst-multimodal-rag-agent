from typing import List, Dict, Any
from rag.vector_store import VectorStore
from core.llm_client import LLMClient

class RAGRetriever:
    def __init__(
        self,
        vector_store: VectorStore,
        llm_client: LLMClient,
        top_k: int = 4,
        similarity_threshold: float = 0.7
    ):
        """
        RAG retriever'ı başlatır.
        
        Args:
            vector_store: Vektör veritabanı
            llm_client: LLM istemcisi
            top_k: Döndürülecek en alakalı belge sayısı
            similarity_threshold: Benzerlik eşiği
        """
        self.vector_store = vector_store
        self.llm_client = llm_client
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def _format_context(self, results: List[tuple]) -> str:
        """
        Benzerlik arama sonuçlarını bağlam metnine dönüştürür.
        
        Args:
            results: (metin, benzerlik skoru) çiftleri
            
        Returns:
            str: Formatlanmış bağlam metni
        """
        context_parts = []
        
        for text, score in results:
            if score <= self.similarity_threshold:
                context_parts.append(f"İlgili bilgi: {text}")
        
        return "\n\n".join(context_parts)

    def _create_prompt(self, question: str, context: str) -> str:
        """
        Soru ve bağlamı kullanarak prompt oluşturur.
        
        Args:
            question: Kullanıcı sorusu
            context: İlgili bağlam
            
        Returns:
            str: Formatlanmış prompt
        """
        return f"""Aşağıdaki bağlamı kullanarak soruyu yanıtla. 
Eğer bağlamda yanıt için yeterli bilgi yoksa, "Bu konuda yeterli bilgim yok" de.

Bağlam:
{context}

Soru: {question}

Yanıt:"""

    def query(self, question: str) -> Dict[str, Any]:
        """
        Kullanıcı sorusunu yanıtlar.
        
        Args:
            question: Kullanıcı sorusu
            
        Returns:
            Dict[str, Any]: Yanıt ve ilgili bilgiler
        """
        # Benzer belgeleri bul
        results = self.vector_store.similarity_search(
            query=question,
            k=self.top_k
        )
        
        # Bağlamı oluştur
        context = self._format_context(results)
        
        # Prompt oluştur
        prompt = self._create_prompt(question, context)
        
        # LLM'den yanıt al
        response = self.llm_client.get_completion(prompt)
        
        return {
            "answer": response,
            "context": context,
            "sources": [text for text, _ in results],
            "similarity_scores": [score for _, score in results]
        }
