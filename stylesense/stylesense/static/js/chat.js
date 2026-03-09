let chatHistory = [];

async function sendMessage() {
    const input = document.getElementById('chatInput');
    const text = input.value.trim();
    if (!text) return;

    addMessage('user', text);
    input.value = '';
    input.style.height = 'auto';
    chatHistory.push({ role: 'user', content: text });

    const typingId = addTypingIndicator();

    try {
        const response = await fetch('/api/chat/message', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ messages: chatHistory })
        });
        const data = await response.json();
        removeTypingIndicator(typingId);

        if (data.status === 'success') {
            addMessage('assistant', data.response);
            chatHistory.push({ role: 'assistant', content: data.response });
        } else {
            addMessage('assistant', '❌ Sorry, I had trouble responding. Please try again.');
        }
    } catch (err) {
        removeTypingIndicator(typingId);
        addMessage('assistant', '❌ Connection error. Please check your settings.');
    }
}

function addMessage(role, content) {
    const container = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = `message ${role}-message`;
    const icon = role === 'assistant' ? 'fa-robot' : 'fa-user';
    div.innerHTML = `
        <div class="message-avatar"><i class="fas ${icon}"></i></div>
        <div class="message-content">${renderMarkdown(content)}</div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return div;
}

function addTypingIndicator() {
    const id = Date.now();
    const container = document.getElementById('chatMessages');
    const div = document.createElement('div');
    div.className = 'message assistant-message';
    div.id = 'typing-' + id;
    div.innerHTML = `
        <div class="message-avatar"><i class="fas fa-robot"></i></div>
        <div class="message-content">
            <div class="typing-indicator">
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
                <div class="typing-dot"></div>
            </div>
        </div>`;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById('typing-' + id);
    if (el) el.remove();
}

function sendQuickPrompt(text) {
    document.getElementById('chatInput').value = text;
    sendMessage();
}

function clearChat() {
    chatHistory = [];
    document.getElementById('chatMessages').innerHTML = `
        <div class="message assistant-message">
            <div class="message-avatar"><i class="fas fa-robot"></i></div>
            <div class="message-content">
                <p>Chat cleared! How can I help you with your style today? 👗✨</p>
            </div>
        </div>`;
}

function handleChatKeydown(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
    // Auto-resize
    e.target.style.height = 'auto';
    e.target.style.height = Math.min(e.target.scrollHeight, 120) + 'px';
}
