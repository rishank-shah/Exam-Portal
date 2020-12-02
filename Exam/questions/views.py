from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import Group

def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False

def view_exams_prof(request):
    prof = request.user
    permissions = False
    if prof:
        permissions = has_group(prof,"Professor")
    if permissions:
        new_Form = ExamForm()
        if request.method == 'POST' and permissions:
            form = ExamForm(request.POST)
            if form.is_valid():
                exam = form.save(commit=False)
                exam.professor = prof
                exam.save()
                form.save_m2m()
                return redirect('view_exams')

        exams = Exam_Model.objects.filter(professor=prof)
        return render(request, 'exam/mainexam.html', {
            'exams': exams, 'examform': new_Form, 'prof': prof,
        })
    else:
        return redirect('view_exams_student')

def view_exams_student(request):
    exams = Exam_Model.objects.all()
    return render(request,'exam/mainexamstudent.html',{
        'exams':exams
    })