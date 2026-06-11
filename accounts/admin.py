from django.contrib import admin
from .models import Candidate, Resume, Job, Interview, HR, Application

admin.site.register(Candidate)
admin.site.register(Resume)
admin.site.register(Job)
admin.site.register(Interview)
admin.site.register(HR)
admin.site.register(Application)