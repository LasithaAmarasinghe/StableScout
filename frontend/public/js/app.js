// API base URL
const API_BASE_URL = '';

// Set query from example button
function setQuery(query) {
    document.getElementById('queryInput').value = query;
}

// Main analyze function
async function analyzeQuery() {
    const queryInput = document.getElementById('queryInput');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');
    const resultsSection = document.getElementById('resultsSection');
    const resultsContent = document.getElementById('resultsContent');
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');

    const query = queryInput.value.trim();

    if (!query) {
        showError('Please enter a query to analyze.');
        return;
    }

    // Reset UI
    hideError();
    hideResults();
    setLoading(true);

    try {
        console.log('Sending query:', query);

        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `Server error: ${response.status}`);
        }

        const data = await response.json();
        console.log('Received response:', data);

        displayResults(data);

    } catch (error) {
        console.error('Error:', error);
        showError(`Failed to analyze query: ${error.message}`);
    } finally {
        setLoading(false);
    }
}

// Display results
function displayResults(data) {
    const resultsContent = document.getElementById('resultsContent');
    const resultsSection = document.getElementById('resultsSection');

    let html = '';

    if (data.messages && Array.isArray(data.messages)) {
        data.messages.forEach((msg, index) => {
            html += formatMessage(msg, index);
        });
    } else if (data.response) {
        html += `<div class="message-block">
            <div class="message-header">
                <span>🤖</span>
                <span>AI Response</span>
            </div>
            <div class="message-content">${escapeHtml(data.response)}</div>
        </div>`;
    } else {
        html += `<div class="message-block">
            <div class="message-content">${escapeHtml(JSON.stringify(data, null, 2))}</div>
        </div>`;
    }

    resultsContent.innerHTML = html;
    resultsSection.classList.remove('hidden');

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Format individual message
function formatMessage(msg, index) {
    let html = '<div class="message-block">';

    // Determine message type and icon
    let icon = '💬';
    let type = 'Message';

    if (msg.type === 'human' || msg.role === 'user') {
        icon = '👤';
        type = 'User';
    } else if (msg.type === 'ai' || msg.role === 'assistant') {
        icon = '🤖';
        type = 'AI Agent';
    } else if (msg.type === 'tool') {
        icon = '🔧';
        type = 'Tool Result';
    } else if (msg.type === 'system') {
        icon = '⚙️';
        type = 'System';
    }

    // Add agent name if available
    if (msg.name) {
        type = msg.name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        if (type.includes('Analyst')) icon = '📊';
        if (type.includes('Risk')) icon = '🛡️';
    }

    html += `<div class="message-header">
        <span>${icon}</span>
        <span>${type}</span>
    </div>`;

    // Message content
    if (msg.content) {
        html += `<div class="message-content">${formatContent(msg.content)}</div>`;
    }

    // Tool calls
    if (msg.tool_calls && msg.tool_calls.length > 0) {
        msg.tool_calls.forEach(toolCall => {
            html += `<div class="tool-call">
                <div class="tool-name">🔧 Calling: ${toolCall.name || toolCall.function?.name || 'Unknown Tool'}</div>
                <div class="tool-args">${escapeHtml(JSON.stringify(toolCall.args || toolCall.function?.arguments || {}, null, 2))}</div>
            </div>`;
        });
    }

    html += '</div>';
    return html;
}

// Format content (handle various formats)
function formatContent(content) {
    if (typeof content === 'string') {
        // Convert newlines to <br> and escape HTML
        return escapeHtml(content).replace(/\n/g, '<br>');
    } else if (Array.isArray(content)) {
        return content.map(item => {
            if (typeof item === 'string') {
                return escapeHtml(item);
            } else if (item.type === 'text') {
                return escapeHtml(item.text || '');
            }
            return escapeHtml(JSON.stringify(item));
        }).join('<br>');
    } else if (typeof content === 'object') {
        return escapeHtml(JSON.stringify(content, null, 2));
    }
    return escapeHtml(String(content));
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Show error message
function showError(message) {
    const errorSection = document.getElementById('errorSection');
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = message;
    errorSection.classList.remove('hidden');
    errorSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Hide error message
function hideError() {
    document.getElementById('errorSection').classList.add('hidden');
}

// Hide results
function hideResults() {
    document.getElementById('resultsSection').classList.add('hidden');
}

// Set loading state
function setLoading(isLoading) {
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = document.getElementById('btnText');
    const btnLoader = document.getElementById('btnLoader');

    if (isLoading) {
        analyzeBtn.disabled = true;
        btnText.classList.add('hidden');
        btnLoader.classList.remove('hidden');
    } else {
        analyzeBtn.disabled = false;
        btnText.classList.remove('hidden');
        btnLoader.classList.add('hidden');
    }
}

// Allow Enter key to submit (Ctrl+Enter for newline)
document.addEventListener('DOMContentLoaded', () => {
    const queryInput = document.getElementById('queryInput');
    
    queryInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
            e.preventDefault();
            analyzeQuery();
        }
    });

    // Check backend health on load
    checkHealth();
});

// Health check
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        console.log('Backend health:', data);
    } catch (error) {
        console.warn('Backend health check failed:', error.message);
        showError('Warning: Cannot connect to backend server. Please make sure both Node.js and Python servers are running.');
    }
}
