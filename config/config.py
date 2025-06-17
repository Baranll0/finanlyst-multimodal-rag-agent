import os
from dotenv import load_dotenv
from pathlib import Path

# .env dosyasını yükle
load_dotenv()

# Temel dizin yapısı
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
VECTOR_DB_DIR = DATA_DIR / "vector_db"
UPLOAD_DIR = DATA_DIR / "uploads"

# API Anahtarları
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Uygulama Ayarları
APP_ENV = os.getenv("APP_ENV", "development")
DEBUG = os.getenv("DEBUG", "True").lower() == "true"
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# RAG Ayarları
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "200"))
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "5"))

# Gradio Arayüzü
GRADIO_SERVER_PORT = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
GRADIO_SERVER_NAME = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")

# Dizinleri oluştur
for directory in [DATA_DIR, VECTOR_DB_DIR, UPLOAD_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Model Ayarları
MODEL_NAME = os.getenv("MODEL_NAME", "google/flan-t5-large")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

# Hugging Face Ayarları
HF_CACHE_DIR = DATA_DIR / "model_cache"
HF_CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Ajan Ayarları
AGENT_TIMEOUT = 30  # saniye
MAX_RETRIES = 3 