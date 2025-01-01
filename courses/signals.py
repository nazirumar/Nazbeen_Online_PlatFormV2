# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from courses.models import Course
# from helpers.embeddings import generate_query_embedding, pineconeindex  # Replace `myapp` with your app name

# @receiver(post_save, sender=Course)
# def create_course_embedding(sender, instance, created, **kwargs):
#     """
#     Signal to generate and store embedding for a Course when it is created.
#     """
#     if created:
#         description = instance.description
#         title = instance.title
#         price = instance.price
#         likes = instance.likes


#         try:
#             # Generate embedding for the course description
#             course_embedding = generate_query_embedding(description)
#             metadata = {
#                 "title": title,
#                 "description": description,
#                 "price": price,
#                 "likes": likes,
#             }

#             # Store the embedding in Pinecone
#             index = pineconeindex()
#             index.upsert([(str(instance.id), course_embedding, metadata)])

#             print(f"Embedding for course '{instance.title}' created and stored successfully.")

#         except Exception as e:
#             # Handle errors without interrupting the save process
#             print(f"Error creating embedding for course '{instance.title}': {e}")