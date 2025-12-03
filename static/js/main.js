// File upload handling
const fileInput = document.getElementById('fileInput');
const uploadCard = document.getElementById('uploadCard');
const uploadProgress = document.getElementById('uploadProgress');

// Drag and drop functionality
uploadCard.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadCard.style.borderColor = 'var(--primary-color)';
    uploadCard.style.background = 'rgba(14, 165, 233, 0.05)';
});

uploadCard.addEventListener('dragleave', (e) => {
    e.preventDefault();
    uploadCard.style.borderColor = '';
    uploadCard.style.background = '';
});

uploadCard.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadCard.style.borderColor = '';
    uploadCard.style.background = '';

    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileUpload(files[0]);
    }
});

// File input change
fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileUpload(e.target.files[0]);
    }
});

// Handle file upload
function handleFileUpload(file) {
    // Validate file type
    const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword', 'text/plain'];

    if (!allowedTypes.includes(file.type)) {
        alert('Invalid file type. Please upload PDF, DOCX, or TXT files.');
        return;
    }

    // Validate file size (16MB max)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        alert('File too large. Maximum size is 16MB.');
        return;
    }

    // Show progress
    uploadCard.style.display = 'none';
    uploadProgress.style.display = 'block';

    // Create form data
    const formData = new FormData();
    formData.append('file', file);

    // Add options
    const customPrompt = document.getElementById('custom-prompt').value;
    const summaryLength = document.getElementById('summary-length').value;
    formData.append('custom_prompt', customPrompt);
    formData.append('summary_length', summaryLength);

    // Hide options area
    document.getElementById('optionsArea').style.display = 'none';

    // Upload file
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirect to dashboard
                window.location.href = data.redirect;
            } else {
                throw new Error(data.error || 'Upload failed');
            }
        })
        .catch(error => {
            alert('Error: ' + error.message);
            uploadCard.style.display = 'block';
            uploadProgress.style.display = 'none';
        });
}

// Add click handler to upload card
uploadCard.addEventListener('click', (e) => {
    if (e.target.tagName !== 'BUTTON') {
        fileInput.click();
    }
});
