import pytest
from rag.chunker import TextChunker
from utils.text_cleaner import TextCleaner

def test_text_chunker():
    chunker = TextChunker(chunk_size=100, chunk_overlap=20)
    
    # Test metni
    text = """Bu bir test paragrafıdır. İkinci cümle burada.
    Yeni bir paragraf başlıyor. Bu paragraf biraz daha uzun olacak.
    Üçüncü cümle de burada yer alıyor. Dördüncü cümle ile devam ediyoruz.
    Beşinci cümle de bu paragrafın son cümlesi olsun."""
    
    chunks = chunker.split_text(text)
    
    # Chunk'ların boş olmadığını kontrol et
    assert len(chunks) > 0
    
    # Her chunk'ın maksimum boyutu geçmediğini kontrol et
    for chunk in chunks:
        assert len(chunk) <= 100

def test_text_cleaner():
    cleaner = TextCleaner()
    
    # Test metni
    text = "  Bu   bir   test   metni...   !!!   "
    
    # Temizlenmiş metin
    cleaned = cleaner.clean_text(text)
    
    # Boşlukların normalize edildiğini kontrol et
    assert "  " not in cleaned
    
    # Noktalama işaretlerinin düzeltildiğini kontrol et
    assert "..." not in cleaned
    assert "!!!" not in cleaned

def test_multiple_documents():
    chunker = TextChunker()
    cleaner = TextCleaner()
    
    # Test belgeleri
    documents = [
        "Birinci belge. İkinci cümle.",
        "İkinci belge... Üçüncü cümle!!!"
    ]
    
    # Belgeleri temizle
    cleaned_docs = cleaner.clean_documents(documents)
    assert len(cleaned_docs) == 2
    
    # Belgeleri parçala
    chunks = chunker.split_documents(cleaned_docs)
    assert len(chunks) > 0 