from accounts.models import Employer, Jobseeker
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import ModelForm
from .models import *

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']

class JobseekerForm(ModelForm):
    class Meta:
        model = Jobseeker
        fields = "__all__"
        exclude = ['user','accounttype']

class EmployerForm(ModelForm):
    class Meta:
        model = Employer
        fields = "__all__"
        exclude = ['user','accounttype']

class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = "__all__"
        exclude = ['employer','brochure']        