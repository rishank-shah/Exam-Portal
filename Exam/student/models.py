from django.db import models
from django.contrib.auth.models import User

class StudentInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True)
    stream = models.CharField(max_length=50, blank=True)
    picture = models.ImageField(upload_to = 'student_profile_pics', blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Student Info'