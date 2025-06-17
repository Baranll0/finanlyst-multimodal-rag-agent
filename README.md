# Finanlyst Agent: Çok Modlu, RAG Destekli Finansal Yapay Zeka Sistemi

![Finanlyst Agent](https://img.shields.io/badge/AI-Finance-blue)

Finanlyst Agent, metin, CSV, PDF ve görsel (PNG, JPG) dosyalarını analiz edebilen, RAG (Retrieval-Augmented Generation) destekli, çok modlu ve ajan tabanlı bir yapay zeka platformudur. Finansal analiz, belge özetleme, doküman tabanlı soru-cevap ve daha fazlası için modern bir arayüz sunar.

---

## 🚀 Özellikler
- **Çok Modlu Girdi:** Metin, CSV, PDF ve görsel dosyalarını analiz edebilme
- **RAG Pipeline:** Vektör veritabanı ile dokümanlardan bilgi çekme ve LLM ile birleştirme
- **Ajan Mimarisi:** Finansal analiz, belge işleme ve planlayıcı ajanlar
- **Sohbet Geçmişi:** Oturum bazlı geçmiş ve doküman üzerinden tekrar tekrar soru sorma
- **Modern Arayüz:** Bootstrap tabanlı, kullanıcı dostu ve responsive web arayüzü
- **Türkçe Destek:** Tüm analizler ve özetler Türkçe olarak sunulur
- **Kolay Dağıtım:** Docker ve docker-compose desteği

---

## 📦 Kurulum

### 1. Depoyu Klonla
```sh
git clone https://github.com/Baranll0/finanlyst-multimodal-rag-agent.git
cd finanlyst-multimodal-rag-agent
```

### 2. Ortamı Hazırla
Python 3.9+ önerilir.
```sh
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
```

### 3. Ortam Değişkenlerini Ayarla
`.env.example` dosyasını `.env` olarak kopyala ve doldur:
```sh
cp .env.example .env
```
Gerekli anahtarlar:
- `TOGETHER_API_KEY` (Together AI veya Hugging Face API anahtarı)
- `MODEL_NAME` (örn: meta-llama/Llama-3-8b-chat-hf)

### 4. (İsteğe Bağlı) Docker ile Çalıştır
```sh
docker-compose up --build
```

---

## 🖥️ Kullanım

### Uygulamayı Başlat
```sh
python app/ui/interface.py
```

Tarayıcıda `http://localhost:5000` adresine git.

### Özellikler:
- **Metin Analizi:** Metin kutusuna yazıp analiz et.
- **CSV/PDF/Görsel Yükle:** Dosya yükleyip özet ve analiz al.
- **Sohbete Devam Et:** Yüklediğin doküman üzerinden tekrar tekrar soru sor.
- **Sonuçlar:** Özet, istatistikler ve detaylar kart içinde gösterilir.

---

## 🧠 Mimarinin Özeti

- **Ajanlar:**
  - `FinancialAgent`: Finansal veri analizi ve öneriler
  - `DocumentAgent`: Belge özetleme, vektör veritabanı, doküman tabanlı QA
  - `PlannerAgent`: Görev türünü belirler ve uygun ajana yönlendirir
- **RAG Pipeline:**
  - Metinler embedding ile vektör veritabanına eklenir
  - Soru geldiğinde en alakalı içerik çekilir ve LLM'e iletilir
- **Frontend:**
  - Bootstrap tabanlı, modern ve responsive arayüz
  - Dosya yükleme, metin kutusu, analiz sonucu kartı, yükleme animasyonu

---

## 📄 Örnek Kullanım

1. **PDF Yükle:**
   - PDF dosyasını yükle, özet ve istatistikleri gör.
2. **Soru Sor:**
   - "Bu dokümanda X nasıl yapılır?" gibi sorular sor, sistem dokümandan yanıt üretir.
3. **CSV Yükle:**
   - Finansal CSV dosyası yükle, otomatik analiz ve öneriler al.
4. **Görsel Yükle:**
   - Fatura, makbuz veya ekran görüntüsü yükle, OCR ile metin çıkar ve analiz et.

---

## 🛠️ Geliştirici Notları
- **.env** dosyasını asla repoya yükleme!
- Büyük dosyalar için Git LFS kullanabilirsin.
- Testler için `pytest` desteği vardır: `pytest`
- Prompt şablonları `config/prompts/` klasöründe JSON olarak tutulur.

---

## 🤝 Katkı ve Geliştirme

1. Fork'la ve yeni bir branch aç.
2. Değişikliklerini yap, test et.
3. Pull request gönder.

---

## 📢 Lisans

MIT Lisansı ile sunulmuştur.

---

## 📬 İletişim & Destek

Her türlü soru, öneri ve katkı için [GitHub Issues](https://github.com/Baranll0/finanlyst-multimodal-rag-agent/issues) üzerinden iletişime geçebilirsin.
