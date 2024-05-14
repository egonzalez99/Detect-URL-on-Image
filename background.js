// Listen for messages from content script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.type === "hidden_url_detected") {
        // Send image data to Flask server
        fetch('http://localhost:5000/process_image', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ imageData: message.imageData })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to send image data to server');
            }
            return response.json();
        })
        .then(data => {
            console.log('Server response:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
});