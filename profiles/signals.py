from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
 # Ensure you import the utility function
import logging
from courses.models import Enrollment, EnrollmentStatus
from instructors.models import Certificate
from .models import ProfileUser, generate_certificate_pdf

User = get_user_model()


@receiver(post_save, sender=User)
def create_staff_for_new_user(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(user=instance)





logger = logging.getLogger(__name__)
@receiver(post_save, sender=Enrollment)
def create_certificate(sender, instance, **kwargs):
    """
    Generate a certificate PDF when an Enrollment is marked as COMPLETED.
    """
    if instance.status == EnrollmentStatus.COMPLETED:
        try:
            with transaction.atomic():
                certificate, created = Certificate.objects.get_or_create(
                    student=instance.student,
                    course=instance.course
                )
                if created:
                    pdf_generated = generate_certificate_pdf(certificate)
                    if not pdf_generated:
                        logger.error(f"Failed to generate certificate for {certificate.student.user.username}")
        except Exception as e:
            logger.exception(f"Error generating certificate for Enrollment ID {instance.id}: {e}")