from django.db import models
from django.contrib.auth.models import User
from questions.question_models import Question_DB
from questions.questionpaper_models import Question_Paper

class StudentInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True)
    stream = models.CharField(max_length=50, blank=True)
    picture = models.ImageField(upload_to = 'student_profile_pics', blank=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = 'Student Info'

class Stu_Question(Question_DB):
    professor = None
    student = models.ForeignKey(User, limit_choices_to={'groups__name': "Student"}, on_delete=models.CASCADE, null=True)
    choice = models.CharField(max_length=3, default="E")

    def __str__(self):
        return str(self.student.username) + " "+ str(self.qno) +"-Stu_QuestionDB"


class StuExam_DB(models.Model):
    student = models.ForeignKey(User, limit_choices_to={'groups__name': "Student"}, on_delete=models.CASCADE, null=True)
    examname = models.CharField(max_length=100)
    qpaper = models.ForeignKey(Question_Paper, on_delete=models.CASCADE, null=True)
    questions = models.ManyToManyField(Stu_Question)
    score = models.IntegerField(default=0)
    completed = models.IntegerField(default=0)

    def __str__(self):
        return str(self.student.username) +" " + str(self.examname) + " " + str(self.qpaper.qPaperTitle) + "-StuExam_DB"


class StuResults_DB(models.Model):
    student = models.ForeignKey(User, limit_choices_to={'groups__name': "Student"}, on_delete=models.CASCADE, null=True)
    exams = models.ManyToManyField(StuExam_DB)

    def __str__(self):
        return str(self.student.username) +" -StuResults_DB"