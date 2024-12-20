# Generated by Django 4.0.10 on 2024-10-18 15:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0003_remove_class_password_student_password'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='email',
        ),
        migrations.RemoveField(
            model_name='student',
            name='name',
        ),
        migrations.RemoveField(
            model_name='student',
            name='password',
        ),
        migrations.AddField(
            model_name='student',
            name='user',
            field=models.OneToOneField(default=123, on_delete=django.db.models.deletion.CASCADE, related_name='student_profile', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
