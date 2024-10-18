from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('classes/', views.class_list, name='class-list'),
    path('students/', views.student_list, name='student-list'),
    path('teams/', views.team_list, name='team-list'),
    path('login/', views.login, name='login'),
    path('student/<int:sid>/', views.get_student_info, name='get_student_info'),
]

