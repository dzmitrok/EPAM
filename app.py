from flask import Flask, jsonify, send_from_directory, abort
import os

app = Flask(__name__)

# Path to the .well-known directory
WELL_KNOWN_DIR = os.path.join(os.path.dirname(__file__), '.well-known')

@app.route('/')
def index():
    """Basic homepage"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>JSON File Server</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            h1 {
                color: #333;
            }
            .info {
                background-color: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            code {
                background-color: #f4f4f4;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: monospace;
            }
            a {
                color: #007bff;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to JSON File Server</h1>
        <div class="info">
            <p>This server serves JSON files from the <code>.well-known</code> folder for <strong>epmgess.com</strong>.</p>
            <p><strong>Usage:</strong> Access JSON files using the URL pattern:</p>
            <p><code>/.well-known/&lt;filename&gt;.json</code> or <code>/well-known/&lt;filename&gt;.json</code></p>
            <p><strong>Examples:</strong></p>
            <ul>
                <li><a href="/.well-known/did.json">/.well-known/did.json</a></li>
                <li><a href="/well-known/did.json">/well-known/did.json</a></li>
                <li><a href="/.well-known/">/.well-known/</a> (list all files)</li>
            </ul>
        </div>
    </body>
    </html>
    '''

@app.route('/.well-known/')
@app.route('/.well-known')
def well_known_index():
    """List available JSON files in .well-known directory"""
    try:
        files = [f for f in os.listdir(WELL_KNOWN_DIR) if f.endswith('.json')]
        if files:
            # Return JSON list of available files
            return jsonify({
                'available_files': files,
                'files': {f: f'/.well-known/{f}' for f in files}
            })
        else:
            return jsonify({'message': 'No JSON files found in .well-known directory'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/.well-known/<path:filename>')
@app.route('/well-known/<path:filename>')
def serve_json(filename):
    """Serve JSON files from the .well-known directory"""
    # Ensure the file has .json extension
    if not filename.endswith('.json'):
        filename = filename + '.json'
    
    # Security: prevent directory traversal
    if '..' in filename or filename.startswith('/'):
        abort(400)
    
    # Check if file exists
    file_path = os.path.join(WELL_KNOWN_DIR, filename)
    if not os.path.exists(file_path):
        abort(404)
    
    # Serve the JSON file with proper headers
    return send_from_directory(WELL_KNOWN_DIR, filename, mimetype='application/json')

@app.errorhandler(404)
def not_found(error):
    """Custom 404 error handler"""
    return jsonify({'error': 'File not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    """Custom 400 error handler"""
    return jsonify({'error': 'Bad request'}), 400

# Create .well-known directory if it doesn't exist
os.makedirs(WELL_KNOWN_DIR, exist_ok=True)

if __name__ == '__main__':
    # Get port from environment variable (Azure sets this) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    # Run the Flask app
    app.run(debug=False, host='0.0.0.0', port=port)

