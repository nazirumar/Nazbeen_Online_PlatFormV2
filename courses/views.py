from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.conf import settings
from django.db.models import Q
from chatbot.utils import SQLChatBot
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
import helpers
from django.contrib import messages
from decouple import config
import helpers.utils
from .models import Category, CourseProgress, Lesson, Likes, PublishStatus, Student, Subject, Course, Module, Enrollment
from django.contrib.auth.decorators import login_required
from courses import services 


def search_api(request):
    query = request.GET.get('q', '').strip()
    results = {
        'categories': [],
        'subjects': [],
        'lessons': [],
        'courses': [],
    }

    if query:
        # Perform the search
        results['categories'] = list(Category.objects.filter(title__icontains=query).values('id', 'title')[:10])
        results['subjects'] = list(Subject.objects.filter(title__icontains=query).values('id', 'title')[:10])
        results['lessons'] = list(Lesson.objects.filter(title__icontains=query).values('id', 'title')[:10])
        results['courses'] = list(Course.objects.filter(title__icontains=query).values('id', 'title')[:10])
    return JsonResponse(results)



def category_view(request, slug):
    category = get_object_or_404(Category, public_id=slug)
    subjects = category.subjects.prefetch_related('subject_courses')

    # bot = SQLChatBot(
    #     db_url=config("DATABASE_URL"),
    #     groq_model="llama3-8b-8192",
    #     groq_api_key=config("GROQ_API_KEY")
    # )

    # # Run a query through the workflow
    # response = bot.run_query("please how many users we have in the database?")

    # print(response["messages"][-1].tool_calls[0]["args"]["final_answer"])
    courses = {
        subject: subject.subject_courses.filter(status=PublishStatus.PUBLISHED)
        for subject in subjects
    }
    context = {
        'courses': courses
    }
    return render(request, 'category/list.html', context)

def category_detail_view(request, slug):
   lesson = get_object_or_404(Course, public_id=slug)
   videos = lesson.lessons_video.all()
   return render(request, 'category/detail.html', {'lesson':lesson, 'videos':videos})


# Like function
@login_required
def like_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    liked_count = course.liked_by.count()

    # Check if the user already liked the course
    like, created = Likes.objects.get_or_create(user=request.user, course=course)

    if created:
        # If the like was just created
        liked_count += 1
        status = 'liked'
    else:
        # If the user is already liked the course, we can remove the like
        like.delete()  # This will remove the existing like
        liked_count -= 1
        status = 'unliked'

    return JsonResponse({'status': status, 'liked_count': liked_count})



def complete_lesson(request, course_id, lesson_id):
    course = get_object_or_404(Course, id=course_id)
    lesson = get_object_or_404(Lesson, id=lesson_id, course=course)
    progress, created = CourseProgress.objects.get_or_create(user=request.user, course=course)

    if lesson not in progress.completed_lessons.all():
        progress.completed_lessons.add(lesson)
        # Check if course is completed
        if progress.completed_lessons.count() == course.total_lessons:
            progress.completed_on = timezone.now()
        progress.save()

    return JsonResponse({'progress': progress.progress_percentage})


# View to display details of a course videos title in the lesson
login_required
def course_detail_view(request, course_id):
    course = services.get_course_detail(course_id=course_id)

    progress = CourseProgress.objects.filter(user=request.user, course=course.id).first()
    
    modules = course.modules.all()
    # Fetch videos and the public ID of the last lesson processed
    all_lessons, last_lesson_public_id = services.get_course_lesson_videos(modules=modules)
    if request.user.is_authenticated:
        student, created = Student.objects.get_or_create(user=request.user)
        is_enrolled = Enrollment.objects.filter(student=student, course=course).exists()
    else:
        is_enrolled = False
    
    context = {
        'progress': progress,
        'course': course,
        'lessons':all_lessons,
        'lesson_public_id': last_lesson_public_id,
        'is_enrolled':is_enrolled,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,

    }
    return render(request, 'courses/course_detail.html', context)


def get_content(request, course_id):
    # Fetch the full course description
    course = get_object_or_404(Course, id=course_id)
    return HttpResponse(course.description)


from cloudinary.utils import cloudinary_url

def generate_private_video_url(public_id):
    url, options = cloudinary_url(
        public_id,
        resource_type="video",
        private=True,  # Ensure the video is marked as private
        secure=True    # Use HTTPS
    )
    return url


login_required
def lesson_detail_view(request, course_id=None, lesson_id=None):
    # Retrieve the course, modules, lessons, and videos
    course_modules_lessons_video = services.get_lessons_video_watch(course_public_id=course_id)

    # Check if data exists
    if not course_modules_lessons_video or not course_modules_lessons_video[3]:
        raise Http404("Lessons or videos not found")

    # Extract course, modules, lessons, and videos
    course = course_modules_lessons_video[0]
    modules = course_modules_lessons_video[1]
    lessons = course_modules_lessons_video[2]
    videos = course_modules_lessons_video[3]

    # Prepare the first video for embedding
    initial_video = videos[0] if videos else None
    video_embed_html = helpers.get_cloudinary_video_object(
        initial_video,
        field_name='video',
        as_html=True,
        width=1250,
    ) if initial_video else ""
   
    context = {
        'course': course,
        'modules': modules,
        'lessons': lessons,
        'videos': videos,
        'video_embed_html': video_embed_html,
    }
    return render(request, 'lesson/lessons_videos.html', context)






@login_required
def student_enroll_course(request, course_id):
    # Call the course enrollment service
    course, message = services.course_enrollment(course_id, request.user)
    
    # Add a success message to notify the user of their enrollment status
    messages.success(request, message)
    
    # Redirect to the course detail page after enrollment
    return redirect('course_detail', course_id=course.public_id)


# View to display topics under a module
def module_detail(request, public_id):
    module = get_object_or_404(Module, public_id=public_id)
    # topics = module.le.all()
    return render(request, 'elearning/module_detail.html', {'module': module, 'topics': 'topics'})




def module_courses(request, module_id):
    module = Module.objects.get(id=module_id)
    courses = module.courses.all()  # Assuming 'courses' is the related name in the Module model
    courses_data = [{'id': course.id, 'title': course.title} for course in courses]
    return JsonResponse({'courses': courses_data})
# Enroll a student in a course



