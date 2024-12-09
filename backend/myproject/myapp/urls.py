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
    path('teams/create/', views.create_team, name='create-team'),
    path('teams/<int:tid>/join-request/', views.join_request, name='join-request'),
    path('classes/add/', views.add_class, name='add-class'),
    path('student/<int:sid>/enroll/', views.enroll_course, name='enroll_course'),
    path('student/<int:sid>/courses/', views.student_courses, name='student-courses'), 
    path('student/<int:sid>/courses/drop/<str:cid>/', views.drop_course, name='drop_course'),
    path('teams/toggle-recruiting/<int:tid>/', views.toggle_recruiting, name='toggle-recruiting'),
    path('teams/disband/<int:tid>/', views.disband_team, name='disband-team'),
    path('teams/join/<int:tid>/', views.join_team, name='join-team'),
    path('teams/<int:tid>/leave/', views.leave_team, name='leave-team'),
    path('team-requests/create/', views.create_team_request, name='create-team-request'),
    path('team-requests/', views.list_team_requests, name='list-team-requests'),
    path('team-requests/<int:request_id>/invite/', views.invite_from_request, name='invite-from-request'),
    path('student/<int:sid>/teams/', views.student_teams, name='student-teams'),
    path('team-requests/<int:request_id>/cancel/', views.cancel_team_request, name='cancel_team_request'),
    path('teams/update/<int:tid>/', views.update_team, name='update-team'),
]

