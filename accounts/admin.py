from django.contrib import admin
from .models import Candidate, Resume, Job

admin.site.register(Candidate)
admin.site.register(Resume)
admin.site.register(Job)