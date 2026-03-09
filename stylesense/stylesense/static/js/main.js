function toggleMobileMenu() {
    const links = document.querySelector('.nav-links');
    links.style.display = links.style.display === 'flex' ? 'none' : 'flex';
    links.style.flexDirection = 'column';
    links.style.position = 'absolute';
    links.style.top = '68px';
    links.style.left = '0';
    links.style.right = '0';
    links.style.background = 'rgba(10,10,15,0.98)';
    links.style.padding = '1rem 2rem';
    links.style.borderBottom = '1px solid rgba(255,255,255,0.08)';
}

function renderMarkdown(text) {
    return text
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^- (.*$)/gim, '<li>$1</li>')
        .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
        .replace(/\n\n/g, '<br><br>')
        .replace(/\n/g, '<br>');
}

function showLoading(containerId, message = "AI is working its magic...") {
    document.getElementById(containerId).innerHTML = `
        <div class="loading-state">
            <div class="spinner"></div>
            <p class="loading-text">${message}</p>
        </div>`;
}

function showError(containerId, message) {
    document.getElementById(containerId).innerHTML = `
        <div class="empty-state">
            <i class="fas fa-exclamation-circle" style="color: var(--secondary)"></i>
            <h3>Something went wrong</h3>
            <p>${message}</p>
        </div>`;
}

// Chip selection
document.addEventListener('click', e => {
    if (e.target.classList.contains('chip')) {
        const field = e.target.dataset.field;
        if (field) {
            document.querySelectorAll(`.chip[data-field="${field}"]`).forEach(c => c.classList.remove('active'));
        }
        e.target.classList.toggle('active');
    }
});
