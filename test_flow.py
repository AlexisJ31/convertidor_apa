import os
import json
from unittest.mock import MagicMock
# pyrefly: ignore [missing-import]
import google.generativeai as genai
import docx

# Crear un archivo docx de prueba
doc_path = "test_doc.docx"
doc = docx.Document()
doc.add_paragraph("Texto de prueba. Referencia: Smith, J. (2020). Libro falso. Editorial X.")
doc.save(doc_path)

# Mockear el modelo de Gemini para evitar usar la API Key
class MockResponse:
    def __init__(self, text):
        self.text = text

mock_genai_model = MagicMock()
mock_genai_model.generate_content.return_value = MockResponse(
    text='```json\n[{"autor": "Smith, J.", "año": "2020", "título": "Libro falso", "editorial/fuente": "Editorial X", "URL": null}]\n```'
)
genai.GenerativeModel = MagicMock(return_value=mock_genai_model)
genai.configure = MagicMock()

# Ahora probamos nuestro flujo
try:
    from services.extractor_service import get_extractor
    from services.ai_service import AIService

    print("1. Módulos importados correctamente")

    # Extraer
    extractor = get_extractor(doc_path)
    texto = extractor.extract_text()
    print(f"2. Texto extraído: {texto.strip()}")

    # Inicializar AI Service
    ai_service = AIService()
    print("3. AIService inicializado")

    # Reemplazar la instancia del modelo para la prueba
    ai_service.model = mock_genai_model

    # Parsear referencias
    referencias = ai_service.parse_references(texto)
    print("4. Referencias extraídas:")
    print(json.dumps(referencias, indent=2, ensure_ascii=False))
    
    print("\nTODO ESTA FUNCIONANDO CORRECTAMENTE")
except Exception as e:
    print(f"\nERROR: {e}")
finally:
    # Limpiar archivo de prueba
    if os.path.exists(doc_path):
        os.remove(doc_path)
