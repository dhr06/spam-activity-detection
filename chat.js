document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const scanStatus = document.getElementById('scanStatus');
    
    // Sample responses (in a real app, these would come from other users)
    const sampleResponses = [
        "Hi there! How can I help you today?",
        "That's interesting. Tell me more about it.",
        "I understand your concern. Let me think about that.",
        "Have you tried restarting your device?",
        "That's a great question! The answer depends on several factors."
    ];
    
    // Function to add a message to the chat
    function addMessage(content, type, isThreat = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const messageContent = document.createElement('p');
        messageContent.textContent = content;
        messageDiv.appendChild(messageContent);
        
        chatMessages.appendChild(messageDiv);
        
        // If message is a threat, add a warning
        if (isThreat) {
            const warningDiv = document.createElement('div');
            warningDiv.className = 'system-message threat-warning';
            warningDiv.innerHTML = '<strong>⚠️ Warning:</strong> This message has been flagged as potentially harmful.';
            chatMessages.appendChild(warningDiv);
        }
        
        // Scroll to the bottom of the chat
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to scan a message for threats
    async function scanMessage(message) {
        scanStatus.textContent = 'Scanning message...';
        scanStatus.className = 'scan-status scanning';
        
        try {
            const response = await fetch('/api/scan', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    content: message,
                    scan_type: 'message'
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            
            if (result.is_threat) {
                scanStatus.textContent = `Threat detected! (${result.confidence_score}% confidence)`;
                scanStatus.className = 'scan-status threat';
                return true;
            } else {
                scanStatus.textContent = `Message is safe (${result.confidence_score}% confidence)`;
                scanStatus.className = 'scan-status safe';
                setTimeout(() => {
                    scanStatus.textContent = '';
                }, 3000);
                return false;
            }
        } catch (error) {
            console.error('Error scanning message:', error);
            scanStatus.textContent = 'Error scanning message: ' + error.message;
            scanStatus.className = 'scan-status threat';
            return false;
        }
    }
    
    // Function to get a random response
    function getRandomResponse() {
        const randomIndex = Math.floor(Math.random() * sampleResponses.length);
        return sampleResponses[randomIndex];
    }
    
    // Handle form submission
    chatForm.addEventListener('submit', async function(event) {
        event.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, 'user-message');
        messageInput.value = '';
        
        // Scan the message
        const isThreat = await scanMessage(message);
        
        // If not a threat, get a response after a short delay
        if (!isThreat) {
            setTimeout(() => {
                const response = getRandomResponse();
                addMessage(response, 'other-message');
            }, 1000);
        }
    });
});