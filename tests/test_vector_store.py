import pytest
import os
import shutil
from core.embeddings import EmbeddingModel
from rag.vector_store import VectorStore

@pytest.fixture
def embedding_model():
    return EmbeddingModel()

@pytest.fixture
def vector_store(embedding_model):
    # Test için geçici dizin
    test_dir = "test_data"
    os.makedirs(test_dir, exist_ok=True)
    
    store = VectorStore(
        embedding_model=embedding_model,
        index_path=f"{test_dir}/test_index"
    )
    
    yield store
    
    # Test sonrası temizlik
    shutil.rmtree(test_dir)

def test_embedding_model(embedding_model):
    # Test metni
    text = "Bu bir test cümlesidir."
    
    # Embedding oluştur
    embedding = embedding_model.encode(text)
    
    # Boyut kontrolü
    assert embedding.shape[0] == 1  # Tek metin
    assert embedding.shape[1] == embedding_model.get_dimension()

def test_vector_store_add_texts(vector_store):
    # Test metinleri
    texts = [
        "Python programlama dili",
        "Yapay zeka ve makine öğrenmesi",
        "Veri bilimi ve analizi"
    ]
    
    # Metinleri ekle
    vector_store.add_texts(texts)
    
    # Metin sayısı kontrolü
    assert len(vector_store.texts) == len(texts)

def test_vector_store_similarity_search(vector_store):
    # Test metinleri
    texts = [
        "Python programlama dili çok popüler",
        "Yapay zeka ve makine öğrenmesi geleceğin teknolojisi",
        "Veri bilimi ve analizi önemli bir alan"
    ]
    
    # Metinleri ekle
    vector_store.add_texts(texts)
    
    # Benzerlik araması yap
    query = "programlama dilleri"
    results = vector_store.similarity_search(query, k=2)
    
    # Sonuç kontrolü
    assert len(results) == 2
    assert isinstance(results[0][0], str)  # metin
    assert isinstance(results[0][1], float)  # benzerlik skoru

def test_vector_store_persistence(vector_store):
    # Test metinleri
    texts = ["Test metni 1", "Test metni 2"]
    
    # Metinleri ekle
    vector_store.add_texts(texts)
    
    # Yeni bir vector store oluştur (aynı dizini kullan)
    new_store = VectorStore(
        embedding_model=vector_store.embedding_model,
        index_path=vector_store.index_path
    )
    
    # Verilerin yüklendiğini kontrol et
    assert len(new_store.texts) == len(texts)
    assert new_store.texts == texts 