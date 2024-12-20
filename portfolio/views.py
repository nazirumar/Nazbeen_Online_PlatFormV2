from django.shortcuts import get_object_or_404, render

from courses import services 


from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    courses = services.get_publish_courses().order_by('-created_at')
    paginator = Paginator(courses, 10)  # Show 10 courses per page
    page_number = request.GET.get('page')

    # Ensure page_number is valid (greater than or equal to 1)
    try:
        page_number = int(page_number) if page_number else 1
        if page_number < 1:
            page_number = 1  # Reset to 1 if page number is less than 1
    except (ValueError, TypeError):
        page_number = 1  # Default to the first page if invalid

    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results
        page_obj = paginator.page(paginator.num_pages)

    courses_likes = []
    for course in page_obj:
        liked_count = course.liked_by.count()
        courses_likes.append((course, liked_count))
        
    return render(request, 'index.html', {'courses_likes': courses_likes, 'page_obj': page_obj})
def about(request):
    return render(request, 'pages/about.html')