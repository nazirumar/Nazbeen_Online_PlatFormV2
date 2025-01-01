# from sentence_transformers import SentenceTransformer

# from pinecone import Pinecone as PineconeClient
# from decouple import config

# # # Initialize Pinecone client
# pinecone_client = PineconeClient(api_key=config('PINECONE_API_KEY'))

# # Pinecone index name
# INDEX_NAME = "course-index"

# def pineconeindex():
#     try:
#         # Connect to Pinecone index
#         pinecone_index = pinecone_client.Index(INDEX_NAME)
#     except Exception as e:
#         raise RuntimeError(f"Failed to connect to Pinecone index '{INDEX_NAME}': {e}")
#     return pinecone_index

# embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# def generate_query_embedding(query):
#     """
#     Generate embeddings for the query using a pre-trained SentenceTransformer model.
#     """
#     return embedding_model.encode(query).tolist()

# def query_pinecone(query_embedding):
#     """
#     Query Pinecone for the most similar items based on the generated query embedding.
#     """
#     index = pineconeindex()
#     results = index.query(vector=query_embedding, top_k=5, include_metadata=True)

#     return results