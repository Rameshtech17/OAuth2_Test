from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Teacher, Student, School, Subject, Class


class CreateUserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'SchoolName']


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'TeacherName', 'Class', 'Subject']
        depth = 2


class TeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'TeacherName']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'Subject']


class StudentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'FirstName', 'LastName']


class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['id', 'ClassName', 'Student']
        depth = 1
