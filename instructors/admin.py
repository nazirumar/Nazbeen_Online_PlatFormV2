from django.contrib import admin

from instructors.models import Certificate, Instructor, Organization

# Register your models here.

from django.contrib import admin
from .models import Instructor

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio']

admin.site.register(Organization)




@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('course', 'student',)

