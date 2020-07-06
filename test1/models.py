from django.db import models


class School(models.Model):
    SchoolName = models.CharField(max_length=100)

    def __str__(self):
        return self.SchoolName


class Student(models.Model):
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)

    def __str__(self):
        return self.FirstName


class Class(models.Model):
    ClassName = models.CharField(max_length=50)
    Student = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.ClassName


class Subject(models.Model):
    Subject = models.CharField(max_length=100)

    def __str__(self):
        return self.Subject


class Teacher(models.Model):
    TeacherName = models.CharField(max_length=100)
    Subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True)
    Class = models.ForeignKey(Class, on_delete=models.SET_NULL, null=True)
    Roll = models.CharField(max_length=50)

    def __str__(self):
        return self.TeacherName
