from django.contrib import admin
from .models import Jobseeker,Employer,Job,Application
# Register your models here.
admin.site.register(Jobseeker)
admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(Application)