from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
# Login检查
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Class, Student, Team
from .serializers import ClassSerializer, StudentSerializer, TeamSerializer

# Login API
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def login(request):
    identifier = request.data.get('identifier')
    password = request.data.get('password')

    user = None

    # 1. 尝试通过用户名进行身份验证
    user = authenticate(username=identifier, password=password)

    # 2. 如果通过用户名找不到用户，再尝试通过电子邮件查找
    if user is None:
        try:
            user = User.objects.get(email=identifier)
            if not user.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            pass

    # 3. 如果通过电子邮件找不到，再尝试通过学号查找
    if user is None:
        try:
            student = Student.objects.get(sid=identifier)
            user = student.user  # 获取 Student 对应的 User
            if not user.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # 创建JWT令牌
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'sid': student.sid,
                    'username': student.user.username,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    # 创建JWT令牌
    refresh = RefreshToken.for_user(user)
    return Response({
        'message': 'Login successful',
        'sid': user.student_profile.sid,
        'username': user.username,
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }, status=status.HTTP_200_OK)

# StudentInfo Page
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_info(request, sid):
    try:
        student = Student.objects.get(sid=sid)
        student_data = {
            'sid': student.sid,
            'name': student.user.username,
            'cur_major': student.cur_major,
            'email': student.user.email,
        }
        return Response(student_data, status=status.HTTP_200_OK)
    except Student.DoesNotExist:
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)

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
