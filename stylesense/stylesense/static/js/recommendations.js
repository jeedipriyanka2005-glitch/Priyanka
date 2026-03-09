function getSelectedChipValue(field) {
    const chip = document.querySelector(`.chip.active[data-field="${field}"]`);
    return chip ? chip.dataset.value : null;
}

async function getRecommendations() {
    const preferences = {
        style: getSelectedChipValue('style') || 'Casual',
        occasion: getSelectedChipValue('occasion') || 'Everyday Casual',
        season: getSelectedChipValue('season') || 'All-season',
        colors: getSelectedChipValue('colors') || 'Neutral tones',
        budget: document.getElementById('budget').value,
        gender: document.getElementById('gender').value,
        body_type: getSelectedChipValue('body_type') || 'Not specified'
    };

    showLoading('recommendationsOutput', '✨ Crafting your personalized outfits...');

    try {
        const response = await fetch('/api/recommendations/personalized', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(preferences)
        });

        const data = await response.json();
        if (data.status === 'success') {
            document.getElementById('recommendationsOutput').innerHTML = `
                <div class="result-content">${renderMarkdown(data.recommendations)}</div>`;
        } else {
            showError('recommendationsOutput', data.detail || 'Failed to get recommendations');
        }
    } catch (err) {
        showError('recommendationsOutput', 'Network error: ' + err.message);
    }
}
