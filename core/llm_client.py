import os
print("MODEL_NAME ENV:", os.getenv("MODEL_NAME"))
import requests
from dotenv import load_dotenv

# Ortam değişkenlerini yükle
load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3-8b-chat-hf")

class LLMClient:
    def __init__(self, api_key=None, model_name=None):
        self.api_key = api_key or TOGETHER_API_KEY
        self.model_name = model_name or MODEL_NAME
        self.api_url = "https://api.together.ai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def generate(self, prompt, max_tokens=128, temperature=0.7):
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "Sen yardımcı bir yapay zekasın. Kullanıcıya daima ve sadece Türkçe cevap ver. İngilizce veya başka bir dilde asla cevap verme."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                print("Detaylı hata:", e.response.text)
            raise Exception(f"Together AI API Hatası: {str(e)}")

# Basit test
if __name__ == "__main__":
    client = LLMClient()
    try:
        cevap = client.generate("Merhaba, nasılsın?", max_tokens=100)
        print("Model Yanıtı:", cevap)
    except Exception as e:
        print(f"Hata: {str(e)}")
