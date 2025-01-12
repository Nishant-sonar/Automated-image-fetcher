from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
import os
import logging
from backend import scrape_google_images

# Initialize the Flask application
app = Flask(__name__)
CORS(app)  # Enable CORS globally
logging.basicConfig(level=logging.DEBUG)

# Serve the main HTML file
@app.route('/')
def index():
    return send_file('index.html')

# Serve static files (CSS, JS, images)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# Endpoint for searching images
@app.route('/search', methods=['POST'])
def search_images():
    try:
        # Get JSON data from the request
        data = request.get_json()
        query = data.get("query")
        quantity = int(data.get("quantity", 10))  # Default to 10 images if not specified

        # Validate query
        if not query:
            return jsonify({"status": "error", "message": "No search query provided."}), 400

        # Call scrape_google_images function and get results
        results = scrape_google_images(query, num_images=quantity)
        return jsonify(results)  # Send JSON response to the frontend

    except Exception as e:
        # Log and return any other errors
        app.logger.error(f"Error in /search endpoint: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Run the app on a specified port
if __name__ == '__main__':
    # Use the PORT environment variable if set, otherwise default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
