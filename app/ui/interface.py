import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from flask import Flask, render_template_string, request, redirect, url_for, flash
import pandas as pd
from agents.planner_agent import PlannerAgent
from agents.financial_agent import FinancialAgent
from agents.document_agent import DocumentAgent
from core.llm_client import LLMClient
from rag.retriever import RAGRetriever
from rag.vector_store import VectorStore
from core.embeddings import EmbeddingModel
from utils.prompt_templates import PromptManager
from utils.text_cleaner import TextCleaner
from rag.chunker import TextChunker
import PyPDF2
import json
from PIL import Image
import pytesseract

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "finanlyst-secret")

# --- Agent ve bağımlılıkları başlat ---
llm_client = LLMClient()
embedding_model = EmbeddingModel()
vector_store = VectorStore(embedding_model)
retriever = RAGRetriever(vector_store, llm_client)
chunker = TextChunker()
cleaner = TextCleaner()
prompt_manager = PromptManager()
financial_agent = FinancialAgent(llm_client)
document_agent = DocumentAgent(llm_client, retriever, chunker, cleaner)
planner_agent = PlannerAgent(llm_client, financial_agent, document_agent)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang=\"tr\">
<head>
    <meta charset=\"UTF-8\">
    <title>Finanlyst Agent - Demo</title>
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
    <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css\" rel=\"stylesheet\">
    <link rel=\"stylesheet\" href=\"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css\">
    <style>
        body { background: #f7f7f7; }
        .main-card { background: #fff; padding: 32px; border-radius: 16px; max-width: 700px; margin: 40px auto; box-shadow: 0 2px 16px #d0d0d0; }
        .result-card { background: #eafaf1; border: 1px solid #b2dfdb; border-radius: 12px; margin-top: 32px; padding: 24px; }
        .result-card h4 { color: #009688; }
        .spinner-border { width: 2.5rem; height: 2.5rem; }
        .custom-file-label { font-weight: 400; }
        .form-label { font-weight: 600; }
        .icon { color: #009688; margin-right: 8px; }
    </style>
</head>
<body>
    <div class=\"main-card\">
        <h2 class=\"mb-4\"><i class=\"fa-solid fa-robot icon\"></i>Finanlyst Agent</h2>
        <form method=\"POST\" enctype=\"multipart/form-data\" class=\"mb-3\">
            <div class=\"mb-3\">
                <label for=\"text\" class=\"form-label\">Metin Analizi</label>
                <textarea name=\"text\" id=\"text\" class=\"form-control\" placeholder=\"Buraya metin girin...\"></textarea>
            </div>
            <div class=\"mb-3\">
                <label for=\"file\" class=\"form-label\">CSV, PDF veya Görsel Yükle</label>
                <input type=\"file\" name=\"file\" id=\"file\" class=\"form-control\" accept=\".csv,.pdf,.png,.jpg,.jpeg,.webp\">
            </div>
            <button type=\"submit\" class=\"btn btn-success\"><i class=\"fa-solid fa-magnifying-glass-chart\"></i> Analiz Et</button>
        </form>
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for category, message in messages %}
              <div class=\"alert alert-danger\" role=\"alert\">{{ message }}</div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        {% if loading %}
        <div class=\"d-flex justify-content-center my-4\">
            <div class=\"spinner-border text-success\" role=\"status\">
              <span class=\"visually-hidden\">Yükleniyor...</span>
            </div>
        </div>
        {% endif %}
        {% if result %}
        <div class=\"result-card\">
            <h4><i class=\"fa-solid fa-chart-line icon\"></i>Analiz Sonucu</h4>
            {{ result|safe }}
        </div>
        {% endif %}
    </div>
    <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js\"></script>
</body>
</html>
"""

def format_result(result):
    """Agent sonucunu okunabilir HTML olarak biçimlendirir."""
    if isinstance(result, str):
        try:
            result = json.loads(result)
        except Exception:
            return f"<pre>{result}</pre>"
    if isinstance(result, dict):
        html = "<ul class='list-unstyled'>"
        for key, value in result.items():
            html += f"<li><b>{key.replace('_', ' ').capitalize()}:</b> "
            if isinstance(value, dict):
                html += "<ul>"
                for k, v in value.items():
                    html += f"<li><b>{k.replace('_', ' ').capitalize()}:</b> {v}</li>"
                html += "</ul>"
            elif isinstance(value, list):
                html += "<ul>"
                for v in value:
                    html += f"<li>{v}</li>"
                html += "</ul>"
            else:
                html += f"{value}</li>"
        html += "</ul>"
        return html
    return f"<pre>{str(result)}</pre>"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    formatted_result = None
    loading = False
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        file = request.files.get("file")
        try:
            loading = True
            if file and file.filename:
                filename = file.filename.lower()
                if filename.endswith(".csv"):
                    df = pd.read_csv(file)
                    agent_result = planner_agent.process(df)
                    formatted_result = format_result(agent_result)
                elif filename.endswith(".pdf"):
                    pdf_reader = PyPDF2.PdfReader(file)
                    pdf_text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
                    agent_result = planner_agent.process(pdf_text)
                    formatted_result = format_result(agent_result)
                elif filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
                    image = Image.open(file.stream)
                    ocr_text = pytesseract.image_to_string(image, lang="tur")
                    if not ocr_text.strip():
                        flash("Görselden metin çıkarılamadı.")
                    else:
                        agent_result = planner_agent.process(ocr_text)
                        formatted_result = format_result(agent_result)
                else:
                    flash("Sadece CSV, PDF veya görsel dosyası yükleyebilirsiniz.")
            elif text:
                agent_result = planner_agent.process(text)
                formatted_result = format_result(agent_result)
            else:
                flash("Lütfen analiz için metin girin veya dosya yükleyin.")
        except Exception as e:
            flash(f"Hata: {str(e)}")
        loading = False
    return render_template_string(HTML_TEMPLATE, result=formatted_result, loading=loading)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
