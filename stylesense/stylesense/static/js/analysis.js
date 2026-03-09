let selectedFile = null;

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    selectedFile = file;
    const reader = new FileReader();
    reader.onload = e => {
        document.getElementById('previewImg').src = e.target.result;
        document.getElementById('imagePreview').style.display = 'block';
        document.getElementById('uploadZone').style.display = 'none';
    };
    reader.readAsDataURL(file);
}

function clearImage() {
    selectedFile = null;
    document.getElementById('imagePreview').style.display = 'none';
    document.getElementById('uploadZone').style.display = 'block';
    document.getElementById('imageInput').value = '';
}

function switchTab(type, btn) {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const radio = document.querySelector(`input[name="analysisType"][value="${type}"]`);
    if (radio) {
        radio.checked = true;
        document.querySelectorAll('.option-card').forEach(c => c.classList.remove('active'));
        radio.parentElement.classList.add('active');
    }
}

async function analyzeImage() {
    if (!selectedFile) {
        alert('Please upload an image first');
        return;
    }
    const analysisType = document.querySelector('input[name="analysisType"]:checked').value;
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('analysis_type', analysisType);

    showLoading('analysisOutput', '🔍 Analyzing your outfit with AI...');

    try {
        const response = await fetch('/api/analysis/image', { method: 'POST', body: formData });
        const data = await response.json();
        if (data.status === 'success') {
            let html = `<div class="result-content">${renderMarkdown(data.gemini_analysis)}</div>`;
            if (data.hf_classification?.status === 'success' && data.hf_classification.classifications?.length) {
                html += `<hr style="border-color:var(--border);margin:1.5rem 0">
                <h3 style="color:var(--primary);margin-bottom:1rem">🤖 AI Classification</h3>
                <div style="display:flex;flex-wrap:wrap;gap:.5rem">`;
                data.hf_classification.classifications.slice(0, 5).forEach(c => {
                    const pct = Math.round((c.score || 0) * 100);
                    html += `<span style="background:rgba(108,99,255,.1);border:1px solid rgba(108,99,255,.2);padding:.4rem .8rem;border-radius:100px;font-size:.8rem">${c.label} (${pct}%)</span>`;
                });
                html += '</div>';
            }
            document.getElementById('analysisOutput').innerHTML = html;
        } else {
            showError('analysisOutput', data.detail || 'Analysis failed');
        }
    } catch (err) {
        showError('analysisOutput', 'Error: ' + err.message);
    }
}

// Drag and drop
const zone = document.getElementById('uploadZone');
if (zone) {
    zone.addEventListener('dragover', e => { e.preventDefault(); zone.style.borderColor = 'var(--primary)'; });
    zone.addEventListener('dragleave', () => { zone.style.borderColor = ''; });
    zone.addEventListener('drop', e => {
        e.preventDefault();
        zone.style.borderColor = '';
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            document.getElementById('imageInput').files = e.dataTransfer.files;
            handleImageUpload({ target: { files: [file] } });
        }
    });
}
