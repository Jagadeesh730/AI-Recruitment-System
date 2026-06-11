from django.shortcuts import render, redirect
from .models import Candidate
from .models import Candidate, Resume, Job, Interview, HR, Application
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

            request.session['candidate_id'] = candidate.id

            applications = Application.objects.filter(
                candidate_name=candidate.name
            )
            interviews = Interview.objects.filter(
                candidate_name__icontains=candidate.name
            )
            applied_count = applications.filter(
                status='Applied'
            ).count()

            shortlisted_count = applications.filter(
                status='Shortlisted'
            ).count()

            interview_count = applications.filter(
                 status='Interview Scheduled'
            ).count()

            rejected_count = applications.filter(
                 status='Rejected'
            ).count()

            resume = Resume.objects.filter(
                candidate=candidate
            ).last()

            match_scores = []

            if resume:

                jobs = Job.objects.all()

                for job in jobs:

                    candidate_skills = resume.extracted_skills.split(",")

                    job_skills = [
                        skill.strip()
                        for skill in job.required_skills.split(",")
                    ]

                    score = calculate_match_score(
                        candidate_skills,
                        job_skills
                    )

                    match_scores.append({
                        'job': job.title,
                        'score': score
                    })

            total_applications = applications.count()

            highest_score = 0

            for item in match_scores:

                if item['score'] > highest_score:

                    highest_score = item['score']

            resume_uploaded = "Yes" if resume else "No"
            best_job = None

            if match_scores:

                best_job = max(
                     match_scores,
                     key=lambda x: x['score']
            )

            return render(
                request,
                'dashboard.html',
                {
                    'candidate': candidate,
                    'applications': applications,
                    'total_applications': total_applications,
                    'match_scores': match_scores,
                    'highest_score': highest_score,
                    'resume_uploaded': resume_uploaded,
                    'applied_count': applied_count,
                    'shortlisted_count': shortlisted_count,
                    'interview_count': interview_count,
                    'rejected_count': rejected_count,
                    'interviews': interviews,
                    'best_job': best_job
                }
            )

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
    if 'hr_id' not in request.session:
        return redirect('/hr-login/')

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
    if 'hr_id' not in request.session:
        return redirect('/hr-login/')

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

    if 'hr_id' not in request.session:
        return redirect('/hr-login/')

    rankings = []
    search_query = request.GET.get('search')

    search_results = []

    job = Job.objects.last()
    resumes = Resume.objects.all()

    if job:

        for resume in resumes:

            candidate_skills = resume.extracted_skills.split(",")

            job_skills = [
                skill.strip()
                for skill in job.required_skills.split(",")
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

    total_candidates = Candidate.objects.count()
    total_jobs = Job.objects.count()
    total_interviews = Interview.objects.count()
    if search_query:

     search_results = [

        candidate

        for candidate in rankings

        if search_query.lower()
        in candidate['name'].lower()

    ]

    return render(
        request,
        'hr_dashboard.html',
        {
            'top_candidate': top_candidate,
            'total_candidates': total_candidates,
            'rankings': rankings,
            'search_results': search_results,
            'total_jobs': total_jobs,
            'total_interviews': total_interviews
        }
    )
def schedule_interview(request):

    if 'hr_id' not in request.session:
        return redirect('/hr-login/')

    message = ""

    if request.method == "POST":

        candidate = request.POST.get('candidate')

        job_title = request.POST.get('job_title')

        date = request.POST.get('date')

        time = request.POST.get('time')

        Interview.objects.create(
            candidate_name=candidate,
            job_title=job_title,
            interview_date=date,
            interview_time=time
        )

        Application.objects.filter(
            candidate_name__iexact=candidate.strip(),
            job_title__iexact=job_title.strip()
        ).update(
            status='Interview Scheduled'
        )

        message = "Interview Scheduled Successfully!"

    return render(
        request,
        'schedule_interview.html',
        {
            'message': message
        }
    )
def hr_login(request):

    message = ""

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:

            hr = HR.objects.get(
                email=email,
                password=password
            )

            request.session['hr_id'] = hr.id

            return redirect('/hr-dashboard/')

        except:

            message = "Invalid Credentials"

    return render(
        request,
        'hr_login.html',
        {'message': message}
    )
def jobs(request):

    jobs = Job.objects.all()

    return render(
        request,
        'jobs.html',
        {'jobs': jobs}
    )
def apply_job(request, job_id):

    if 'candidate_id' not in request.session:
        return redirect('/login/')

    candidate = Candidate.objects.get(
        id=request.session['candidate_id']
    )

    job = Job.objects.get(id=job_id)

    already_applied = Application.objects.filter(
        candidate_name=candidate.name,
        job_title=job.title
    ).exists()

    if not already_applied:

        Application.objects.create(
            candidate_name=candidate.name,
            job_title=job.title
        )

        return render(
            request,
            'application_success.html',
            {
                'job': job
            }
        )

    return render(
        request,
        'application_success.html',
        {
            'job': job
        }
    )
def view_applications(request):
    if 'hr_id' not in request.session:
         return redirect('/hr-login/')

    applications = Application.objects.all()

    return render(
        request,
        'applications.html',
        {
            'applications': applications
        }
    )
def logout_view(request):

    return redirect('/')
def candidate_details(request, candidate_name):

    candidate = Candidate.objects.get(
        name=candidate_name
    )

    applications = Application.objects.filter(
        candidate_name=candidate_name
    )

    return render(
        request,
        'candidate_details.html',
        {
            'candidate': candidate,
            'applications': applications
        }
    )
def shortlist_candidate(request, candidate_name):

    Application.objects.filter(
        candidate_name=candidate_name
    ).update(
        status='Shortlisted'
    )

    return redirect('/hr-dashboard/')
def application_summary(request):

    if 'candidate_id' not in request.session:

        return redirect('/login/')

    candidate = Candidate.objects.get(
        id=request.session['candidate_id']
    )

    applications = Application.objects.filter(
        candidate_name=candidate.name
    )

    total_applications = applications.count()

    shortlisted_count = applications.filter(
        status='Shortlisted'
    ).count()

    interview_count = applications.filter(
        status='Interview Scheduled'
    ).count()

    rejected_count = applications.filter(
        status='Rejected'
    ).count()

    return render(
        request,
        'application_summary.html',
        {
            'total_applications': total_applications,
            'shortlisted_count': shortlisted_count,
            'interview_count': interview_count,
            'rejected_count': rejected_count
        }
    )