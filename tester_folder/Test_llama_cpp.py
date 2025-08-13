from agent.llm import call_llm, DEFAULT_MODEL, EMBED_MODEL
import numpy as np

def cosine_similarity(vec1, vec2):
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def test_chat():
    print("\n=== Chat Model Test ===")
    prompt = "What is the capital of the Philippines?"
    response = call_llm(prompt, model=DEFAULT_MODEL)
    print("Response:\n", response)

def test_embeddings():
    print("\n=== Embedding Test ===")
    query1 = "What is artificial intelligence?"
    query2 = "Explain AI like I am five."

    embed1 = call_llm(query1, model=EMBED_MODEL)
    embed2 = call_llm(query2, model=EMBED_MODEL)

    sim = cosine_similarity(embed1, embed2)
    print(f"Cosine similarity: {sim:.4f}")

if __name__ == "__main__":
    test_chat()
    test_embeddings()
