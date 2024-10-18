from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Class, Student, StudentClass, Team, TeamMember, TeamRequest

admin.site.register(Class)
admin.site.register(Student)
admin.site.register(StudentClass)
admin.site.register(Team)
admin.site.register(TeamMember)
admin.site.register(TeamRequest)
