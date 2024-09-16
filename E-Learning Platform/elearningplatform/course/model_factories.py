import factory

from django.test import TestCase
from django.conf import settings
from django.core.files import File
from random import randint
from random import choice
from django.contrib.auth.models import User
from .models import *
import datetime

class DepartmentFactory(factory.django.DjangoModelFactory):
    title=choice(['Computer Science','Maths','Science'])

    class Meta:
        model=Department


class UserFactory(factory.django.DjangoModelFactory):
    username =factory.Sequence(lambda n: 'teacher%d' % n+str(1))

    class Meta:
        model=User

class CourseFactory(factory.django.DjangoModelFactory):
   
    user = factory.SubFactory(UserFactory)
    department =factory.SubFactory(DepartmentFactory)
    title = factory.Sequence(lambda n: 'course%d' % n+str(1))
    description = factory.Faker('sentence',nb_words=1)
    created = factory.LazyFunction(datetime.datetime.now)

    class Meta:
        model = Course