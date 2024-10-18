from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Class, Student, Team
from .serializers import ClassSerializer, StudentSerializer, TeamSerializer

@api_view(['GET'])
def class_list(request):
    classes = Class.objects.all()
    serializer = ClassSerializer(classes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def student_list(request):
    students = Student.objects.all()
    serializer = StudentSerializer(students, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def team_list(request):
    teams = Team.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)
