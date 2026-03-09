// =============================================
// StyleSense AI - Analyze Page JavaScript
// =============================================

let currentFile = null;

function handleImageUpload(event) {
  const file = event.target.files[0];
  if (!file) return;
  
  currentFile = file;
  const reader = new FileReader();
  reader.onload = (e) => {
    document.getElementById('previewImg').src = e.target.result;
    document.getElementById('imagePreview').style.display = 'block';
    document.getElementById('uploadArea').style.display = 'none';
    document.getElementById('analyzeBtn').disabled = false;
  };
  reader.readAsDataURL(file);
  
  // Drag drop style
  const uploadArea = document.getElementById('uploadArea');
  uploadArea.addEventListener('dragover', (e) => { e.preventDefault(); uploadArea.style.borderColor = '#667eea'; });
  uploadArea.addEventListener('dragleave', () => { uploadArea.style.borderColor = ''; });
  uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    if (file) { document.getElementById('imageInput').files = e.dataTransfer.files; handleImageUpload({target: {files: [file]}}); }
  });
}

function removeImage() {
  currentFile = null;
  document.getElementById('imageInput').value = '';
  document.getElementById('imagePreview').style.display = 'none';
  document.getElementById('uploadArea').style.display = 'block';
  document.getElementById('analyzeBtn').disabled = true;
  document.getElementById('analysisResults').innerHTML = `
    <div class="results-placeholder">
      <div class="placeholder-icon">👁️</div>
      <h3>Upload an outfit photo to get started</h3>
      <p>Our AI will analyze style, colors, occasion suitability, and more</p>
    </div>`;
}

