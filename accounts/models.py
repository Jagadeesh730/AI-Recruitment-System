from django.db import models

class Candidate(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    skills = models.TextField()

    def __str__(self):
        return self.name
class Resume(models.Model):
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE
    )

    resume_file = models.FileField(
        upload_to='resumes/'
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.candidate.name
class Job(models.Model):

    title = models.CharField(max_length=100)

    description = models.TextField()

    required_skills = models.TextField()

    def __str__(self):
        return self.title