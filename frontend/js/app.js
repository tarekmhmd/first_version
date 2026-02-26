/* ========================================
   APP.JS - MEDICAL AI ASSISTANT
   Enhanced Frontend with UI/UX Improvements
   HCI Principles: Feedback, Consistency, Affordance
   ======================================== */

// ---------- Global Configuration ----------
const CONFIG = {
    API_BASE_URL: 'http://localhost:5000/api',
    ANIMATION_DURATION: 300,
    MESSAGE_DELAY: 500,
    CACHE_DURATION: 5 * 60 * 1000, // 5 minutes
};

// Cache for API responses
const apiCache = new Map();

// ---------- Authentication & Security ----------

/**
 * Check if user is authenticated
 * Implements security check for protected pages
 */
function checkAuth() {
    const token = localStorage.getItem('token');
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const publicPages = ['index.html', ''];
    
    // Redirect to login if no token and on protected page
    if (!token && !publicPages.includes(currentPage)) {
        window.location.href = 'index.html';
        return false;
    }
    
    // Redirect to dashboard if token exists and on login page
    if (token && publicPages.includes(currentPage)) {
        window.location.href = 'dashboard.html';
        return false;
    }
    
    return true;
}

/**
 * Get authentication headers for API requests
 */
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
    };
}

// ---------- UI/UX Feedback System ----------

/**
 * Show notification message
 * Implements immediate feedback principle (HCI)
 */
function showNotification(message, type = 'info', duration = 5000) {
    // Remove existing notifications
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();
    
    const notification = document.createElement('div');
    notification.className = `message ${type} notification`;
    notification.textContent = message;
    notification.setAttribute('role', 'alert');
    notification.setAttribute('aria-live', 'polite');
    
    // Style for fixed positioning
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        zIndex: '10000',
        minWidth: '300px',
        maxWidth: '400px',
        boxShadow: 'var(--shadow-lg)',
        animation: 'slideInRight 0.3s ease-out',
    });
    
    document.body.appendChild(notification);
    
    // Auto-remove after duration
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, duration);
    
    // Add animation keyframes if not present
    if (!document.querySelector('#notification-styles')) {
        const style = document.createElement('style');
        style.id = 'notification-styles';
        style.textContent = `
            @keyframes slideInRight {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOutRight {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
}

/**
 * Show loading state
 * Provides visual feedback during async operations
 */
function showLoading(container) {
    if (!container) return;
    
    const loader = document.createElement('div');
    loader.className = 'spinner';
    loader.setAttribute('aria-label', 'Loading');
    loader.setAttribute('role', 'status');
    
    container.innerHTML = '';
    container.appendChild(loader);
}

/**
 * Hide loading state
 */
function hideLoading(container) {
    if (!container) return;
    const spinner = container.querySelector('.spinner');
    if (spinner) spinner.remove();
}

// ---------- Sidebar Menu (Three Dots) ----------

/**
 * Initialize the animated sidebar
 * Implements Fitts's Law - easy to click toggle
 */
function initSidebar() {
    // Create menu toggle if it doesn't exist
    if (!document.querySelector('.menu-toggle')) {
        const toggle = document.createElement('div');
        toggle.className = 'menu-toggle';
        toggle.setAttribute('aria-label', 'Toggle menu');
        toggle.setAttribute('role', 'button');
        toggle.setAttribute('tabindex', '0');
        
        // Add three dots
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('span');
            toggle.appendChild(dot);
        }
        
        document.body.appendChild(toggle);
        
        // Add click event
        toggle.addEventListener('click', toggleSidebar);
        toggle.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleSidebar();
            }
        });
    }
    
    // Add open class to main content based on sidebar state
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    
    if (sidebar && mainContent) {
        // Check local storage for sidebar state
        const sidebarState = localStorage.getItem('sidebarOpen');
        if (sidebarState === 'true') {
            sidebar.classList.add('open');
            mainContent.classList.add('sidebar-open');
            document.querySelector('.menu-toggle')?.classList.add('open');
        }
    }
}

/**
 * Toggle sidebar open/closed
 */
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    const mainContent = document.querySelector('.main-content');
    const toggle = document.querySelector('.menu-toggle');
    
    if (!sidebar || !mainContent || !toggle) return;
    
    sidebar.classList.toggle('open');
    mainContent.classList.toggle('sidebar-open');
    toggle.classList.toggle('open');
    
    // Save state
    localStorage.setItem('sidebarOpen', sidebar.classList.contains('open'));
    
    // Announce for screen readers
    const isOpen = sidebar.classList.contains('open');
    toggle.setAttribute('aria-label', isOpen ? 'Close menu' : 'Open menu');
}

// ---------- Password Visibility Toggle ----------

/**
 * Add password visibility toggles to all password fields
 * Improves usability (HCI principle of user control)
 */
function initPasswordToggles() {
    document.querySelectorAll('input[type="password"]').forEach(passwordField => {
        // Skip if already wrapped
        if (passwordField.parentElement.classList.contains('password-input-wrapper')) return;
        
        // Create wrapper
        const wrapper = document.createElement('div');
        wrapper.className = 'password-input-wrapper';
        
        // Insert wrapper before password field
        passwordField.parentNode.insertBefore(wrapper, passwordField);
        
        // Move password field into wrapper
        wrapper.appendChild(passwordField);
        
        // Create toggle button
        const toggleBtn = document.createElement('button');
        toggleBtn.type = 'button';
        toggleBtn.className = 'toggle-password';
        toggleBtn.setAttribute('aria-label', 'Toggle password visibility');
        toggleBtn.innerHTML = '👁️';
        
        // Add toggle functionality
        toggleBtn.addEventListener('click', () => {
            const type = passwordField.type === 'password' ? 'text' : 'password';
            passwordField.type = type;
            toggleBtn.innerHTML = type === 'password' ? '👁️' : '👁️‍🗨️';
        });
        
        wrapper.appendChild(toggleBtn);
    });
}

// ---------- Enhanced Chat Functionality ----------

/**
 * Add message to chat with proper formatting
 * Organizes messages neatly (solves the "كلام مش منظم" problem)
 */
function addChatMessage(text, sender) {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return null;
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message-bubble message-${sender}`;
    messageDiv.setAttribute('role', sender === 'user' ? 'complementary' : 'article');
    
    // Format message with proper line breaks and paragraphs
    const formattedText = text
        .split('\n')
        .filter(line => line.trim())
        .map(line => {
            // Check if line is a list item
            if (line.trim().match(/^[-*•]/)) {
                return `<li>${line.trim().substring(1).trim()}</li>`;
            }
            // Check if line is numbered
            if (line.trim().match(/^\d+\./)) {
                return `<li style="list-style-type: decimal;">${line.trim().substring(line.indexOf('.') + 1).trim()}</li>`;
            }
            return `<p>${line.trim()}</p>`;
        })
        .join('');
    
    messageDiv.innerHTML = formattedText;
    
    // Add styling for lists
    const listItems = messageDiv.querySelectorAll('li');
    if (listItems.length > 0) {
        const list = document.createElement(sender === 'user' ? 'div' : 'ul');
        list.style.margin = 'var(--space-xs) 0 var(--space-xs) var(--space-md)';
        listItems.forEach(item => list.appendChild(item.cloneNode(true)));
        messageDiv.innerHTML = '';
        messageDiv.appendChild(list);
    }
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTo({
        top: messagesContainer.scrollHeight,
        behavior: 'smooth'
    });
    
    return messageDiv;
}

