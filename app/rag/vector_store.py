from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384

index = faiss.IndexFlatL2(dimension)

documents = []


def add_document(text):

    embedding = model.encode([text])

    index.add(np.array(embedding))

    documents.append(text)


def search(query):

    if len(documents) == 0:
        return "No patient data available."

    embedding = model.encode([query])

    D, I = index.search(np.array(embedding), k=1)

    return documents[I[0][0]]