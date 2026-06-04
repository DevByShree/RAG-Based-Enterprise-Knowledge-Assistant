import os

import ollama
import chromadb
from sentence_transformers import SentenceTransformer
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#  Setup - 
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.PersistentClient(path="vector_db")
collection = client.get_or_create_collection(name="my_notes")
OLLAMA_MODEL_CANDIDATES = [
    os.getenv("OLLAMA_MODEL"),
    "llama3.2:1b",
    "llama3.2:latest",
]

def retrieve_chunks(question):
    question_embedding = embedding_model.encode(question).tolist()
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )
    return results['documents'][0]

def get_answer(question, chunks):
    context = "\n\n".join(chunks)

    messages = [
        {
            "role": "system",
            "content": "You are a helpful study assistant. Answer only based on the provided notes."
        },
        {
            "role": "user",
            "content": f"Notes:\n{context}\n\nQuestion: {question}"
        }
    ]

    tried_models = []
    last_error = None

    for model_name in [model for model in OLLAMA_MODEL_CANDIDATES if model]:
        tried_models.append(model_name)
        try:
            response = ollama.chat(
                model=model_name,
                messages=messages
            )
            return response['message']['content']
        except Exception as exc:
            last_error = exc
            error_text = str(exc).lower()
            if "not found" in error_text or "connectionerror" in type(exc).__name__.lower():
                continue
            raise

    raise RuntimeError(
        f"No usable Ollama model found. Tried: {', '.join(tried_models)}. Last error: {last_error}"
    )

#  Frontend serve 
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

#  RAG API endpoint
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json or {}
        question = data.get('question', '')

        if not question.strip():
            return jsonify({'answer': 'Ask questions', 'sources': []})

        print(f"\n Question: {question}")
        print(" Searching notes...")
        chunks = retrieve_chunks(question)

        print(" Generating answer...")
        answer = get_answer(question, chunks)

        print(f" Done!\n{'-'*40}")
        return jsonify({
            'answer': answer,
            'sources': ['your_doc.pdf']
        })
    except Exception as exc:
        app.logger.exception("Failed to answer question")
        return jsonify({
            'answer': f"Server error: {exc}",
            'sources': []
        }), 503

if __name__ == '__main__':
    print("=" * 50)
    print("  RAG PDF Chatbot - Web Mode")
    print("  Open: http://localhost:5000")
    print("=" * 50)
    app.run(port=5000, debug=True)