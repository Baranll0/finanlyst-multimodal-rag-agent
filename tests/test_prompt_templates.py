import pytest
import os
import shutil
from utils.prompt_templates import PromptTemplate, PromptManager

@pytest.fixture
def prompt_manager():
    # Test için geçici dizin
    test_dir = "test_prompts"
    os.makedirs(test_dir, exist_ok=True)
    
    manager = PromptManager(templates_dir=test_dir)
    
    yield manager
    
    # Test sonrası temizlik
    shutil.rmtree(test_dir)

def test_prompt_template_formatting():
    # Test şablonu
    template = PromptTemplate(
        template="Merhaba ${name}! ${message}",
        variables={"name": "Dünya"}
    )
    
    # Şablonu formatla
    result = template.format(message="Nasılsın?")
    
    # Sonucu kontrol et
    assert "Merhaba Dünya!" in result
    assert "Nasılsın?" in result

def test_prompt_manager_operations(prompt_manager):
    # Yeni şablon ekle
    prompt_manager.add_template(
        name="test_template",
        template="Test: ${message}",
        variables={"message": "Varsayılan mesaj"}
    )
    
    # Şablonu getir
    template = prompt_manager.get_template("test_template")
    assert template is not None
    
    # Şablonu formatla
    result = template.format(message="Özel mesaj")
    assert "Test: Özel mesaj" in result
    
    # Şablonu sil
    prompt_manager.remove_template("test_template")
    assert prompt_manager.get_template("test_template") is None

def test_prompt_manager_file_operations(prompt_manager):
    # Şablon dosyası oluştur
    test_template = {
        "name": "file_template",
        "template": "Dosya: ${content}",
        "variables": {"content": "Test içerik"}
    }
    
    # Şablonu ekle
    prompt_manager.add_template(
        name=test_template["name"],
        template=test_template["template"],
        variables=test_template["variables"]
    )
    
    # Dosyanın oluşturulduğunu kontrol et
    file_path = os.path.join(prompt_manager.templates_dir, "file_template.json")
    assert os.path.exists(file_path)
    
    # Yeni bir manager oluştur ve şablonların yüklendiğini kontrol et
    new_manager = PromptManager(templates_dir=prompt_manager.templates_dir)
    assert new_manager.get_template("file_template") is not None 