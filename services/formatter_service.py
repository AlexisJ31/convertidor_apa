"""
Servicio de formateo APA 7 para documentos DOCX.
Aplica estrictamente los estándares APA 7ª edición de forma inteligente.
"""

import os
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


class FormatterService:
    """
    Servicio para formatear documentos DOCX según las normas APA 7.
    Aplica estilos de forma inteligente sin deformar elementos complejos.
    """
    
    MARGIN_SIZE = Inches(1)  # 1 pulgada = 2.54 cm
    FONT_NAME = "Times New Roman"
    FONT_SIZE = 12
    LINE_SPACING = 2.0  # Doble espaciado
    FIRST_LINE_INDENT = Inches(0.5)  # Sangría de primera línea
    
    # Estilos que NO deben tener sangría de primera línea
    HEADING_STYLES = {'Heading 1', 'Heading 2', 'Heading 3', 'Heading 4', 'Heading 5', 
                     'Heading 6', 'Title', 'Subtitle'}
    
    # Estilos de cuerpo que SÍ necesitan sangría y formateo
    BODY_STYLES = {'Normal', 'Body Text', 'List Paragraph', 'Quote'}
    
    def __init__(self, file_path: str):
        """
        Inicializa el formateador con la ruta del archivo.
        
        Args:
            file_path: Ruta absoluta al archivo DOCX a formatear.
        """
        self.file_path = file_path
        self.doc = None
        
    def format_document(self) -> str:
        """
        Aplica el formato APA 7 al documento de forma inteligente y guarda una copia formateada.
        
        Returns:
            Ruta del archivo formateado.
            
        Raises:
            ValueError: Si hay un error al formatear el documento.
        """
        try:
            # Cargar documento
            self.doc = Document(self.file_path)
            
            # Aplicar márgenes
            self._apply_margins()
            
            # Formatear párrafos con reglas inteligentes
            self._format_paragraphs()
            
            # Guardar documento formateado
            formatted_path = self._save_formatted_document()
            
            return formatted_path
            
        except Exception as e:
            raise ValueError(f"Error al formatear el documento APA: {str(e)}")
    
    def _apply_margins(self):
        """Aplica márgenes de 1 pulgada (2.54 cm) en todos los lados de todas las secciones."""
        try:
            sections = self.doc.sections
            for section in sections:
                section.top_margin = self.MARGIN_SIZE
                section.bottom_margin = self.MARGIN_SIZE
                section.left_margin = self.MARGIN_SIZE
                section.right_margin = self.MARGIN_SIZE
        except Exception as e:
            raise ValueError(f"Error al aplicar márgenes: {str(e)}")
    
    def _format_paragraphs(self):
        """
        Formatea todos los párrafos del documento con reglas inteligentes según el estilo.
        - Párrafos de cuerpo: Interlineado doble, sangría primera línea, alineación izquierda
        - Títulos: Interlineado doble, SIN sangría primera línea, centrados/negrita según nivel
        - Protege la portada: Primeros 15 párrafos centrados no reciben sangría
        """
        try:
            for idx, paragraph in enumerate(self.doc.paragraphs):
                style_name = paragraph.style.name
                current_alignment = paragraph.alignment
                is_centered = current_alignment == WD_ALIGN_PARAGRAPH.CENTER
                is_heading = self._is_heading_style(style_name)
                is_early_paragraph = idx < 15  # Primeros 15 párrafos (típicamente portada)
                
                # Aplicar configuración base a todos los párrafos
                self._apply_base_formatting(paragraph, style_name)
                
                # LÓGICA DEFENSIVA 1: Si está centrado (portada) o es título, NO aplicar sangría
                if is_centered or is_heading:
                    self._format_centered_or_heading(paragraph, is_heading, is_centered)
                
                # LÓGICA DEFENSIVA 2: Protección especial de portada (primeros 15 párrafos centrados)
                elif is_early_paragraph and is_centered:
                    self._format_cover_paragraph(paragraph)
                
                # LÓGICA DEFENSIVA 3: Aplicar sangría SOLO a cuerpo normal, no centrado, no vacío
                elif self._is_body_style(style_name) and not is_centered and self._has_valid_text(paragraph):
                    self._format_body_paragraph(paragraph)
                
                else:
                    # Para estilos desconocidos: aplicar base pero sin sangría
                    self._apply_spacing_only(paragraph)
                    
        except Exception as e:
            raise ValueError(f"Error al formatear párrafos: {str(e)}")
    
    def _format_centered_or_heading(self, paragraph, is_heading: bool, is_centered: bool):
        """
        Formatea títulos y párrafos centrados (portada).
        NUNCA aplica sangría de primera línea.
        """
        paragraph_format = paragraph.paragraph_format
        
        # Forzar a None para eliminar cualquier sangría preexistente
        paragraph_format.first_line_indent = None
        paragraph_format.left_indent = None
        paragraph_format.right_indent = None
        
        # Interlineado doble
        paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        
        # Limpieza de espacios
        paragraph_format.space_before = Pt(0)
        paragraph_format.space_after = Pt(0)
        
        # Forzar centrado para títulos principales y portada
        if is_heading and ('Heading 1' in paragraph.style.name or 'Title' in paragraph.style.name):
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            # Negrita para títulos
            for run in paragraph.runs:
                run.font.bold = True
        elif is_centered:
            # Mantener el centrado de la portada
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif is_heading:
            # Heading 2+ normalmente a la izquierda
            paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for run in paragraph.runs:
                run.font.bold = True
    
    def _format_cover_paragraph(self, paragraph):
        """
        Formatea párrafos de la portada (primeros 15 párrafos centrados).
        - Times New Roman 12pt
        - Interlineado doble
        - Centrado
        - SIN sangría
        """
        paragraph_format = paragraph.paragraph_format
        
        # Forzar limpieza de sangrías
        paragraph_format.first_line_indent = None
        paragraph_format.left_indent = None
        
        # Interlineado doble
        paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        
        # Limpieza de espacios
        paragraph_format.space_before = Pt(0)
        paragraph_format.space_after = Pt(0)
        
        # Mantener centrado
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    def _apply_spacing_only(self, paragraph):
        """
        Aplica SOLO espaciado a párrafos desconocidos o especiales (como listas).
        - Interlineado doble
        - Sin sangría
        - Sin espacios extra
        """
        paragraph_format = paragraph.paragraph_format
        
        # Limpiar sangrías previas
        paragraph_format.first_line_indent = None
        
        # Interlineado doble
        paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        
        # Limpieza de espacios
        paragraph_format.space_before = Pt(0)
        paragraph_format.space_after = Pt(0)
    
    def _has_valid_text(self, paragraph) -> bool:
        """
        Verifica si el párrafo tiene texto válido (no está vacío o solo con espacios).
        """
        text = paragraph.text.strip()
        return len(text) > 0
    
    def _apply_base_formatting(self, paragraph, style_name: str):
        """
        Aplica formateo base a todos los párrafos: fuente y tamaño.
        Preserva bold, italic y otros formatos existentes.
        """
        # Aplicar fuente y tamaño sin sobrescribir otros estilos
        for run in paragraph.runs:
            # Solo cambiar nombre de fuente y tamaño, preservar negrita e itálica
            run.font.name = self.FONT_NAME
            run.font.size = Pt(self.FONT_SIZE)
            # Asegurar color negro
            if run.font.color.rgb is None:
                run.font.color.rgb = RGBColor(0, 0, 0)
    
    def _format_body_paragraph(self, paragraph):
        """
        Formatea párrafos de cuerpo con:
        - Interlineado doble
        - Sangría primera línea 0.5" (SOLO aquí, no en otros casos)
        - Alineación izquierda
        - Sin espaciado extra antes/después
        
        IMPORTANTE: Este método SOLO se llama desde _format_paragraphs() 
        cuando se verifica que el párrafo cumple requisitos defensivos.
        """
        paragraph_format = paragraph.paragraph_format
        
        # Asegurar que no hay sangrías previas deformando
        paragraph_format.left_indent = None
        paragraph_format.right_indent = None
        
        # Interlineado doble (constante WD_LINE_SPACING para máxima compatibilidad)
        paragraph_format.line_spacing_rule = WD_LINE_SPACING.DOUBLE
        
        # Alineación a izquierda
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        
        # SANGRÍA DE PRIMERA LÍNEA: 0.5 pulgadas (SOLO aquí)
        paragraph_format.first_line_indent = self.FIRST_LINE_INDENT
        
        # Limpieza de espacios: CRÍTICO para que el doble espaciado sea consistente
        paragraph_format.space_before = Pt(0)
        paragraph_format.space_after = Pt(0)
    
    def _is_heading_style(self, style_name: str) -> bool:
        """Verifica si el estilo es un encabezado/título."""
        return any(heading in style_name for heading in self.HEADING_STYLES)
    
    def _is_body_style(self, style_name: str) -> bool:
        """Verifica si el estilo es de cuerpo de texto."""
        return any(body in style_name for body in self.BODY_STYLES)
    
    def _save_formatted_document(self) -> str:
        """
        Guarda el documento formateado en la carpeta temporal.
        
        Returns:
            Ruta del archivo guardado.
        """
        # Crear nombre único para el archivo formateado
        base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        formatted_filename = f"{base_name}_APA_FORMATEADO.docx"
        formatted_path = os.path.join("temp", formatted_filename)
        
        # Guardar documento
        self.doc.save(formatted_path)
        
        return formatted_path

