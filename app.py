from flask import Flask, request, jsonify
from flask import send_from_directory

app = Flask(__name__)

# Define a route for the root URL
@app.route('/')
def index():
    return 'Welcome to the Image Finder API'

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

# Define your other routes here...

@app.route('/localhost:5000/process_image', methods=['POST'])
def process_image():
    data = request.json
    image_data = data.get('imageData')
    # Process the image data here
    print("Received image data:", image_data)
    # Respond with a message indicating successful processing
    return jsonify({'message': 'Image data received and processed successfully'})

if __name__ == '__main__':
    app.run(debug=True)