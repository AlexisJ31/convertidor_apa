const dropArea = document.querySelector('#drop-area');
const fileInput = document.querySelector('#file-input');
const fileStatus = document.querySelector('#file-status');
const processButton = document.querySelector('#process-button');

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

function handleFile(file) {
  if (!file) return;

  const extension = getExtension(file.name);
  const isValid = validExtensions.includes(extension);

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
    
    // Aquí el usuario podría renderizar `data.references` en el HTML
    
  } catch (error) {
    console.error('Error procesando el documento:', error);
    updateStatus(`Ocurrió un error: ${error.message}`, 'error');
  } finally {
    processButton.disabled = false;
  }
});

const uploadForm = document.querySelector('.upload-card');
if (uploadForm) {
  uploadForm.addEventListener('submit', (event) => {
    event.preventDefault();
  });
}
