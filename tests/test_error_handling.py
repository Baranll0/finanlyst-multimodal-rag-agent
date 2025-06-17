import pytest
from agents.planner_agent import PlannerAgent
from agents.financial_agent import FinancialAgent
from agents.document_agent import DocumentAgent
from core.llm_client import LLMClient

@pytest.mark.unit
def test_invalid_financial_data(financial_agent: FinancialAgent):
    """Geçersiz finansal veri durumunu test eder."""
    # Geçersiz veri
    invalid_data = "Bu bir metin"
    
    # ValueError bekleniyor
    with pytest.raises(ValueError):
        financial_agent.process(invalid_data)

@pytest.mark.unit
def test_invalid_document_data(document_agent: DocumentAgent):
    """Geçersiz belge verisi durumunu test eder."""
    # Geçersiz veri
    invalid_data = 123
    
    # ValueError bekleniyor
    with pytest.raises(ValueError):
        document_agent.process(invalid_data)

@pytest.mark.unit
def test_empty_document(document_agent: DocumentAgent):
    """Boş belge durumunu test eder."""
    # Boş belge
    empty_doc = ""
    
    # İşleme sonuçlarını kontrol et
    result = document_agent.process(empty_doc)
    assert result["processing_results"]["chunk_count"] == 0
    assert result["processing_results"]["total_length"] == 0

@pytest.mark.unit
def test_invalid_question(document_agent: DocumentAgent):
    """Geçersiz soru durumunu test eder."""
    # Boş soru
    empty_question = ""
    
    # Sorgu sonuçlarını kontrol et
    result = document_agent.query_document(empty_question)
    assert "answer" in result
    assert "Bu konuda yeterli bilgim yok" in result["answer"]

@pytest.mark.unit
def test_llm_client_error(llm_client: LLMClient):
    """LLM istemcisi hata durumunu test eder."""
    # Geçersiz prompt
    invalid_prompt = None
    
    # TypeError bekleniyor
    with pytest.raises(TypeError):
        llm_client.get_completion(invalid_prompt)

@pytest.mark.integration
def test_planner_agent_error_handling(planner_agent: PlannerAgent):
    """Planlayıcı ajan hata durumlarını test eder."""
    # Geçersiz girdi
    invalid_input = None
    
    # Sonuçları kontrol et
    result = planner_agent.process(invalid_input)
    assert result["task_type"] == "unknown"
    assert "error" in result["result"]
    
    # Geçersiz soru
    invalid_question = None
    
    # TypeError bekleniyor
    with pytest.raises(TypeError):
        planner_agent.query(invalid_question)

@pytest.mark.integration
def test_concurrent_requests(planner_agent: PlannerAgent):
    """Eşzamanlı istek durumunu test eder."""
    import threading
    
    def process_request():
        try:
            planner_agent.process("Test veri")
        except Exception as e:
            assert False, f"Eşzamanlı istek hatası: {str(e)}"
    
    # Birden fazla istek oluştur
    threads = []
    for _ in range(5):
        thread = threading.Thread(target=process_request)
        threads.append(thread)
        thread.start()
    
    # Tüm isteklerin tamamlanmasını bekle
    for thread in threads:
        thread.join() 