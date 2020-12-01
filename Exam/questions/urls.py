from django.urls import path
from . import views
urlpatterns = [
    path('viewexams/',views.view_exams,name="view_exams")
]
