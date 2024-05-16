// Function to extract image data from a base64 string
function extractImageData(base64Image) {
    // Remove the data URL prefix
    var base64ImageWithoutPrefix = base64Image.replace(/^data:image\/(png|jpeg|jpg);base64,/, "");
    return base64ImageWithoutPrefix;
}

// Listen for messages from content script
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
    if (message.type === "hidden_url_detected") {
        // Extract image data from the message
        var imageData = extractImageData(message.imageData);
        
        // Send the image data to the Flask server for processing
        detectHiddenUrlsInImages(imageData);
    }
});
