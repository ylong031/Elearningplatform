from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.template.loader import render_to_string
from django.urls import reverse



class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobileNumber = models.IntegerField(null=True, blank=True)
    courses_enrolled = models.ManyToManyField('Course', related_name='students_enrolled', blank=True)
    is_teacher = models.BooleanField(default=False)
    profilePic=models.ImageField(blank=True)
    status = models.TextField(blank=True)

    def __unicode__(self):
        return self.user.username
    
    def __str__(self):
        return self.user.username



class Department(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class Course(models.Model):
    user = models.ForeignKey(User, related_name="courses_created", on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name="courses", on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(User, related_name="courses_joined", blank=True)
   

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Content(models.Model):
    course = models.ForeignKey(Course, related_name="content", on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    file = models.FileField(blank=False,null=True)

    def __str__(self):
        return self.title
    
class Feedback(models.Model):
    user = models.ForeignKey(User, related_name="feedback_created", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="feedback", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)












































