function extractImageData(imgElement) {
    // Create a canvas element to draw the image
    var canvas = document.createElement('canvas');
    var context = canvas.getContext('2d');
    canvas.width = imgElement.width;
    canvas.height = imgElement.height;
    // Draw the image onto the canvas
    context.drawImage(imgElement, 0, 0, imgElement.width, imgElement.height);
    // Get the image data from the canvas
    var imageData = canvas.toDataURL('image/jpeg');
    return imageData;
}

// Function to detect hidden URLs in images
function detectHiddenUrlsInImages(imageData) {
    // Send image data to Flask server
    fetch('http://localhost:5000/process_image', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ imageData: imageData })
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

// Add event listener to detect image load events
document.addEventListener('load', function(event) {
    if (event.target.tagName === 'IMG') {
        // Assuming you have a function to extract image data from the loaded image
        var imageData = extractImageData(event.target);
        detectHiddenUrlsInImages(imageData);
    }
});
