from langchain.chains import RetrievalQA
from langchain_community.llms.huggingface_pipeline import HuggingFacePipeline
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from transformers import pipeline
from courses.models import Course

def load_llm():
    """Load a pre-trained LLM for generation."""
    llm_pipeline = pipeline("text-generation", model="facebook/opt-1.3b", max_new_tokens=200)
    llm = HuggingFacePipeline(pipeline=llm_pipeline)
    return llm

def initialize_vector_store():
    """Initialize the FAISS vector store with course data."""
    courses = Course.objects.all()
    
    if not courses.exists():
        print("No course data available. Skipping vector store initialization.")
        return None  # Skip initialization

    documents = [
        {
            "text": f"Course: {course.title}\nDescription: {course.description}\nInstructor: {course.instructor}\nSubject: {course.subject.name if course.subject else 'N/A'}",
            "metadata": {
                "id": course.id,
                "price": course.price,
                "status": course.status,
            },
        }
        for course in courses
    ]

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    texts = [doc["text"] for doc in documents]
    metadata = [doc["metadata"] for doc in documents]

    if not texts:  # Ensure texts are not empty
        print("No text data to initialize vector store.")
        return None

    vector_store = FAISS.from_texts(texts, embeddings, metadatas=metadata)
    return vector_store


def generate_response(user_query, vector_store):
    """Generate a response to a user's query using RAG."""
    retriever = vector_store.as_retriever(search_kwargs={"k": 2})  # Retrieve top 2 results
    qa_chain = RetrievalQA.from_chain_type(
        llm=load_llm(),
        retriever=retriever,
        chain_type="stuff",
    )
    response = qa_chain.run(user_query)
    return response
