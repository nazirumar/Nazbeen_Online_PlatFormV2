from django.db.models.signals import post_save
from django.dispatch import receiver

from helpers.embeddings import store_embeddings
from .models import Course, LessonVideo
# from .tasks import generate_transcript_task

# @receiver(post_save, sender=LessonVideo)
# def video_uploaded_handler(sender, instance, created, **kwargs):
#     if created and instance.video:
#         # Trigger the task only if the video file exists and is uploaded
#         generate_transcript_task.delay(instance.id)



@receiver(post_save, sender=Course)
def update_course_embedding(sender, instance, created, **kwargs):
    if created:
        store_embeddings()

