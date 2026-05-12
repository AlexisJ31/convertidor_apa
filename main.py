from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.documents import router as documents_router

app = FastAPI(
    title="Convertidor APA SaaS API",
    description="API para el servicio de conversión de documentos.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents_router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}
