from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):
    # user = serializers.StringRelatedField()
    # department = serializers.StringRelatedField()
    class Meta:
        model = Course
        fields = ['user', 'department','title','description','created']

class CourseListSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    class Meta:
        model = Course
        fields = ['pk','user', 'department','title','description','created']

class UserSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    courses_enrolled = serializers.StringRelatedField(many=True)
    class Meta:
        model = AppUser
        fields = [ 'pk','user','mobileNumber','status','courses_enrolled']