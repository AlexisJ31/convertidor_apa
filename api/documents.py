import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from services.extractor_service import get_extractor
from services.ai_service import AIService

router = APIRouter()

ALLOWED_EXTENSIONS = {".doc", ".docx", ".pdf"}
TEMP_DIR = "temp"

# Asegurarnos de que el directorio temporal existe
os.makedirs(TEMP_DIR, exist_ok=True)

@router.post("/api/v1/convert", tags=["Documents"])
async def convert_document(file: UploadFile = File(...)):
    # Obtener extensión del archivo
    _, ext = os.path.splitext(file.filename)
    if ext.lower() not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Tipo de archivo no permitido. Solo se permiten: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    
    # Ruta de guardado
    file_path = os.path.join(TEMP_DIR, file.filename)
    
    # Guardar el archivo temporalmente y obtener el tamaño
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        file_size = os.path.getsize(file_path)
        
        # Extraer texto del documento
        extractor = get_extractor(file_path)
        extracted_text = extractor.extract_text()
        
        # Procesar texto con la IA de Gemini
        ai_service = AIService()
        references = ai_service.parse_references(extracted_text)
        
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar el archivo: {str(e)}"
        )
    finally:
        file.file.close()
        
    return {
        "filename": file.filename,
        "size": file_size,
        "references": references
    }
