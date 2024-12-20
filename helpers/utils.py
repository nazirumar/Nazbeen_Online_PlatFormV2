from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres.vectorstores import PGVector


def query_courses(question):
    database_url = "postgresql+psycopg2://postgres:z@localhost:5433/platform"
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vector_store = PGVector(
        connection=database_url,
        embeddings=embeddings,
        collection_name="course"
    )

    # Perform similarity search with the question
    return vector_store.similarity_search(question, k=5)

