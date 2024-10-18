from django.urls import path
from .views import class_list, student_list, team_list

urlpatterns = [
    path('classes/', class_list, name='class-list'),
    path('students/', student_list, name='student-list'),
    path('teams/', team_list, name='team-list'),
]
