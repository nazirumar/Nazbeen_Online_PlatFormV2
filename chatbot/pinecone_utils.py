# from pinecone import Pinecone as PineconeClient, ServerlessSpec
# from decouple import config
# from langchain_huggingface import HuggingFaceEmbeddings
# import requests

# embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
# # Initialize Pinecone client
# pinecone_client = PineconeClient(api_key=config("PINECONE_API_KEY"))


# # Pinecone index name


# # Function to get or create a Pinecone index
# def get_or_create_pinecone_index():
#     try:

#         INDEX_NAME = "course-index"
#         # Connect to the existing index
#         index =pinecone_client.Index(INDEX_NAME)
#     except Exception as e:
#         raise RuntimeError(f"Failed to connect to or create Pinecone index '{INDEX_NAME}': {e}")
#     return index

# # Function to generate query embeddings using Groq
# def generate_embedding(query):
#     try:
#         # Use Groq API to generate embeddings
#         embedding = embeddings.embed_query(query)
#         return embedding
#     except Exception as e:
#         raise RuntimeError(f"Failed to generate embeddings for query '{query}': {e}")

# # Function to add documents to Pinecone
# def add_document_to_pinecone(document_id, text, metadata=None):
#     try:
#         index = get_or_create_pinecone_index()
#         embedding = generate_embedding(text)
#         print(embedding)
#         # Upsert the document with its embedding and optional metadata
#         index.upsert([(str(document_id), embedding, metadata or {})])
#     except Exception as e:
#         raise RuntimeError(f"Failed to add document '{document_id}' to Pinecone: {e}")

# # Function to search for similar documents in Pinecone
# def search_similar_documents(query, top_k=3):
#     try:
#         query_embedding = generate_embedding(query)
#         index = get_or_create_pinecone_index()

#         # Perform the search in Pinecone with additional fields in metadata
#         response = index.query(vector=query_embedding, top_k=top_k, include_metadata=True)
        
#         serialized_matches = [
#             {
#                 "id": match.id,
#                 "score": match.score,
#                 "metadata": match.metadata,
#             }
#             for match in response["matches"]
#         ]
#         return serialized_matches
#     except Exception as e:
#         raise RuntimeError(f"Failed to search for similar documents: {e}")

# # Function to generate a response using Groq AI
# HUGGINGFACE_API_TOKEN = config("HUGGINGFACE_API_TOKEN")
# def generate_response_with_huggingface(query, context):
#     try:
#         # Provide default context if none is found
#         context = context or "No relevant information found in the knowledge base."

#         prompt = (
#             f"User query: {query}\n\n"
#             f"Relevant Information:\n{context}\n\n"
#             "Provide a clear and concise explanation for the user's query:"
#         )

#         api_url = "https://api-inference.huggingface.co/models/bigscience/bloom"
#         headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
#         payload = {
#             "inputs": prompt,
#             "parameters": {
#                 "max_new_tokens": 150,
#                 "temperature": 0.5,  # Adjusted for more focused output
#             },
#         }

#         response = requests.post(api_url, headers=headers, json=payload)
#         response.raise_for_status()

#         response_data = response.json()
#         if isinstance(response_data, list) and "generated_text" in response_data[0]:
#             generated_text = response_data[0]["generated_text"]
#             return generated_text.strip()
#         else:
#             raise RuntimeError("Unexpected response structure from Hugging Face API")

#     except Exception as e:
#         raise RuntimeError(f"Failed to generate response with Hugging Face API for query '{query}': {e}")
