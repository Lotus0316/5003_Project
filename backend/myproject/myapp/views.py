from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging

logger = logging.getLogger(__name__)
# Login检查
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse


from .models import Class, Student, Team, StudentClass, TeamMember, TeamRequest
from .serializers import ClassSerializer, StudentSerializer, TeamSerializer


# Login API
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
@permission_classes([AllowAny])
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
            user = student.user
            if not user.check_password(password):
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # 创建JWT令牌
                refresh = RefreshToken.for_user(user)
                refresh['sid'] = user.student_profile.sid

                return Response({
                    'message': 'Login successful',
                    'sid': student.sid,
                    'username': student.user.username,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token)
                }, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)

    # 创建JWT令牌
    refresh = RefreshToken.for_user(user)
    refresh['sid'] = user.student_profile.sid
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
        # 获取要访问的学生对象
        student = Student.objects.get(sid=sid)
        
        # 自定义权限检查
        jwt_authenticator = JWTAuthentication()
        try:
            # 从请求中提取令牌并验证用户
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response({'error': 'Invalid token or unauthorized access'}, status=status.HTTP_403_FORBIDDEN)

        # 确保请求的用户是该学生的所有者
        if student.user != current_user:
            return Response({'error': 'You do not have permission to access this student information', 'csid': current_user.student_profile.sid}, status=status.HTTP_403_FORBIDDEN)

        # 如果权限检查通过，返回学生信息
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
    teams = Team.objects.select_related('cid').all()
    team_data = []
    for team in teams:
        members = TeamMember.objects.filter(tid=team).select_related('sid')
        member_data = [
            {
                'id': member.sid.sid,
                'name': member.sid.user.username
            } for member in members
        ]
        team_data.append({
            'tid': team.tid,
            'tname': team.tname,
            'is_recruiting': team.is_recruiting,
            'leader': team.leader.sid,
            'leader_name': team.leader.user.username, 
            'cid': team.cid.cid,
            'description': team.info,
            'members': member_data
        })
    return Response(team_data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team(request):
    try:
        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response({'error': 'Invalid token or unauthorized access'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        name = request.data.get('name')
        description = request.data.get('description')
        cid = request.data.get('cid')
        
        try:
            course = Class.objects.get(cid=cid)
        except Class.DoesNotExist:
            return Response({'error': 'Course not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
                          
        if not StudentClass.objects.filter(sid=current_user.student_profile, cid=course).exists():
            return Response({'error': 'You must enroll in the course first'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        if TeamMember.objects.filter(sid=current_user.student_profile, cid=course).exists():
            return Response({'error': 'You are already in a team for this course'}, 
                          status=status.HTTP_400_BAD_REQUEST)

        team = Team.objects.create(
            tname=name,
            info=description,
            leader=current_user.student_profile,
            cid=course,
            is_recruiting=False # Defaulting is False initially
        )

        TeamMember.objects.create(
            tid=team,
            cid=course,
            sid=current_user.student_profile
        )
        
        return Response({
            'status': 'success', 
            'message': 'Team created successfully',
            'team_id': team.tid
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
 
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def disband_team(request, tid):
    try:
        jwt_authenticator = JWTAuthentication()
        token = request.headers.get('Authorization').split(' ')[1]
        validated_token = jwt_authenticator.get_validated_token(token)
        current_user = jwt_authenticator.get_user(validated_token)
        
        team = Team.objects.get(tid=tid)
        
        if team.leader.user != current_user:
            return Response({
                'error': 'Only team leader can disband the team'
            }, status=status.HTTP_403_FORBIDDEN)
            
        TeamMember.objects.filter(tid=team).delete()
        
        TeamRequest.objects.filter(cid=team.cid).delete()
        
        team.delete()
        
        return Response({
            'status': 'success',
            'message': 'Team disbanded successfully'
        }, status=status.HTTP_200_OK)
        
    except Team.DoesNotExist:
        return Response({
            'error': 'Team not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error', 
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
                
@api_view(['POST'])
@permission_classes([IsAuthenticated]) 
def toggle_recruiting(request, tid):
    try:
        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response({'error': 'Invalid token or unauthorized access'}, 
                          status=status.HTTP_403_FORBIDDEN)

        team = Team.objects.get(tid=tid)
        
        if team.leader.user != current_user:
            return Response({
                'error': 'Only team leader can modify recruiting status',
                'csid': current_user.student_profile.sid
            }, status=status.HTTP_403_FORBIDDEN)
        
        team.is_recruiting = not team.is_recruiting
        team.save()
        
        return Response({
            'status': 'success',
            'is_recruiting': team.is_recruiting
        }, status=status.HTTP_200_OK)
        
    except Team.DoesNotExist:
        return Response({'error': 'Team not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_request(request, tid):
    try:
        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response({'error': 'Invalid token or unauthorized access'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        team = Team.objects.get(tid=tid)
        
        if not team.is_recruiting:
            return Response({'error': 'This team is not recruiting'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if TeamMember.objects.filter(sid=current_user.student_profile, cid=team.cid).exists():
            return Response({'error': 'You are already in a team for this course'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if TeamRequest.objects.filter(sid=current_user.student_profile, cid=team.cid).exists():
            return Response({'error': 'You have already sent a request for this course'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        TeamRequest.objects.create(
            sid=current_user.student_profile,
            cid=team.cid,
            info=request.data.get('message', '')  
        )
        
        return Response({
            'status': 'success',
            'message': 'Join request sent successfully'
        }, status=status.HTTP_201_CREATED)
        
    except Team.DoesNotExist:
        return Response({'error': 'Team not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_class(request):
    try:

        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response({'error': 'Invalid token or unauthorized access'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': 'success',
                'message': 'Course added successfully',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request, sid):
    logger.debug(f"Received enrollment request, student ID: {sid}, request data: {request.data}")
    try:
        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            logger.warning(f"Invalid token or unauthorized access, student ID: {sid}")
            return Response({'error': 'Invalid token or unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            student = Student.objects.get(sid=sid)
        except Student.DoesNotExist:
            logger.error(f"Student not found, student ID: {sid}")
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if student.user != current_user:
            logger.warning(f"User {current_user.username} attempted to enroll for student ID {sid}")
            return Response({
                'error': 'You can only enroll for yourself',
                'csid': current_user.student_profile.sid
            }, status=status.HTTP_403_FORBIDDEN)
        
        cid = request.data.get('cid')
        if not cid:
            logger.error("No course ID provided in request")
            return Response({'error': 'Course ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            course = Class.objects.get(cid=cid)
        except Class.DoesNotExist:
            logger.error(f"Course not found, course ID: {cid}")
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if StudentClass.objects.filter(sid=student, cid=course).exists():
            logger.info(f"Student ID: {sid} already enrolled in course ID: {cid}")
            return Response({'error': 'You are already enrolled in this course'}, status=status.HTTP_400_BAD_REQUEST)
        
        StudentClass.objects.create(sid=student, cid=course)
        logger.info(f"Student ID: {sid} successfully enrolled in course ID: {cid}")
        
        return Response({
            'status': 'success',
            'message': 'Course enrollment successful'
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        logger.exception("Unexpected error during course enrollment")
        return Response({
            'status': 'error',
            'message': 'Internal server error, please try again later.'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_courses(request, sid): 
    try:
        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response(
                {'error': 'Invalid token or unauthorized access'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        try:
            student = Student.objects.get(sid=sid)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, 
                          status=status.HTTP_404_NOT_FOUND)
                          
        if student.user != current_user:
            return Response({
                'error': 'You do not have permission to access this student\'s course information',
                'csid': current_user.student_profile.sid
            }, status=status.HTTP_403_FORBIDDEN)

        student_classes = StudentClass.objects.filter(
            sid=student
        ).select_related('cid')
        
        courses = [sc.cid for sc in student_classes]
        serializer = ClassSerializer(courses, many=True)
        
        return Response(serializer.data)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def drop_course(request, sid, cid):
    try:
        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response({'error': 'Invalid token or unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            student = Student.objects.get(sid=sid)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if student.user != current_user:
            return Response({
                'error': 'You can only drop your own courses',
                'csid': current_user.student_profile.sid
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            course = Class.objects.get(cid=cid)
        except Class.DoesNotExist:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            student_class = StudentClass.objects.get(sid=student, cid=course)
        except StudentClass.DoesNotExist:
            return Response({'error': 'You are not enrolled in this course'}, status=status.HTTP_404_NOT_FOUND)
        
        student_class.delete()
        
        return Response({
            'status': 'success',
            'message': 'Course dropped successfully'
        }, status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_team_requests(request):
    jwt_authenticator = JWTAuthentication()
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        validated_token = jwt_authenticator.get_validated_token(token)
        current_user = jwt_authenticator.get_user(validated_token)
    except Exception:
        return Response({'error': 'Invalid token or unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        leader_student = current_user.student_profile
    except Student.DoesNotExist:
        return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    teams = Team.objects.filter(leader=leader_student)
    
    team_requests = TeamRequest.objects.filter(tid__in=teams)
    
    data = []
    for req in team_requests:
        data.append({
            'id': req.id,
            'studentName': req.sid.user.username,
            'cid': req.tid.cid.cid,
            'cname': req.tid.cid.cname,
            'teamId': req.tid.tid,
            'teamName': req.tid.tname,
            'info': req.info
        })
    
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_requests(request):
    jwt_authenticator = JWTAuthentication()
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        validated_token = jwt_authenticator.get_validated_token(token)
        current_user = jwt_authenticator.get_user(validated_token)
    except Exception:
        return Response({'error': 'Invalid token or unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        student = current_user.student_profile
    except Student.DoesNotExist:
        return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    my_requests = TeamRequest.objects.filter(sid=student)
    
    data = []
    for req in my_requests:
        data.append({
            'id': req.id,
            'tid': req.tid.tid,
            'tname': req.tid.tname,
            'cid': req.tid.cid.cid,
            'cname': req.tid.cid.cname,
            'info': req.info
        })
    
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def handle_request(request, request_id):
    jwt_authenticator = JWTAuthentication()
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        validated_token = jwt_authenticator.get_validated_token(token)
        current_user = jwt_authenticator.get_user(validated_token)
    except Exception:
        return Response({'error': 'Invalid token or unauthorized access'}, status=status.HTTP_403_FORBIDDEN)
    
    try:
        leader_student = current_user.student_profile
    except Student.DoesNotExist:
        return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
    
    teams = Team.objects.filter(leader=leader_student)
    
    try:
        team_request = TeamRequest.objects.get(id=request_id, tid__in=teams)
    except TeamRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)
    
    action = request.data.get('action')
    if action not in ['accept', 'reject']:
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
    
    if action == 'accept':
        TeamMember.objects.create(
            tid=team_request.tid,
            cid=team_request.tid.cid,
            sid=team_request.sid
        )
        team_request.delete()
        return Response({'status': 'success', 'message': 'Request accepted'}, status=status.HTTP_200_OK)
    else:
        team_request.delete()
        return Response({'status': 'success', 'message': 'Request rejected'}, status=status.HTTP_200_OK)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_team(request, tid):
    
    try:
        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response({'error': 'Invalid token or unauthorized access'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        team = Team.objects.get(tid=tid)
        student = current_user.student_profile
        
        if not team.is_recruiting:
            return Response({'error': 'This team is not recruiting'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if TeamMember.objects.filter(tid=team, sid=student).exists():
            return Response({'error': 'You are already a member of this team'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if not StudentClass.objects.filter(sid=student, cid=team.cid).exists():
            return Response({'error': 'You must enroll in the course first'}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
        if TeamMember.objects.filter(sid=student, cid=team.cid).exists():
            return Response({'error': 'You are already in another team for this course'}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
        TeamMember.objects.create(
            tid=team,
            cid=team.cid,
            sid=student
        )
        
        return Response({
            'status': 'success',
            'message': 'Successfully joined the team'
        }, status=status.HTTP_200_OK)
        
    except Team.DoesNotExist:
        return Response({'error': 'Team not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def leave_team(request, tid):
    try:
        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response({'error': 'Invalid token or unauthorized access'}, 
                          status=status.HTTP_403_FORBIDDEN)
        
        team = Team.objects.get(tid=tid)
        student = current_user.student_profile
        
        try:
            team_member = TeamMember.objects.get(tid=team, sid=student)
        except TeamMember.DoesNotExist:
            return Response({'error': 'You are not a member of this team'}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        if team.leader == student:
            return Response({'error': 'Team leader cannot leave team. Please disband the team instead'}, 
                          status=status.HTTP_400_BAD_REQUEST)
            
        team_member.delete()
        
        return Response({
            'status': 'success',
            'message': 'Successfully left the team'
        }, status=status.HTTP_200_OK)
        
    except Team.DoesNotExist:
        return Response({'error': 'Team not found'}, 
                       status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET'])
@permission_classes([IsAuthenticated]) 
def student_teams(request, sid):
    try:
        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response({'error': 'Invalid token or unauthorized access'}, 
                          status=403)
            
        try:
            student = Student.objects.get(sid=sid)
            if student.user != current_user:
                return Response({
                    'error': 'You do not have permission to access this information',
                    'csid': current_user.student_profile.sid
                }, status=403)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, 
                          status=404)
        
        team_members = TeamMember.objects.filter(sid=student).select_related('tid', 'tid__leader', 'tid__cid')
        
        teams_data = []
        for team_member in team_members:
            team = team_member.tid
            members = TeamMember.objects.filter(tid=team).select_related('sid__user')
            member_data = [
                {
                    'id': member.sid.sid,
                    'name': member.sid.user.username
                } for member in members
            ]
            
            teams_data.append({
                'tid': team.tid,
                'tname': team.tname,
                'leader': team.leader.sid,
                'leader_name': team.leader.user.username,
                'cid': team.cid.cid,
                'cname': team.cid.cname,
                'is_recruiting': team.is_recruiting,
                'info': team.info,
                'members': member_data
            })
            
        return Response(teams_data, status=200)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=400)
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_team_request(request):
    try:
        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response({'error': 'Invalid token or unauthorized access'}, 
                          status=status.HTTP_403_FORBIDDEN)

        student = current_user.student_profile
        cid = request.data.get('courseId')
        info = request.data.get('info', '')

        try:
            course = Class.objects.get(cid=cid)
        except Class.DoesNotExist:
            return Response({'error': 'Course not found'},
                          status=status.HTTP_404_NOT_FOUND)
                          
        if TeamMember.objects.filter(sid=student, cid=course).exists():
            return Response({'error': 'You are already in a team for this course'},
                          status=status.HTTP_400_BAD_REQUEST)

        if TeamRequest.objects.filter(sid=student, cid=course).exists():
            return Response({'error': 'You already have a pending request for this course'},
                          status=status.HTTP_400_BAD_REQUEST)

        TeamRequest.objects.create(
            sid=student,
            cid=course,
            info=info
        )

        return Response({
            'status': 'success',
            'message': 'Team request created successfully'
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET']) 
@permission_classes([IsAuthenticated])
def list_team_requests(request):
    try:
        requests = TeamRequest.objects.select_related('sid', 'cid').all()
        
        data = []
        for req in requests:
            data.append({
                'id': req.id,
                'studentId': req.sid.sid,
                'studentName': req.sid.user.username,
                'courseId': req.cid.cid, 
                'courseName': req.cid.cname,
                'info': req.info
            })
            
        return Response(data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_from_request(request, request_id):
    try:
        jwt_authenticator = JWTAuthentication()
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            validated_token = jwt_authenticator.get_validated_token(token)
            current_user = jwt_authenticator.get_user(validated_token)
        except Exception:
            return Response({'error': 'Invalid token or unauthorized access'},
                          status=status.HTTP_403_FORBIDDEN)

        team_request = TeamRequest.objects.get(id=request_id)
        student = team_request.sid
        course = team_request.cid

        try:
            team = Team.objects.get(
                leader=current_user.student_profile,
                cid=course
            )
        except Team.DoesNotExist:
            return Response({'error': 'You are not a team leader for this course'},
                          status=status.HTTP_403_FORBIDDEN)

        if TeamMember.objects.filter(sid=student, cid=course).exists():
            return Response({'error': 'Student is already in a team for this course'},
                          status=status.HTTP_400_BAD_REQUEST)

        TeamMember.objects.create(
            tid=team,
            cid=course,
            sid=student
        )

        team_request.delete()

        return Response({
            'status': 'success',
            'message': 'Student has been added to your team'
        }, status=status.HTTP_200_OK)

    except TeamRequest.DoesNotExist:
        return Response({'error': 'Team request not found'},
                       status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
        
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_team_request(request, request_id):
    jwt_authenticator = JWTAuthentication()
    try:
        token = request.headers.get('Authorization').split(' ')[1]
        validated_token = jwt_authenticator.get_validated_token(token)
        current_user = jwt_authenticator.get_user(validated_token)
    except Exception:
        return Response({'error': 'Invalid token or unauthorized access'}, status=403)
    
    try:
        team_request = TeamRequest.objects.get(id=request_id, sid=current_user.student_profile)
    except TeamRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=404)
    
    team_request.delete()
    return Response({'status': 'success', 'message': 'Request cancelled'}, status=200)