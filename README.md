# Finanlyst Agent

Çok modlu, RAG destekli, ajan tabanlı profesyonel bir Yapay Zeka Sistemi.

## 🚀 Özellikler

- 🤖 Çoklu Ajan Mimarisi
- 📚 RAG (Retrieval-Augmented Generation) Desteği
- 📊 Finansal Veri Analizi
- 📄 Çoklu Format Desteği (PDF, Excel, CSV, Görsel)
- 🎯 Akıllı Belge İşleme
- 💡 Gradio Web Arayüzü

## 🛠️ Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/yourusername/financial-agents.git
cd financial-agents
```

2. Sanal ortam oluşturun ve aktif edin:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# veya
.\venv\Scripts\activate  # Windows
```

3. Bağımlılıkları yükleyin:
```bash
pip install -r requirements.txt
```

4. `.env` dosyasını oluşturun:
```bash
cp .env.example .env
```

5. `.env` dosyasını düzenleyin ve gerekli API anahtarlarını ekleyin.

## 🏃‍♂️ Çalıştırma

```bash
python app/main.py
```

Uygulama varsayılan olarak http://localhost:7860 adresinde çalışacaktır.

## 📁 Proje Yapısı

```
financial-agents/
├── agents/           # Ajan tanımlamaları
├── app/             # Ana uygulama
├── core/            # Çekirdek işlevsellik
├── rag/             # RAG implementasyonu
├── utils/           # Yardımcı fonksiyonlar
├── tests/           # Test dosyaları
├── config/          # Yapılandırma
└── notebooks/       # Jupyter notebook'ları
```

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.
