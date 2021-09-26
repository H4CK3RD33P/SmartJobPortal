"""jobportal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from accounts import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name="home"),
    path('createjobseeker/',views.createjobseeker,name="createjobseeker"),
    path('initjobseeker/',views.initjobseeker,name="initjobseeker"),
    path('loginjobseeker',views.loginjobseeker,name="loginjobseeker"),
    path('jobseeker/',views.jobseekerprofile,name="jobseekerprofile"),
    path('jobseeker/<int:jobseeker_id>/edit',views.editjobseeker,name="editjobseeker"),
    path('createemployer/',views.createemployer,name="createemployer"),
    path('initemployer/',views.initemployer,name="initemployer"),
    path('loginemployer/',views.loginemployer,name="loginemployer"),
    path('employer/',views.employerprofile,name="employerprofile"),
    path('employer/<int:employer_id>/edit',views.editemployer,name="editemployer"),
    path('createjob/',views.createjob,name="createjob"),
    path('logout/',views.logoutuser,name='logoutuser'),
    path('job/<int:job_id>',views.jobdetail,name="jobdetail"),
    path('alljobs/',views.alljobs,name="alljobs"),
    path('job/<int:job_id>/apply',views.jobapply,name="jobapply"),
    path('job/<int:job_id>/save',views.jobsave,name="jobsave"),
    path('application/<int:application_id>',views.applicantdetails,name="applicantdetails"),
    path('job/<int:job_id>/delete',views.jobdelete,name="jobdelete"),
    path('job/<int:job_id>/edit',views.jobedit,name="jobedit"),
    path('application/<int:application_id>/delete',views.applicationdelete,name="applicationdelete"),
    path('applicaiton/<int:application_id>/accept',views.applicationaccept,name="applicationaccept"),
    path('applicaiton/<int:application_id>/reject',views.applicationreject,name="applicationreject"),
]

urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 