# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from courses.models import Course
# from .pinecone_utils import generate_embedding, get_or_create_pinecone_index
# from pinecone import Index
# from django.conf import settings

# # Initialize Pinecone index
# INDEX_NAME = "course-index"
# index = get_or_create_pinecone_index()

# @receiver(post_save, sender=Course)
# def store_embeddings(sender, instance, **kwargs):
#     """
#     Store or update the embedding in Pinecone when a Course is saved.
#     """
#     try:
#         # Generate the embedding for the course description
#         embedding = generate_embedding(instance.description)

#         # Prepare metadata
#         metadata = {
#             "title": instance.title,
#             "description": instance.description,
#             "price": str(instance.price),  # Convert Decimal to string
#             "instructor": instance.instructor.user.username if instance.instructor else "Unknown Instructor",
#             "owner": instance.owner.username,
#             "subject": instance.subject.title if instance.subject else "General",
#             "students": instance.students.count(),
#             "access": instance.access,
#             "is_free": instance.is_free,
#         }

#         # Upsert into Pinecone
#         index.upsert(vectors=[(str(instance.id), embedding, metadata)])
#         print(f"Embedding stored for course: {instance.title}")

#     except Exception as e:
#         print(f"Error storing embedding for course {instance.title}: {e}")


# @receiver(post_delete, sender=Course)
# def delete_embeddings(sender, instance, **kwargs):
#     """
#     Delete the embedding from Pinecone when a Course is deleted.
#     """
#     try:
#         # Delete from Pinecone
#         index.delete(ids=[str(instance.id)])
#         print(f"Embedding deleted for course: {instance.title}")

#     except Exception as e:
#         print(f"Error deleting embedding for course {instance.title}: {e}")
