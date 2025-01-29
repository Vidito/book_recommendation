from flask import Flask, request, jsonify, render_template
import faiss
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

# Load book dataset
df = pd.read_csv("data.csv")

# Load FAISS index
index = faiss.read_index("faiss_books.index")

# Load Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Flask app
app = Flask(__name__)


def recommend_books(user_query, top_n=5):
    """Given a user query, return the top_n most similar books."""
    query_vector = model.encode([user_query])
    query_vector = np.array(query_vector, dtype=np.float32)
    distances, indices = index.search(query_vector, top_n)
    recommendations = df.iloc[indices[0]]
    return recommendations[["title", "genre", "summary"]].to_dict(orient="records")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/recommend", methods=["POST"])
def get_recommendations():
    """API endpoint to get book recommendations"""
    data = request.get_json()
    user_query = data.get("query", "")

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    recommendations = recommend_books(user_query)
    return jsonify(recommendations)


if __name__ == "__main__":
    app.run(debug=True)
