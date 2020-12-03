from django.urls import path
from .views import Register,LoginView,LogoutView
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name="faculty-index"),
    path('register/',Register.as_view(),name = "faculty-register"),
    path('login/',LoginView.as_view(),name="faculty-login"),
    path('logout/',LogoutView.as_view(),name="faculty-logout"),
    path('reset-password/',auth_views.PasswordResetView.as_view(template_name="faculty/resetPassword.html"),name="password_reset_faculty"),
    path('reset-password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="faculty/resetPasswordSent.html"),name="password_reset_done_faculty"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="faculty/setNewPassword.html"),name="password_reset_confirm_faculty"),
    path('reset-password-complete/',auth_views.PasswordResetCompleteView.as_view(template_name="faculty/resetPasswordDone.html"),name="password_reset_complete_faculty"),
]
