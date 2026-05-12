import os
import json
from google import genai
from dotenv import load_dotenv

class AIService:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
        
    def parse_references(self, text: str) -> list:
        prompt = (
            "Tu tarea es identificar todas las referencias bibliográficas en el siguiente texto. "
            "Debes devolver estrictamente una lista en formato JSON donde cada objeto tenga los campos: "
            "autor, año, título, editorial/fuente y URL (si existe). Solo devuelve el JSON puro, sin markdown ni texto adicional.\n\n"
            f"Texto:\n{text}"
        )
        
        try:
            response = self.client.models.generate_content(
                model='gemini-2.0-flash',
                contents=prompt
            )
            # Clean up potential markdown formatting from the response
            response_text = response.text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            
            return json.loads(response_text.strip())
        except Exception as e:
            print(f"Error procesando referencias con IA: {e}")
            return []
