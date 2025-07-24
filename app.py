from flask import Flask, request, jsonify
from loader import load_documents
from rag_pipeline import query_rag_pipeline

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    # Load and parse the document
    text = load_documents(file)
    return jsonify({'message': 'File uploaded successfully', 'text': text}), 200

@app.route('/query', methods=['POST'])
def query():
    data = request.get_json()
    if 'question' not in data:
        return jsonify({'error': 'No question provided'}), 400
    
    answer = query_rag_pipeline(data['question'])
    return jsonify({'answer': answer}), 200

if __name__ == '__main__':
    app.run(debug=True)