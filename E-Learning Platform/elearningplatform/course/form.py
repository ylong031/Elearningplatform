from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.models import User

class CourseForm(forms.ModelForm):
 class Meta:
    model = Course
    fields = ['title','description']
 
class FeedbackForm(forms.ModelForm):
 class Meta:
    model = Feedback
    fields = ['description']


class ContentForm(ModelForm):
    class Meta:
        model = Content
        fields = ['title','description','file']


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')        


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = AppUser
        fields = ('mobileNumber', 'profilePic')


