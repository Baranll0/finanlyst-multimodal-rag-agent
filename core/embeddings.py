from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """
        Embedding modelini başlatır.
        
        Args:
            model_name: Kullanılacak model adı
        """
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """
        Metinleri vektörlere dönüştürür.
        
        Args:
            texts: Tek bir metin veya metin listesi
            
        Returns:
            np.ndarray: Embedding vektörleri
        """
        if isinstance(texts, str):
            texts = [texts]
        
        # Metinleri vektörlere dönüştür
        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )
        
        return embeddings

    def get_dimension(self) -> int:
        """
        Embedding vektörlerinin boyutunu döndürür.
        
        Returns:
            int: Vektör boyutu
        """
        return self.dimension
