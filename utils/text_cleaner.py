import re
from typing import Optional

class TextCleaner:
    def __init__(self):
        # Gereksiz boşlukları temizlemek için regex
        self.whitespace_pattern = re.compile(r'\s+')
        # Özel karakterleri temizlemek için regex
        self.special_chars_pattern = re.compile(r'[^\w\s.,!?-]')
        # Birden fazla noktalama işaretini temizlemek için regex
        self.multiple_punctuation = re.compile(r'([.,!?])\1+')

    def clean_text(
        self,
        text: str,
        remove_special_chars: bool = False,
        normalize_whitespace: bool = True,
        remove_multiple_punctuation: bool = True
    ) -> str:
        """
        Metni temizler ve normalize eder.
        
        Args:
            text: Temizlenecek metin
            remove_special_chars: Özel karakterleri kaldır
            normalize_whitespace: Boşlukları normalize et
            remove_multiple_punctuation: Tekrarlanan noktalama işaretlerini temizle
            
        Returns:
            str: Temizlenmiş metin
        """
        if not text:
            return ""

        # Boşlukları normalize et
        if normalize_whitespace:
            text = self.whitespace_pattern.sub(' ', text)
            text = text.strip()

        # Özel karakterleri kaldır
        if remove_special_chars:
            text = self.special_chars_pattern.sub('', text)

        # Tekrarlanan noktalama işaretlerini temizle
        if remove_multiple_punctuation:
            text = self.multiple_punctuation.sub(r'\1', text)

        return text

    def clean_documents(
        self,
        documents: list[str],
        remove_special_chars: bool = False,
        normalize_whitespace: bool = True,
        remove_multiple_punctuation: bool = True
    ) -> list[str]:
        """
        Birden fazla belgeyi temizler.
        
        Args:
            documents: Temizlenecek belgeler listesi
            remove_special_chars: Özel karakterleri kaldır
            normalize_whitespace: Boşlukları normalize et
            remove_multiple_punctuation: Tekrarlanan noktalama işaretlerini temizle
            
        Returns:
            list[str]: Temizlenmiş belgeler listesi
        """
        return [
            self.clean_text(
                doc,
                remove_special_chars,
                normalize_whitespace,
                remove_multiple_punctuation
            )
            for doc in documents
        ]