/**
 * Show typing indicator in chat
 */
function showTypingIndicator() {
    const messagesContainer = document.getElementById('chatMessages');
    if (!messagesContainer) return null;
    
    const indicator = document.createElement('div');
    indicator.className = 'typing-indicator';
    indicator.id = 'typing-indicator';
    
    for (let i = 0; i < 3; i++) {
        const dot = document.createElement('span');
        indicator.appendChild(dot);
    }
    
    messagesContainer.appendChild(indicator);
    messagesContainer.scrollTo({
        top: messagesContainer.scrollHeight,
        behavior: 'smooth'
    });
    
    return indicator;
}

/**
 * Hide typing indicator
 */
function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) indicator.remove();
}

// ---------- API Communication (Unchanged - Safe) ----------

/**
 * API call wrapper with caching
 */
async function apiCall(endpoint, options = {}) {
    const cacheKey = `${endpoint}-${JSON.stringify(options)}`;
    const cached = apiCache.get(cacheKey);
    
    // Return cached response if valid
    if (cached && Date.now() - cached.timestamp < CONFIG.CACHE_DURATION) {
        return cached.data;
    }
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                ...getAuthHeaders(),
                ...options.headers
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Request failed');
        }
        
        // Cache successful GET requests
        if (!options.method || options.method === 'GET') {
            apiCache.set(cacheKey, {
                data,
                timestamp: Date.now()
            });
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        showNotification(error.message, 'error');
        throw error;
    }
}

/**
 * Upload file to API (Preserved exactly)
 */
