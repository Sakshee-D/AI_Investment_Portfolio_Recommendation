from vector_store import model, index, stored_data
import numpy as np

def retrieve(query):
    print("Index size:", index.ntotal)
    print("Stored data size:", len(stored_data))
    
    if index.ntotal == 0:
        return stored_data[:3]

    query_embedding = model.encode(query)
    query_embedding = np.array([query_embedding])

    D, I = index.search(query_embedding, k=3)

    results = []
    for i in I[0]:
        if i < len(stored_data):
            results.append(stored_data[i])

    if not results:
        return stored_data[:3]

    print("QUERY:", query)
    print("RESULTS:", results)

    return results