---
schemaVersion: 1
scope: workspace
updatedAt: "2026-05-12T19:31:01.082Z"
workspaceName: "dise;os"
---

# Project Memory

## Project Overview
- Landing Page moderna y minimalista para el SaaS "AutoAPA".
- Objetivo: presentar una herramienta para subir documentos académicos y procesarlos hacia formato APA, con flujo claro y profesional.

## Current State
- Workspace iniciado desde cero.
- Se crearon archivos separados para la implementación web:
  - `index.html`
  - `styles.css`
  - `script.js`
  - `tailwind.css`
  - `DESIGN.md`
- La landing incluye Hero, zona Dropzone, sección "Cómo funciona" en 3 pasos y diseño responsive.
- La previsualización cargó correctamente sin errores de consola ni assets.
- La validación final del host reportó un recurso bloqueado tipo `ERR_BLOCKED_BY_CLIENT.Inspector`, aparentemente externo/al entorno, no ligado a los assets del proyecto.

## Artifacts
- `index.html`: estructura semántica de la landing, navegación, hero, dropzone y pasos del flujo.
- `styles.css`: estilos visuales principales, layout responsive, estados interactivos y estética académica.
- `script.js`: interactividad vanilla JavaScript para drag-and-drop y selección de archivos.
- `tailwind.css`: utilidades locales tipo Tailwind para evitar dependencia CDN/external.
- `DESIGN.md`: primera documentación del sistema visual del proyecto.

## Design Direction
- Estética limpia, profesional y académica.
- Tonos azules, mucho espacio en blanco, cards suaves y jerarquía clara.
- Diseño responsive para móvil, tablet y desktop.
- Interacciones accesibles con foco visible y estados de arrastre en la dropzone.
- Evitar dependencias externas para mantener el prototipo autocontenido.

## User Feedback
- El usuario pidió actuar como Senior Frontend Developer y UX Designer.
- Requisitos explícitos: HTML5, Tailwind CSS, JavaScript vanilla, archivos separados y diseño responsive.
- Preferencia estética: moderna, minimalista, profesional, azul académico y espaciosa.

## Decisions
- Se implementó el stack en archivos separados.
- Se sustituyó Tailwind CDN por una hoja local `tailwind.css` para evitar bloqueos de recursos externos.
- Se mantuvo JavaScript vanilla para el drag-and-drop.
- Se agregó favicon embebido para reducir solicitudes externas.
- Se creó `DESIGN.md` como fuente inicial del sistema visual.

## Open Questions
- Confirmar si AutoAPA tendrá carga real de archivos o solo prototipo visual.
- Definir textos finales de marketing y propuesta de valor.
- Definir si habrá autenticación, pricing, FAQ o testimonios en futuras iteraciones.
- Confirmar si se debe usar Tailwind compilado completo en un build real.

## Next Steps
- Revisar visualmente la landing en breakpoints clave.
- Probar drag-and-drop con `.doc`, `.docx` y `.pdf`.
- Ajustar copy final del hero y CTA si el usuario lo solicita.
- Añadir secciones complementarias si se requiere conversión comercial: beneficios, seguridad, pricing o FAQ.

## Promotion Candidates For DESIGN.md
- Paleta académica azul con fondos claros y contraste profesional.
- Dropzone como patrón principal de interacción del producto.
- Estética de cards suaves, bordes redondeados y sombras discretas.
- Flujo de 3 pasos: Sube, Procesa, Descarga.

## Recent History
- 2026-05-12: Se creó la landing inicial de AutoAPA desde workspace vacío.
- 2026-05-12: Se añadieron `index.html`, `styles.css`, `script.js` y `DESIGN.md`.
- 2026-05-12: Se reemplazaron dependencias externas por recursos locales/autocontenidos.
- 2026-05-12: Previsualización correcta; verificador del host mantuvo advertencia externa `ERR_BLOCKED_BY_CLIENT.Inspector`.