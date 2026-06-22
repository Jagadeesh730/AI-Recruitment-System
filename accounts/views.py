from django.shortcuts import render, redirect
from .models import Candidate
from .models import Candidate, Resume, Job, Interview, HR, Application
from .matcher import calculate_match_score
from .skill_extractor import extract_skills
from django.core.mail import send_mail
from django.conf import settings

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

            return redirect('/dashboard/')

    return render(
        request,
        'login.html'
    )
def candidate_dashboard(request):

    if 'candidate_id' not in request.session:
        return redirect('/login/')

    candidate = Candidate.objects.get(
        id=request.session['candidate_id']
    )

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

    resume_score = 0
    feedback = ""
    interview_questions = ""
    skill_gap = ""

    if resume:
        resume_score = resume.resume_score
        feedback = resume.feedback
        interview_questions = resume.interview_questions
        skill_gap = resume.skill_gap

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
            'resume_score': resume_score,
            'feedback': feedback,
            'interview_questions': interview_questions,
            'skill_gap': skill_gap,
            'applied_count': applied_count,
            'shortlisted_count': shortlisted_count,
            'interview_count': interview_count,
            'rejected_count': rejected_count,
            'interviews': interviews,
            'best_job': best_job
        }
    )
def upload_resume(request):

    if request.method == "POST":

        uploaded_file = request.FILES.get('resume')

        candidate = Candidate.objects.get(
            id=request.session['candidate_id']
        )

        resume = Resume.objects.create(
            candidate=candidate,
            resume_file=uploaded_file
        )

        skills = extract_skills(
            resume.resume_file.path
        )

        resume.extracted_skills = ",".join(skills)

        # AI Resume Score
        score = min(len(skills) * 10, 100)

        feedback = []

        if len(skills) < 5:
            feedback.append("Add more technical skills")

        if "python" not in [s.lower() for s in skills]:
            feedback.append("Consider learning Python")

        if "sql" not in [s.lower() for s in skills]:
            feedback.append("Add database skills like SQL")

        if len(skills) >= 8:
            feedback.append("Strong skill profile")

        resume.resume_score = score
        resume.feedback = "\n".join(feedback)

        # AI Interview Questions
        skills_lower = [skill.lower() for skill in skills]

        job_based_questions = ""

        if "machine learning" in skills_lower:
            job_based_questions += """
For ML Engineer:

1. What is supervised learning?
2. What is unsupervised learning?
3. What is overfitting?
4. What is underfitting?
5. Explain Random Forest.
"""

        if "python" in skills_lower:
            job_based_questions += """
For Python Developer:

1. What are Python decorators?
2. Explain list vs tuple.
3. What is exception handling?
4. What is list comprehension?
5. Explain OOP concepts.
"""

        if (
            "html" in skills_lower
            or "css" in skills_lower
            or "javascript" in skills_lower
            or "django" in skills_lower
        ):
            job_based_questions += """
For Full Stack Developer:

1. What is HTML5?
2. What is Flexbox?
3. What is JavaScript hoisting?
4. What is Django ORM?
5. Explain MTV architecture.
"""

        if "sql" in skills_lower or "mysql" in skills_lower:
            job_based_questions += """
For Database Developer:

1. What is normalization?
2. What is a primary key?
3. What is a foreign key?
4. Explain SQL JOINs.
5. Explain ACID properties.
"""

        resume.interview_questions = job_based_questions

        # AI Skill Gap Analysis
        skill_gap_list = []

        latest_job = Job.objects.last()

        if latest_job:

            job_skills = [
                skill.strip().lower()
                for skill in latest_job.required_skills.split(",")
            ]

            candidate_skills = [
                skill.strip().lower()
                for skill in skills
            ]

            for job_skill in job_skills:

                found = False

                for candidate_skill in candidate_skills:

                    if (
                        candidate_skill in job_skill
                        or job_skill in candidate_skill
                    ):
                        found = True
                        break

                if not found:
                    skill_gap_list.append(job_skill)

        resume.skill_gap = "\n".join(skill_gap_list)

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

    if not resume or not job:

        return render(
            request,
            'match_result.html',
            {
                'score': 0,
                'job': 'No job or resume found'
            }
        )

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
    total_applications = Application.objects.count()

    applied_count = Application.objects.filter(
    status='Applied'
    ).count()

    shortlisted_count = Application.objects.filter(
    status='Shortlisted'
    ).count()

    interview_scheduled_count = Application.objects.filter(
    status='Interview Scheduled'
    ).count()

    rejected_count = Application.objects.filter(
    status='Rejected'
    ).count()
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
            'total_applications': total_applications,
            'applied_count': applied_count,
            'shortlisted_count': shortlisted_count,
            'interview_scheduled_count': interview_scheduled_count,
            'rejected_count': rejected_count,
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

        candidate_obj = Candidate.objects.filter(
            name__iexact=candidate.strip()
        ).first()

        if candidate_obj:

            send_mail(
                'Interview Scheduled',
                f'''
Hello {candidate},

Your interview has been scheduled.

Job Title: {job_title}

Date: {date}

Time: {time}

Best of luck!

AI Recruitment Team
                ''',
                settings.EMAIL_HOST_USER,
                [candidate_obj.email],
                fail_silently=False,
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
            'job': job,
            'already_applied': already_applied
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
def job_recommendations(request):

    if 'hr_id' not in request.session:
        return redirect('/hr-login/')

    jobs = Job.objects.all()

    recommendations = {}

    for job in jobs:

        candidate_list = []

        resumes = Resume.objects.all()

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

            candidate_list.append({
                'name': resume.candidate.name,
                'score': score
            })

        candidate_list = sorted(
            candidate_list,
            key=lambda x: x['score'],
            reverse=True
        )

        recommendations[job.title] = candidate_list[:5]

    return render(
        request,
        'job_recommendations.html',
        {
            'recommendations': recommendations
        }
    )
