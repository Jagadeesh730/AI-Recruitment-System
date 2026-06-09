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

    extracted_skills = models.TextField(
        blank=True
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )
class Job(models.Model):

    title = models.CharField(max_length=100)

    description = models.TextField()

    required_skills = models.TextField()

    def __str__(self):
        return self.title
class Interview(models.Model):

    candidate_name = models.CharField(
        max_length=100
    )

    interview_date = models.DateField()

    interview_time = models.TimeField()

    def __str__(self):
        return self.candidate_name