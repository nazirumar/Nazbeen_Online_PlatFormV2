from pinecone import Pinecone as PineconeClient
from sentence_transformers import SentenceTransformer
from decouple import config

# Initialize Pinecone client
pinecone_client = PineconeClient(api_key=config('PINECONE_API_KEY'))


# Pinecone index name
INDEX_NAME = "course-index"

# Initialize Sentence-Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Function to get Pinecone index
def pineconeindex():
    try:
        # Connect to Pinecone index
        index = pinecone_client.Index(INDEX_NAME)
    except Exception as e:
        raise RuntimeError(f"Failed to connect to Pinecone index '{INDEX_NAME}': {e}")
    return index

# Preprocess the query (optional: for case-insensitive comparison)
def preprocess_query(query):
    return query.strip().lower()

# Function to generate query embedding from the sentence transformer model
def generate_query_embedding(query):
    return model.encode(query).tolist()

# Function to search for similar documents in Pinecone
def get_similar_documents(query, top_k=3):
    # Preprocess the query and generate embedding
    query_embedding = generate_query_embedding(query)

    # Query Pinecone for the top_k most similar documents
    index = pineconeindex()
    response = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)

    return response['matches']  # Returning the results (matches)
