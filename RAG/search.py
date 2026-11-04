from sentence_transformers import SentenceTransformer
import faiss

from RAG.document_loader import load_pdfs


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


documents = load_pdfs()


texts = []

for doc in documents:

    text = doc["text"]

    # chunks
    for i in range(0, len(text), 500):

        chunk = text[i:i+500]

        texts.append(chunk)



print("Total chunks:", len(texts))


# Create embeddings

embeddings = model.encode(
    texts
)


dimension = embeddings.shape[1]


index = faiss.IndexFlatL2(
    dimension
)


index.add(
    embeddings
)



def search_pdf(query):

    if len(texts)==0:
        return None


    query_vector = model.encode(
        [query]
    )


    distance, result = index.search(
        query_vector,
        3
    )


    answer = ""

    for i in result[0]:

        answer += texts[i] + "\n"


    return answer[:500]