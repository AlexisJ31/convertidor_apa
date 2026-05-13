# AutoAPA - Formato APA Automático

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**AutoAPA** es una aplicación web que convierte documentos académicos en entregables formateados según las normas APA 7ª edición. Utiliza inteligencia artificial para procesar documentos y aplicar automáticamente el formato académico requerido.

## 🚀 Características Principales

### ✨ Funcionalidades
- **Formato APA 7 Automático**: Aplica márgenes, fuentes, interlineado y sangrías según las normas APA 7
- **Procesamiento Inteligente**: Detecta títulos, portadas y párrafos de cuerpo para aplicar reglas específicas
- **Descarga Inmediata**: Genera archivos .docx formateados listos para entrega académica
- **Interfaz Web Moderna**: Diseño responsive con Tailwind CSS
- **Validación de Archivos**: Solo acepta formatos compatibles (.docx, .pdf)
- **Procesamiento Seguro**: Archivos temporales eliminados automáticamente

### 🎯 Beneficios
- **Ahorra tiempo**: Formatea documentos en segundos en lugar de minutos
- **Reduce errores**: Aplicación consistente de normas APA 7
- **Profesional**: Resultados listos para revisión académica
- **Accesible**: Funciona en móvil y escritorio

## 🏗️ Arquitectura

### Backend (FastAPI)
```
backend/
├── main.py                 # Configuración FastAPI y CORS
├── api/
│   └── documents.py        # Endpoint de conversión
└── services/
    ├── ai_service.py       # Integración con IA (Gemini/Groq)
    ├── extractor_service.py # Extracción de texto de documentos
    └── formatter_service.py # Formateo APA 7 con python-docx
```

### Frontend (Vanilla JavaScript)
```
frontend/
├── index.html             # Estructura HTML con Tailwind CSS
├── script.js              # Lógica de subida y descarga
├── styles.css             # Estilos personalizados
└── tailwind.css           # Framework CSS
```

## 📋 Requisitos del Sistema

- **Python**: 3.8 o superior
- **Node.js**: Para desarrollo frontend (opcional)
- **API Keys**: Google Gemini y Groq para procesamiento de IA

## 🛠️ Instalación y Configuración

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/autoapa.git
cd autoapa
```

### 2. Configurar Entorno Virtual
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno
Crear archivo `.env` en la raíz del proyecto:
```env
# API Keys para procesamiento de IA
GOOGLE_API_KEY=tu_clave_de_google_gemini
GROQ_API_KEY=tu_clave_de_groq

# Modelo de Groq (opcional)
GROQ_MODEL=llama-3.3-70b-versatile
```

### 5. Ejecutar la Aplicación
```bash
# Iniciar servidor de desarrollo
python -m uvicorn main:app --reload

# La aplicación estará disponible en:
# http://127.0.0.1:8000
```

### 6. Abrir Frontend
Abrir `index.html` en un navegador web o usar un servidor local:
```bash
# Con Python (recomendado)
python -m http.server 5500

# O con Node.js
npx live-server --port=5500
```

## 📖 Uso

### Flujo Básico
1. **Abrir la aplicación** en el navegador
2. **Seleccionar archivo**: Arrastrar o hacer clic para subir un documento .docx
3. **Procesar**: Hacer clic en "Procesar documento"
4. **Descargar**: El archivo formateado se descarga automáticamente

### Formato APA 7 Aplicado
- **Márgenes**: 1 pulgada (2.54 cm) en todos los lados
- **Fuente**: Times New Roman, tamaño 12pt
- **Interlineado**: Doble (2.0)
- **Sangría**: Primera línea de párrafos de cuerpo: 0.5 pulgadas
- **Alineación**: Izquierda para cuerpo, centrada para títulos y portada

### Validación de Archivos
- ✅ **.docx**: Procesamiento completo con formateo APA 7
- ❌ **.pdf**: Rechazado (mensaje informativo)
- ❌ **Otros**: No permitidos

## 🔧 Configuración Avanzada

### Variables de Entorno
```env
# API Keys (requeridas)
GOOGLE_API_KEY=tu_clave_aqui
GROQ_API_KEY=tu_clave_aqui

# Modelo de IA (opcional)
GROQ_MODEL=llama-3.3-70b-versatile

# Configuración del servidor (opcional)
HOST=0.0.0.0
PORT=8000
```

### Configuración CORS (Producción)
En `main.py`, cambiar:
```python
allow_origins=["https://tu-dominio.com"]
```

### Personalización del Formateo
Modificar `services/formatter_service.py` para ajustar:
- Tamaños de margen
- Tipos de fuente
- Reglas de sangría
- Estilos de párrafo

## 🧪 Testing

### Ejecutar Tests
```bash
# Instalar pytest
pip install pytest

# Ejecutar tests
pytest
```

### Testing Manual
1. Subir diferentes tipos de documentos .docx
2. Verificar que el formateo APA 7 se aplique correctamente
3. Comprobar que títulos y portadas mantengan centrado
4. Validar descarga automática del archivo

## 🔒 Seguridad

### Medidas Implementadas
- ✅ **Variables de entorno**: API keys nunca hardcodeadas
- ✅ **Validación de entrada**: Solo archivos permitidos
- ✅ **Archivos temporales**: Eliminados automáticamente
- ✅ **CORS configurado**: Control de orígenes permitidos
- ✅ **Fail-safe**: Validación de variables críticas al inicio

### Mejores Prácticas
- Nunca commitear archivos `.env`
- Rotar API keys periódicamente
- Usar HTTPS en producción
- Configurar límites de tamaño de archivo

## 📁 Estructura del Proyecto

```
convertidor_apa/
├── .env                    # Variables de entorno (no commitear)
├── .gitignore             # Archivos ignorados por Git
├── main.py                # Punto de entrada FastAPI
├── requirements.txt       # Dependencias Python
├── index.html             # Frontend principal
├── script.js              # Lógica JavaScript
├── styles.css             # Estilos personalizados
├── tailwind.css           # Framework CSS
├── test_flow.py           # Script de testing
├── api/
│   └── documents.py       # API endpoints
├── core/                  # Configuración central
├── services/              # Lógica de negocio
│   ├── ai_service.py      # Servicio de IA
│   ├── extractor_service.py # Extracción de texto
│   └── formatter_service.py # Formateo APA 7
├── temp/                  # Archivos temporales (ignorado)
└── utils/                 # Utilidades
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

### Guías de Contribución
- Seguir PEP 8 para código Python
- Usar commits descriptivos
- Documentar nuevas funcionalidades
- Agregar tests para cambios importantes

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🙏 Agradecimientos

- **FastAPI**: Framework web moderno y rápido
- **python-docx**: Para manipulación de documentos Word
- **Google Gemini**: Para procesamiento inteligente de texto
- **Groq**: API alternativa para IA
- **Tailwind CSS**: Framework CSS utilitario

## 📞 Soporte

Para soporte técnico o preguntas:
- Crear issue en GitHub
- Revisar documentación en `DESIGN.md`
- Contactar al equipo de desarrollo

---

**AutoAPA** - Transformando la preparación de documentos académicos desde 2024.