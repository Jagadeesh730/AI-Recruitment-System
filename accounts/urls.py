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
]