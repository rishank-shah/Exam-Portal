from django.shortcuts import render
from .models import StudentPreferenceModel
from django.contrib import messages

def index(request):
    exists = StudentPreferenceModel.objects.filter(user=request.user).exists()
    student_preference = None
    
    if request.method == 'GET':
        var = "On"
        if exists:
            var="Off"
            student_preference = StudentPreferenceModel.objects.get(user=request.user)
            if student_preference.sendEmailOnLogin:
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

