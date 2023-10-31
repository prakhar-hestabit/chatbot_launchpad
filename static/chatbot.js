document.addEventListener('DOMContentLoaded', function() {
    const chatDisplay = document.getElementById('chat-display');
    const userMessageInput = document.getElementById('user-message');
    const sendButton = document.getElementById('send-button');
    const personaSelect = document.getElementById('persona-select');  // Dropdown menu for persona selection
    const llmSelect = document.getElementById('llm-select');  // Dropdown menu for LLM selection

    sendButton.addEventListener('click', sendMessage);

    function appendMessage(sender, message) {
        const messageContainer = document.createElement('div');
        messageContainer.classList.add('message', sender);
        messageContainer.textContent = message;
        chatDisplay.appendChild(messageContainer);

        // Scroll to the bottom to show the latest message
        chatDisplay.scrollTop = chatDisplay.scrollHeight;
    }

    function sendMessage() {
        const userMessage = userMessageInput.value;
        const selectedPersona = personaSelect.value;  // Get the selected persona value
        const selectedLLM = llmSelect.value;  // Get the selected LLM value // EXTRA

        if (userMessage.trim() === '') {
            return;
        }

        // Display the user's message
        appendMessage('user', userMessage);

        // Send the user's message and selected persona to the Flask server
        fetch('/send_message', {
            method: 'POST',
            // EXTRA
            body: new URLSearchParams({ 'user_message': userMessage, 'persona': selectedPersona, 'model': selectedLLM}),
            // body: new URLSearchParams({ 'user_message': userMessage, 'persona': selectedPersona}),
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
            }
        })
        .then(response => response.json())
        .then(data => {
            // Display the chatbot's response
            appendMessage('chatbot', data.message);

            // Clear the user input field
            userMessageInput.value = '';
        })
        .catch(error => {
            console.error('Error sending message:', error);
        });
    }
});
