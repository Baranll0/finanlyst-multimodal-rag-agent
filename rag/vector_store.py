import os
import pickle
from typing import List, Tuple, Optional
import numpy as np
import faiss
from core.embeddings import EmbeddingModel

class VectorStore:
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        index_path: str = "data/vector_store",
        dimension: Optional[int] = None
    ):
        """
        Vektör veritabanını başlatır.
        
        Args:
            embedding_model: Embedding modeli
            index_path: FAISS index'inin kaydedileceği yol
            dimension: Vektör boyutu (None ise model'den alınır)
        """
        self.embedding_model = embedding_model
        self.index_path = index_path
        self.dimension = dimension or embedding_model.get_dimension()
        
        # FAISS index'ini oluştur
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Metinleri saklamak için liste
        self.texts: List[str] = []
        
        # Eğer kayıtlı index varsa yükle
        self._load_if_exists()

    def add_texts(self, texts: List[str]) -> None:
        """
        Metinleri vektör veritabanına ekler.
        
        Args:
            texts: Eklenecek metinler
        """
        # Metinleri vektörlere dönüştür
        embeddings = self.embedding_model.encode(texts)
        
        # FAISS index'ine ekle
        self.index.add(embeddings)
        
        # Metinleri sakla
        self.texts.extend(texts)
        
        # Değişiklikleri kaydet
        self._save()

    def similarity_search(
        self,
        query: str,
        k: int = 4
    ) -> List[Tuple[str, float]]:
        """
        Verilen sorguya en benzer metinleri bulur.
        
        Args:
            query: Arama sorgusu
            k: Döndürülecek sonuç sayısı
            
        Returns:
            List[Tuple[str, float]]: (metin, benzerlik skoru) çiftleri
        """
        # Sorguyu vektöre dönüştür
        query_vector = self.embedding_model.encode(query)
        
        # En yakın komşuları bul
        distances, indices = self.index.search(query_vector, k)
        
        # Sonuçları formatla
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.texts):  # Geçerli index kontrolü
                results.append((self.texts[idx], float(distance)))
        
        return results

    def _save(self) -> None:
        """FAISS index'ini ve metinleri kaydeder."""
        # Dizin oluştur
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        
        # FAISS index'ini kaydet
        faiss.write_index(self.index, f"{self.index_path}.index")
        
        # Metinleri kaydet
        with open(f"{self.index_path}.pkl", "wb") as f:
            pickle.dump(self.texts, f)

    def _load_if_exists(self) -> None:
        """Kayıtlı FAISS index'i ve metinleri yükler."""
        index_file = f"{self.index_path}.index"
        texts_file = f"{self.index_path}.pkl"
        
        if os.path.exists(index_file) and os.path.exists(texts_file):
            # FAISS index'ini yükle
            self.index = faiss.read_index(index_file)
            
            # Metinleri yükle
            with open(texts_file, "rb") as f:
                self.texts = pickle.load(f)
