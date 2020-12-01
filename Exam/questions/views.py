from django.shortcuts import render
from django.contrib.auth.models import User
from .models import *

def view_exams(request):
    prof = request.user
    new_Form = ExamForm()
    if request.method == 'POST':
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