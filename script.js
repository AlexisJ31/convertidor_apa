const dropArea = document.querySelector('#drop-area');
const fileInput = document.querySelector('#file-input');
const fileStatus = document.querySelector('#file-status');
const processButton = document.querySelector('#process-button');
const resultsContainer = document.querySelector('#results-container');
const resultMessageContainer = document.querySelector('#result-message-container');

const validExtensions = new Set(['doc', 'docx', 'pdf']);

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
  const isValid = validExtensions.has(extension);

  // Ocultar resultados previos si hay una nueva selección
  resultsContainer.style.display = 'none';
  resultMessageContainer.innerHTML = '';

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
  console.log('Botón clickeado, previniendo recarga...');

  if (!selectedFile) {
    updateStatus('Por favor, selecciona un archivo primero.', 'error');
    return;
  }

  // Limpiar resultados previos
  resultsContainer.style.display = 'none';
  resultMessageContainer.innerHTML = '';

  // Deshabilitar botón para evitar doble envío
  processButton.disabled = true;
  updateStatus('Procesando documento y aplicando formato APA 7... por favor espera', 'neutral');

  const formData = new FormData();
  formData.append('file', selectedFile);

  try {
    const response = await fetch('https://convertidor-apa.onrender.com', {
      method: 'POST',
      body: formData
    });

    if (!response.ok) {
      let errorMessage = `Error del servidor: ${response.status}`;
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch (e) {
        // Si no es JSON, mantener el mensaje por defecto
      }
      throw new Error(errorMessage);
    }

    // Obtener el blob del archivo DOCX formateado
    const blob = await response.blob();
    console.log('Archivo DOCX recibido, tamaño:', blob.size, 'bytes');

    // Crear enlace dinámico e iniciar descarga
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'Documento_Formato_APA.docx';
    document.body.appendChild(a);
    a.click();
    a.remove();
    window.URL.revokeObjectURL(url);

    // Mostrar mensaje de éxito
    updateStatus('¡Documento formateado con éxito! Se ha iniciado la descarga.', 'success');
    
    // Inyectar mensaje de éxito en el contenedor
    resultMessageContainer.innerHTML = `
      <p class="text-green-600 font-semibold mb-2">✓ Documento procesado y descargado con éxito</p>
      <p class="text-sm text-gray-600">Se aplicó formato APA 7: Márgenes de 1", Times New Roman 12pt, interlineado doble.</p>
    `;
    resultsContainer.style.display = 'block';
    
    // Desplazarse suavemente hacia los resultados
    setTimeout(() => {
      resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
    
  } catch (error) {
    console.error('Error procesando el documento:', error);
    updateStatus(`Ocurrió un error: ${error.message}`, 'error');
  } finally {
    processButton.disabled = false;
  }
});

const uploadForm = document.querySelector('#upload-form');
if (uploadForm) {
  uploadForm.addEventListener('submit', (event) => {
    event.preventDefault();
  });
}
