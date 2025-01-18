from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
# from .pinecone_utils import search_similar_documents, generate_response_with_huggingface



@require_http_methods(["POST"])
def chatbot_view(request):
    pass
    # try:
    #     # Parse the request
    #     data = json.loads(request.body)
    #     user_query = data.get("query")
    #     if not user_query:
    #         return JsonResponse({"error": "Query is required."}, status=400)

    #     # Identify the intent from the user query
    #     intent = identify_intent(user_query)
        
    #     # Search for relevant documents
    #     search_results = search_similar_documents(user_query, top_k=3)
    #     if not search_results:
    #         return JsonResponse({"error": "No relevant courses found."}, status=404)

    #     # Process the response based on intent
    #     if intent == "price":
    #         response = "\n".join([f"The price of '{match['metadata'].get('title', 'Unknown Course')}' is ${match['metadata'].get('price', 'N/A')}." for match in search_results])
    #     elif intent == "owner":
    #         response = "\n".join([f"The owner/instructor of '{match['metadata'].get('title', 'Unknown Course')}' is {match['metadata'].get('instructor', 'Unknown')}." for match in search_results])
    #     elif intent == "duration":
    #         response = "\n".join([f"The duration of '{match['metadata'].get('title', 'Unknown Course')}' is {match['metadata'].get('duration', 'N/A')}." for match in search_results])
    #     elif intent == "description":
    #         response = "\n".join([f"The description of '{match['metadata'].get('title', 'Unknown Course')}' is: {match['metadata'].get('description', 'No description available.')}." for match in search_results])
    #     else:
    #         response = "I'm sorry, I didn't understand your question. Could you rephrase it?"

    #     return JsonResponse({"query": user_query, "response": response}, status=200)
    
    # except Exception as e:
    #     return JsonResponse({"error": str(e)}, status=500)
