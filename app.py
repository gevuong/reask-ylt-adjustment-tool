import matplotlib
import numpy as np
import logging
import os
import json

from flask import Flask, request, jsonify, Response, send_file, abort
from pathlib import Path
from pylt import adjust_ylt
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger('matplotlib').setLevel(logging.WARNING)

# Load environment variables from a .env file
load_dotenv();

matplotlib.use('Agg')  # Use a non-GUI backend

app = Flask(__name__)

# Define paths
DATA_DIR = Path(os.getenv('DATA_DIR'))
INPUT_YLT_PATH = DATA_DIR / os.getenv('INPUT_YLT_FILE')
COUNTS_PATH = DATA_DIR / os.getenv('COUNTS_FILE')
METRICS_PATH = DATA_DIR / os.getenv('METRICS_FILE')
GATES_PATH = DATA_DIR / os.getenv('GATES_FILE')
SAVE_DIR = os.getenv("SAVE_DIR")

def validate_paths():
    if not INPUT_YLT_PATH.exists() or not INPUT_YLT_PATH.is_file():
        raise FileNotFoundError(f"Input YLT path not found: {INPUT_YLT_PATH}")
    if not COUNTS_PATH.exists() or not COUNTS_PATH.is_file():
        raise FileNotFoundError(f"Counts path not found: {COUNTS_PATH}")
    if not METRICS_PATH.exists() or not METRICS_PATH.is_file():
        raise FileNotFoundError(f"Metrics path not found: {METRICS_PATH}")
    if not GATES_PATH.exists() or not GATES_PATH.is_file():
        raise FileNotFoundError(f"Gates path not found: {GATES_PATH}")

    app.logger.debug("Input YLT path: %s", INPUT_YLT_PATH)
    app.logger.debug("Counts path: %s", COUNTS_PATH)
    app.logger.debug("Metrics path: %s", METRICS_PATH)
    app.logger.debug("Gates path: %s", GATES_PATH)
    app.logger.debug("Save directory: %s", SAVE_DIR)

# Ensure preflight request passes access control check and has an HTTP ok status
@app.before_request
def basic_authentication():
    if request.method.lower() == 'options':
        return Response()

@app.route('/adjust', methods=['POST'])
def adjust():
    try:
        app.logger.debug("Received request: %s", request.data)
        validate_paths();

        # Call the adjust_ylt function and capture the DataFrame

        app.logger.debug("DataFrame shape: %s", df_adjusted.shape)

        # Slice the DataFrame to return only the first 5 records
        limited_df = df_adjusted.head(5)

        # Convert the sliced DataFrame to JSON
        json_result = limited_df.to_json(orient='records')

        # Return the JSON result
        return app.response_class(response=json_result, status=200, mimetype='application/json')

    except Exception as e:
        app.logger.error("Error during adjustment process: %s", str(e))
        return jsonify({"error": str(e)}), 500
    
@app.route('/get-image/<filename>', methods=['GET'])
def image_endpoint(filename):
    
    filepath = os.path.join(SAVE_DIR, filename)

    # Secure the filename to prevent directory traversal attacks
    from werkzeug.utils import secure_filename
    safe_filename = secure_filename(filename)

    # Rebuild the filepath with the safe filename
    filepath = os.path.join(SAVE_DIR, safe_filename)
    
    if os.path.isfile(filepath):
        print("File found, sending...")
        return send_file(filepath, mimetype='image/png')
    else:
        print("File not found, aborting...")
        abort(404, description="Resource not found")

@app.route('/', methods=['GET'])
def home():
    return "Welcome to the Climate Insurance Backend API. Use the /adjust endpoint to adjust YLT data."

if __name__ == "__main__":
    app.run(debug=True, port=5000)
