from django.db import models
from django.contrib.auth.models import User
from django.db.models.base import Model
import os

# Create your models here.
class Jobseeker(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE )
    linkedin = models.URLField(max_length=200,blank=True,null=True,unique=True)
    phone = models.CharField(max_length=10,blank=True,null=True,unique=True)
    profilepic = models.ImageField(blank=True,null=True,upload_to='images/')
    resume = models.FileField(blank=True,null=True, upload_to='documents/')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Employer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    organization = models.CharField(max_length=200,default='')
    designation = models.CharField(max_length=200,default='')
    linkedin = models.URLField(max_length=200,blank=True,null=True,unique=True)
    phone = models.CharField(max_length=10,blank=True,null=True,unique=True)
    profilepic = models.ImageField(blank=True,null=True,upload_to='images/')

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class Job(models.Model):
    jobtypechoices = (
        ('part-time','part-time'),
        ('full-time','full-time'),
        ('internship','internship'),
    )

    operationtypechoices = (
        ('on-site','on-site'),
        ('remote','remote'),
    )

    title = models.CharField(max_length=200)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    salary_in_LPA = models.PositiveIntegerField(default=0)
    duration_per_day = models.PositiveSmallIntegerField(default=0)
    job_type = models.CharField(choices=jobtypechoices,max_length=200)
    operation_type = models.CharField(choices=operationtypechoices,max_length=200)
    responsibilities = models.TextField(max_length=2000,default='')
    eligibility = models.TextField(max_length=2000, default='')
    preferred = models.TextField(max_length=2000,null=True,blank=True)
    brochure = models.FilePathField(path=f"{os.getcwd()}/media/documents",null=True,blank=True)

    def __str__(self):
        return self.title

class Application(models.Model):
    statuschoices = (
        ('ACCEPTED','ACCEPTED'),
        ('REJECTED','REJECTED'),
        ('PENDING','PENDING')
    )
    employer = models.ForeignKey(Employer,on_delete=models.CASCADE)
    jobseeker = models.ForeignKey(Jobseeker, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    appliedon = models.DateTimeField(auto_now_add=True)
    isapplied = models.BooleanField(default=False)
    status = models.CharField(choices=statuschoices,default="PENDING",max_length=200)

    def __str__(self):
        return f"{self.job.title}, {self.employer.user} applied by {self.jobseeker.user}"