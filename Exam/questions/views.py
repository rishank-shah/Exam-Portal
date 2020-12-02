from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.models import Group
from student.models import *
from django.utils import timezone

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
    list_of_completed = []
    list_un = []
    for exam in exams:
        if StuExam_DB.objects.filter(examname=exam.name).exists():
            if StuExam_DB.objects.get(examname=exam.name).completed == 1:
                list_of_completed.append(exam)
        else:
            list_un.append(exam)

    return render(request,'exam/mainexamstudent.html',{
        'exams':list_un,
        'completed':list_of_completed
    })

def appear_exam(request,id):
    student = request.user
    if request.method == 'GET':
        exam = Exam_Model.objects.get(pk=id)
        context = {
            "exam":exam,
            "question_list":exam.question_paper.questions.all(),
        }
        return render(request,'exam/giveExam.html',context)
    if request.method == 'POST' :
        paper = request.POST['paper']
        stuExam = StuExam_DB.objects.get_or_create(examname=paper, student=student)[0]
        examMain = Exam_Model.objects.get(name=paper)
        qPaper = stuExam.qpaper
        stuExam.questions.all().delete()

        qPaperQuestionsList = examMain.question_paper.questions.all()

        for ques in qPaperQuestionsList:
            student_question = Stu_Question(question=ques.question, optionA=ques.optionA, optionB=ques.optionB,optionC=ques.optionC, optionD=ques.optionD,
            answer=ques.answer, student=student,max_marks=ques.max_marks)
            student_question.save()
            stuExam.questions.add(student_question)
            stuExam.save()

        stuExam.completed = 1
        stuExam.save()
        secs = 0
        stuExam = StuExam_DB.objects.get(examname=paper, student=student)
        qPaper = stuExam.qpaper

        examQuestionsList = stuExam.questions.all()
        examScore = 0
        for ques in examQuestionsList:
            ans = request.POST.get(ques.question, False)
            if not ans:
                ans = "E"
            ques.choice = ans
            ques.save()
            if ans == ques.answer:
                examScore = examScore + ques.max_marks

        stuExam.score = examScore
        stuExam.save()

        return redirect('view_exams_student')

def result(request,id):
    student = request.user
    exam = Exam_Model.objects.get(pk=id)
    score = StuExam_DB.objects.get(student=student,examname=exam.name).score
    return render(request,'exam/result.html',{'exam':exam,"score":score})
