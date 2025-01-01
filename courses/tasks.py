# from celery import shared_task
# from courses.models import Course
# from helpers.embeddings import generate_query_embedding, pineconeindex


# @shared_task
# def create_course_embedding_task(course_id):
#     """
#     Celery task to generate and store embedding for a Course.
#     """
#     try:
#         # Get the course instance
#         course = Course.objects.get(id=course_id)
#         description = course.description
#         title = course.title
#         price = course.price
#         likes = course.likes
#         instructor_name = course.instructor.user if course.instructor else "Unknown"

#         # Generate embedding for the course description
#         course_embedding = generate_query_embedding(description)

#         # Prepare metadata with new fields
#         metadata = {
#             "title": title,
#             "description": description,
#             "price": price,
#             "likes": likes,
#             "instructor": instructor_name
#         }

#         # Store the embedding and metadata in Pinecone
#         index = pineconeindex()
#         index.upsert([(str(course.id), course_embedding, metadata)])

#         print(f"Embedding for course '{course.title}' created and stored successfully.")
    
#     except Exception as e:
#         print(f"Error creating embedding for course ID {course_id}: {e}")