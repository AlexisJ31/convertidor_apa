import abc
import os
import docx
import pdfplumber

class DocumentExtractor(abc.ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abc.abstractmethod
    def extract_text(self) -> str:
        """Extrae y retorna el texto del documento."""
        pass

class DocxExtractor(DocumentExtractor):
    def extract_text(self) -> str:
        try:
            doc = docx.Document(self.file_path)
            return "\n".join([paragraph.text for paragraph in doc.paragraphs])
        except Exception as e:
            raise ValueError(f"Error al leer el archivo Word: {str(e)}")

class PdfExtractor(DocumentExtractor):
    def extract_text(self) -> str:
        text = ""
        try:
            with pdfplumber.open(self.file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            raise ValueError(f"Error al leer el archivo PDF: {str(e)}")

def get_extractor(file_path: str) -> DocumentExtractor:
    """Factory para obtener la instancia del extractor adecuado."""
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext in {".doc", ".docx"}:
        return DocxExtractor(file_path)
    elif ext == ".pdf":
        return PdfExtractor(file_path)
    else:
        raise ValueError(f"Extensión de archivo no soportada: {ext}")
