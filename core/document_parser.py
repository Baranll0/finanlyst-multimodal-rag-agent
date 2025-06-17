import os
import pandas as pd
from PIL import Image
import pdfplumber
import pytesseract

# PDF'den metin çıkarma
def parse_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

# Görselden metin çıkarma (OCR)
def parse_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image, lang='tur')
    return text

# CSV'den dataframe çıkarma
def parse_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string(index=False)

# Excel'den tablo çıkarma
def parse_excel(file_path):
    df = pd.read_excel(file_path)
    return df.to_string(index=False)

# Dosya uzantısına göre yönlendirme
def parse_document(file_path):
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == '.pdf':
        return parse_pdf(file_path)
    elif ext in ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']:
        return parse_image(file_path)
    elif ext == '.csv':
        return parse_csv(file_path)
    elif ext in ['.xls', '.xlsx']:
        return parse_excel(file_path)
    else:
        raise ValueError(f"Desteklenmeyen dosya türü: {ext}")
