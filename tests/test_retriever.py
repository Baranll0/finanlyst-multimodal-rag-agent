import pytest
from core.embeddings import EmbeddingModel
from core.llm_client import LLMClient
from rag.vector_store import VectorStore
from rag.retriever import RAGRetriever

@pytest.fixture
def embedding_model():
    return EmbeddingModel()

@pytest.fixture
def vector_store(embedding_model):
    return VectorStore(embedding_model=embedding_model)

@pytest.fixture
def llm_client():
    return LLMClient()

@pytest.fixture
def retriever(vector_store, llm_client):
    return RAGRetriever(
        vector_store=vector_store,
        llm_client=llm_client,
        top_k=2,
        similarity_threshold=0.8
    )

def test_retriever_initialization(retriever):
    assert retriever.top_k == 2
    assert retriever.similarity_threshold == 0.8
    assert retriever.vector_store is not None
    assert retriever.llm_client is not None

def test_context_formatting(retriever):
    # Test verileri
    results = [
        ("Python programlama dili", 0.5),
        ("Yapay zeka ve makine öğrenmesi", 0.9)
    ]
    
    # Bağlamı formatla
    context = retriever._format_context(results)
    
    # Sadece eşik değerinin altındaki sonuçların eklendiğini kontrol et
    assert "Python programlama dili" in context
    assert "Yapay zeka ve makine öğrenmesi" not in context

def test_prompt_creation(retriever):
    # Test verileri
    question = "Python nedir?"
    context = "Python programlama dili"
    
    # Prompt oluştur
    prompt = retriever._create_prompt(question, context)
    
    # Prompt içeriğini kontrol et
    assert question in prompt
    assert context in prompt
    assert "Bağlam:" in prompt
    assert "Soru:" in prompt
    assert "Yanıt:" in prompt

def test_query_flow(retriever, vector_store):
    # Test verileri
    texts = [
        "Python, yüksek seviyeli bir programlama dilidir.",
        "Python, Guido van Rossum tarafından geliştirilmiştir.",
        "Python, yorumlanan bir dildir."
    ]
    
    # Vektör veritabanına metinleri ekle
    vector_store.add_texts(texts)
    
    # Sorgu yap
    result = retriever.query("Python nedir?")
    
    # Sonuç yapısını kontrol et
    assert "answer" in result
    assert "context" in result
    assert "sources" in result
    assert "similarity_scores" in result
    
    # Kaynak sayısını kontrol et
    assert len(result["sources"]) <= retriever.top_k
    assert len(result["similarity_scores"]) <= retriever.top_k 