import pytest
import os
import shutil
from core.llm_client import LLMClient
from core.embeddings import EmbeddingModel
from rag.vector_store import VectorStore
from rag.retriever import RAGRetriever
from rag.chunker import TextChunker
from utils.text_cleaner import TextCleaner
from utils.prompt_templates import PromptManager
from agents.financial_agent import FinancialAgent
from agents.document_agent import DocumentAgent
from agents.planner_agent import PlannerAgent

@pytest.fixture(scope="session")
def llm_client():
    """LLM istemcisi fixture'ı."""
    return LLMClient()

@pytest.fixture(scope="session")
def embedding_model():
    """Embedding modeli fixture'ı."""
    return EmbeddingModel()

@pytest.fixture(scope="session")
def vector_store(embedding_model):
    """Vektör veritabanı fixture'ı."""
    return VectorStore(embedding_model=embedding_model)

@pytest.fixture(scope="session")
def retriever(vector_store, llm_client):
    """RAG retriever fixture'ı."""
    return RAGRetriever(
        vector_store=vector_store,
        llm_client=llm_client
    )

@pytest.fixture(scope="session")
def chunker():
    """Metin parçalayıcı fixture'ı."""
    return TextChunker()

@pytest.fixture(scope="session")
def cleaner():
    """Metin temizleyici fixture'ı."""
    return TextCleaner()

@pytest.fixture(scope="session")
def prompt_manager():
    """Prompt yöneticisi fixture'ı."""
    return PromptManager()

@pytest.fixture(scope="session")
def financial_agent(llm_client):
    """Finansal ajan fixture'ı."""
    return FinancialAgent(llm_client=llm_client)

@pytest.fixture(scope="session")
def document_agent(llm_client, retriever, chunker, cleaner):
    """Belge ajanı fixture'ı."""
    return DocumentAgent(
        llm_client=llm_client,
        retriever=retriever,
        chunker=chunker,
        cleaner=cleaner
    )

@pytest.fixture(scope="session")
def planner_agent(llm_client, financial_agent, document_agent):
    """Planlayıcı ajan fixture'ı."""
    return PlannerAgent(
        llm_client=llm_client,
        financial_agent=financial_agent,
        document_agent=document_agent
    )

@pytest.fixture(scope="function")
def temp_dir():
    """Geçici dizin fixture'ı."""
    # Test için geçici dizin oluştur
    temp_dir = "test_temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    yield temp_dir
    
    # Test sonrası temizlik
    shutil.rmtree(temp_dir)

@pytest.fixture(scope="function")
def sample_financial_data():
    """Örnek finansal veri fixture'ı."""
    return {
        "price": [100, 105, 98, 110, 115],
        "volume": [1000, 1200, 800, 1500, 1300],
        "date": ["2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"]
    }

@pytest.fixture(scope="function")
def sample_document():
    """Örnek belge fixture'ı."""
    return """Python programlama dili, Guido van Rossum tarafından 1991 yılında geliştirilmiştir.
Yüksek seviyeli, yorumlanan ve genel amaçlı bir programlama dilidir.
Python'ın tasarım felsefesi, kodun okunabilirliğini vurgular ve sözdizimi, programcıların daha az kod yazarak kavramları ifade etmelerine olanak tanır.
Python, dinamik tipli ve çöp toplamalı bir dildir. Çoklu programlama paradigmalarını destekler:
- Nesne yönelimli programlama
- Yapısal programlama
- Fonksiyonel programlama
- Aspect-oriented programlama""" 