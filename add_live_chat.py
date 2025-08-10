import os
import re

# Live chat widget CSS
chat_css = """

/* Live Chat Widget */
.chat-widget {
    position: fixed;
    bottom: 30px;
    left: 30px;
    z-index: 998;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.chat-button {
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: white;
    border: none;
    cursor: pointer;
    box-shadow: 0 8px 25px rgba(74, 144, 226, 0.4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    transition: all 0.3s ease;
    animation: bounce 2s infinite;
}

.chat-button:hover {
    transform: scale(1.1);
    box-shadow: 0 12px 35px rgba(74, 144, 226, 0.5);
}

.chat-button.active {
    animation: none;
}

@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}

.chat-notification {
    position: absolute;
    top: -5px;
    right: -5px;
    background: #ff4444;
    color: white;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: bold;
    animation: pulse-red 1.5s infinite;
}

@keyframes pulse-red {
    0% { box-shadow: 0 0 0 0 rgba(255, 68, 68, 0.7); }
    70% { box-shadow: 0 0 0 10px rgba(255, 68, 68, 0); }
    100% { box-shadow: 0 0 0 0 rgba(255, 68, 68, 0); }
}

.chat-window {
    position: absolute;
    bottom: 80px;
    left: 0;
    width: 380px;
    height: 500px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
    display: none;
    flex-direction: column;
    overflow: hidden;
    animation: slideUp 0.3s ease;
}

.chat-window.active {
    display: flex;
}

@keyframes slideUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.chat-header {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: white;
    padding: 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.chat-header-info {
    display: flex;
    align-items: center;
    gap: 12px;
}

.agent-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
}

.agent-details h4 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
}

.agent-details p {
    margin: 0;
    font-size: 12px;
    opacity: 0.9;
}

.online-indicator {
    display: inline-block;
    width: 8px;
    height: 8px;
    background: #44ff44;
    border-radius: 50%;
    margin-left: 5px;
    animation: pulse-green 2s infinite;
}

@keyframes pulse-green {
    0% { box-shadow: 0 0 0 0 rgba(68, 255, 68, 0.7); }
    70% { box-shadow: 0 0 0 5px rgba(68, 255, 68, 0); }
    100% { box-shadow: 0 0 0 0 rgba(68, 255, 68, 0); }
}

.chat-close {
    background: none;
    border: none;
    color: white;
    font-size: 24px;
    cursor: pointer;
    padding: 0;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: background 0.3s;
}

.chat-close:hover {
    background: rgba(255, 255, 255, 0.2);
}

.chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 20px;
    background: #f8f9fa;
}

.message {
    margin-bottom: 15px;
    display: flex;
    animation: fadeIn 0.3s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.message.agent {
    justify-content: flex-start;
}

.message.user {
    justify-content: flex-end;
}

.message-bubble {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 15px;
    word-wrap: break-word;
}

.message.agent .message-bubble {
    background: white;
    color: #333;
    border-bottom-left-radius: 5px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.message.user .message-bubble {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: white;
    border-bottom-right-radius: 5px;
}

.message-time {
    font-size: 11px;
    opacity: 0.7;
    margin-top: 5px;
}

.typing-indicator {
    display: flex;
    gap: 4px;
    padding: 15px;
    background: white;
    border-radius: 15px;
    border-bottom-left-radius: 5px;
    width: fit-content;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.typing-dot {
    width: 8px;
    height: 8px;
    background: #999;
    border-radius: 50%;
    animation: typing 1.4s infinite;
}

.typing-dot:nth-child(2) {
    animation-delay: 0.2s;
}

.typing-dot:nth-child(3) {
    animation-delay: 0.4s;
}

@keyframes typing {
    0%, 60%, 100% {
        transform: translateY(0);
        opacity: 0.5;
    }
    30% {
        transform: translateY(-10px);
        opacity: 1;
    }
}

.chat-input-area {
    padding: 20px;
    background: white;
    border-top: 1px solid #e0e0e0;
}

.chat-input-form {
    display: flex;
    gap: 10px;
}

.chat-input {
    flex: 1;
    padding: 12px;
    border: 1px solid #e0e0e0;
    border-radius: 25px;
    outline: none;
    font-size: 14px;
    transition: border-color 0.3s;
}

.chat-input:focus {
    border-color: #4a90e2;
}

.chat-send {
    background: linear-gradient(135deg, #4a90e2 0%, #357abd 100%);
    color: white;
    border: none;
    padding: 12px 20px;
    border-radius: 25px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s;
}

.chat-send:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(74, 144, 226, 0.3);
}

.quick-actions {
    display: flex;
    gap: 8px;
    margin-top: 10px;
    flex-wrap: wrap;
}

.quick-action {
    padding: 6px 12px;
    background: white;
    border: 1px solid #4a90e2;
    color: #4a90e2;
    border-radius: 15px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.3s;
}

.quick-action:hover {
    background: #4a90e2;
    color: white;
}

@media (max-width: 768px) {
    .chat-widget {
        left: 20px;
        bottom: 20px;
    }
    
    .chat-window {
        width: calc(100vw - 40px);
        max-width: 380px;
        height: 450px;
    }
    
    .floating-quote-btn {
        bottom: 100px;
    }
}
"""

