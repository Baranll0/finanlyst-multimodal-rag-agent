import sys
import os
import uuid
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from flask import Flask, render_template_string, request, redirect, url_for, flash, session, jsonify
import pandas as pd
from agents.planner_agent import PlannerAgent
from agents.financial_agent import FinancialAgent
from agents.document_agent import DocumentAgent
from core.llm_client import LLMClient
from rag.retriever import RAGRetriever
from rag.vector_store import PineconeVectorStore
from core.embeddings import EmbeddingModel
from utils.prompt_templates import PromptManager
from utils.text_cleaner import TextCleaner
from rag.chunker import TextChunker
import PyPDF2
import json
from PIL import Image
import pytesseract
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.secret_key = os.environ.get("SECRET_KEY", "finanlyst-secret")

# --- Agent ve bağımlılıkları başlat ---
llm_client = LLMClient()
embedding_model = EmbeddingModel()
# Her oturum için ayrı index ismi oluşturulacak
retriever = None
chunker = TextChunker()
cleaner = TextCleaner()
prompt_manager = PromptManager()
financial_agent = FinancialAgent(llm_client)
document_agent = None
planner_agent = None

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
        <form method=\"POST\" class=\"mb-3\">
            <div class=\"mb-3\">
                <label for=\"followup\" class=\"form-label\">Sohbete Devam Et / Soru Sor</label>
                <input type=\"text\" name=\"followup\" id=\"followup\" class=\"form-control\" placeholder=\"Yüklediğiniz doküman hakkında soru sorun...\">
            </div>
            <button type=\"submit\" name=\"followup_btn\" value=\"1\" class=\"btn btn-primary\"><i class=\"fa-solid fa-comments\"></i> Soru Sor</button>
            <button type=\"submit\" name=\"reset_btn\" value=\"1\" class=\"btn btn-outline-danger ms-2\"><i class=\"fa-solid fa-eraser\"></i> Yeni Sohbet Başlat</button>
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

def get_session_index():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
    return f"finanlyst-index-{session['session_id']}"

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
    global retriever, document_agent, planner_agent
    result = None
    formatted_result = None
    loading = False
    # Oturuma özel index ve agent başlat
    index_name = "finanlyst-index"
    session_id = session.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        session["session_id"] = session_id
    vector_store = PineconeVectorStore(session_id=session_id, index_name=index_name)
    retriever = RAGRetriever(vector_store, llm_client)
    document_agent = DocumentAgent(llm_client, retriever, chunker, cleaner)
    planner_agent = PlannerAgent(llm_client, financial_agent, document_agent)

    if request.method == "POST":
        # Yeni sohbet başlat
        if request.form.get("reset_btn"):
            session.clear()
            flash("Yeni bir sohbet başlatıldı. Önce doküman veya veri yükleyin.")
            return redirect(url_for("index"))
        # Sohbete devam et (soru sor)
        followup = request.form.get("followup", "").strip()
        if request.form.get("followup_btn") and followup:
            try:
                agent_result = planner_agent.process(followup)
                formatted_result = format_result(agent_result)
            except Exception as e:
                flash(f"Hata: {str(e)}")
            return render_template_string(HTML_TEMPLATE, result=formatted_result, loading=loading)
        # Dosya/metin yükleme
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

@app.route("/api/chat", methods=["POST"])
def api_chat():
    global retriever, document_agent, planner_agent
    session_id = session.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
        session["session_id"] = session_id
    # Oturuma özel agent başlat (gerekirse)
    index_name = "finanlyst-index"
    vector_store = PineconeVectorStore(session_id=session_id, index_name=index_name)
    retriever = RAGRetriever(vector_store, llm_client)
    document_agent = DocumentAgent(llm_client, retriever, chunker, cleaner)
    planner_agent = PlannerAgent(llm_client, financial_agent, document_agent)

    text = request.form.get("message", "").strip()
    file = request.files.get("file")
    try:
        input_data = None
        if file and file.filename:
            filename = file.filename.lower()
            if filename.endswith(".csv"):
                df = pd.read_csv(file)
                file_content = df
            elif filename.endswith(".pdf"):
                pdf_reader = PyPDF2.PdfReader(file)
                file_content = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
            elif filename.endswith((".png", ".jpg", ".jpeg", ".webp")):
                image = Image.open(file.stream)
                file_content = pytesseract.image_to_string(image, lang="tur")
            else:
                return jsonify({"reply": "Sadece CSV, PDF veya görsel dosyası yükleyebilirsiniz."})
            if text:
                # Prompt ve dosya birlikte: birleştir, tuple olarak gönder
                input_data = {"prompt": text, "file_content": file_content}
            else:
                input_data = file_content
        elif text:
            input_data = text
        else:
            return jsonify({"reply": "Lütfen analiz için metin girin veya dosya yükleyin."})
        # Akıllı agent ile işle
        agent_result = planner_agent.process(input_data)
        # Sonucu string veya dict olarak döndür
        if isinstance(agent_result, dict):
            reply = agent_result.get("result") or agent_result
        else:
            reply = agent_result
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"Hata: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
