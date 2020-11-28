from django.shortcuts import render,redirect
from django.views import View
from .forms import StudentForm, StudentInfoForm
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode 
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from .utils import account_activation_token
from django.core.mail import EmailMessage
import threading
from django.contrib.auth.models import User
from studentPreferences.models import StudentPreferenceModel

@login_required(login_url='login')
def index(request):
    return render(request,'student/index.html')

class Register(View):
    def get(self,request):
        student_form = StudentForm()
        student_info_form = StudentInfoForm()
        return render(request,'student/register.html',{'student_form':student_form,'student_info_form':student_info_form})
    
    def post(self,request):
        student_form = StudentForm(data=request.POST)
        student_info_form = StudentInfoForm(data=request.POST)
        email = request.POST['email']

        if student_form.is_valid() and student_info_form.is_valid():
            student = student_form.save()
            student.set_password(student.password)
            student.is_active = False
            student.save()

            uidb64 = urlsafe_base64_encode(force_bytes(student.pk))
            domain = get_current_site(request).domain
            link = reverse('activate',kwargs={'uidb64':uidb64,'token':account_activation_token.make_token(student)})
            activate_url = 'http://' + domain +link
            email_subject = 'Activate your Portal account'
            email_body = 'Hi ' + '. Please use this link to verify your account\n' + activate_url
            fromEmail = 'noreply@exam.com'
            email = EmailMessage(
				email_subject,
				email_body,
				fromEmail,
				[email],
            )
            student_info = student_info_form.save(commit=False)
            student_info.user = student
            if 'picture' in request.FILES:
                student_info.picture = request.FILES['picture']
            student_info.save()
            messages.success(request,"Registered Succesfully. Check Email for confirmation")
            EmailThread(email).start()
            return redirect('login')
        else:
            print(student_form.errors,student_info_form.errors)
            return render(request,'student/register.html',{'student_form':student_form,'student_info_form':student_info_form})
    
class LoginView(View):
	def get(self,request):
		return render(request,'student\login.html')
	def post(self,request):
		username = request.POST['username']
		password = request.POST['password']

		if username and password:
			user = auth.authenticate(username=username,password=password)

			if user:
				if user.is_active:
					auth.login(request,user)
					student_pref = StudentPreferenceModel.objects.filter(user = request.user).exists()
					email = User.objects.get(username=username).email

					email_subject = 'You Logged into your Portal account'
					email_body = 'If you think someone else logged in. Please contact support or reset your password'
					fromEmail = 'noreply@exam.com'
					email = EmailMessage(
						email_subject,
						email_body,
						fromEmail,
						[email],
					)
					if student_pref :
						student = StudentPreferenceModel.objects.get(user=request.user)
						sendEmail = student.sendEmailOnLogin 
					if not student_pref :
						EmailThread(email).start()
					elif sendEmail:
						EmailThread(email).start()
					messages.success(request,"Welcome, "+ user.username + ". You are now logged in.")

					return redirect('index')
					
				messages.error(request,'Account not ACTIVATED')

				return render(request,'student/login.html')

			messages.error(request,'Invalid credentials')
			return render(request,'student/login.html')
		messages.error(request,'Please fill all fields')
		return render(request,'student/login.html')

class LogoutView(View):
	def post(self,request):
		auth.logout(request)
		messages.success(request,'Logged Out')
		return redirect('login')

class EmailThread(threading.Thread):
	def __init__(self,email):
		self.email = email
		threading.Thread.__init__(self)

	
	def run(self):
		self.email.send(fail_silently = False)

class VerificationView(View):
	def get(self,request,uidb64,token):
		try:
			id = force_text(urlsafe_base64_decode(uidb64))
			user = User.objects.get(pk=id)
			if not account_activation_token.check_token(user,token):
				return redirect('login'+'?message=' +'USER ALREADY ACTIVATED')
			if user.is_active:
				return redirect('login')
			user.is_active = True
			user.save()
			messages.success(request,'Account activated Sucessfully')
			return redirect('login')
		except Exception as e:
			raise e
		return redirect('login')
	