async function analyzeOutfit() {
  if (!currentFile) return;
  
  const analysisType = document.querySelector('input[name="analysis_type"]:checked').value;
  const formData = new FormData();
  formData.append('file', currentFile);
  formData.append('analysis_type', analysisType);
  
  showLoading();
  
  try {
    const response = await fetch('/api/analyze/outfit-image', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();
    renderAnalysis(result, analysisType);
  } catch (error) {
    showError('Analysis failed. Please check your Gemini API key and try again.');
  } finally {
    hideLoading();
  }
}

function renderAnalysis(data, type) {
  const container = document.getElementById('analysisResults');
  
  if (data.error) {
    container.innerHTML = `<div class="results-placeholder"><div class="placeholder-icon">⚠️</div><h3>Analysis Error</h3><p>${data.error}</p><p style="margin-top:0.5rem;font-size:0.8rem;color:#6c757d">Ensure GEMINI_API_KEY is set in .env</p></div>`;
    return;
  }

  let html = '';

  if (type === 'style_score') {
    html = renderStyleScore(data);
  } else if (type === 'color_palette') {
    html = renderColorPalette(data);
  } else {
    html = renderFullAnalysis(data);
  }

  html += `<div class="provider-info"><span class="provider-dot"></span>Analyzed by ${data.provider || 'Gemini Vision'}</div>`;
  container.innerHTML = html;
}

function renderStyleScore(data) {
  const score = data.overall_score || 0;
  const color = score >= 8 ? '#6dc96d' : score >= 6 ? '#f5a623' : '#e94560';
  
  let html = `<div class="analysis-card">
    <h3>⭐ Style Score</h3>
    <div class="score-display">
      <div class="score-circle" style="border-color:${color};color:${color}">${score}/10</div>
      <div class="score-details">`;
  
  if (data.breakdown) {
    Object.entries(data.breakdown).forEach(([key, val]) => {
      html += `<div class="score-bar-wrapper">
        <div class="score-bar-label"><span>${key.replace(/_/g, ' ')}</span><span>${val}/10</span></div>
        <div class="score-bar"><div class="score-bar-fill" style="width:${val * 10}%"></div></div>
      </div>`;
    });
  }
  html += `</div></div>`;
  
  if (data.verdict) html += `<p style="color:var(--gray-400);font-size:0.9rem;margin-top:1rem">${data.verdict}</p>`;
  if (data.celebrity_style_match) html += `<div class="styling-tip-box">✨ Style Match: ${data.celebrity_style_match}</div>`;
  html += `</div>`;

  if (data.compliments && data.compliments.length > 0) {
    html += `<div class="analysis-card"><h3>💚 What Works Well</h3><div class="tips-list">
      ${data.compliments.map(c => `<div class="tip-item">${c}</div>`).join('')}
    </div></div>`;
  }

  if (data.improvement_tips && data.improvement_tips.length > 0) {
    html += `<div class="analysis-card"><h3>💡 Improvement Tips</h3><div class="tips-list">
      ${data.improvement_tips.map(t => `<div class="tip-item">${t}</div>`).join('')}
    </div></div>`;
  }
  
  return html;
}

function renderColorPalette(data) {
  let html = `<div class="analysis-card"><h3>🎨 Color Palette Extraction</h3>`;
  
  if (data.colors) {
    html += `<div class="color-blocks">`;
    data.colors.forEach(c => {
      html += `<div class="color-block">
        <div class="color-dot" style="background:${c.hex || '#ccc'}"></div>
        <div>
          <div style="font-size:0.85rem;font-weight:600">${c.name || ''}</div>
          <div style="font-size:0.75rem;color:var(--gray-600)">${c.hex || ''} · ${c.percentage || 0}% · ${c.role || ''}</div>
        </div>
      </div>`;
    });
    html += `</div>`;
  }
  
  if (data.palette_type) html += `<p style="margin-top:1rem;color:var(--gray-400);font-size:0.9rem"><strong>Palette Type:</strong> ${data.palette_type}</p>`;
  if (data.color_harmony) html += `<p style="color:var(--gray-400);font-size:0.9rem"><strong>Color Harmony:</strong> ${data.color_harmony}</p>`;
  if (data.mood) html += `<p style="color:var(--gray-400);font-size:0.9rem"><strong>Mood:</strong> ${data.mood}</p>`;
  
  if (data.complementary_colors) {
    html += `<div style="margin-top:1rem"><h4 style="font-size:0.85rem;color:var(--gray-400);margin-bottom:0.5rem">Complementary Colors</h4>
      <div class="color-palette-display">
        ${data.complementary_colors.map(c => `<div class="palette-swatch" style="background:${c}" title="${c}"></div>`).join('')}
      </div></div>`;
  }
  html += `</div>`;
  return html;
}

function renderFullAnalysis(data) {
  let html = '';

  // Overall style
  html += `<div class="analysis-card">
    <h3>👗 Style Overview</h3>
    <p style="font-size:1rem;font-weight:600;margin-bottom:0.5rem">${data.overall_style || ''}</p>
    <p style="color:var(--gray-400);font-size:0.9rem">${data.style_category || ''}</p>
    ${data.trend_alignment ? `<div class="styling-tip-box" style="margin-top:1rem">📈 ${data.trend_alignment}</div>` : ''}
  </div>`;

  // Identified pieces
  if (data.identified_pieces && data.identified_pieces.length > 0) {
    html += `<div class="analysis-card"><h3>🔍 Identified Pieces</h3>
      <div class="pieces-grid">
        ${data.identified_pieces.map(p => `
          <div class="piece-card">
            <div class="piece-card-item">${p.item || ''}</div>
            <div class="piece-card-color">${p.color || ''} ${p.pattern ? '· ' + p.pattern : ''}</div>
            ${p.estimated_brand_style ? `<div style="font-size:0.75rem;color:var(--gray-600);margin-top:0.25rem">${p.estimated_brand_style}</div>` : ''}
          </div>`).join('')}
      </div>
    </div>`;
  }

  // Color analysis
  if (data.color_analysis) {
    html += `<div class="analysis-card"><h3>🎨 Color Analysis</h3>
      <div class="color-blocks" style="margin-bottom:0.75rem">
        ${(data.color_analysis.dominant_colors || []).map(c => `
          <div class="color-block"><div class="color-dot" style="background:${c}"></div><span>${c}</span></div>`).join('')}
      </div>
      <p style="color:var(--gray-400);font-size:0.85rem"><strong>Harmony:</strong> ${data.color_analysis.color_harmony || ''}</p>
      <p style="color:var(--gray-400);font-size:0.85rem"><strong>Palette Type:</strong> ${data.color_analysis.palette_type || ''}</p>
    </div>`;
  }

  // Occasion suitability
  if (data.occasion_suitability && data.occasion_suitability.length > 0) {
    html += `<div class="analysis-card"><h3>📍 Occasion Suitability</h3>
      <div class="occasion-tags">
        ${data.occasion_suitability.map(o => `<span class="occasion-tag">${o}</span>`).join('')}
      </div>
    </div>`;
  }

  // Style score
  if (data.style_score) {
    const color = data.style_score >= 8 ? '#6dc96d' : data.style_score >= 6 ? '#f5a623' : '#e94560';
    html += `<div class="analysis-card"><h3>⭐ Style Score: <span style="color:${color}">${data.style_score}/10</span></h3></div>`;
  }

  // Strengths
  if (data.strengths && data.strengths.length > 0) {
    html += `<div class="analysis-card"><h3>💚 Strengths</h3><div class="tips-list">
      ${data.strengths.map(s => `<div class="tip-item">${s}</div>`).join('')}
    </div></div>`;
  }

  // Suggestions
  if (data.improvement_suggestions && data.improvement_suggestions.length > 0) {
    html += `<div class="analysis-card"><h3>💡 Improvement Suggestions</h3>
      ${data.improvement_suggestions.map(s => `<div class="suggestion-item">${s}</div>`).join('')}
    </div>`;
  }

  // Accessory recommendations
  if (data.accessory_recommendations && data.accessory_recommendations.length > 0) {
    html += `<div class="analysis-card"><h3>💎 Accessory Recommendations</h3>
      <div class="trend-pieces">
        ${data.accessory_recommendations.map(a => `<span class="trend-piece">${a}</span>`).join('')}
      </div>
    </div>`;
  }

  return html;
}

function showLoading() {
  document.getElementById('loadingOverlay').classList.add('active');
}
function hideLoading() {
  document.getElementById('loadingOverlay').classList.remove('active');
}
function showError(msg) {
  document.getElementById('analysisResults').innerHTML = `
    <div class="results-placeholder">
      <div class="placeholder-icon">⚠️</div>
      <h3>Error</h3><p>${msg}</p>
    </div>`;
}
