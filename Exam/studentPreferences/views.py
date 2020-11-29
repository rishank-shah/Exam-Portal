from django.shortcuts import render, redirect
from .models import StudentPreferenceModel
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    exists = StudentPreferenceModel.objects.filter(user=request.user).exists()
    student_preference = None
    
    if request.method == 'GET':
        var = "On"
        if exists:
            var="Off"
            student_preference = StudentPreferenceModel.objects.get(user=request.user)
            if student_preference.sendEmailOnLogin == True:
                var = "On"
        return render(request,'studentPreferences/pref.html',{'student_preference':student_preference,'email_pref_value':var})

    if request.method == 'POST':
        if exists:
            student_preference = StudentPreferenceModel.objects.get(user=request.user)
            var = "Off"
        pref = request.POST['email_pref']
        if exists:
            student_preference.sendEmailOnLogin = pref
            student_preference.save()
        else:
            var = "On"
            StudentPreferenceModel.objects.create(user = request.user, sendEmailOnLogin=pref)

        student_preference = StudentPreferenceModel.objects.filter(user=request.user)
        if pref == 'True':
            var = "On"

        messages.success(request,"Email Notifications are turned " + var)

        return render(request,'studentPreferences/pref.html',{'student_preference':student_preference,'email_pref_value':var})

@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'studentPreferences/change_password.html', {
        'form': form
    })