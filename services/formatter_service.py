"""
Servicio de formateo APA 7 para documentos DOCX.
Aplica estrictamente los estándares APA 7ª edición de forma inteligente.
"""

import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import copy

class FormatterService:
    """
    Servicio para formatear documentos DOCX según las normas APA 7.
    Aplica estilos basados en clasificación heurística de párrafos.
    """

    MARGIN_SIZE = Inches(1)
    FONT_NAME = "Times New Roman"
    FONT_SIZE = 12
    LINE_SPACING = 2.0

    SECTION_TITLES = {
        'introducción', 'introduction',
        'resumen', 'abstract',
        'referencias', 'references', 'bibliografía', 'bibliography',
        'metodología', 'methodology', 'método', 'method', 'metodo', 'metodologia',
        'resultados', 'results',
        'conclusión', 'conclusiones', 'conclusion', 'conclusions',
        'discusión', 'discussion', 'discusion',
        'introduccion',
    }

    # Subsecciones de nivel 2 (dentro de Método, etc.)
    SUBSECTION_TITLES = {
        'participantes', 'participants',
        'instrumentos', 'instruments', 'measures',
        'procedimiento', 'procedure',
        'análisis', 'analisis', 'análisis de datos', 'data analysis',
        'materiales', 'materials',
        'diseño', 'design',
    }

    REFERENCE_SECTION_TITLES = {
        'referencias', 'references', 'bibliografía', 'bibliography'
    }

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.doc = None

    def format_document(self) -> str:
        try:
            self.doc = Document(self.file_path)
            self._apply_margins()
            self._format_paragraphs()
            return self._save_formatted_document()
        except Exception as e:
            raise ValueError(f"Error al formatear el documento APA: {str(e)}")

    def _apply_margins(self):
        for section in self.doc.sections:
            section.top_margin = self.MARGIN_SIZE
            section.bottom_margin = self.MARGIN_SIZE
            section.left_margin = self.MARGIN_SIZE
            section.right_margin = self.MARGIN_SIZE

    def _clasificar(self, paragraphs):
        """
        Primera pasada: clasifica todos los párrafos antes de formatear.
        Retorna lista de (paragraph, categoria).
        """
        classified = []
        portada_count = 0
        portada_done = False
        in_referencias = False
        resumen_done = False
        just_saw_resumen = False

        for p in paragraphs:
            text = p.text.strip()

            if not text:
                classified.append((p, 'vacio'))
                continue

            lower = text.lower()

            # --- Detección de tipo ---

            # Título de sección nivel 1
            is_seccion = lower in self.SECTION_TITLES
            # Subsección nivel 2
            is_subseccion = lower in self.SUBSECTION_TITLES
            # ¿Empieza bloque de referencias?
            is_ref_header = lower in self.REFERENCE_SECTION_TITLES

            # Portada: los primeros párrafos antes del primer título de sección
            if not portada_done:
                if is_seccion:
                    portada_done = True
                    in_referencias = is_ref_header
                    just_saw_resumen = (lower in ['resumen', 'abstract'])
                    classified.append((p, 'titulo_seccion'))
                else:
                    portada_count += 1
                    classified.append((p, 'portada'))
                continue

            # Ya pasamos la portada
            if in_referencias:
                if is_seccion and not is_ref_header:
                    # Nuevo bloque (ej. Anexos) — salir de referencias
                    in_referencias = False
                    just_saw_resumen = False
                    classified.append((p, 'titulo_seccion'))
                elif is_seccion:
                    classified.append((p, 'titulo_seccion'))
                else:
                    classified.append((p, 'referencia'))
                continue

            if is_ref_header:
                in_referencias = True
                just_saw_resumen = False
                classified.append((p, 'titulo_seccion'))
                continue

            if is_seccion:
                just_saw_resumen = (lower in ['resumen', 'abstract'])
                classified.append((p, 'titulo_seccion'))
                continue

            if is_subseccion:
                just_saw_resumen = False
                classified.append((p, 'titulo_subseccion'))
                continue

            if just_saw_resumen:
                classified.append((p, 'resumen_cuerpo'))
                just_saw_resumen = False
                continue

            classified.append((p, 'cuerpo'))

        return classified

    def _set_run(self, paragraph, bold=False):
        """
        Consolida todos los runs en uno solo con formato limpio.
        Evita el problema de runs vacíos o fragmentados.
        """
        full_text = paragraph.text

        # Limpiar todos los runs existentes
        for run in paragraph.runs:
            run.text = ''

        # Usar el primer run si existe, si no crear uno
        if paragraph.runs:
            run = paragraph.runs[0]
        else:
            run = paragraph.add_run()

        run.text = full_text
        run.font.name = self.FONT_NAME
        run.font.size = Pt(self.FONT_SIZE)
        run.font.bold = bold
        run.font.italic = False
        run.font.underline = False
        run.font.color.rgb = RGBColor(0, 0, 0)

    def _base_pf(self, paragraph):
        """Aplica interlineado doble y sin espacio antes/después."""
        pf = paragraph.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing_rule = WD_LINE_SPACING.DOUBLE

    def _format_paragraphs(self):
        classified = self._clasificar(self.doc.paragraphs)

        portada_end_idx = None
        ref_start_idx = None

        # Encontrar índices clave para saltos de página
        for i, (p, cat) in enumerate(classified):
            if cat == 'portada' and portada_end_idx is None:
                portada_end_idx = i
            if cat == 'portada':
                portada_end_idx = i
            if cat == 'titulo_seccion' and p.text.strip().lower() in self.REFERENCE_SECTION_TITLES:
                ref_start_idx = i

        inserted_page_breaks = set()

        for i, (paragraph, categoria) in enumerate(classified):
            text = paragraph.text.strip()

            # Vacíos: eliminar contenido pero dejar el párrafo (evita errores de XML)
            if categoria == 'vacio':
                paragraph.clear()
                continue

            # Salto de página antes del primer título (fin de portada)
            if categoria == 'titulo_seccion' and i not in inserted_page_breaks:
                prev_cats = [c for _, c in classified[:i] if c == 'portada']
                if prev_cats and i not in inserted_page_breaks:
                    self._insert_page_break_before(paragraph)
                    inserted_page_breaks.add(i)

            # Salto de página antes de Referencias
            if categoria == 'titulo_seccion' and text.lower() in self.REFERENCE_SECTION_TITLES:
                if i not in inserted_page_breaks:
                    self._insert_page_break_before(paragraph)
                    inserted_page_breaks.add(i)

            # Aplicar formato según categoría
            if categoria == 'portada':
                self._base_pf(paragraph)
                self._clear_indent(paragraph)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                self._set_run(paragraph, bold=False)

            elif categoria == 'titulo_seccion':
                self._base_pf(paragraph)
                self._clear_indent(paragraph)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
                self._set_run(paragraph, bold=True)

            elif categoria == 'titulo_subseccion':
                self._base_pf(paragraph)
                self._clear_indent(paragraph)
                paragraph.paragraph_format.first_line_indent = Inches(0.5)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                self._set_run(paragraph, bold=True)

            elif categoria == 'resumen_cuerpo':
                self._base_pf(paragraph)
                self._clear_indent(paragraph)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT

            elif categoria == 'referencia':
                self._base_pf(paragraph)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                pf = paragraph.paragraph_format
                pf.left_indent = Inches(0.5)
                pf.first_line_indent = Inches(-0.5)
                self._set_run(paragraph, bold=False)

            elif categoria == 'cuerpo':
                self._base_pf(paragraph)
                paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
                pf = paragraph.paragraph_format
                pf.left_indent = Pt(0)
                pf.right_indent = Pt(0)
                pf.first_line_indent = Inches(0.5)
                self._set_run(paragraph, bold=False)

    def _clear_indent(self, paragraph):
        """
        FIX CRÍTICO: Poner explícitamente en 0, no None.
        None hereda del estilo base y no limpia la sangría.
        """
        pf = paragraph.paragraph_format
        pf.first_line_indent = Pt(0)
        pf.left_indent = Pt(0)
        pf.right_indent = Pt(0)

    def _insert_page_break_before(self, paragraph):
        """Inserta un salto de página antes del párrafo dado."""
        new_p = OxmlElement('w:p')
        new_r = OxmlElement('w:r')
        new_br = OxmlElement('w:br')
        new_br.set(qn('w:type'), 'page')
        new_r.append(new_br)
        new_p.append(new_r)
        paragraph._p.addprevious(new_p)

    def _save_formatted_document(self) -> str:
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        formatted_filename = f"{base_name}_APA_FORMATEADO.docx"
        os.makedirs("temp", exist_ok=True)
        formatted_path = os.path.join("temp", formatted_filename)
        self.doc.save(formatted_path)
        return formatted_path