from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
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
]