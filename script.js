const dropArea = document.querySelector('#drop-area');
const fileInput = document.querySelector('#file-input');
const fileStatus = document.querySelector('#file-status');
const processButton = document.querySelector('#process-button');
const resultsContainer = document.querySelector('#results-container');
const referencesTbody = document.querySelector('#references-tbody');
const downloadButton = document.querySelector('#download-button');

const validExtensions = ['doc', 'docx', 'pdf'];

function getExtension(fileName) {
  return fileName.split('.').pop().toLowerCase();
}

function formatFileSize(bytes) {
  if (bytes < 1024 * 1024) return `${Math.max(1, Math.round(bytes / 1024))} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function updateStatus(message, type = 'neutral') {
  fileStatus.textContent = message;
  fileStatus.classList.remove('success', 'error');
  if (type !== 'neutral') fileStatus.classList.add(type);
}

let selectedFile = null;
let currentReferences = [];

function handleFile(file) {
  if (!file) return;

  const extension = getExtension(file.name);
  const isValid = validExtensions.includes(extension);

  // Ocultar resultados previos si hay una nueva selección
  resultsContainer.style.display = 'none';
  currentReferences = [];
  referencesTbody.innerHTML = '';

  if (!isValid) {
    updateStatus('Formato no compatible. Sube un archivo .doc, .docx o .pdf.', 'error');
    processButton.disabled = true;
    fileInput.value = '';
    selectedFile = null;
    return;
  }

  selectedFile = file;
  updateStatus(`Archivo listo: ${file.name} · ${formatFileSize(file.size)}.`, 'success');
  processButton.disabled = false;
}

['dragenter', 'dragover'].forEach((eventName) => {
  dropArea.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropArea.classList.add('drag-over');
  });
});

['dragleave', 'drop'].forEach((eventName) => {
  dropArea.addEventListener(eventName, (event) => {
    event.preventDefault();
    dropArea.classList.remove('drag-over');
  });
});

dropArea.addEventListener('drop', (event) => {
  const [file] = event.dataTransfer.files;
  handleFile(file);
});

fileInput.addEventListener('change', (event) => {
  const [file] = event.target.files;
  handleFile(file);
});

dropArea.addEventListener('keydown', (event) => {
  if (event.key === 'Enter' || event.key === ' ') {
    event.preventDefault();
    fileInput.click();
  }
});

processButton.addEventListener('click', async (event) => {
  event.preventDefault(); // Prevenir cualquier comportamiento por defecto

  if (!selectedFile) {
    updateStatus('Por favor, selecciona un archivo primero.', 'error');
    return;
  }

  // Deshabilitar botón para evitar doble envío
  processButton.disabled = true;
  updateStatus('Procesando documento con IA... por favor espera', 'neutral');

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const response = await fetch('http://127.0.0.1:8000/api/v1/convert', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Error del servidor: ${response.status}`);
    }

    const data = await response.json();
    updateStatus('¡Documento procesado exitosamente!', 'success');
    console.log('Respuesta de Gemini:', data);
    
    if (data.references && data.references.length > 0) {
      currentReferences = data.references;
      renderTable(currentReferences);
      resultsContainer.style.display = 'block';
      // Desplazarse suavemente hacia los resultados
      setTimeout(() => {
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }, 100);
    } else {
      updateStatus('Se procesó el documento pero no se encontraron referencias.', 'neutral');
    }
    
  } catch (error) {
    console.error('Error procesando el documento:', error);
    updateStatus(`Ocurrió un error: ${error.message}`, 'error');
  } finally {
    processButton.disabled = false;
  }
});

function renderTable(references) {
  referencesTbody.innerHTML = '';
  
  references.forEach(ref => {
    const tr = document.createElement('tr');
    
    // Asegurar que las propiedades existan o poner un guion
    const autor = ref.autor || ref.Autor || '-';
    const anio = ref['año'] || ref.año || ref.Año || ref.year || '-';
    const titulo = ref['título'] || ref.título || ref.Título || ref.title || '-';
    const fuente = ref['editorial/fuente'] || ref.fuente || ref.Fuente || ref.editorial || '-';
    
    tr.innerHTML = `
      <td>${autor}</td>
      <td>${anio}</td>
      <td><strong>${titulo}</strong></td>
      <td>${fuente}</td>
    `;
    
    referencesTbody.appendChild(tr);
  });
}

downloadButton.addEventListener('click', () => {
  if (!currentReferences || currentReferences.length === 0) return;
  
  // Generar texto en formato APA
  let textContent = "Referencias Bibliográficas (Formato APA)\n\n";
  
  currentReferences.forEach(ref => {
    const autor = ref.autor || ref.Autor || '';
    const anio = ref['año'] || ref.año || ref.Año || ref.year || '';
    const titulo = ref['título'] || ref.título || ref.Título || ref.title || '';
    const fuente = ref['editorial/fuente'] || ref.fuente || ref.Fuente || ref.editorial || '';
    const url = ref.url || ref.URL || '';
    
    // Construcción básica estilo APA
    let refText = "";
    if (autor) refText += `${autor} `;
    if (anio) refText += `(${anio}). `;
    if (titulo) refText += `${titulo}. `;
    if (fuente) refText += `${fuente}.`;
    if (url) refText += ` ${url}`;
    
    textContent += refText.trim() + "\n\n";
  });
  
  // Crear y descargar el archivo .txt
  const blob = new Blob([textContent], { type: "text/plain;charset=utf-8" });
  const downloadUrl = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = downloadUrl;
  a.download = "referencias_apa.txt";
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(downloadUrl);
});

const uploadForm = document.querySelector('.upload-card');
if (uploadForm) {
  uploadForm.addEventListener('submit', (event) => {
    event.preventDefault();
  });
}
