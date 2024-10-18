from django.db import models
from django.contrib.auth.models import User 

class Class(models.Model):
    cid = models.CharField(max_length=16, primary_key=True)
    semester = models.CharField(max_length=16)
    cname = models.CharField(max_length=64)
    room = models.CharField(max_length=64)
    ctime = models.CharField(max_length=64)
    info = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.cname

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile') # 与User一一映射，有name，email和password
    sid = models.AutoField(primary_key=True)
    cur_major = models.CharField(max_length=64)
    info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


class StudentClass(models.Model):
    sid = models.ForeignKey(Student, on_delete=models.CASCADE)
    cid = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('sid', 'cid')

class Team(models.Model):
    tid = models.AutoField(primary_key=True)
    tname = models.CharField(max_length=64)
    leader = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='teams_led')
    cid = models.ForeignKey(Class, on_delete=models.CASCADE)
    is_recruiting = models.BooleanField()
    info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.tname

class TeamMember(models.Model):
    tid = models.ForeignKey(Team, on_delete=models.CASCADE)
    cid = models.ForeignKey(Class, on_delete=models.CASCADE)
    sid = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('tid', 'cid', 'sid')

class TeamRequest(models.Model):
    sid = models.ForeignKey(Student, on_delete=models.CASCADE)
    cid = models.ForeignKey(Class, on_delete=models.CASCADE)
    info = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('sid', 'cid')
