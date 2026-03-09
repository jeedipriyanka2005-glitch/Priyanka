let selectedCategory = 'women';

document.querySelectorAll('#categoryChips .chip').forEach(chip => {
    chip.addEventListener('click', () => {
        document.querySelectorAll('#categoryChips .chip').forEach(c => c.classList.remove('active'));
        chip.classList.add('active');
        selectedCategory = chip.dataset.value;
    });
});

async function getTrends() {
    const season = document.getElementById('trendSeason').value;
    showLoading('trendsOutput', '🔥 Discovering the hottest trends...');

    try {
        const response = await fetch('/api/trends/insights', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ category: selectedCategory, season })
        });
        const data = await response.json();
        if (data.status === 'success') {
            document.getElementById('trendsOutput').innerHTML = `
                <div class="result-content">${renderMarkdown(data.insights)}</div>`;
        } else {
            showError('trendsOutput', data.detail || 'Failed to fetch trends');
        }
    } catch (err) {
        showError('trendsOutput', 'Error: ' + err.message);
    }
}
