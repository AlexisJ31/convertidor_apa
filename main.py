from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.documents import router as documents_router
import os

# 🔐 VALIDACIÓN DE ENTORNO: Verificar variables críticas antes de iniciar
required_env_vars = ["GROQ_API_KEY", "GOOGLE_API_KEY"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]

if missing_vars:
    error_msg = f"❌ FALTAN VARIABLES DE ENTORNO CRÍTICAS: {', '.join(missing_vars)}\n"
    error_msg += "Por favor, crea un archivo .env con las siguientes variables:\n"
    error_msg += "GROQ_API_KEY=tu_clave_de_groq\n"
    error_msg += "GOOGLE_API_KEY=tu_clave_de_google\n"
    print(error_msg)
    # No lanzamos excepción para permitir que el servidor inicie, pero el error se mostrará
    # En producción, podríamos lanzar una excepción aquí

app = FastAPI(
    title="Convertidor APA SaaS API",
    description="API para el servicio de conversión de documentos.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    # ⚠️  SEGURIDAD: Cambiar "*" por la URL específica de producción
    # Ejemplo para Netlify: allow_origins=["https://tu-app.netlify.app"]
    # Para desarrollo local: allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"]
    allow_origins=["https://autoapa.netlify.app", "http://localhost:5500", "http://127.0.0.1:5500"],  # Permitir Netlify y desarrollo local
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
