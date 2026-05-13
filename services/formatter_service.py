"""
Servicio de formateo APA 7 para documentos DOCX.
Aplica estrictamente los estándares APA 7ª edición de forma inteligente.
"""

import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING, WD_BREAK

class FormatterService:
    """
    Servicio para formatear documentos DOCX según las normas APA 7.
    Aplica estilos basados en clasificación heurística de párrafos.
    """
    
    MARGIN_SIZE = Inches(1)  # 1 pulgada = 2.54 cm
    FONT_NAME = "Times New Roman"
    FONT_SIZE = 12
    LINE_SPACING = 2.0  # Doble espaciado
    
    HEADING_STYLES = {'Heading 1', 'Heading 2', 'Heading 3', 'Heading 4', 'Heading 5', 
                     'Heading 6', 'Title', 'Subtitle'}
                     
    COMMON_TITLES = {
        'introducción', 'introduction',
        'resumen', 'abstract',
        'referencias', 'references', 'bibliografía', 'bibliography',
        'metodología', 'methodology',
        'resultados', 'results',
        'conclusión', 'conclusiones', 'conclusion', 'conclusions',
        'discusión', 'discussion',
        'método', 'method'
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
        """Aplica márgenes de 1 pulgada (2.54 cm)."""
        for section in self.doc.sections:
            section.top_margin = self.MARGIN_SIZE
            section.bottom_margin = self.MARGIN_SIZE
            section.left_margin = self.MARGIN_SIZE
            section.right_margin = self.MARGIN_SIZE

    def _is_titulo(self, text: str, paragraph) -> bool:
        """Determina si un párrafo es un título de sección."""
        # Por estilo de Word
        if any(h in paragraph.style.name for h in self.HEADING_STYLES):
            return True
        # Por coincidencia exacta con títulos comunes
        if text.lower() in self.COMMON_TITLES:
            return True
        # Heurística de título: muy corto, capitalizado, sin punto final (opcional)
        if len(text) > 0 and len(text) < 60 and text.istitle() and not text.endswith('.'):
            # Es riesgoso asumir todo texto corto como título, confiamos más en COMMON_TITLES
            pass
        return False

    def _format_paragraphs(self):
        """Aplica formato clasificando iterativamente los párrafos."""
        in_referencias = False
        is_portada_done = False
        just_saw_resumen = False
        portada_p_count = 0
        portada_page_break_inserted = False

        for paragraph in self.doc.paragraphs:
            text = paragraph.text.strip()
            
            # Ignorar párrafos completamente vacíos para que no sumen espacio
            if not text:
                paragraph.clear()
                continue
                
            # Identificar título
            is_titulo = self._is_titulo(text, paragraph)
            lower_text = text.lower()
            
            # Manejo de estado
            if is_titulo and not is_portada_done:
                is_portada_done = True
                
            # Salto de portada: antes del primer título si no se ha insertado
            if is_portada_done and not portada_page_break_inserted:
                # Insertamos antes de este párrafo si es el primer título encontrado
                if is_titulo:
                    paragraph.insert_paragraph_before().add_run().add_break(WD_BREAK.PAGE)
                    portada_page_break_inserted = True

            # Clasificación
            categoria = 'cuerpo'
            if in_referencias:
                if is_titulo and lower_text not in ['referencias', 'bibliografía', 'references', 'bibliography']:
                    categoria = 'titulo_seccion'
                    in_referencias = False # Salimos de referencias (e.g. Anexos)
                elif is_titulo:
                    categoria = 'titulo_seccion'
                else:
                    categoria = 'referencia'
            elif is_titulo:
                categoria = 'titulo_seccion'
                if lower_text in ['referencias', 'bibliografía', 'references', 'bibliography']:
                    in_referencias = True
                    # Salto de página ANTES de Referencias
                    paragraph.insert_paragraph_before().add_run().add_break(WD_BREAK.PAGE)
            elif not is_portada_done and portada_p_count < 6:
                categoria = 'portada'
                portada_p_count += 1
            elif just_saw_resumen:
                categoria = 'resumen_cuerpo'

            # Aplicar formato base a todos
            self._apply_base_formatting(paragraph)

            # Aplicar formato específico por categoría
            if categoria == 'portada':
                self._format_as_portada(paragraph)
                # Salto de portada: después del 6to párrafo si no se ha insertado
                if portada_p_count == 6 and not portada_page_break_inserted:
                    paragraph.add_run().add_break(WD_BREAK.PAGE)
                    portada_page_break_inserted = True
                    is_portada_done = True
                    
            elif categoria == 'titulo_seccion':
                self._format_as_titulo(paragraph)
                just_saw_resumen = (lower_text in ['resumen', 'abstract'])
                
            elif categoria == 'referencia':
                self._format_as_referencia(paragraph)
                just_saw_resumen = False
                
            elif categoria == 'resumen_cuerpo':
                self._format_as_resumen_cuerpo(paragraph)
                just_saw_resumen = False
                
            elif categoria == 'cuerpo':
                self._format_as_cuerpo(paragraph)
                just_saw_resumen = False

    def _apply_base_formatting(self, paragraph):
        """Aplica fuente Times New Roman 12pt, color negro y limpia espaciados de párrafo."""
        paragraph_format = paragraph.paragraph_format
        
        # Limpieza de espacios superior/inferior para no romper el interlineado
        paragraph_format.space_before = Pt(0)
        paragraph_format.space_after = Pt(0)
        
        # Interlineado doble estricto
        paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        
        for run in paragraph.runs:
            run.font.name = self.FONT_NAME
            run.font.size = Pt(self.FONT_SIZE)
            if run.font.color.rgb is None:
                run.font.color.rgb = RGBColor(0, 0, 0)

    def _format_as_portada(self, paragraph):
        """Centrado, negrita, sin sangría."""
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf = paragraph.paragraph_format
        pf.first_line_indent = None
        pf.left_indent = None
        pf.right_indent = None
        for run in paragraph.runs:
            run.font.bold = True

    def _format_as_titulo(self, paragraph):
        """Centrado, negrita, sin sangría."""
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf = paragraph.paragraph_format
        pf.first_line_indent = None
        pf.left_indent = None
        pf.right_indent = None
        for run in paragraph.runs:
            run.font.bold = True

    def _format_as_cuerpo(self, paragraph):
        """Alineación izquierda, sangría 1ra línea 0.5"."""
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = paragraph.paragraph_format
        pf.left_indent = None
        pf.right_indent = None
        pf.first_line_indent = Inches(0.5)

    def _format_as_resumen_cuerpo(self, paragraph):
        """Alineación izquierda, SIN sangría 1ra línea."""
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = paragraph.paragraph_format
        pf.left_indent = None
        pf.right_indent = None
        pf.first_line_indent = None

    def _format_as_referencia(self, paragraph):
        """Alineación izquierda, sangría francesa (0.5" izquierda, -0.5" primera línea)."""
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = paragraph.paragraph_format
        pf.right_indent = None
        pf.left_indent = Inches(0.5)
        pf.first_line_indent = Inches(-0.5)

    def _save_formatted_document(self) -> str:
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        formatted_filename = f"{base_name}_APA_FORMATEADO.docx"
        os.makedirs("temp", exist_ok=True)
        formatted_path = os.path.join("temp", formatted_filename)
        self.doc.save(formatted_path)
        return formatted_path
