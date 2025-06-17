from typing import Dict, Any, Optional
from string import Template
import json
import os

class PromptTemplate:
    def __init__(self, template: str, variables: Optional[Dict[str, Any]] = None):
        """
        Prompt şablonu.
        
        Args:
            template: Şablon metni
            variables: Şablon değişkenleri
        """
        self.template = template
        self.variables = variables or {}

    def format(self, **kwargs) -> str:
        """
        Şablonu değişkenlerle formatlar.
        
        Args:
            **kwargs: Format değişkenleri
            
        Returns:
            str: Formatlanmış prompt
        """
        # Tüm değişkenleri birleştir
        all_vars = {**self.variables, **kwargs}
        
        # Şablonu formatla
        return Template(self.template).safe_substitute(all_vars)

class PromptManager:
    def __init__(self, templates_dir: str = "config/prompts"):
        """
        Prompt yöneticisi.
        
        Args:
            templates_dir: Şablonların bulunduğu dizin
        """
        self.templates_dir = templates_dir
        self.templates: Dict[str, PromptTemplate] = {}
        self._load_templates()

    def _load_templates(self) -> None:
        """Şablonları yükler."""
        # Dizin yoksa oluştur
        os.makedirs(self.templates_dir, exist_ok=True)
        
        # Şablon dosyalarını tara
        for filename in os.listdir(self.templates_dir):
            if filename.endswith(".json"):
                self._load_template_file(filename)

    def _load_template_file(self, filename: str) -> None:
        """
        Şablon dosyasını yükler.
        
        Args:
            filename: Şablon dosyası adı
        """
        file_path = os.path.join(self.templates_dir, filename)
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            
            template_name = data.get("name")
            template_text = data.get("template")
            variables = data.get("variables", {})
            
            if template_name and template_text:
                self.templates[template_name] = PromptTemplate(
                    template=template_text,
                    variables=variables
                )

    def get_template(self, name: str) -> Optional[PromptTemplate]:
        """
        Şablonu adına göre getirir.
        
        Args:
            name: Şablon adı
            
        Returns:
            Optional[PromptTemplate]: Şablon
        """
        return self.templates.get(name)

    def add_template(
        self,
        name: str,
        template: str,
        variables: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Yeni şablon ekler.
        
        Args:
            name: Şablon adı
            template: Şablon metni
            variables: Şablon değişkenleri
        """
        self.templates[name] = PromptTemplate(template, variables)
        
        # Şablonu dosyaya kaydet
        file_path = os.path.join(self.templates_dir, f"{name}.json")
        
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({
                "name": name,
                "template": template,
                "variables": variables or {}
            }, f, ensure_ascii=False, indent=2)

    def remove_template(self, name: str) -> None:
        """
        Şablonu siler.
        
        Args:
            name: Şablon adı
        """
        if name in self.templates:
            del self.templates[name]
            
            # Şablon dosyasını sil
            file_path = os.path.join(self.templates_dir, f"{name}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
