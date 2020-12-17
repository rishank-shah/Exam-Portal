from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from validate_email import validate_email
from .views import EmailThread
from django.core.mail import EmailMessage

class UsernameValidation(View):
    def post(self,request):
        data = json.loads(request.body)
        username = data['username']

        if not str(username).isalnum():
            return JsonResponse({'username_error':'Username should only contain alphanumeric characters'},status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error':'Username Exists'},status=409)

        return JsonResponse({'username_valid':True})

class EmailValidationView(View):
	def post(self,request):
		data = json.loads(request.body)
		email = data['email']

		if not validate_email(email):
			return JsonResponse({'email_error':'Email is invalid'},status = 400)

		if User.objects.filter(email = email ).exists():
			return JsonResponse({'email_error':'email exists'},status = 409)
		
		return JsonResponse({'email_valid':True})

class Cheating(View):
	def get(self,request,professorname):
		student = str(request.user.username)
		email = User.objects.get(username=professorname).email
		email_subject = 'Student Cheating'
		email_body = 'Student caught changing window for 5 times. Student username is :' + student
		fromEmail = 'noreply@exam.com'
		email_obj = EmailMessage(
		    email_subject,
		    email_body,
            fromEmail,
		    [email],
		)
		EmailThread(email_obj).start()
		return JsonResponse({'sent':True})