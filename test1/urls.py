from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register),
    path('token/', views.token),
    path('token/refresh/', views.refresh_token),
    path('token/revoke/', views.revoke_token),
    path('school/', views.SchoolAPIView.as_view()),
    path('class/', views.ClassAPIView.as_view()),
    path('student/', views.StudentListAPIView.as_view()),
]
