from rest_framework import generics
from rest_framework import mixins
from .models import *
from .models import *
from .serializers import *
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

class mypermission(LoginRequiredMixin,UserPassesTestMixin):

    def test_func(self):
        if self.request.user.appuser.is_teacher:
            return self.request.user.appuser.is_teacher

    def handle_no_permission(self):
       
        return render(self.request, 'course/error_page.html')

class CourseList(mypermission,generics.ListAPIView):
    queryset=Course.objects.all()
    serializer_class=CourseListSerializer

class StudentList(mypermission,generics.ListAPIView):
    queryset=AppUser.objects.filter(is_teacher="False")
    serializer_class=UserSerializer

class TeacherList(mypermission,generics.ListAPIView):
    queryset=AppUser.objects.filter(is_teacher="True")
    serializer_class=UserSerializer




class CourseDetails(mypermission,mixins.CreateModelMixin,
                 mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)