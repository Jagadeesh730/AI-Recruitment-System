from django.shortcuts import render
from .models import Candidate
from .models import Candidate, Resume, Job
from .matcher import calculate_match_score
def home(request):
    return render(request, 'home.html')

def register(request):

    message = ""

    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        skills = request.POST.get('skills')

        Candidate.objects.create(
            name=name,
            email=email,
            password=password,
            skills=skills
        )

        message = "Registration Successful!"

    return render(
        request,
        'register.html',
        {'message': message}
    )
def login(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        candidate = Candidate.objects.filter(
            email=email,
            password=password
        ).first()

        if candidate:
            return render(request, 'dashboard.html')

    return render(request, 'login.html')
def upload_resume(request):

    if request.method == "POST":

        uploaded_file = request.FILES.get('resume')

        candidate = Candidate.objects.first()

        Resume.objects.create(
            candidate=candidate,
            resume_file=uploaded_file
        )

    return render(
        request,
        'upload_resume.html'
    )
def post_job(request):

    if request.method == "POST":

        title = request.POST.get('title')
        description = request.POST.get('description')
        skills = request.POST.get('skills')

        Job.objects.create(
            title=title,
            description=description,
            required_skills=skills
        )

    return render(request, 'job_post.html')
def match_candidate(request):

    candidate_skills = [
        "python",
        "java",
        "sql",
        "machine learning"
    ]

    job_skills = [
        "python",
        "django",
        "sql",
        "html"
    ]

    score = calculate_match_score(
        candidate_skills,
        job_skills
    )

    return render(
        request,
        'match_result.html',
        {'score': score}
    )