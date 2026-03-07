// static/bg.js
async function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const originalPreview = document.getElementById('original-preview');
    const resultPreview = document.getElementById('result-preview');
    const resultsArea = document.getElementById('results');
    const loading = document.getElementById('loading');
    const downloadBtn = document.getElementById('download-bg');

    // Show preview and results area
    resultsArea.style.display = 'grid';
    originalPreview.src = URL.createObjectURL(file);
    resultPreview.style.display = 'none';
    loading.style.display = 'flex';

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/api/bg/remove-background', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) throw new Error('Processing failed');

        const blob = await response.blob();
        const resultUrl = URL.createObjectURL(blob);

        resultPreview.src = resultUrl;
        resultPreview.style.display = 'block';
        
        downloadBtn.href = resultUrl;
        downloadBtn.download = `processed-${file.name.split('.')[0]}.png`;

    } catch (error) {
        console.error(error);
        alert('Error processing image. Please try again.');
    } finally {
        loading.style.display = 'none';
    }
}

// Drag and drop logic
const dropZone = document.getElementById('drop-zone');

['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
});

function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
}

['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.add('highlight'), false);
});

['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, () => dropZone.classList.remove('highlight'), false);
});

dropZone.addEventListener('drop', handleDrop, false);

function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFileUpload({ target: { files } });
}
