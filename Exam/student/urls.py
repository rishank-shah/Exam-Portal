from django.urls import path
from . import views
from .views import Register,LoginView,LogoutView,VerificationView
from .api import UsernameValidation,EmailValidationView,Cheating
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name = "index"),
    path('register/',Register.as_view(),name="register"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('username-validate',UsernameValidation.as_view(),name="username-validate"),
    path('cheat/<str:professorname>',Cheating.as_view(),name="cheat"),
    path('email-validate',EmailValidationView.as_view(),name="email-validate"),
    path('activate/<uidb64>/<token>',VerificationView.as_view(),name = 'activate'), 
    path('reset-password/',auth_views.PasswordResetView.as_view(template_name="student/resetPassword.html"),name="password_reset"),
    path('reset-password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="student/resetPasswordSent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="student/setNewPassword.html"),name="password_reset_confirm"),
    path('reset-password-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="student/resetPasswordDone.html"),name="password_reset_complete"),
]
