from django import forms 
from .models import FacultyInfo
from django.contrib.auth.models import User

class FacultyForm(forms.ModelForm):
    class Meta():
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs = {'id':'passwordfield','class':'form-control'}),
            'email' : forms.EmailInput(attrs = {'id':'emailfield','class':'form-control'}),
            'username' : forms.TextInput(attrs = {'id':'usernamefield','class':'form-control'})
        }

class FacultyInfoForm(forms.ModelForm):
    class Meta():
        model = FacultyInfo
        fields = ['address','subject','picture']
        widgets = {
            'address': forms.Textarea(attrs = {'class':'form-control'}),
            'subject' : forms.TextInput(attrs = {'class':'form-control'})
        }
