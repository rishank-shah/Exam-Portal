from django.db import models
from django.contrib.auth.models import User

class StudentPreferenceModel(models.Model): 
    user = models.OneToOneField(to = User,on_delete=models.CASCADE)
    sendEmailOnLogin = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user) + 's' + 'preferences' 