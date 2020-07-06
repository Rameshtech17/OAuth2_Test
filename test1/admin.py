from django.contrib import admin
from .models import School, Class, Teacher, Subject,Student


admin.site.register(School)
admin.site.register(Class)
admin.site.register(Teacher)
admin.site.register(Subject)
admin.site.register(Student)

# Register your models here.
