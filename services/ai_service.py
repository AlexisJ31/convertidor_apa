import os
import json
from google import genai
from groq import Groq
from dotenv import load_dotenv

class AIService:
    def __init__(self):
        load_dotenv()
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if google_api_key:
            self.client = genai.Client(api_key=google_api_key)
            
        groq_api_key = os.getenv("GROQ_API_KEY")
        if groq_api_key:
            self.groq_client = Groq(api_key=groq_api_key)
            self.groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        else:
            self.groq_client = None
            self.groq_model = None
        
    def parse_references(self, text: str) -> list:
        prompt = (
            "Tu tarea es identificar todas las referencias bibliográficas en el siguiente texto. "
            "Debes devolver estrictamente una lista en formato JSON donde cada objeto tenga los campos: "
            "autor, año, título, editorial/fuente y URL (si existe). Solo devuelve el JSON puro, sin markdown ni texto adicional.\n\n"
            f"Texto:\n{text}"
        )
        
        try:
            response = self.client.models.generate_content(
                model='gemini-1.5-flash',
                contents=prompt
            )
            return self._extract_json(response.text)
        except Exception:
            print("Gemini saturado, cambiando a Groq...")
            return self._parse_with_groq(prompt)

    def _parse_with_groq(self, prompt: str) -> list:
        if not self.groq_client:
            print("Error: No se configuró GROQ_API_KEY.")
            return []
            
        try:
            if not self.groq_model:
                print("Error: No se configuró el modelo Groq.")
                return []

            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.groq_model,
            )
            return self._extract_json(chat_completion.choices[0].message.content)
        except Exception as e:
            print(f"Error procesando referencias con Groq: {e}")
            return []

    def _extract_json(self, response_text: str) -> list:
        response_text = response_text.strip()
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        try:
            return json.loads(response_text.strip())
        except Exception as e:
            print(f"Error decodificando JSON: {e}")
            return []