# Live chat widget HTML and JavaScript
chat_html = """
    <!-- Live Chat Widget -->
    <div class="chat-widget">
        <button class="chat-button" onclick="toggleChat()" id="chatButton">
            💬
            <span class="chat-notification">1</span>
        </button>
        
        <div class="chat-window" id="chatWindow">
            <div class="chat-header">
                <div class="chat-header-info">
                    <div class="agent-avatar">👤</div>
                    <div class="agent-details">
                        <h4>Property Expert <span class="online-indicator"></span></h4>
                        <p>Online - Typically replies instantly</p>
                    </div>
                </div>
                <button class="chat-close" onclick="toggleChat()">×</button>
            </div>
            
            <div class="chat-messages" id="chatMessages">
                <div class="message agent">
                    <div class="message-bubble">
                        <div>👋 Hi! I'm here to help with your property management needs.</div>
                        <div class="message-time">Just now</div>
                    </div>
                </div>
                <div class="message agent">
                    <div class="message-bubble">
                        <div>How can I assist you today? I can help with:</div>
                        <div style="margin-top: 8px;">
                            • Getting a free quote<br>
                            • Learning about our services<br>
                            • Scheduling a consultation<br>
                            • Answering your questions
                        </div>
                        <div class="message-time">Just now</div>
                    </div>
                </div>
            </div>
            
            <div class="chat-input-area">
                <form class="chat-input-form" onsubmit="sendMessage(event)">
                    <input type="text" class="chat-input" id="chatInput" placeholder="Type your message..." autocomplete="off">
                    <button type="submit" class="chat-send">Send</button>
                </form>
                <div class="quick-actions">
                    <button class="quick-action" onclick="quickMessage('I need a quote')">Get Quote</button>
                    <button class="quick-action" onclick="quickMessage('What services do you offer?')">Services</button>
                    <button class="quick-action" onclick="quickMessage('Schedule consultation')">Book Call</button>
                    <button class="quick-action" onclick="quickMessage('Contact info')">Contact</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let chatOpen = false;
        let messageCount = 2;
        
        function toggleChat() {
            chatOpen = !chatOpen;
            const chatWindow = document.getElementById('chatWindow');
            const chatButton = document.getElementById('chatButton');
            const notification = document.querySelector('.chat-notification');
            
            if (chatOpen) {
                chatWindow.classList.add('active');
                chatButton.classList.add('active');
                if (notification) notification.style.display = 'none';
                document.getElementById('chatInput').focus();
            } else {
                chatWindow.classList.remove('active');
                chatButton.classList.remove('active');
            }
        }
        
        function sendMessage(event) {
            event.preventDefault();
            const input = document.getElementById('chatInput');
            const message = input.value.trim();
            
            if (message) {
                // Add user message
                addMessage(message, 'user');
                input.value = '';
                
                // Show typing indicator
                showTyping();
                
                // Simulate agent response
                setTimeout(() => {
                    removeTyping();
                    const response = getAgentResponse(message);
                    addMessage(response, 'agent');
                }, 1500);
            }
        }
        
        function quickMessage(text) {
            document.getElementById('chatInput').value = text;
            sendMessage(new Event('submit'));
        }
        
        function addMessage(text, sender) {
            const messagesDiv = document.getElementById('chatMessages');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'message ' + sender;
            
            const time = new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
            
            messageDiv.innerHTML = `
                <div class="message-bubble">
                    <div>${text}</div>
                    <div class="message-time">${time}</div>
                </div>
            `;
            
            messagesDiv.appendChild(messageDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
            messageCount++;
        }
        
        function showTyping() {
            const messagesDiv = document.getElementById('chatMessages');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'typing-indicator';
            typingDiv.id = 'typingIndicator';
            typingDiv.innerHTML = `
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            `;
            messagesDiv.appendChild(typingDiv);
            messagesDiv.scrollTop = messagesDiv.scrollHeight;
        }
        
        function removeTyping() {
            const typing = document.getElementById('typingIndicator');
            if (typing) typing.remove();
        }
        
        function getAgentResponse(message) {
            const lowerMessage = message.toLowerCase();
            
            if (lowerMessage.includes('quote') || lowerMessage.includes('price') || lowerMessage.includes('cost')) {
                return "I'd be happy to provide you with a customized quote! For the most accurate pricing, I'll connect you with our team. You can call us directly at <a href='tel:8476522338' style='color: #4a90e2; font-weight: bold;'>(847) 652-2338</a> or I can have someone call you. What works best?";
            } else if (lowerMessage.includes('service') || lowerMessage.includes('offer') || lowerMessage.includes('what do you do')) {
                return "We provide comprehensive property management services including:<br><br>🏢 Condominium Management<br>🏘️ HOA Management<br>🏡 Townhome Management<br>💰 Financial Management<br>🔧 Maintenance Coordination<br>📋 Board Support<br><br>Would you like details about any specific service?";
            } else if (lowerMessage.includes('consultation') || lowerMessage.includes('meeting') || lowerMessage.includes('schedule') || lowerMessage.includes('book')) {
                return "Perfect! I'll help you schedule a free consultation. Please call us at <a href='tel:8476522338' style='color: #4a90e2; font-weight: bold;'>(847) 652-2338</a> to speak with a property management expert immediately, or share your phone number and preferred time, and we'll call you.";
            } else if (lowerMessage.includes('contact') || lowerMessage.includes('phone') || lowerMessage.includes('email') || lowerMessage.includes('reach')) {
                return "Here's how to reach us:<br><br>📞 Phone: <a href='tel:8476522338' style='color: #4a90e2; font-weight: bold;'>(847) 652-2338</a><br>✉️ Email: <a href='mailto:service@manage369.com' style='color: #4a90e2;'>service@manage369.com</a><br>📍 Office: 1400 Patriot Blvd 357, Glenview, IL<br><br>We're available Monday-Friday, 9AM-5PM. How else can I help?";
            } else if (lowerMessage.includes('area') || lowerMessage.includes('location') || lowerMessage.includes('where')) {
                return "We proudly serve 68+ communities across Chicago and the North Shore, including Wilmette, Winnetka, Highland Park, Glencoe, Evanston, Glenview, Lincoln Park, Gold Coast, and many more. Which area are you interested in?";
            } else if (lowerMessage.includes('experience') || lowerMessage.includes('how long') || lowerMessage.includes('years')) {
                return "Manage369 has been serving Chicago and North Shore communities for over 18 years! We currently manage 50+ properties with 2,450+ units. Our team holds CAI, IREM, and CCIM certifications. Would you like to know more about our qualifications?";
            } else {
                return "Thanks for your message! For immediate assistance, please call us at <a href='tel:8476522338' style='color: #4a90e2; font-weight: bold;'>(847) 652-2338</a>. Our property management experts are ready to help with your specific needs. Is there anything specific you'd like to know about our services?";
            }
        }
        
        // Show initial notification after 5 seconds
        setTimeout(() => {
            const notification = document.querySelector('.chat-notification');
            if (notification && !chatOpen) {
                notification.style.display = 'flex';
            }
        }, 5000);
    </script>"""

# Append CSS to styles file
with open('css/styles.css', 'a', encoding='utf-8') as f:
    f.write(chat_css)

print("[OK] Added live chat CSS")

# Add chat widget to all HTML pages
def add_chat_to_page(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Only add if not already present
    if 'chat-widget' not in content:
        # Add before closing body tag
        content = content.replace('</body>', chat_html + '\n</body>')
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

# Add to main index
if add_chat_to_page('index.html'):
    print("[OK] Added chat to index.html")

# Add to all property pages
property_dirs = os.listdir('property-management')
updated = 0
for d in property_dirs:
    if os.path.isdir(f'property-management/{d}'):
        filepath = f'property-management/{d}/index.html'
        if os.path.exists(filepath):
            if add_chat_to_page(filepath):
                updated += 1

print(f"[OK] Added chat to {updated} property pages")

# Add to blog pages
blog_files = ['blog/index.html', 'blog/2025-illinois-hoa-law-changes.html', 
              'blog/top-5-financial-mistakes-hoa-boards-avoid.html']
for bf in blog_files:
    if os.path.exists(bf):
        if add_chat_to_page(bf):
            print(f"[OK] Added chat to {bf}")

print("\nLive chat widget successfully added to all pages!")