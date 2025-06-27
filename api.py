from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from backend.core import ingest, qa
import os

app = Flask(__name__, static_folder='frontend')
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    os.makedirs('vectorstore', exist_ok=True)
    file_path = os.path.join('vectorstore', file.filename)
    file.save(file_path)
    try:
        ingest.process_pdf(file_path)
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question', '')
    if not question:
        return jsonify({'error': 'No question provided'}), 400
    try:
        answer = qa.ask_question(question)
        if isinstance(answer, dict) and 'result' in answer:
            answer = answer['result']
        return jsonify({'answer': str(answer)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Servir archivos estáticos del frontend
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
