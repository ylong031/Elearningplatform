import json
from django.test import TestCase
from django.urls import reverse
from django.urls import reverse_lazy

from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from .model_factories import *
from .serializers import *


class CourseSerializerTest(APITestCase):
    course1=None
    courseserializer=None

    def setUp(self):
        self.course1=CourseFactory.create(pk=1,title='course1')
        self.courseserializer=CourseSerializer(instance=self.course1)

    def tearDown(self):
        User.objects.all().delete()
        Course.objects.all().delete()
        Department.objects.all().delete()

        UserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        DepartmentFactory.reset_sequence(0)

    def test_courseSerializer(self):
        data=self.courseserializer.data
        self.assertEqual(set(data.keys()),set(['user', 'department','title','description','created']))
        

    def test_courseSerializerCourseTitlehasCorrectData(self):
        data=self.courseserializer.data
        self.assertEqual(data['title'],'course1')

class CourseTest(APITestCase):

    course1=''
    course2=''
    course3=''

    def setUp(self):
        self.course1=CourseFactory.create(pk=1,title='course1')
        self.course2=CourseFactory.create(pk=2,title='course2')
        self.course3=CourseFactory.create(pk=3,title='course3')
    

    def tearDown(self):
        User.objects.all().delete()
        Course.objects.all().delete()
        Department.objects.all().delete()

        UserFactory.reset_sequence(0)
        CourseFactory.reset_sequence(0)
        DepartmentFactory.reset_sequence(0)

    def test_courseDetailReturnSuccess(self):
      
        url=reverse('course_api',kwargs={'pk':1})
        response=self.client.get(url,format='json')
        self.assertEqual(response.status_code,200)
        

    def test_courseDetailReturnFailOnBadPK(self):
     
        url="/api/course/H/"
        response=self.client.get(url,format='json')
        self.assertEqual(response.status_code,404)
      






