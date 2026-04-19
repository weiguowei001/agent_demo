import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RAG:
    def __init__(self, data_path="./data"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.texts = []
        self.index = None

        self.load_data(data_path)
        self.build_index()

    def load_data(self, path):
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith((".txt", ".md", ".py", ".cpp")):
                    full_path = os.path.join(root, file)
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        chunks = self.split_text(content)
                        self.texts.extend(chunks)

    def split_text(self, text, chunk_size=500):
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    def build_index(self):
        embeddings = self.model.encode(self.texts)
        dim = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(embeddings))

    def search(self, query, top_k=3):
        query_vec = self.model.encode([query])
        D, I = self.index.search(np.array(query_vec), top_k)

        results = [self.texts[i] for i in I[0]]
        return "\n\n".join(results)