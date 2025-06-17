import pytest
import pandas as pd
from agents.planner_agent import PlannerAgent

@pytest.mark.integration
def test_financial_analysis_flow(
    planner_agent: PlannerAgent,
    sample_financial_data: dict
):
    """Finansal analiz akışını test eder."""
    # Finansal veriyi işle
    result = planner_agent.process(sample_financial_data)
    
    # Sonuçları kontrol et
    assert result["task_type"] == "financial"
    assert result["agent"] == "Finansal Analiz Uzmanı"
    assert "analysis" in result["result"]
    assert "interpretation" in result["result"]
    
    # Analiz sonuçlarını kontrol et
    analysis = result["result"]["analysis"]
    assert "summary" in analysis
    assert "trends" in analysis
    assert "recommendations" in analysis

@pytest.mark.integration
def test_document_processing_flow(
    planner_agent: PlannerAgent,
    sample_document: str
):
    """Belge işleme akışını test eder."""
    # Belgeyi işle
    result = planner_agent.process(sample_document)
    
    # Sonuçları kontrol et
    assert result["task_type"] == "document"
    assert result["agent"] == "Belge İşleme Uzmanı"
    assert "processing_results" in result["result"]
    assert "summary" in result["result"]
    
    # İşleme sonuçlarını kontrol et
    processing = result["result"]["processing_results"]
    assert "chunk_count" in processing
    assert "total_length" in processing
    assert "average_chunk_length" in processing

@pytest.mark.integration
def test_document_qa_flow(
    planner_agent: PlannerAgent,
    sample_document: str
):
    """Belge soru-cevap akışını test eder."""
    # Önce belgeyi işle
    planner_agent.process(sample_document)
    
    # Belge hakkında soru sor
    question = "Python'ı kim geliştirdi?"
    result = planner_agent.query(question)
    
    # Sonuçları kontrol et
    assert "answer" in result
    assert "context" in result
    assert "sources" in result
    assert "similarity_scores" in result
    
    # Yanıtın doğruluğunu kontrol et
    assert "Guido van Rossum" in result["answer"]

@pytest.mark.integration
def test_unknown_task_flow(planner_agent: PlannerAgent):
    """Bilinmeyen görev akışını test eder."""
    # Geçersiz girdi
    result = planner_agent.process(123)
    
    # Sonuçları kontrol et
    assert result["task_type"] == "unknown"
    assert result["agent"] == "Bilinmeyen"
    assert "error" in result["result"]
    assert "input" in result["result"]

@pytest.mark.integration
def test_conversation_history(
    planner_agent: PlannerAgent,
    sample_financial_data: dict,
    sample_document: str
):
    """Konuşma geçmişi akışını test eder."""
    # İlk görev
    result1 = planner_agent.process(sample_financial_data)
    assert len(planner_agent.conversation_history) > 0
    
    # İkinci görev
    result2 = planner_agent.process(sample_document)
    assert len(planner_agent.conversation_history) > len(result1["result"])
    
    # Geçmişi sıfırla
    planner_agent.reset()
    assert len(planner_agent.conversation_history) == 1  # Sadece sistem mesajı 