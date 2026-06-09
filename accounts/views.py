from django.shortcuts import render
from .models import Candidate
from .models import Candidate, Resume, Job, Interview
from .matcher import calculate_match_score
from .skill_extractor import extract_skills
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

        resume = Resume.objects.create(
            candidate=candidate,
            resume_file=uploaded_file
        )

        skills = extract_skills(
            resume.resume_file.path
        )

        resume.extracted_skills = ",".join(skills)

        resume.save()

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

    resume = Resume.objects.last()

    job = Job.objects.last()

    candidate_skills = (
        resume.extracted_skills
        .split(",")
    )

    job_skills = [
        skill.strip()
        for skill in
        job.required_skills.split(",")
    ]

    score = calculate_match_score(
        candidate_skills,
        job_skills
    )

    return render(
        request,
        'match_result.html',
        {
            'score': score,
            'job': job.title
        }
    )
def candidate_ranking(request):

    rankings = []

    job = Job.objects.last()

    resumes = Resume.objects.all()

    for resume in resumes:

        candidate_skills = (
            resume.extracted_skills
            .split(",")
        )

        job_skills = [
            skill.strip()
            for skill in
            job.required_skills.split(",")
        ]

        score = calculate_match_score(
            candidate_skills,
            job_skills
        )

        rankings.append({
            'name': resume.candidate.name,
            'score': score
        })

    rankings = sorted(
        rankings,
        key=lambda x: x['score'],
        reverse=True
    )

    return render(
        request,
        'ranking.html',
        {'rankings': rankings}
    )
def hr_dashboard(request):

    rankings = []

    job = Job.objects.last()

    resumes = Resume.objects.all()

    for resume in resumes:

        candidate_skills = (
            resume.extracted_skills
            .split(",")
        )

        job_skills = [
            skill.strip()
            for skill in
            job.required_skills.split(",")
        ]

        score = calculate_match_score(
            candidate_skills,
            job_skills
        )

        rankings.append({
            'name': resume.candidate.name,
            'score': score
        })

    rankings = sorted(
        rankings,
        key=lambda x: x['score'],
        reverse=True
    )

    top_candidate = None

    if rankings:
        top_candidate = rankings[0]

    return render(
        request,
        'hr_dashboard.html',
        {
            'top_candidate': top_candidate
        }
    )
def schedule_interview(request):

    message = ""

    if request.method == "POST":

        candidate = request.POST.get('candidate')
        date = request.POST.get('date')
        time = request.POST.get('time')

        Interview.objects.create(
            candidate_name=candidate,
            interview_date=date,
            interview_time=time
        )

        message = "Interview Scheduled Successfully!"

    return render(
        request,
        'schedule_interview.html',
        {'message': message}
    )