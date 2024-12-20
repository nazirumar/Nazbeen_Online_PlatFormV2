from django.core.management.base import BaseCommand
from commando.management.commands.utils.rag import initialize_vector_store

class Command(BaseCommand):
    help = "Initialize the vector store for the chatbot."

    def handle(self, *args, **kwargs):
        vector_store = initialize_vector_store()
        if vector_store:
            print("Vector store initialized successfully.")
        else:
            print("Vector store initialization skipped.")
