from typing import List, Optional
import re

class TextChunker:
    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        separator: str = "\n"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separator = separator

    def split_text(self, text: str) -> List[str]:
        """
        Metni belirtilen boyutta parçalara ayırır.
        
        Args:
            text: Parçalanacak metin
            
        Returns:
            List[str]: Parçalanmış metin listesi
        """
        if not text:
            return []

        # Metni paragraflara ayır
        paragraphs = text.split(self.separator)
        chunks = []
        current_chunk = []
        current_length = 0

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # Eğer paragraf tek başına chunk_size'dan büyükse
            if len(paragraph) > self.chunk_size:
                if current_chunk:
                    chunks.append(self.separator.join(current_chunk))
                    current_chunk = []
                    current_length = 0
                
                # Paragrafı cümlelere böl
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                temp_chunk = []
                temp_length = 0
                
                for sentence in sentences:
                    if temp_length + len(sentence) > self.chunk_size:
                        if temp_chunk:
                            chunks.append(self.separator.join(temp_chunk))
                        temp_chunk = [sentence]
                        temp_length = len(sentence)
                    else:
                        temp_chunk.append(sentence)
                        temp_length += len(sentence)
                
                if temp_chunk:
                    chunks.append(self.separator.join(temp_chunk))
                continue

            # Normal paragraf işleme
            if current_length + len(paragraph) > self.chunk_size:
                chunks.append(self.separator.join(current_chunk))
                # Örtüşme için son paragrafları koru
                overlap_start = max(0, len(current_chunk) - self.chunk_overlap)
                current_chunk = current_chunk[overlap_start:]
                current_length = sum(len(p) for p in current_chunk)
            
            current_chunk.append(paragraph)
            current_length += len(paragraph)

        if current_chunk:
            chunks.append(self.separator.join(current_chunk))

        return chunks

    def split_documents(self, documents: List[str]) -> List[str]:
        """
        Birden fazla belgeyi parçalara ayırır.
        
        Args:
            documents: Parçalanacak belgeler listesi
            
        Returns:
            List[str]: Tüm belgelerin parçalanmış hali
        """
        all_chunks = []
        for doc in documents:
            chunks = self.split_text(doc)
            all_chunks.extend(chunks)
        return all_chunks
