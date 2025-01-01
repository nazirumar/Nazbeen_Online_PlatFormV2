import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .pinecone_utils import get_similar_documents  # Helper for Pinecone queries
from decouple import config

# Hugging Face API setup
HF_API_URL = "https://api-inference.huggingface.co/models/gpt2"  # Switch to a stronger model if available
HF_API_KEY = config('HF_API_KEY')

# Function to call the Hugging Face API
def generate_response_with_hf(query, context):
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
    }
    # Payload combining query and context
    payload = {
        "inputs": f"""
        User query: {query}
        
        Relevant Information:
        {context}
        
        Response:
        """,
        "parameters": {
            "max_length": 300,  # Limit response length
            "temperature": 0.7,  # Balance between creativity and precision
            "top_p": 0.5,       # Sampling to improve response diversity
        }
    }
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except requests.RequestException as e:
        return f"Error generating response: {e}"

@csrf_exempt
def chat_with_bot(request):
    if request.method == "POST":
        try:
            # Parse the user query
            body = json.loads(request.body)
            query = body.get("query", "").strip()
            if not query:
                return JsonResponse({"error": "No query provided."}, status=400)

            # Step 1: Retrieve relevant documents from Pinecone
            results = get_similar_documents(query, top_k=5)  # Limit to top-5 documents

            if not results:
                return JsonResponse({"response": "Sorry, I couldn't find relevant information to assist you."}, status=200)

            # Step 2: Build a concise and meaningful context
            context_parts = []
            for res in results:
                metadata = res.get("metadata", {})
                title = metadata.get("title", "")
                description = metadata.get("description", "")
                context_parts.append(f"Title: {title}\nDescription: {description}")
            context = "\n".join(context_parts[:3])  # Limit to the top-3 results

            # Step 3: Generate a response using the Hugging Face API
            response = generate_response_with_hf(query, context)

            return JsonResponse({"response": response}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format."}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method."}, status=405)