async function uploadFile(endpoint, file, fileFieldName = 'image') {
    const formData = new FormData();
    formData.append(fileFieldName, file);
    
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Upload failed');
        }
        
        return data;
    } catch (error) {
        console.error('Upload Error:', error);
        showNotification(error.message, 'error');
        throw error;
    }
}

// ---------- Display Functions ----------

/**
 * Format date consistently
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

/**
 * Display analysis result with severity badge
 */
function displayResult(container, result) {
    if (!container) return;
    
    if (result.error) {
        container.innerHTML = `
            <div class="message error" role="alert">
                <strong>Error:</strong> ${result.error}
            </div>
        `;
        return;
    }
    
    container.innerHTML = `
        <div class="result-box" role="article">
            <div class="result-item">
                <div class="result-label">Diagnosis</div>
                <div class="result-value">${result.diagnosis}</div>
            </div>
            
            ${result.confidence ? `
            <div class="result-item">
                <div class="result-label">Confidence</div>
                <div class="result-value">${result.confidence}%</div>
            </div>
            ` : ''}
            
            <div class="result-item">
                <div class="result-label">Severity</div>
                <span class="severity-badge severity-${result.severity}">${result.severity.toUpperCase()}</span>
            </div>
            
            <div class="result-item">
                <div class="result-label">Treatment Recommendations</div>
                <div class="result-value">${result.treatment}</div>
            </div>
            
            ${result.recommendations && result.recommendations.length > 0 ? `
            <div class="result-item">
                <div class="result-label">Additional Recommendations</div>
                <ul style="margin-top: var(--space-xs); padding-left: var(--space-lg);">
                    ${result.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
            ` : ''}
        </div>
    `;
}

// ---------- File Upload Handlers ----------

/**
 * Handle file input change
 */
function handleFileSelection(file, previewElementId, buttonId) {
    if (!file || !file.type.startsWith('image/') && !file.type.startsWith('audio/')) {
        showNotification('Please select a valid file', 'error');
        return false;
    }
    
    const preview = document.getElementById(previewElementId);
    const button = document.getElementById(buttonId);
    
    if (preview) {
        const reader = new FileReader();
        reader.onload = (e) => {
            if (preview.tagName === 'IMG') {
                preview.src = e.target.result;
            } else if (preview.tagName === 'AUDIO') {
                preview.src = e.target.result;
            }
            preview.classList.remove('hidden');
        };
        reader.readAsDataURL(file);
    }
    
    if (button) button.classList.remove('hidden');
    
    return true;
}

/**
 * Setup drag and drop
 */
function setupDragAndDrop(dropZone, callback) {
    if (!dropZone) return;
    
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });
    
    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });
    
    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        
        const file = e.dataTransfer.files[0];
        if (file) callback(file);
    });
}

// ---------- Logout Function ----------

/**
 * Logout user and clear session
 */
function logout() {
    // Clear all storage
    localStorage.clear();
    sessionStorage.clear();
    apiCache.clear();
    
    // Show goodbye message
    showNotification('Logged out successfully', 'success');
    
    // Redirect to login
    setTimeout(() => {
        window.location.href = 'index.html';
    }, 500);
}

// ---------- Initialize Everything ----------

/**
 * Main initialization function
 * Runs when DOM is loaded
 */
document.addEventListener('DOMContentLoaded', () => {
    // Check authentication
    checkAuth();
    
    // Initialize UI components
    initSidebar();
    initPasswordToggles();
    
    // Set active nav link
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('.nav-link');
    
    navLinks.forEach(link => {
        const href = link.getAttribute('href');
        if (href === currentPage) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        } else {
            link.classList.remove('active');
            link.removeAttribute('aria-current');
        }
    });
    
    // Add keyboard navigation support
    document.addEventListener('keydown', (e) => {
        // ESC key closes sidebar
        if (e.key === 'Escape') {
            const sidebar = document.querySelector('.sidebar.open');
            if (sidebar) toggleSidebar();
        }
    });
    
    // Log performance
    if (window.performance) {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        console.log(`Page loaded in ${pageLoadTime}ms`);
    }
});

// Export functions for global use
window.checkAuth = checkAuth;
window.logout = logout;
window.showNotification = showNotification;
window.formatDate = formatDate;
window.apiCall = apiCall;
window.uploadFile = uploadFile;
window.displayResult = displayResult;
window.setupDragAndDrop = setupDragAndDrop;
window.toggleSidebar = toggleSidebar;
window.addChatMessage = addChatMessage;