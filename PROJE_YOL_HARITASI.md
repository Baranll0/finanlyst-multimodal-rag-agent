# Finanlyst Agent — Proje Yol Haritası

## 🎯 Amaç
Finanlyst Agent — Çok Modlu, RAG destekli, Ajan tabanlı, profesyonel bir Yapay Zeka Sistemi.

## 🧠 PROJE YOL HARİTASI — AŞAMA AŞAMA
Her bir aşama bir "modül" gibidir. Her modül tamamlandığında bir üst seviyeye geçersin. Hedef: iş başvurusunda gururla gösterebileceğin, baştan sona tek başına çıkardığın bir üretim seviyesi proje.

### 🔹 AŞAMA 1: Ortam Kurulumu & Yapılandırma
**Amaç:**
- Sanal ortam oluştur
- Ortam değişkenleri (.env)
- Bağımlılıklar (requirements.txt)
- config.py üzerinden yapılandırma

**Yapılacaklar:**
- Python sanal ortamı oluştur ve aktif et
- requirements.txt dosyasını hazırla
- .env dosyasını doldur
- config/ klasöründe config.py dosyasını yaz
- .env.example dosyasını da yedeğe koy

### 🔹 AŞAMA 2: LLM Entegrasyonu (Gemini)
**Amaç:**
- Gemini Pro API bağlantısını kurmak
- LLM isteklerini yönetmek

**Yapılacaklar:**
- Google AI Studio üzerinden Gemini API key al
- core/llm_client.py dosyasını yaz
- API key doğrulama kontrolü yap
- Basit bir test çağrısı yap ("Merhaba de")

### 🔹 AŞAMA 3: Gradio Arayüzü
**Amaç:**
- Basit bir frontend arayüzü kurmak
- Text input ve output alanları ile çalışan bir demo hazırlamak

**Yapılacaklar:**
- app/ui/ içinde interface.py oluştur
- app/main.py dosyasından UI'i ayağa kaldır
- Gradio GUI üzerinden prompt girip LLM yanıtını al
- UI ile backendi birbirine bağla

### 🔹 AŞAMA 4: Çok Modlu Girdi İşleme
**Amaç:**
- Kullanıcıdan PDF, görsel, CSV, Excel gibi veriler alabilmek

**Yapılacaklar:**
- core/document_parser.py oluştur
- PDF → metin, Görsel → OCR, CSV → dataframe, Excel → tablo olarak ayrıştır
- Kullanıcının yüklediği dosyaları uygun formata çevir
- Dosya uzantısına göre yönlendirme yaz
- Kullanıcının gönderdiği veriyi "tek biçimli metne" dönüştür

### 🔹 AŞAMA 5: Chunking & Metin Temizleme
**Amaç:**
- Uzun belgeleri parçalara ayırmak (chunk)
- Temiz, düzgün veri üretmek

**Yapılacaklar:**
- rag/chunker.py ve utils/text_cleaner.py oluştur
- Paragraf/paragraf veya cümle/cümle kır
- Chunk uzunluğunu ve örtüşmeyi ayarlanabilir yap
- Gereksiz karakterleri, boşlukları temizle
- Doğru prompt'lanabilir metin parçaları hazırla

### 🔹 AŞAMA 6: Vektörleştirme ve Vektör Veri Tabanı
**Amaç:**
- Belgeleri embedding'lere dönüştürmek
- FAISS veya Chroma DB içine kaydetmek

**Yapılacaklar:**
- core/embeddings.py içinde sentence-transformers veya başka bir modelle vektör çıkar
- rag/vector_store.py oluştur
- FAISS index oluştur, belge chunk'larını içine ata
- .save() ve .load() metodları yaz
- Test amaçlı bir dosya yükle, vektörlerini DB'ye kaydet

### 🔹 AŞAMA 7: Retriever & RAG Uygulaması
**Amaç:**
- Kullanıcının sorusuna göre ilgili belgeleri arayıp LLM'e bağlam vermek

**Yapılacaklar:**
- rag/retriever.py oluştur
- FAISS DB içinde semantik arama yap
- En alakalı n tane chunk'ı al
- Bunları bağlam olarak LLM'e gönder
- "Question + context" yapısıyla prompt hazırla

### 🔹 AŞAMA 8: Agent Mimarisi
**Amaç:**
- Ajan tabanlı bir yapı kurmak (multi-agent coordination)
- Görev bazlı uzman ajanlar

**Yapılacaklar:**
- agents/base_agent.py → Ortak sınıf
- agents/financial_agent.py → Veri analizi yapan
- agents/document_agent.py → Belge işleyen
- agents/retrieval_agent.py → RAG'le çalışan
- agents/planner_agent.py → Tüm ajanları koordine eden
- Prompt chaining + görev bölme yapısı kur
- Ajanların çalışma sırasını tanımlayan iş akışı oluştur

### 🔹 AŞAMA 9: Prompt Template Sistemi
**Amaç:**
- Promptları ayrı tutmak, merkezi yönetmek
- Gelişmiş prompt mühendisliği

**Yapılacaklar:**
- utils/prompt_templates.py oluştur
- Her ajan için prompt'ları ayrı şablonlara koy
- Promptlara değişken geçirme sistematiği kur
- Kapsamlı test promptları ile deneme yap

### 🔹 AŞAMA 10: Testler & Debug
**Amaç:**
- Projeyi bozulmaya karşı test etmek
- Hataları erken yakalamak

**Yapılacaklar:**
- tests/ klasöründe pytest veya unittest kullan
- Her core, agent, rag modülüne özel testler
- test_app.py ile UI testleri
- API key yoksa ne olur? Yanlış dosya gelirse? gibi senaryoları kontrol et

### 🔹 AŞAMA 11: CI/CD, Docker, Deployment
**Amaç:**
- Projeyi otomatik test & dağıtıma hazır hale getirmek

**Yapılacaklar:**
- Dockerfile oluştur
- docker-compose.yml yaz
- .github/workflows/ altında CI/CD YAML dosyası yaz
- Production sunucuya otomatik build & deploy pipeline kur
- Opsiyonel: Streamlit/Gradio app'ini bir bulut servise yükle (Render, GCP, AWS, vs.)

### 🔹 AŞAMA 12: README, Lisans, Belgeler
**Amaç:**
- Projeyi dış dünyaya sunmak
- İş başvurularında net anlatım sunmak

**Yapılacaklar:**
- README.md → demo videosu, mimari diyagram, teknolojiler
- LICENSE → MIT lisansı ekle
- notebooks/ klasörüne kullanım senaryosu
- PDF halini hazırla, GitHub'a yükle 