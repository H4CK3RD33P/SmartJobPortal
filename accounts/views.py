import loguru
import re
from django.shortcuts import get_object_or_404, render, redirect
from .forms import *
from django.contrib.auth.models import Group
from django.db import IntegrityError
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .tests import *
from django.db.models import Q
import requests
import os
# Create your views here.
@user_passes_test(is_unauthenticated_user,login_url="/jobseeker/")
def home(request):
    return render(request,"accounts/home.html")

@login_required
def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")
#JOBSEEKER
@user_passes_test(is_unauthenticated_user,login_url="/jobseeker/")
def createjobseeker(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        jobseekerform = JobseekerForm(data=request.POST,files=request.FILES)
        userexists = User.objects.filter(username=request.POST['username']).first()
        phonepattern = bool(re.match(r"^[6-9]\d{9}$",request.POST['phone']))
        linkedinexists = Jobseeker.objects.filter(linkedin=request.POST['linkedin']).first()
        emailpattern =  bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+',request.POST['email']))
        emailexists = User.objects.filter(email=request.POST['email']).first()
        phoneexists = Jobseeker.objects.filter(phone=request.POST['phone']).first()
        linkedinpattern = bool(re.match(r"https://www\.linkedin\.com/in/[\w-]+$",request.POST['linkedin']))
        if request.POST.get('password1')==request.POST.get('password2'):
            if (request.POST['email']!="" and not emailexists) or request.POST['email']=="":
                if (request.POST['email']!="" and emailpattern) or request.POST['email']=="":
                    if (request.POST['phone']!="" and not phoneexists) or request.POST['phone']=="":
                        if (request.POST['phone']!="" and phonepattern) or request.POST['phone']=="":
                            if (request.POST['linkedin']!="" and not linkedinexists) or request.POST['linkedin']=="":
                                if (request.POST['linkedin']!="" and linkedinpattern) or request.POST['linkedin']=="":
                                    if not userexists:
                                        if userform.is_valid() and jobseekerform.is_valid():
                                            print("valid")
                                            user = userform.save()
                                            jobseeker = jobseekerform.save(commit=False)
                                            selected_group = Group.objects.get(name='jobseeker')
                                            user.groups.add(selected_group)
                                            jobseeker.user = user 
                                            jobseeker.save()
                                            login(request,user)
                                            print("hello")
                                            return redirect('jobseekerprofile') 
                                        else:
                                            messages.error(request,"Something went wrong :( ")
                                    else:
                                        messages.error(request,"Username already exists")
                                else:
                                    messages.error(request,"Invalid LinkedIn URL")
                            else:
                                messages.error(request,"This LinkedIn URL has already been taken")    
                        else:
                            messages.error(request,"Invalid phone number")
                    else:
                        messages.error(request,"Phone number already exists")
                else:
                    messages.error(request,"Invalid email")
            else:
                messages.error(request,"Email already exists")
        else:
            messages.warning(request,"Passwords do not match! Try again.")
    data = {'userform': UserForm(),'jobseekerform': JobseekerForm()}
    return render(request,"accounts/jobseeker/createjobseeker.html",context=data)


@user_passes_test(is_unauthenticated_user,login_url="/jobseeker/")
def initjobseeker(request):
    return render(request,"accounts/jobseeker/initjobseeker.html")


@user_passes_test(is_unauthenticated_user,login_url="/jobseeker/")
def loginjobseeker(request):
    if request.method == "POST":
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        try:
            profilepic = user.jobseeker.profilepic.url
            profilepicexists = True
        except:
            profilepicexists = False
        if not user is None:
            if (not profilepicexists) or capture_and_verify(profilepic):
                login(request,user)
                return redirect('jobseekerprofile')
            else:
                messages.error(request,"IMPERSONIFICATION IS PROHIBITED")
                ip_addr = requests.get("https://api.ipify.org").text
                api_key = "5be5f0b470c4d878afed50b1c21a0940"
                location_details = requests.get(f"http://api.ipstack.com/{ip_addr}?access_key={api_key}").json()
                location = f"{location_details['city']}, {location_details['region_name']}, {location_details['country_name']}, PINCODE - {location_details['zip']}"
                intruder = f"{os.getcwd()}/media/images/current.jpg"
                recipient = user.email
                subject = "ACCOUNT IN DANDER!"
                content = f'''
                Dear {user.first_name},

                We believe that someone else is trying to access your profile. We have send you the details.
                IP Address: {ip_addr}
                Location: {location}
                
                Thanks & Regards,
                Team JobHunter.
                '''

                attachment = intruder
                create_and_send_email(recipient,subject,content,attachment)

        else:
            messages.warning(request,"Username or Password is incorrect! Try again.")
    authform = AuthenticationForm()
    return render(request,"accounts/jobseeker/loginjobseeker.html",{'authform':authform})

@login_required(login_url="loginjobseeker")
@user_passes_test(is_jobseeker,login_url="/employer/")
def jobseekerprofile(request):
    jobseeker = request.user.jobseeker
    appliedapplications = Application.objects.filter(jobseeker=jobseeker,isapplied=True)
    savedapplications = Application.objects.filter(jobseeker=jobseeker,isapplied=False)
    return render(request,"accounts/jobseeker/jobseekerprofile.html",{'jobseeker':jobseeker,'appliedapplications':appliedapplications,'savedapplications':savedapplications})

def editjobseeker(request,jobseeker_id):
    jobseeker = get_object_or_404(Jobseeker,pk=jobseeker_id)
    user = get_object_or_404(User,pk=jobseeker.user.id)
    if request.method == "GET":
        jobseekerform = JobseekerForm(instance=jobseeker)
        userform = UserForm(instance=user)
        data = {'jobseeker':jobseeker,'user':user,'jobseekerform':jobseekerform,'userform':userform}
        return render(request,"accounts/jobseeker/editjobseeker.html",context=data)
    elif request.method == "POST":
        userform = UserForm(request.POST,instance=user)
        jobseekerform = JobseekerForm(data=request.POST,files=request.FILES,instance=jobseeker)
        userexists = User.objects.filter(username=request.POST['username']).exclude(pk=user.id).first()
        emailexists = User.objects.filter(email=request.POST['email']).exclude(pk=user.id).first()
        phoneexists = Jobseeker.objects.filter(phone=request.POST['phone']).exclude(pk=jobseeker.id).first()
        linkedinexists = Jobseeker.objects.filter(linkedin=request.POST['linkedin']).exclude(pk=jobseeker.id).first()
        emailpattern =  bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+',request.POST['email']))
        phonepattern = bool(re.match(r"^[6-9]\d{9}$",request.POST['phone']))
        linkedinpattern = bool(re.match(r"https://www\.linkedin\.com/in/[\w-]+$",request.POST['linkedin']))
        if (request.POST['phone']!="" and not phoneexists) or request.POST['phone']=="":
            if phonepattern or request.POST['phone']=="":
                if (request.POST['linkedin']!="" and not linkedinexists) or request.POST['linkedin']=="":
                    if linkedinpattern or request.POST['linkedin']=="":
                        if (request.POST['email']!="" and not emailexists) or request.POST['email']=="":
                            if emailpattern or request.POST['email']=="":
                                if request.POST['username']!="" and not userexists:
                                    if userform.is_valid() and jobseekerform.is_valid():
                                        user = userform.save()
                                        jobseekerform.save()
                                        login(request,user)
                                        return redirect('jobseekerprofile')
                                    else:
                                        messages.error(request,"BAD DATA PASSED!")
                                else:
                                    messages.error(request,"Username already exists!")
                            else:
                                messages.error(request,"Invalid email")
                        else:
                            messages.error(request,"This email already exists!")
                    else:
                        messages.error(request,"Invalid LinkedIn URL")
                else:
                    messages.error(request,"This LinkedIn URL already exists!")
            else:
                messages.error(request,"Invalid phone number")
        else:
            messages.error(request,"This phone number already exists!")
        return redirect('editjobseeker',jobseeker_id)



#EMPLOYER

@user_passes_test(is_unauthenticated_user,login_url="/employer/")
def createemployer(request):
    if request.method == "POST":
        userform = UserForm(request.POST)
        employerform = EmployerForm(data=request.POST,files=request.FILES)
        userexists = User.objects.filter(username=request.POST['username']).first()
        phonepattern = bool(re.match(r"^[6-9]\d{9}$",request.POST['phone']))
        linkedinexists = Employer.objects.filter(linkedin=request.POST['linkedin']).first()
        emailpattern =  bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+',request.POST['email']))
        emailexists = User.objects.filter(email=request.POST['email']).first()
        phoneexists = Employer.objects.filter(phone=request.POST['phone']).first()
        linkedinpattern = bool(re.match(r"https://www\.linkedin\.com/in/[\w-]+$",request.POST['linkedin']))
        if request.POST.get('password1')==request.POST.get('password2'):
            if (request.POST['email']!="" and not emailexists) or request.POST['email']=="":
                if (request.POST['email']!="" and emailpattern) or request.POST['email']=="":
                    if (request.POST['phone']!="" and not phoneexists) or request.POST['phone']=="":
                        if (request.POST['phone']!="" and phonepattern) or request.POST['phone']=="":
                            if (request.POST['linkedin']!="" and not linkedinexists) or request.POST['linkedin']=="":
                                if (request.POST['linkedin']!="" and linkedinpattern) or request.POST['linkedin']=="":
                                    if not userexists:
                                        if userform.is_valid() and employerform.is_valid():
                                            user = userform.save()
                                            employer = employerform.save(commit=False)
                                            selected_group = Group.objects.get(name='employer')
                                            user.groups.add(selected_group)
                                            employer.user = user 
                                            employer.save()
                                            login(request,user)
                                            return redirect('employerprofile') 
                                        else:
                                            messages.error(request,"Something went wrong :( ")
                                    else:
                                        messages.error(request,"Username already exists")
                                else:
                                    messages.error(request,"Invalid LinkedIn URL")
                            else:
                                messages.error(request,"This LinkedIn URL has already been taken")    
                        else:
                            messages.error(request,"Invalid phone number")
                    else:
                        messages.error(request,"Phone number already exists")
                else:
                    messages.error(request,"Invalid email")
            else:
                messages.error(request,"Email already exists")
        else:
            messages.warning(request,"Passwords do not match! Try again.")
    data = {'userform': UserForm(),'employerform': EmployerForm()}
    return render(request,"accounts/employer/createemployer.html",context=data)


def editemployer(request,employer_id):
    employer = get_object_or_404(Employer,pk=employer_id)
    user = get_object_or_404(User,pk=employer.user.id)
    if request.method == "GET":
        employerform = EmployerForm(instance=employer)
        userform = UserForm(instance=user)
        data = {'employer':employer,'user':user,'employerform':employerform,'userform':userform}
        return render(request,"accounts/employer/editemployer.html",context=data)
    elif request.method == "POST":
        userform = UserForm(request.POST,instance=user)
        employerform = EmployerForm(data=request.POST,files=request.FILES,instance=employer)
        userexists = User.objects.filter(username=request.POST['username']).exclude(pk=user.id).first()
        emailexists = User.objects.filter(email=request.POST['email']).exclude(pk=user.id).first()
        phoneexists = Employer.objects.filter(phone=request.POST['phone']).exclude(pk=employer.id).first()
        linkedinexists = Employer.objects.filter(linkedin=request.POST['linkedin']).exclude(pk=employer.id).first()
        emailpattern =  bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+',request.POST['email']))
        phonepattern = bool(re.match(r"^[6-9]\d{9}$",request.POST['phone']))
        linkedinpattern = bool(re.match(r"https://www\.linkedin\.com/in/[\w-]+$",request.POST['linkedin']))
        if (request.POST['phone']!="" and not phoneexists) or request.POST['phone']=="":
            if phonepattern or request.POST['phone']=="":
                if (request.POST['linkedin']!="" and not linkedinexists) or request.POST['linkedin']=="":
                    if linkedinpattern or request.POST['linkedin']=="":
                        if (request.POST['email']!="" and not emailexists) or request.POST['email']=="":
                            if emailpattern or request.POST['email']=="":
                                if request.POST['username']!="" and not userexists:
                                    if userform.is_valid() and employerform.is_valid():
                                        user = userform.save()
                                        employerform.save()
                                        login(request,user)
                                        return redirect('employerprofile')
                                    else:
                                        messages.error(request,"BAD DATA PASSED!")
                                        print(request.POST)
                                else:
                                    messages.error(request,"Username already exists!")
                            else:
                                messages.error(request,"Invalid email")
                        else:
                            messages.error(request,"This email already exists!")
                    else:
                        messages.error(request,"Invalid LinkedIn URL")
                else:
                    messages.error(request,"This LinkedIn URL already exists!")
            else:
                messages.error(request,"Invalid phone number")
        else:
            messages.error(request,"This phone number already exists!")
        return redirect('editemployer',employer_id)

@user_passes_test(is_unauthenticated_user,login_url="/employer/")
def initemployer(request):
    return render(request,"accounts/employer/initemployer.html")


@user_passes_test(is_unauthenticated_user,login_url="/employer/")
def loginemployer(request):
    if request.method == "POST":
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        try:
            profilepic = user.employer.profilepic.url
            profilepicexists = True
        except:
            profilepicexists = False
        if not user is None:
            if (not profilepicexists) or capture_and_verify(profilepic):
                login(request,user)
                return redirect('employerprofile')
            else:
                messages.error(request,"IMPERSONIFICATION IS PROHIBITED!")
        else:
            messages.warning(request,"Username or Password is incorrect! Try again.")
    authform = AuthenticationForm()
    return render(request,"accounts/employer/loginemployer.html",{'authform':authform})

@login_required(login_url="loginemployer")
@user_passes_test(is_employer,login_url="/jobseeker/")
def employerprofile(request):
    employer = request.user.employer
    applications = employer.application_set.filter(isapplied=True)
    jobs = Job.objects.filter(employer=employer)
    user = employer.user
    return render(request,"accounts/employer/employerprofile.html",{'employer':employer,'jobs':jobs,'applications':applications})

@login_required(login_url="loginemployer")
@user_passes_test(is_employer,login_url="/jobseeker/")
def createjob(request):
    if request.method == "POST":
        jobform = JobForm(request.POST)
        if jobform.is_valid():
            job = jobform.save(commit=False)
            job.employer = request.user.employer
            job.brochure = createjobbrochure(job)
            job.save()
            return redirect("/employer/")
    jobform = JobForm()
    return render(request,"accounts/employer/createjob.html",{'jobform':jobform})

def jobdetail(request,job_id):
    job = get_object_or_404(Job,pk=job_id)
    accounttype = None
    if request.user.groups.filter(name="employer").exists():
        accounttype = "employer"
    elif request.user.groups.filter(name="jobseeker").exists():
        accounttype = "jobseeker"
    print(accounttype)
    try:
        brochurename = os.path.basename(job.brochure)
        brochureurl = f"/media/documents/{brochurename}"
    except:
        brochureurl = None
    return render(request,"accounts/employer/jobdetail.html",{'job':job,'accounttype':accounttype,'brochureurl':brochureurl})

def alljobs(request):
    jobs = Job.objects.all()
    return render(request,"accounts/jobseeker/alljobs.html",{'jobs':jobs})

def jobapply(request,job_id=None):
    if request.method == "POST":
        job = get_object_or_404(Job,pk=job_id)
        savedexisting = Application.objects.filter(jobseeker=request.user.jobseeker,job=job, isapplied=False).exists()
        if savedexisting:
            savedjob = Application.objects.filter(jobseeker=request.user.jobseeker,job=job, isapplied=False)
            savedjob.delete() 
        existing = Application.objects.filter(jobseeker=request.user.jobseeker,job=job, isapplied=True).exists()
        print(existing)
        if not existing:
            application = Application.objects.create(
                employer=job.employer,
                isapplied=True, 
                jobseeker=request.user.jobseeker,
                job=job
            )
            application.save()
            return redirect('/jobseeker/')
        else:
            messages.error(request,"You can only apply once for a job")
            return redirect('/alljobs/')

def jobsave(request,job_id):
    if request.method == "POST":
        job = get_object_or_404(Job,pk=job_id)
        applied = Application.objects.filter(jobseeker=request.user.jobseeker,job=job, isapplied=True).exists()
        saved = Application.objects.filter(jobseeker=request.user.jobseeker,job=job, isapplied=False).exists()
        if not (applied or saved):
            application = Application.objects.create(
                employer=job.employer, 
                jobseeker=request.user.jobseeker,
                job=job
            )
            application.save()
            return redirect('/jobseeker/')
        else:
            messages.error(request,"You already saved this or applied for this job.")
            return redirect('/alljobs/')

def applicantdetails(request,application_id):
    application = get_object_or_404(Application,pk=application_id)
    all_applications = Application.objects.filter(jobseeker=application.jobseeker,employer=application.employer)
    return render(request,"accounts/employer/applicantdetails.html",{'application':application,'all_applications':all_applications})

def jobdelete(request,job_id):
    if request.method == "POST":
        job = get_object_or_404(Job,pk=job_id)
        job.delete()
        return redirect('/employer/')

def jobedit(request,job_id):
    job = get_object_or_404(Job,pk=job_id)
    if request.method == "GET":        
        jobform = JobForm(instance=job)
        return render(request,"accounts/employer/jobedit.html",{'job':job,'jobform':jobform})
    elif request.method == "POST":
        jobform = JobForm(request.POST,instance=job)
        if jobform.is_valid():
            jobform.save()
            job.brochure = createjobbrochure(job)
            return redirect('/employer/')

def applicationdelete(request,application_id):
    if request.method == "POST":
        application = get_object_or_404(Application,pk=application_id)
        application.delete()
        return redirect('/jobseeker/')

def applicationaccept(request,application_id):
    if request.method == "POST":
        application = get_object_or_404(Application,pk=application_id)
        application.status = "ACCEPTED"
        application.save()
        jobseekeremail = application.jobseeker.user.email
        subject = "APPLICATION ACCEPTED!"
        content = f'''
        Dear {application.jobseeker.user.first_name},

        Congratulations! Your application for {application.job.title} at {application.employer.organization}
        has been accepted. The employer will contact you soon through email or phone.

        Thanks & Regards,
        Team JobHunters.
        '''
        create_and_send_email(jobseekeremail,subject,content)
        return redirect('/employer/')

def applicationreject(request,application_id):
    if request.method == "POST":
        application = get_object_or_404(Application,pk=application_id)
        application.status = "REJECTED"
        jobseekeremail = application.jobseeker.user.email
        subject = "APPLICATION REJECTED!"
        content = f'''
        Dear {application.jobseeker.user.first_name},

        Sorry! Your application for {application.job.title} at {application.employer.organization} has been rejected.

        Thanks & Regards,
        Team JobHunters.
        '''
        create_and_send_email(jobseekeremail,subject,content)
        application.save()
        return redirect('/employer/')