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

function handleFile(file) {
  if (!file) return;

  const extension = getExtension(file.name);
  const isValid = validExtensions.includes(extension);

  if (!isValid) {
    updateStatus('Formato no compatible. Sube un archivo .doc, .docx o .pdf.', 'error');
    processButton.disabled = true;
    fileInput.value = '';
    return;
  }

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

processButton.addEventListener('click', () => {
  updateStatus('Documento recibido. AutoAPA iniciaría el procesamiento en la versión conectada.', 'success');
});
