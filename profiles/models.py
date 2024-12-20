from django.db import models
from django.conf import settings
from django.utils.text import slugify
from io import BytesIO
from django.template.loader import get_template
from django.core.files import File
from xhtml2pdf import pisa

from courses.models import Course, Enrollment, Student
from instructors.models import Organization

# Create your models here.


class ProfileUser(models.Model):
    slug = models.SlugField(max_length=200, unique=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    bio  = models.TextField(max_length=2000, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile/img', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    courses_enrollments = models.ManyToManyField(Enrollment, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.user.username)
        super().save(*args, **kwargs)

        
        
    def __str__(self):
        return str(self.full_name)



from weasyprint import HTML
from django.conf import settings
from django.core.files import File
from django.template.loader import render_to_string
from io import BytesIO
import logging

logger = logging.getLogger(__name__)

def generate_certificate_pdf(certificate):
    """
    Generate a PDF for the given certificate and save it to the model.
    """
    template_path = 'profile/certificate_template.html'
    
    # Fetch organization or fallback to default values
    try:
        organization = Organization.objects.latest('id')
    except Organization.DoesNotExist:
        organization = None

    context = {
        'certificate': certificate,
        'student': certificate.student,
        'course': certificate.course,
        'organization': organization,
    }
    
    try:
        # Render the HTML template with context
        html_string = render_to_string(template_path, context)

        # Use STATIC_URL for development or STATIC_ROOT for production
        base_url = settings.STATIC_URL if settings.DEBUG else settings.STATIC_ROOT

        # Generate the PDF
        pdf_buffer = BytesIO()
        HTML(string=html_string, base_url=base_url).write_pdf(pdf_buffer)

        # Save the PDF to the model
        pdf_buffer.seek(0)
        certificate.certificate_file.save(
            f"certificate_{certificate.student.user.username}.pdf", File(pdf_buffer)
        )
        pdf_buffer.close()

        logger.info(f"PDF generated successfully for {certificate.student.user.username}")
        return True
    except Exception as e:
        logger.exception(f"Error generating certificate PDF: {e}")
        return False