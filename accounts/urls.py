from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.candidate_dashboard, name='dashboard'),
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('post-job/', views.post_job, name='post_job'),
    path(
    'match/',
    views.match_candidate,
    name='match_candidate'
),
path(
    'ranking/',
    views.candidate_ranking,
    name='candidate_ranking'
),
path(
    'hr-dashboard/',
    views.hr_dashboard,
    name='hr_dashboard'
),
path(
    'schedule-interview/',
    views.schedule_interview,
    name='schedule_interview'
),
path(
    'hr-login/',
    views.hr_login,
    name='hr_login'
),
path(
    'jobs/',
    views.jobs,
    name='jobs'
),
path(
    'apply-job/<int:job_id>/',
    views.apply_job,
    name='apply_job'
),
path(
    'applications/',
    views.view_applications,
    name='applications'
),
path(
    'logout/',
    views.logout_view,
    name='logout'
),
path(
    'candidate-details/<str:candidate_name>/',
    views.candidate_details,
    name='candidate_details'
),
path(
    'shortlist/<str:candidate_name>/',
    views.shortlist_candidate,
    name='shortlist_candidate'
),
path(
    'application-summary/',
    views.application_summary,
    name='application_summary'
),
path(
    'job-recommendations/',
    views.job_recommendations,
    name='job_recommendations'
),
]