from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from core import ingest, qa
import os
import shutil

app = Flask(__name__, static_folder='frontend')
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    print("[DEBUG] Recibida petición /upload")
    # --- BORRAR VECTORSTORE ANTES DE GUARDAR EL PDF ---
    vectorstore_path = '/tmp/vectorstore'
    try:
        if os.path.exists(vectorstore_path):
            shutil.rmtree(vectorstore_path)
            print(f"[DEBUG] Vectorstore anterior eliminada: {vectorstore_path}")
    except Exception as e:
        print(f"[ERROR] No se pudo eliminar vectorstore: {e}")
    if 'file' not in request.files:
        print("[ERROR] No file uploaded")
        return jsonify({'error': 'No file uploaded'}), 400
    file = request.files['file']
    os.makedirs('/tmp/vectorstore', exist_ok=True)
    file_path = os.path.join('/tmp/vectorstore', file.filename)
    print(f"[DEBUG] Guardando archivo en {file_path}")
    file.save(file_path)
    try:
        from core import ingest
        ingest.process_pdf(file_path)
        print("[DEBUG] PDF procesado con éxito")
        return jsonify({'status': 'ok'})
    except Exception as e:
        print(f"[ERROR] Fallo en process_pdf: {e}")
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
